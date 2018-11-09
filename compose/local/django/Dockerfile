FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # python libraries dependencies
  && apk add gcc python3-dev musl-dev g++ \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/local/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

COPY ./compose/local/django/celery/worker.sh /worker.sh
RUN sed -i 's/\r//' /worker.sh
RUN chmod +x /worker.sh

WORKDIR /app
