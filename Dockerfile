FROM continuumio/miniconda3

# Fill in these with a link to the bucket containing the model and the model file name
ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/tf/pix2pix
ARG model_file=pix2pix-bw-to-color.tar.gz

WORKDIR /workspace
RUN mkdir assets
RUN wget -nv ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}
RUN tar -x -C assets/ -f assets/${model_file} -v

# Python package versions
ARG tf_version=1.5.0

RUN pip install --upgrade pip && \
    pip install tensorflow==${tf_version} && \
    pip install flask-restplus
    # Add other packages needed here

COPY . /workspace

EXPOSE 5000

CMD python app.py
