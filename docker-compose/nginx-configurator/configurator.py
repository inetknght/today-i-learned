
import sys
import os
import json
import secrets

import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define as define_opt
from tornado.options import options
import tornado.escape
import tornado.log

import logging
_logger = logging.getLogger('tornado.general')

define_opt('listen', default=False, type=bool, help='listen to me dude')
define_opt('port', default=os.environ.get('LISTEN_PORT', 8888), help='what do you think this does')

class MainHandler(tornado.web.RequestHandler):
    def json(self, j):
        self.set_status(200)
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        self.write(json.dumps(j))
        self.finish()

    def selfcheck(self):
        if self.request.remote_ip != '127.0.0.1':
            raise tornado.web.HTTPError(400)
        _logger.info('-> self-check')
        tokens = self.get_body_arguments('token', None)
        if None == tokens or 1 != len(tokens):
            raise tornado.web.HTTPError(400)
        token = tokens[0]
        if token != self.application._token:
            raise tornado.web.HTTPError(403)
        return self.json({
            'all_ok': True
        })

    def decode_argument(self, value: bytes, name: str = None) -> str:
        if 'digest' == name or 'token' == name:
            return value
        return super().decode_argument(value=value,name=name)

    def instruct_exit(self, exit_code = None):
        return {
            'exit': int(exit_code) if None != exit_code else 0
        }

    def instruct_rename(self, newname):
        return {
            'rename': newname
        }

    def instruct_reload(self, digest):
        return {
            'reload': '/{}'.format(tornado.escape.url_escape(digest))
        }

    def consider(self, digest, iam):
        # {'command': 'exit'} # client shall exit
        # {'command': 'reload', 'url': '/digest'} # client shall request a new configuration
        # {'command': 'rename', 'name': 'h3110w0r1d'} # use a new alias instead of socket.gethostname()
        _logger.info('-> Checkin: {}'.format(iam))
        return self.json({
            'commands': [
                self.instruct_rename('h3110w0rld'),
                self.instruct_reload(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'),
                self.instruct_exit(),
            ]
        })

    def get(self):
        selfcheck = self.get_argument('selfcheck', None)
        if None != selfcheck:
            return self.selfcheck()
        iam = self.get_argument('iam', None) # socket.gethostname()
        if None == iam:
            raise tornado.web.HTTPError(400)
        digest = self.get_argument('digest', None) # sha256(nginx -T)
        if None == digest:
            raise tornado.web.HTTPError(400)
        return self.consider(digest, iam)

class ConfiguratorApp(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        self._token = secrets.token_bytes(32)
        with open('/tmp/selfcheck-key', 'wb') as f:
            f.write(self._token)
        super().__init__(*args, **kwargs)

def make_app():
    return ConfiguratorApp([
        (r"/", MainHandler),
    ])

def run_listen():
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

def main():
    _logger.fatal(sys.argv)
    tornado.options.parse_command_line()
    if options.listen:
        return run_listen()
    options.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
