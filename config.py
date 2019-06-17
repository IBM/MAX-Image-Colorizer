
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
