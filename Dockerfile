# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
# ENV
ENV WORK_DIR="/usr/src/app"
ENV USER_NAME=user
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev bash \
    && pip install --upgrade pip setuptools wheel \
    && cd $WORK_DIR \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . $WORK_DIR

# Create user and give permissions
# RUN adduser -D $USER_NAME
# RUN chown -R $USER_NAME:$USER_NAME $WORK_DIR && \
#     chmod -R 755 $WORK_DIR && \
#     chown -R $USER_NAME:$USER_NAME /opt/venv/ && \
#     chmod -R 755 /opt/venv/
# USER $USER_NAME