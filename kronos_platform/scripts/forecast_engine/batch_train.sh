#!/usr/bin/env bash
cd /home/hadoop/
export PYTHONPATH=`pwd`
/usr/bin/python3 /home/hadoop/kronos_platform/src/forecast_engine/batch_train_model.py --client $1 --params $2