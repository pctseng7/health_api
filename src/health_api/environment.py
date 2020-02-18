import os
import logging

class HostEnvironment(object):
    """Provides access to common aspects of the container environment, including
    important system characteristics, filesystem locations, and configuration settings.
    """

    BASE_DIRECTORY = "/opt/ml"
    DEFAULT_DOWNLOAD_DIR_PARAM = "DEFAULT_DOWNLOAD_DIR"
    JOB_NAME_ENV = "JOB_NAME"
    USE_NGINX_ENV = "USE_NGINX"
    HEALTH_SSL_AUTH_ENABLED = "HEALTH_SSL_AUTH_ENABLED"
    GUNICORN_SERVER_WORKER_TIMEOUT = "GUNICORN_SERVER_WORKER_TIMEOUT"
    GUNICORN_SERVER_WORKER_NUM = "GUNICORN_SERVER_WORKER_NUM"
    LOG_LEVEL = "LOG_LEVEL"

    def __init__(self):
        
        # Define the health report download location 
        self.default_storage_dir = os.environ.get("DEFAULT_DOWNLOAD_DIR", "/opt/ml/downloads")

        # Set SSL Auth Enabled Env Var
        self.health_ssl_enabled = os.environ.get("HEALTH_SSL_AUTH_ENABLED", True)

        # Enabled nginx if set to True
        self.use_nginx = os.environ.get("USE_NGINX", False)

        # Define web server worker timeout
        self.server_worker_timeout = os.environ.get("GUNICORN_SERVER_WORKER_TIMEOUT", 60)

        # Define web server worker number(s)
        self.server_worker_num = os.environ.get("GUNICORN_SERVER_WORKER_NUM", 1)

        # Set the log level
        self.log_level = os.environ.get("LOG_LEVEL", 20)


def configure_logging():
    
    env = HostEnvironment()

    if env.log_level == 10:
        default_level = logging.DEBUG
    elif env.log_level == 20:
        default_level = logging.INFO
    elif env.log_level == 30:
        default_level = logging.WARN
    else:
        default_level = logging.ERROR

    logging.basicConfig(format=format, level=default_level)
    logging.getLogger("download").setLevel(default_level)