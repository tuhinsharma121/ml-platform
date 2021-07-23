#!/usr/bin/env bash
cd /home/hadoop/
export PYTHONPATH=`pwd`
spark-submit --py-files $1 --files config.ini --packages net.snowflake:snowflake-jdbc:3.12.17,net.snowflake:spark-snowflake_2.12:2.8.4-spark_3.0 /home/hadoop/kronos_platform/src/forecast_engine/batch_score_model.py --client $2 --params $3
