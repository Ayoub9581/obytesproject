FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
RUN mkdir -p app

WORKDIR /home/user/app/obytesproject

# Install system dependencies
RUN apt-get update && apt-get install gcc build-essential libpq-dev -y && \
    python3 -m pip install --no-cache-dir pip-tools

# install python dependencies
ADD requirements.txt /home/user/app/obytesproject/

RUN pip install -r requirements.txt

# Clean the house
RUN apt-get purge libpq-dev -y && apt-get autoremove -y && \
    rm /var/lib/apt/lists/* rm -rf /var/cache/apt/*

ADD backend/ /home/user/app/obytesproject

USER user
CMD gunicorn todoapp.wsgi --log-file - -b 0.0.0.0:8000 --reload
