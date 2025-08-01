FROM python:3.13-alpine

COPY . /app
WORKDIR /app

RUN apk add cargo  \
&& pip install --no-cache-dir --upgrade pip  \
&& pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "unimport"]
