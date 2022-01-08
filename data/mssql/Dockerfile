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
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
RUN apt-get install apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt-get update
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install \
    unixodbc-dev \
    msodbcsql17 \
    mssql-tools

RUN pip install 'sqlalchemy==1.4.14'
RUN pip install 'pyodbc==4.0.32'

WORKDIR /usr/src/app
COPY . /usr/src/app

CMD ["python", "init_mssql_example.py"]

