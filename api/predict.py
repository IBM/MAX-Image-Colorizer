from core.model import ModelWrapper
from maxfw.core import MAX_API, PredictAPI

from flask import make_response
from flask_restplus import fields
from werkzeug.datastructures import FileStorage

import numpy as np
import base64


# Set up parser for input data
input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files', required=True,
                          help="Black and white JPEG or PNG image to colorize")

# Creating a JSON response model: https://flask-restplus.readthedocs.io/en/stable/marshalling.html#the-api-model-factory
predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message')
})


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()
        input_data = args['image'].read()

        input_encoded = base64.urlsafe_b64encode(input_data)
        input_array = np.array(input_encoded)
        input_instance = np.expand_dims(input_array, axis=0)

        image = self.model_wrapper.predict(input_instance)

        response = make_response(image)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='result.png')

        result['status'] = 'ok'
        return response
