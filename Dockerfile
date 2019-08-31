FROM python:latest

WORKDIR /app

COPY ./features/ /app/features
COPY ./simqle /app/simqle
COPY ./setup.py /app
COPY ./test-requirements.txt /app
COPY ./README.md /app
COPY ./.coveragerc /app

RUN pip install -r test-requirements.txt
RUN pip install .
