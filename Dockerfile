FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN pip install unimol_tools==0.1.0
RUN pip install huggingface_hub==0.24.0

WORKDIR /repo
COPY . /repo
