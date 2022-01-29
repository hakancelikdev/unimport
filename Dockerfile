FROM python:3.9-alpine

COPY . /app
WORKDIR /app

RUN apk add cargo

RUN pip install --upgrade pip
RUN pip install .

ENTRYPOINT [ "python", "-m", "unimport" ]
