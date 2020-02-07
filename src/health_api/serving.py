import logging
import os
import signal
import subprocess
from flask import Flask
import health_api 

logger = logging.getLogger(__name__)


class Server(object):
    """A simple web service wrapper for download/upload health reports from AWS.
    """

    def __init__(self, name, env=None):
        """ Initialize the web service instance.
        :param name: the name of the service
        
        """
        self.app = self._build_flask_app(name)
        self.log = self.app.logger
        self.env = health_api.HostEnvironment() if env is None else env

    @classmethod
    def from_env(cls):
        health_api.configure_logging()
        logger.info("creating Server instance")
        env = health_api.HostEnvironment()

        server = Server("Web Server", env)
        logger.info("returning initialized server")
        return server

    @classmethod
    def start(cls):
        """Prepare the container for model serving, configure and launch the model server stack.
        """

        env = health_api.HostEnvironment()

        gunicorn_bind_address = '0.0.0.0:{}'.format(env.http_port)
        
        # if env.use_nginx:
        #     logger.info("starting nginx")
        #     Server._create_nginx_config(env)
        #     subprocess.check_call(['ln', '-sf', '/dev/stdout', '/var/log/nginx/access.log'])
        #     subprocess.check_call(['ln', '-sf', '/dev/stderr', '/var/log/nginx/error.log'])
        #     gunicorn_bind_address = 'unix:/tmp/gunicorn.sock'
        #     nginx_pid = subprocess.Popen(['nginx', '-c', nginx_config_file]).pid

        logger.info("starting gunicorn")
        gunicorn_pid = subprocess.Popen(["gunicorn",
                                         "--timeout", str(env.server_worker_timeout),
                                         "-k", "gevent",
                                         "-b", gunicorn_bind_address,
                                         "--worker-connections", str(1000 * env.server_worker_num),
                                         "-w", str(env.model_server_workers),
                                         "container_support.wsgi:app"]).pid

        signal.signal(signal.SIGTERM, lambda a, b: Server._sigterm_handler(nginx_pid, gunicorn_pid))

        # children = set([nginx_pid, gunicorn_pid]) if nginx_pid else gunicorn_pid
        children = gunicorn_pid
        logger.info("inference server started. waiting on processes: %s" % children)

        while True:
            pid, _ = os.wait()
            if pid in children:
                break

        Server._sigterm_handler(gunicorn_pid)


    def _build_flask_app(self, name):
        """ Construct the Flask app that will handle requests.
        :param name: the name of the service
        :return: a Flask app ready to handle requests
        """
        app = Flask(name)
        app.add_url_rule('/ping', 'healthcheck', self._healthcheck)
        app.add_url_rule('/download', 'download', self._download, methods=["GET"])
        app.register_error_handler(Exception, self._default_error_handler)
        return app

    def _healthcheck(self):
        return ''

    def _download(self):
        return ''

    def _default_error_handler(self, exception):
        return ''