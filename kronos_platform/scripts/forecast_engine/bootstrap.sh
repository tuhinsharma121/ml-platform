#!/bin/bash -xe

# --------------------------------------------------------------------------------------------------
# this script will be executed by aws spark emr during bootstrap process of each node
# we install python dependencies of our training job here
# Do not do sudo yum -y update
# --------------------------------------------------------------------------------------------------

sudo yum install -y sqlite-devel libffi-devel bzip2-devel
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar xzf Python-3.7.9.tgz
cd Python-3.7.9
sudo ./configure
sudo make
sudo make install
sudo rm /usr/bin/python3
sudo ln -s /usr/local/bin/python3.7 /usr/bin/python3
sudo rm /usr/bin/pip3
sudo ln -s /usr/local/bin/pip3 /usr/bin/pip3
sudo /usr/bin/pip3 install fastapi==0.63.0 uvicorn==0.11.5 requests==2.23.0 coverage==5.1 boto3==1.17.67 snowflake-connector-python==2.4.3 mysql-connector==2.2.9 psycopg2-binary==2.8.6 pandas==1.2.4 ephem==3.7.7.1 numpy==1.20.3 moto==2.0.6 pystan==2.19.1.1 prophet==1.0.1 mlflow==1.16.0 plotly==4.14.3 pyarrow==4.0.0



