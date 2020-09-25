#!/bin/bash

exec gunicorn etos_api.webserver:FALCON_APP \
	--name etos_api \
	--worker-class=gevent \
	--bind 0.0.0.0:8080 \
	--worker-connections=1000 \
	--workers=5 \
	--reload
