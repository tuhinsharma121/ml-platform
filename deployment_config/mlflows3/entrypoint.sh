#!/usr/bin/env bash

# --------------------------------------------------------------------------------------------------
# start mlflow service
# --------------------------------------------------------------------------------------------------

mlflow server \
      --host 0.0.0.0 \
      --port $MLFLOW_PORT \
      --backend-store-uri mysql+pymysql://$MYSQL_USER:$MYSQL_PASSWORD@mlflow_mysql/$MYSQL_DATABASE \
      --default-artifact-root $MLFLOW_ARTIFACT_URI

# --------------------------------------------------------------------------------------------------
# to make the container alive for indefinite time
# --------------------------------------------------------------------------------------------------

#touch /tmp/a.txt
#tail -f /tmp/a.txt