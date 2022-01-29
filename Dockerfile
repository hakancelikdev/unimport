FROM python:3.9.10

# copy source code
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install .

ENTRYPOINT [ "python", "-m", "unimport" ]
