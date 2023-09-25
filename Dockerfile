FROM python:3.9.10-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Install system dependency
RUN apt-get update && apt-get install -y netcat
RUN apt-get install -y \
    curl \
    python3-dev\
    gcc


# ARG INSTALL_NODE_VERSION=${INSTALL_NODE_VERSION:-12}
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y \
    && apt-get -y autoclean

COPY . /app/

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD [ "flask", "run","--host","0.0.0.0","--port","4000"]