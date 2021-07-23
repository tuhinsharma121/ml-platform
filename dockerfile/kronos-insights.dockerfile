FROM ubuntu:18.04
MAINTAINER Tuhin Sharma "tuhin.s@hypersonix.ai"

# --------------------------------------------------------------------------------------------------
# install ubuntu essentials
# --------------------------------------------------------------------------------------------------

RUN apt-get update --fix-missing && \
    apt-get -y install build-essential && \
    apt-get -y install apt-utils && \
    apt-get -y install zlib1g-dev && \
    apt-get -y install libssl-dev && \
    apt-get -y install libbz2-dev && \
    apt-get -y install liblzma-dev && \
    apt-get -y install wget && \
    apt-get -y install libffi-dev && \
    apt-get -y install libsqlite3-dev && \
    apt-get -y install libpq-dev && \
    apt-get -y install zip

# --------------------------------------------------------------------------------------------------
# install python 3.7.9, pip, setuptools, wheel and Cython
# --------------------------------------------------------------------------------------------------

ENV PYTHON_VERSION 3.7.9
ENV PYTHONUNBUFFERED 1
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar -xzf Python-$PYTHON_VERSION.tgz && \
    cd Python-$PYTHON_VERSION && \
    ./configure && \
    make && \
    make install
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir Cython

# --------------------------------------------------------------------------------------------------
# install python packages
# --------------------------------------------------------------------------------------------------

COPY ./requirements.txt /
RUN pip3 install -r /requirements.txt

# --------------------------------------------------------------------------------------------------
# copy src code and scripts into root dir /
# --------------------------------------------------------------------------------------------------

COPY ./kronos_platform /kronos_platform
COPY ./kronos /kronos
COPY ./config.py /config.py
COPY ./kronos.ini /config.ini

# --------------------------------------------------------------------------------------------------
# add entrypoint for the container
# --------------------------------------------------------------------------------------------------

ADD ./deployment_config/kronos_insights/entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh
ENTRYPOINT ["/bin/entrypoint.sh"]
