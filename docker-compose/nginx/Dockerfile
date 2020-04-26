
# For version pinning
ARG DEBIAN_PYTHON_VERSION=3.7.4
ARG DOCKER_NGINX_VERSION=latest
FROM nginx:${DOCKER_NGINX_VERSION}

# Only the ARG variables after FROM are visible in that FROM's scope.
# If the ARG has the same name as used elsewhere, then a default isn't needed.
ARG DEBIAN_PYTHON_VERSION

RUN true \
	&& apt-get update \
	&& apt-get install -y \
		python3="${DEBIAN_PYTHON_VERSION}" \
		python3-venv \
		python3-pip \
	&& apt-get clean \
	&& rm -Rf /var/lib/apt/lists/* \
	&& python3 -m pip install --upgrade pip \
	&& true

COPY requirements.txt /inetknght/

RUN true \
	&& python3 -m venv /inetknght \
	&& /inetknght/bin/python3 -m pip install -r /inetknght/requirements.txt \
	&& true

COPY healthcheck.py /inetknght
RUN /inetknght/bin/python3 /inetknght/healthcheck.py --you-are-in-docker-build

# https://stackoverflow.com/a/42738182/1111557
# docker inspect --format '{{json .State.Health }}' nginx.inetknght_1 | jq
HEALTHCHECK \
	--interval=30s \
	--timeout=5s \
	--start-period=5s \
	--retries=1 \
	CMD /inetknght/bin/python3 /inetknght/healthcheck.py --healthcheck

EXPOSE 443
