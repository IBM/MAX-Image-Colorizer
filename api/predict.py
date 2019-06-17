#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from core.model import ModelWrapper
from maxfw.core import MAX_API, PredictAPI
from config import ERR_MSG

from flask import send_file, abort
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

        try:
            image = self.model_wrapper.predict(input_instance)
        except IOError as e:
            if e.args[0] == ERR_MSG:
                abort(400, ERR_MSG)

        response = send_file(io.BytesIO(image), attachment_filename='result.png', mimetype='image/png')

        return response
