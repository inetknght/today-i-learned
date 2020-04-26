
import sys
import os
import tornado.escape
import requests
import logging

logging.fatal('self-healthcheck.py {}'.format(sys.argv))

# /tmp/selfcheck-key is created during ConfiguratorApp.__init__
# its contents unlocks /?selfcheck and must be submitted in the body.
with open('/tmp/selfcheck-key', 'rb') as f:
    token = f.read(32)

port = os.environ.get('HEALTHCHECK_PORT', 8888)

r = requests.get(
    # tempted to use 'localhost',
    # but avoid requiring a name lookup (localhost could be overridden in hosts)
    'http://127.0.0.1:{}/'.format(port),
    params={ # url query arguments
        'selfcheck': True,
    },
    data={ # form fields
        # hide token from log messages (which include query parameters)
        'token': token
    },
    timeout=1.0 # avoid name lookup, otherwise this timeout might not be respected
)
r.raise_for_status()

if r.status_code != 200:
    sys.stderr.write(r.text)
    sys.exit(1)
