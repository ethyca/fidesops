FROM --platform=linux/amd64 python:3.9.6-slim-buster

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

# SQL Server (MS SQL)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt-get update
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install \
    apt-transport-https \
    unixodbc-dev \
    mssql-tools

# Update pip and install requirements
COPY requirements.txt dev-requirements.txt ./
RUN pip install -U pip  \
    && pip install 'cryptography~=3.4.8' \
    && pip install snowflake-connector-python --no-use-pep517  \
    && pip install -r requirements.txt -r dev-requirements.txt

# Copy in the application files and install it locally
COPY . /fidesops
WORKDIR /fidesops
ARG include_dangerous="False"
RUN if [ "$include_dangerous" = "True" ] ; then \
    pip install -e ".[all,mssql]" ; \
    else \
    pip install -e ".[all]" ; \
    fi

CMD [ "fidesops", "webserver" ]