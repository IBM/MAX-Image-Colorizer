import pytest
import pycurl
import io
from PIL import Image


def test_response():
    c = pycurl.Curl()
    b = io.BytesIO()
    c.setopt(pycurl.URL, 'http://localhost:5000/model/predict')
    c.setopt(pycurl.HTTPHEADER, ['Accept:application/json', 'Content-Type: multipart/form-data'])
    c.setopt(pycurl.HTTPPOST, [('image', (pycurl.FORM_FILE, "assets/bw-city.jpg"))])
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    assert c.getinfo(pycurl.RESPONSE_CODE) == 200
    c.close()

    response = b.getvalue()

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