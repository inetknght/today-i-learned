ARG DOCKER_PYTHON_VERSION=3.7.4-buster
FROM python:${DOCKER_PYTHON_VERSION}

COPY requirements.txt /inetknght/

RUN true \
	&& python3 \
		-m venv /inetknght \
	&& /inetknght/bin/python3 \
		-m pip \
		install -r /inetknght/requirements.txt \
	&& true

EXPOSE 8888
STOPSIGNAL SIGTERM

HEALTHCHECK \
	--interval=5s \
	--timeout=5s \
	--start-period=5s \
	--retries=1 \
	CMD /inetknght/bin/python3 /inetknght/self-healthcheck.py

COPY configurator.py self-healthcheck.py /inetknght/

# Consider --port=portnumber in command line,
# or HEALTHCHECK_PORT=portnumber in environment
CMD /inetknght/bin/python3 /inetknght/configurator.py --listen
