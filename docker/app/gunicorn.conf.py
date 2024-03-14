"""Configuration file for gunicorn"""

import os
from multiprocessing import cpu_count

# gunicorn configuration

workers = cpu_count()
threads = 2

# Example for setting up SSL/TLS if you have certs... Perhaps should be env-var specified?
#
# if os.path.exists("/etc/ssl/app_cert/server.key") and os.path.exists(
#     "/etc/ssl/app_cert/server.pem"
# ):
#     # HTTPS:
#     keyfile = "/etc/ssl/app_cert/server.key"
#     certfile = "/etc/ssl/app_cert/server.pem"
#     ssl_version = "TLS"
#     # Bind:
#     bind = [f'0.0.0.0:{os.environ.get("PORT", 443)}']
# else:
#     # Bind:
#     bind = [f'0.0.0.0:{os.environ.get("PORT", 80)}']

# Bind to the specified port, or port 80 if unspecified
bind = [f'0.0.0.0:{os.environ.get("GUNICORN_PORT", 80)}']

# Logging:
accesslog = "-"  # Access log to stdout; use docker's built-in logging

# Reduce crashing on lower-power servers:
preload_app = True
timeout = 120
graceful_timeout = 90
