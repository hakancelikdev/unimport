FROM python:3.10-alpine

COPY . /app
WORKDIR /app

RUN apk add cargo  \
&& pip install --upgrade pip  \
&& pip install .

ENTRYPOINT ["python", "-m", "unimport"]
