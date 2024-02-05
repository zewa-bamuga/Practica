FROM python:3.12.0

RUN apt-get update && \
    apt-get install -y libgdal-dev && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /fastapi_app

WORKDIR /fastapi_app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh