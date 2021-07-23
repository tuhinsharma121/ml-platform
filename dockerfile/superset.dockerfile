FROM apache/superset
MAINTAINER Tuhin Sharma "tuhin.s@hypersonix.ai"

# --------------------------------------------------------------------------------------------------
# Switching to root to install the required packages
# --------------------------------------------------------------------------------------------------

USER root

# --------------------------------------------------------------------------------------------------
# install python packages
# --------------------------------------------------------------------------------------------------

COPY ./deployment_config/superset/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# --------------------------------------------------------------------------------------------------
# initialize superset
# --------------------------------------------------------------------------------------------------

RUN superset db upgrade && \
    superset fab create-admin --username admin --firstname admin --lastname admin --email admin --password admin && \
    superset init

# --------------------------------------------------------------------------------------------------
# whitelabel the images in superset
# --------------------------------------------------------------------------------------------------

COPY deployment_config/superset/assets/superset-logo-horiz.png /app/superset/static/assets/images/superset-logo-horiz.png
COPY deployment_config/superset/assets/favicon.png /app/superset/static/assets/images/favicon.png
