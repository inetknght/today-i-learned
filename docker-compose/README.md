# Docker Healthcheck

Today I learned Docker Healthcheck.

Not 100% how I like it, but good enough to demo. Demonstrate Docker Healthcheck
which runs a command to query the local container for hostname (container name)
and nginx configuration. Send that information to another container running a
python script. Python script determines whether to shutdown or reload or rename
the nginx container.

Good enough for a healthcheck. Need to be built on though.

# TODO

Story slides showing how it works.

# Containers

There are two example containers.

## `nginx.inetknght`

The nginx container is built FROM the base `nginx` image. The Docker build
process will install Python and any requirements in the `requirements.txt`. Then
it will copy the healthcheck script in. It will run the healthcheck script once
to prove that it's reasonable syntax.

When the container is running, the `healthcheck.py` script will query `nginx` to
dump its configuration (`nginx -T`) and then send a hash of the configuration to
the other container, `nginx-configurator`. Not a good name for it. Whatever.
It's executed inside of the container every interval specified by the
HEALTHCHECK command in the Dockerfile. This could of course be overridden in
`docker-compose.yml`.

## `nginx-configurator.inetknght`.

The `nginx-configurator` container is built from the base `python` image. It
runs a Tornado-based HTTP server scripted with Python. The `healthcheck.py`
will connect to this Tornado instance and check in. Any instruction, such as ask
nginx to exit, is given by the check in.

Contrast with shutdown via other means.
