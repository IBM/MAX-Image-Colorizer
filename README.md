# IBM Code Model Asset Exchange: Image Translation (Grayscale to Color)


This repository contains code to instantiate and deploy an image translation model. This model is a Generative Adversarial Network (GAN) that was trained by the [IBM CODAIT Team](codait.org) on [COCO dataset](http://mscoco.org/) images converted to grayscale and produces colored images. The input to the model is a grayscale image (jpeg or png), and the output is a colored 256 by 256 image (increased resolution will be added in future releases).

The model is based on Christopher Hesse's [Tensorflow implementation of the pix2pix model](https://github.com/affinelayer/pix2pix-tensorflow). The model files are hosted on [IBM Cloud Object Storage](http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/tf/pix2pix/pix2pix-bw-to-color.tar.gz). The code in this repository deploys the model as a web service in a Docker container. This repository was developed as part of the [IBM Code Model Asset Exchange](https://developer.ibm.com/code/exchanges/models/).

## Model Metadata
| Domain | Application | Industry  | Framework | Training Data | Input Data Format |
| ------------- | --------  | -------- | --------- | --------- | -------------- |
| Vision | Image Coloring | General | TensorFlow | [COCO Dataset](http://mscoco.org/) | Images |

## References
* _J. Isola, J. Zhu, T. Zhou, A. Efros_, ["Image-to-Image Translation with Conditional Adversarial Networks"](https://arxiv.org/abs/1611.07004), CVPR 2017
* [pix2pix TensorFlow GitHub Repository](https://github.com/affinelayer/pix2pix-tensorflow)


## Licenses

| Component | License | Link  |
| ------------- | --------  | -------- |
| This repository | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE) |
| Model Code (3rd party) | [MIT](https://opensource.org/licenses/MIT) | [TensorFlow pix2pix Repository](https://github.com/affinelayer/pix2pix-tensorflow/blob/master/LICENSE.txt) |
| Model Weights | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE)
| Test Assets | [CC0 License](https://creativecommons.org/publicdomain/zero/1.0/) | [Asset README](assets/README.md)

## Pre-requisites:

* `docker`: The [Docker](https://www.docker.com/) command-line interface. Follow the [installation instructions](https://docs.docker.com/install/) for your system.
* The minimum recommended resources for this model is 2GB Memory and 2 CPUs.

## Steps

1. [Build the Model](#1-build-the-model)
2. [Deploy the Model](#2-deploy-the-model)
3. [Use the Model](#3-use-the-model)
4. [Development](#4-development)
5. [Clean Up](#5-clean-up)


## 1. Build the Model

Clone this repository locally. In a terminal, run the following command:

```
git clone https://github.com/IBM/MAX-pix2pix.git
```

Change directory into the repository base folder:

```
cd MAX-pix2pix
```

To build the docker image locally, run:

```
docker build -t max-pix2pix .
```

All required model assets will be downloaded during the build process. _Note_ that currently this docker image is CPU only (we will add support for GPU images later).

## 2. Deploy the Model

To run the docker image, which automatically starts the model serving API, run:

```
docker run -it -p 5000:5000 max-pix2pix
```

## 3. Use the Model

The API server automatically generates an interactive Swagger documentation page. Go to `http://localhost:5000` to load it. From there you can explore the API and also create test requests.

Use the `model/predict` endpoint to load a test grayscale image (you can use one of the test images from the `assets` folder) and get a colored image.

![Swagger Doc Screenshot](docs/swagger-screenshot.png)


You can also test it on the command line, for example:

```
curl -F "image=@assets/bw-city.jpg" -XPOST http://127.0.0.1:5000/model/predict > result.png && open result.png
```


## 4. Development

To run the Flask API app in debug mode, edit `config.py` to set `DEBUG = True` under the application settings. You will then need to rebuild the docker image (see [step 1](#1-build-the-model)).


## 5. Cleanup

To stop the docker container type `CTRL` + `C` in your terminal.
