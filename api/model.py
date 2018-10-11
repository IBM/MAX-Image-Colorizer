from flask import make_response
from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from config import MODEL_META_DATA
from core.backend import ModelWrapper
import numpy as np
import base64

api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'description': fields.String(required=True, description='Model description'),
    'license': fields.String(required=False, description='Model license')
})


@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA


# Creating a JSON response model: https://flask-restplus.readthedocs.io/en/stable/marshalling.html#the-api-model-factory
predict_response = api.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message')
})

# Set up parser for input data (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = api.parser()
input_parser.add_argument('image', type=FileStorage, location='files', required=True,
                          help="Black and white JPEG or PNG image to colorize")


@api.route('/predict')
class Predict(Resource):

    model_wrapper = ModelWrapper()

    @api.doc('predict')
    @api.expect(input_parser)
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
