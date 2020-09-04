FROM python:3.7-slim

LABEL name="COLLECTIVE FHIRPATH" \
    description="Plone provider for fhirpath" \
    maintainer="Plone Community"

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python Setuptools
RUN apt-get update -y && \
    apt-get install -y locales git-core gcc g++ netcat libxml2-dev \
    libxslt-dev libz-dev python-dev libyaml-dev iputils-ping curl \
    libcurl4-openssl-dev apt-transport-https openssl libcurl4-openssl-dev ca-certificates

RUN mkdir /app

COPY requirements.txt /requirements.txt
COPY constraints_plone52.txt /constraints_plone52.txt

# Install buildout
RUN pip install -r /requirements.txt
COPY . /app
RUN cd /app && buildout -c buildout.cfg
# RUN /app/bin/test
ENTRYPOINT ["/bin/bash", "-i", "-t"]
