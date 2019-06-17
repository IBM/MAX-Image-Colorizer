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

import pytest
import io
from PIL import Image
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Image Colorizer'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'max-image-colorizer'
    assert metadata['name'] == 'MAX Image Colorizer'
    assert metadata['description'] == 'Converts a grayscale image to a color image.'
    assert metadata['license'] == 'MIT'
    assert metadata['type'] == 'Image-To-Image Translation'
    assert 'max-image-colorizer' in metadata['source']


def _check_response(r):
    assert r.status_code == 200

    response = r.content

    im = Image.open(io.BytesIO(response))

    assert im.size == (256, 256)

    pixel_sky = im.getpixel((30, 30))  # part of the sky in the top left corner
    pixel_road = im.getpixel((40, 220))  # pixel from the road in the bottom left corner
    pixel_bg_bldg = im.getpixel((230, 150))  # buildings in the middle right side of the image
    pixel_trees = im.getpixel((220, 230))  # dark trees in bottom right corner

    # the sky should be dark
    assert pixel_sky[0] < 50
    assert pixel_sky[1] < 50
    assert pixel_sky[2] < 50

    # lots of headlights in the road, this should be bright
    assert pixel_road[0] > 200
    assert pixel_road[1] > 200
    assert pixel_road[2] > 200

    # these buildings are tan/orange
    assert pixel_bg_bldg[0] > 100
    assert pixel_bg_bldg[1] > 100
    assert pixel_bg_bldg[2] < 100  # not a lot of blue

    # this should be dark and maybe a little green
    assert pixel_trees[0] < 50
    assert pixel_trees[1] < 50
    assert pixel_trees[2] < 51
    assert pixel_trees[1] > pixel_trees[0]  # trees have more green than red


def test_predict():
    model_endpoint = 'http://localhost:5000/model/predict'
    formats = ['jpg', 'png']
    file_path = 'tests/bw-city.{}'

    for f in formats:
        p = file_path.format(f)
        with open(p, 'rb') as file:
            file_form = {'image': (p, file, 'image/{}'.format(f))}
            r = requests.post(url=model_endpoint, files=file_form)
        _check_response(r)

    # Test invalid
    file_path = 'README.md'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__])
