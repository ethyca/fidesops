FROM mcr.microsoft.com/azure-sql-edge:latest

WORKDIR /usr/src/app
COPY . /usr/src/app

ENV SA_PASSWORD Mssql_pw1
ENV ACCEPT_EULA Y

EXPOSE 1433
CMD /bin/bash ./entrypoint.sh
