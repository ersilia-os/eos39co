FROM bentoml/model-server:0.11.0-py310
MAINTAINER ersilia

RUN pip install unimol_tools==0.1.0.post1
RUN pip install huggingface_hub==0.24.0

WORKDIR /repo
COPY . /repo
