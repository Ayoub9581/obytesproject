FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
RUN mkdir -p app

WORKDIR /home/user/app/

# Install system dependencies 1
RUN apt-get update && apt-get install gcc build-essential libpq-dev -y && \
    python3 -m pip install --no-cache-dir pip-tools


# Install system dependencies 2
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PORT=8888

# install python dependencies
ADD requirements.txt /home/user/app/

RUN pip install -r requirements.txt

# Clean the house
RUN apt-get purge libpq-dev -y && apt-get autoremove -y && \
    rm /var/lib/apt/lists/* rm -rf /var/cache/apt/*

ADD backend/ /home/user/app/

USER user
CMD gunicorn obytesproject.wsgi --log-file - -b 0.0.0.0:$PORT --reload
