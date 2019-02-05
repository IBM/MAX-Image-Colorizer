from core.model import ModelWrapper
from maxfw.core import MAX_API, PredictAPI

from flask import send_file
from werkzeug.datastructures import FileStorage

import io
import numpy as np
import base64


# Set up parser for input data
input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files', required=True,
                          help="Black and white JPEG or PNG image to colorize")


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    def post(self):
        """Make a prediction given input data"""
        args = input_parser.parse_args()
        input_data = args['image'].read()

        input_encoded = base64.urlsafe_b64encode(input_data)
        input_array = np.array(input_encoded)
        input_instance = np.expand_dims(input_array, axis=0)

        image = self.model_wrapper.predict(input_instance)

        response = send_file(io.BytesIO(image), attachment_filename='result.png', mimetype='image/png')

        return response
