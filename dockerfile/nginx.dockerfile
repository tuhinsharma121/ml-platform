FROM nginx:alpine

# --------------------------------------------------------------------------------------------------
# get the args while building the docker image from docker-compose
# --------------------------------------------------------------------------------------------------

ARG API_HOST
ARG API_PORT

# --------------------------------------------------------------------------------------------------
# add the nginx.conf to the /etc/nginx/conf.d/ directory
# --------------------------------------------------------------------------------------------------

COPY ./deployment_config/nginx/nginx.conf /default.conf.template
RUN envsubst '${API_HOST} ${API_PORT}' < /default.conf.template > /etc/nginx/conf.d/default.conf
