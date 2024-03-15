"""Configuration file for gunicorn"""

import os
from multiprocessing import cpu_count

# gunicorn configuration

workers = cpu_count()
threads = 2

# Don't change these; instead mount different keys to these targets
# from env vars passed to docker compose.
SSL_KEY_FILE="/etc/ssl/server_key.pem"
SSL_PEM_FILE="/etc/ssl/server_cert.pem"

# Set up SSL/TLS if certs exist
if os.path.exists(SSL_KEY_FILE) and os.path.exists(SSL_PEM_FILE) \
  and os.stat(SSL_KEY_FILE).st_size > 0 and os.stat(SSL_PEM_FILE).st_size > 0:

     global ssl_context
     def ssl_context(conf, default_ssl_context_factory):
          import ssl
          context = default_ssl_context_factory()
          context.minimum_version = ssl.TLSVersion.TLSv1_3
          return context

     # HTTPS:
     keyfile = SSL_KEY_FILE
     certfile = SSL_PEM_FILE
     # Bind:
     bind = [f'0.0.0.0:{os.environ.get("PORT", 443)}']
else:
     # Bind:
     bind = [f'0.0.0.0:{os.environ.get("PORT", 80)}']

# Logging:
accesslog = "-"  # Access log to stdout; use docker's built-in logging

# Reduce crashing on lower-power servers:
preload_app = True
timeout = 120
graceful_timeout = 90
