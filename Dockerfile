FROM python

WORKDIR /app

RUN apt-get update && apt-get install apt-transport-https ca-certificates -y

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install msodbcsql17 -y
RUN apt-get update && apt-get install unixodbc-dev -y

COPY ./features/ /app/features
COPY ./simqle /app/simqle
COPY ./setup.py /app
COPY ./test-requirements.txt /app
COPY ./README.md /app
COPY ./.coveragerc /app

RUN pip install -r test-requirements.txt
RUN pip install .
