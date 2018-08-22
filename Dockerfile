FROM codait/max-base

# Fill in these with a link to the bucket containing the model and the model file name
ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/tf/pix2pix
ARG model_file=pix2pix-bw-to-color.tar.gz

WORKDIR /workspace
RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}
RUN tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

# Python package versions
ARG tf_version=1.5.0

RUN pip install tensorflow==${tf_version}

COPY . /workspace

EXPOSE 5000

CMD python app.py
