FROM python:3.9.20

LABEL version="1.3"
MAINTAINER Alexey Manikin <alexey@manikin.dev>

# prepare environment
ENV DEBIAN_FRONTEND noninteractive
ENV APT_GET_INSTALL apt-get install --no-install-recommends -qq -y
ENV APT_GET_UPDATE apt-get update -qq
ENV APT_GET_UPGRADE apt-get dist-upgrade -qq -y

# dist-upgrade
RUN $APT_GET_UPDATE && $APT_GET_UPGRADE

# install base utils
RUN $APT_GET_INSTALL \
    curl \
    wget \
    openssh-client \
    rsync \
    vim \
    mc \
    gnupg2 \
    xz-utils \
    htop \
    man \
    unzip \
    git \
    build-essential

WORKDIR /home
COPY requirements.txt ./
RUN pip install --upgrade pip &&  pip install --no-cache-dir -r requirements.txt
