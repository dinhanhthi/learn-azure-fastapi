#!/bin/sh
set -e
echo "Starting SSH ..."
service ssh start
exec fastapi run app.py --host 0.0.0.0 --port 8000