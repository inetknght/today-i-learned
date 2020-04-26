#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import hashlib
import socket
import json

from urllib.parse import urlparse

import requests
import logging

class inetknghtNginxHealthcheck(object):
    def __init__(self):
        self.args_parser = self._build_args_parser()
        self.args = None

    def _build_args_parser(self):
        parser = argparse.ArgumentParser(
            description="inetknght's nginx healthcheck thing"
        )
        parser.add_argument(
            '--you-are-in-docker-build', action='store_true',
            help="nginx isn't running, so just check that things look okay"
        )
        parser.add_argument(
            '--healthcheck', action='store_true',
            help="nginx is running. check its health, my dude!"
        )
        parser.add_argument(
            '--echo-config', action='store_true',
            help="echo the config getting hashed"
        )
        return parser

    def parse_args(self):
        self.args = self.args_parser.parse_args()
        if self.args.you_are_in_docker_build:
            print("Script executed, imports are good.")
            sys.exit(0)
        if not self.args.healthcheck:
            print(
                "What do you want me to do, man?"
                " Did you forget to add --healthcheck to the invokation?",
                file=sys.stderr
            )
            sys.exit(1)

    def get_nginx_config(self):
        nginx_T = subprocess.run(["nginx", "-T"], capture_output=True)
        if 0 != nginx_T.returncode:
            return None, nginx_T.stderr
        config = nginx_T.stdout
        del nginx_T
        sha256 = hashlib.sha256(config)
        digest = sha256.digest()
        del sha256
        return digest, config

    def session(self):
        a = requests.adapters.HTTPAdapter(max_retries=0)
        s = requests.Session()
        s.mount('http://', a)
        return s

    def get_checkin_url(self):
        # see also docker-compose.yml, there's a service named this
        urlstr = 'http://nginx-configurator.inetknght:8888/'
        url = urlparse(urlstr)
        #
        # If someone knows how to fix this, please make a PR for it.
        # urlparse() returns a named tuple, which can't be modified.
        # but there's _replace() which lets you modify the netloc
        # but it does not let you modify the port.
        # url._replace(port=port)
        port = os.environ.get('HEALTHCHECK_PORT', url.port)
        url = url._replace(netloc='{}:{}'.format(url.hostname, port))
        return url.geturl()

    def run(self):
        logging.fatal('healthcheck.py {}'.format(sys.argv))
        self.parse_args()
        digest, config = self.get_nginx_config()
        try:
            config_utf = config.decode(errors='strict')
            del config
            config_error = None
        except UnicodeError as e:
            print(config_error, file=sys.stderr)
            config_error = e
        if self.args.echo_config:
            if None != config_error:
                sys.stderr.write(config)
            else:
                print(config_utf)
        with self.session() as s:
            params={
                'digest': digest,
                'iam': socket.gethostname(),
            }
            data = None
            if config_error:
                params['config_error'] = 'in-healthcheck-request-body'
                data = str(config_error)
            try:
                r = s.get(
                    self.get_checkin_url(),
                    timeout=1.,
                    params=params,
                    data=data
                )
                r.raise_for_status()
                if 204 == r.status_code:
                    return
            except requests.urllib3.exceptions.NewConnectionError as e:
                print(e)
                sys.exit(1)
            except requests.exceptions.HTTPError as e:
                print(e)
                sys.exit(1)

def main():
    hc = inetknghtNginxHealthcheck()
    hc.run()

if __name__ == "__main__":
    main()
