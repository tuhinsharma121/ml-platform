import os
from configparser import ConfigParser

config = ConfigParser(interpolation=None)
config.read("config.ini")

# --------------------------------------------------------------------------------------------------
# snowflake config
# --------------------------------------------------------------------------------------------------

SF_ACCOUNT = config['snowflake']['SF_ACCOUNT']
SF_WAREHOUSE = config['snowflake']['SF_WAREHOUSE']
SF_USER = config['snowflake']['SF_USER']
SF_PASSWORD = config['snowflake']['SF_PASSWORD']

# --------------------------------------------------------------------------------------------------
# postgres config
# --------------------------------------------------------------------------------------------------

POSTGRES_HOST = config['postgres']['POSTGRES_HOST']
POSTGRES_PORT = config['postgres']['POSTGRES_PORT']
POSTGRES_DB = config['postgres']['POSTGRES_DB']
POSTGRES_USER = config['postgres']['POSTGRES_USER']
POSTGRES_PASSWORD = config['postgres']['POSTGRES_PASSWORD']

# --------------------------------------------------------------------------------------------------
# mysql config
# --------------------------------------------------------------------------------------------------

MYSQL_HOST = config['mysql']['MYSQL_HOST']
MYSQL_DATABASE = config['mysql']['MYSQL_DATABASE']
MYSQL_USER = config['mysql']['MYSQL_USER']
MYSQL_PASSWORD = config['mysql']['MYSQL_PASSWORD']
MYSQL_ROOT_PASSWORD = config['mysql']['MYSQL_ROOT_PASSWORD']

# --------------------------------------------------------------------------------------------------
# emr
# --------------------------------------------------------------------------------------------------

EMR_S3_BUCKET = config['emr']['EMR_S3_BUCKET']
EC2_SUBNET_ID = config['emr']['EC2_SUBNET_ID']
EC2_INSTANCE_TYPE = config['emr']['EC2_INSTANCE_TYPE']
EC2_MASTER_SECURITY_GROUP = config['emr']['EC2_MASTER_SECURITY_GROUP']
EC2_SLAVE_SECURITY_GROUP = config['emr']['EC2_SLAVE_SECURITY_GROUP']
EC2_KEY_NAME = config['emr']['EC2_KEY_NAME']

# --------------------------------------------------------------------------------------------------
# aws
# --------------------------------------------------------------------------------------------------

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = os.environ.get("AWS_REGION", None)
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", None)

# --------------------------------------------------------------------------------------------------
# telegram
# --------------------------------------------------------------------------------------------------

TELEGRAM_URL = config['telegram']['TELEGRAM_URL']
TELEGRAM_CHANNEL_ID = config['telegram']['TELEGRAM_CHANNEL_ID']

# --------------------------------------------------------------------------------------------------
# deployment
# --------------------------------------------------------------------------------------------------

CODE_BASE = config['deployment']['CODE_BASE']
DEPLOYMENT_TYPE = config['deployment']['DEPLOYMENT_TYPE']
PROJECT_PATH = config['deployment']['PROJECT_PATH']
LOGGING_LEVEL = config['deployment']['LOGGING_LEVEL']

# --------------------------------------------------------------------------------------------------
# mlflow
# --------------------------------------------------------------------------------------------------

MLFLOW_TRACKING_URI = config['mlflow']['MLFLOW_TRACKING_URI']
MLFLOW_DEPLOYMENT_TYPE = config['mlflow']['MLFLOW_DEPLOYMENT_TYPE']
