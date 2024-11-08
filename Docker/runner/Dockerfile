FROM python:3.9.20

LABEL version="0.9"
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

# need for developing
RUN $APT_GET_INSTALL openssh-server && mkdir /root/.ssh;

ADD config/sshd_config /etc/ssh/sshd_config
ADD config/authorized_keys /root/.ssh/authorized_keys

WORKDIR /home
COPY requirements.txt ./
RUN pip install --upgrade pip &&  pip install --no-cache-dir -r requirements.txt

WORKDIR /home/sofi

ADD init.sh /sbin/init.sh
RUN chmod 755 /sbin/init.sh

CMD ["/sbin/init.sh"]
