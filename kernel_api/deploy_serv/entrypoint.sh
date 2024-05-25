#!/bin/bash
PATH="/app/venv/bin:$PATH"
WORKERS_COUNT="${WORKERS_COUNT:=1}"
BIND_ADDRESS="${BIND_ADDRESS:=0.0.0.0:2000}"
LOG_LEVEL="${LOG_LEVEL:=info}"
exec gunicorn --bind $BIND_ADDRESS main:app -w $WORKERS_COUNT -k uvicorn_settings.MyUvicornWorker --log-level $LOG_LEVEL