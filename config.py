# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# Application settings

# API metadata
API_TITLE = 'MAX Image Colorizer'
API_DESC = 'Adds color to black and white images.'
API_VERSION = '1.1.0'

ERR_MSG = 'Invalid file type/extension. Please provide a valid image (supported formats: JPEG, PNG).'
# default model
MODEL_NAME = API_TITLE
MODEL_ID = MODEL_NAME.replace(' ', '-').lower()
DEFAULT_MODEL_PATH = 'assets/pix2pix-bw-to-color'
MODEL_LICENSE = 'MIT'
