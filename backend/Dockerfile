FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry and packages
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install poetry && \
    poetry config virtualenvs.create false 

COPY . /app
WORKDIR /app

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH=/app
