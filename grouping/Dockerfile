FROM python:3.9.19-bullseye
LABEL maintainer="jeslinxavi7@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8020

COPY ./register.py /reg/register.py

ARG DEV=false
RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libsm6 \
        libxext6 \
        postgresql-client \
        build-essential \
        libpq-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV="true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user


ENV PATH="/py/bin:$PATH"

USER django-user