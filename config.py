# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# Application settings

# API metadata
API_TITLE = 'MAX Image Colorizer'
API_DESC = 'Adds color to black and white images.'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'pix2pix-bw-to-color'
DEFAULT_MODEL_PATH = 'assets/{}'.format(MODEL_NAME)
MODEL_LICENSE = 'MIT'

MODEL_META_DATA = {
    'id': '{}'.format(MODEL_NAME.lower()),
    'name': '{} TensorFlow Model'.format(MODEL_NAME),
    'description': '{} converts a grayscale image to a color image.'.format(MODEL_NAME),
    'type': 'Image',
    'license': '{}'.format(MODEL_LICENSE)
}
