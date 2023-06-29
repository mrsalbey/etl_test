FROM python:3.10
WORKDIR /etl
COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir
RUN apt-get update && apt install netcat-openbsd -y \
     && apt-get install -y postgresql-client
COPY . .
RUN sed -i 's/\r$//g'  /etl/backup.sql
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]