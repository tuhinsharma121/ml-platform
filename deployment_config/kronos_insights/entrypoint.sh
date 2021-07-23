#!/usr/bin/env bash

# --------------------------------------------------------------------------------------------------
# start web service to provide rest end points for this container
# --------------------------------------------------------------------------------------------------

gunicorn \
      --pythonpath / \
      --bind 0.0.0.0:$SERVER_PORT \
      -k gevent \
      --timeout $SERVER_TIMEOUT \
      --workers=$SERVER_WORKER_COUNT \
      --threads=$SERVER_THREAD_COUNT \
      -k uvicorn.workers.UvicornWorker \
      kronos_platform.deployment.insights.server:app

# --------------------------------------------------------------------------------------------------
# to make the container alive for indefinite time
# --------------------------------------------------------------------------------------------------

#touch /tmp/a.txt
#tail -f /tmp/a.txt
