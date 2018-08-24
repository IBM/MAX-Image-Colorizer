import pytest
import io
from PIL import Image
import requests


def test_response():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'assets/bw-city.jpg'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)
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
    assert pixel_trees[2] < 50
    assert pixel_trees[1] > pixel_trees[0]  # trees have more green than red


if __name__ == '__main__':
    pytest.main([__file__])
