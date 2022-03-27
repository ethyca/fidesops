FROM --platform=linux/amd64 python:3.9.6-slim-buster

ARG MSSQL_REQUIRED

# Install build dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

RUN apt-get update && \
    apt-get install -y \
    git \
    make \
    unixodbc-dev \
    ipython \
    vim \
    curl \
    g++ \
    gnupg \
    gcc


RUN echo "ENVIRONMENT VAR:  $MSSQL_REQUIRED"

# SQL Server (MS SQL)
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
RUN if [ "$MSSQL_REQUIRED" = "true" ] ; then apt-get install apt-transport-https ; fi
RUN if [ "$MSSQL_REQUIRED" = "true" ] ; then curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - ; fi
RUN if [ "$MSSQL_REQUIRED" = "true" ] ; then curl https://packages.microsoft.com/config/debian/10/prod.list | tee /etc/apt/sources.list.d/msprod.list ; fi
RUN if [ "$MSSQL_REQUIRED" = "true" ] ; then apt-get update ; fi
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN if [ "$MSSQL_REQUIRED" = "true" ] ; then apt-get -y install \
    unixodbc-dev \
    msodbcsql17 \
    mssql-tools ; fi

# Update pip and install requirements
COPY requirements.txt dev-requirements.txt ./
RUN pip install -U pip  \
    && pip install 'cryptography~=3.4.8' \
    && pip install snowflake-connector-python --no-use-pep517  \
    && pip install -r requirements.txt -r dev-requirements.txt


# Copy in the application files and install it locally
COPY . /fidesops
WORKDIR /fidesops
RUN if [ "$MSSQL_REQUIRED" = "true" ] ; then pip install -e ".[mssql]" ; else pip install -e . ; fi

CMD [ "fidesops", "webserver" ]
