FROM node:16 as frontend

RUN if [ "$FIDESOPS__ADMINUI__ENABLED" = "true" ] ; then WORKDIR /fidesops/clients/admin-ui ; fi
# install node modules
RUN if [ "$FIDESOPS__ADMINUI__ENABLED" = "true" ] ; then COPY clients/admin-ui/ . ; fi
RUN if [ "$FIDESOPS__ADMINUI__ENABLED" = "true" ] ; then  npm install ; fi

# Build the frontend static files
RUN if [ "$FIDESOPS__ADMINUI__ENABLED" = "true" ] ; then  npm run export ; fi

# Seed empty directory so copy works in the next layer
RUN if [ "$FIDESOPS__ADMINUI__ENABLED" != "true" ] ; then mkdir -p /fidesops/clients/admin-ui/out/ ; fi


FROM --platform=linux/amd64 python:3.9.6-slim-buster as backend

ARG MSSQL_REQUIRED

# Install auxiliary software
RUN apt-get update && \
    apt-get install -y \
    git \
    make \
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
COPY requirements.txt dev-requirements.txt mssql-requirements.txt ./
RUN pip install -U pip  \
    && pip install 'cryptography~=3.4.8' \
    && pip install snowflake-connector-python --no-use-pep517  \
    && pip install -r requirements.txt -r dev-requirements.txt

RUN if [ "$MSSQL_REQUIRED" = "true" ] ; then pip install -U pip -r mssql-requirements.txt ; fi


# Copy in the application files and install it locally
COPY . /fidesops
WORKDIR /fidesops
RUN pip install -e .

# Make a static files directory
RUN mkdir -p /fidesops/src/fidesops/build/static/
# Copy frontend build over. If UI is toggled off this copies over an empty folder
COPY --from=frontend /fidesops/clients/admin-ui/out/ /fidesops/src/fidesops/build/static/

# Enable detection of running within Docker
ENV RUNNING_IN_DOCKER=true

CMD [ "fidesops", "webserver" ]
