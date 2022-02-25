FROM python:3.9-slim

WORKDIR /app/

ARG INSTALL_DEV=true

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Install Poetry and packages
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install poetry && \
    poetry config virtualenvs.create false 

# Copy poetry.lock* in case it doesn't exist in the repo
# COPY ./app/pyproject.toml ./app/poetry.lock* /app/
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . /app
ENV PYTHONPATH=/app
