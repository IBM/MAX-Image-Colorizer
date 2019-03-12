from maxfw.model import MAXModelWrapper

import tensorflow as tf
from tensorflow.contrib.saved_model.python.saved_model import signature_def_utils
from tensorflow import saved_model as sm
import logging
from config import DEFAULT_MODEL_PATH, ERR_MSG, MODEL_NAME, MODEL_LICENSE, MODEL_ID

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):
    """Model wrapper for TensorFlow models in SavedModel format"""

    MODEL_META_DATA = {
        'id': MODEL_ID,
        'name': MODEL_NAME,
        'description': 'Converts a grayscale image to a color image.',
        'type': 'Image-To-Image Translation',
        'license': MODEL_LICENSE,
        'source': 'https://developer.ibm.com/exchanges/models/all/max-image-colorizer'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        sess = tf.Session(graph=tf.Graph())
        # Load the graph
        model_graph_def = sm.loader.load(sess, [sm.tag_constants.SERVING], path)
        sig_def = signature_def_utils.get_signature_def_by_key(model_graph_def, sm.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY)

        input_name = sig_def.inputs['input_images'].name
        output_name = sig_def.outputs['output_images'].name

        # Set up instance variables and required inputs for inference
        self.sess = sess
        self.model_graph_def = model_graph_def
        self.output_tensor = sess.graph.get_tensor_by_name(output_name)
        self.input_name = input_name
        self.output_name = output_name
        logger.info('Loaded model')

    def _predict(self, x):

        # Run prediction on input
        try:
            preds = self.output_tensor.eval(feed_dict={self.input_name: x}, session=self.sess)
            return preds
        except tf.errors.InvalidArgumentError as e:
            if 'Expected image' in e.message:
                raise OSError(ERR_MSG)
            else:
                raise e

