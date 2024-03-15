# Docker Build Process

Docker-Compose is used to create two containers--

- **app**  
    This includes a GUnicorn WSGI server and the BingoSurvey Flask app.
- **db**  
    This is just a MySQL container connected to BingoSurvey-App.

## Building

To build the production images, from this directory, run
``` bash
docker compose build
```

## Running

To use the production containers, after building, create a `.env` file of the following sort:
``` bash
# Required for the Flask app
SECRET_KEY="CHANGE THIS"
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE="<Strict/Lax/None>"

# For communication with the database
MYSQL_PASSWD="ChangeThisPasswd"

# Ports to bind to; specify if different ports are required
#HTTP_PORT=80
#HTTPS_PORT=443  # Irrelevant if cert/key are not specified

# For SSL/TLS; Both SSL_PEM and SSL_KEY must be specified
#SSL_CERT="/path/to/ssl.cert"
#SSL_KEY="/path/to/ssl.key"
```

... and then run
``` bash
docker compose up
```

to start the containers, and

``` bash
docker compose down
```
to stop and remove/clean up the containers.

## Database Persistence
A volume will be automatically created by docker-compose for database persistence. Even after rebuilding the images or stopping the containers, this volume will still be present until deleted manually.


## Database Healthcheck and Startup Procedure
The app container will not start until the database has passed its healthcheck and is ready to start receiving requests. See `docker-compose.yaml`.

## Empty Certificates
`nocert.pem` and `nokey.pem` should be left as blank files- these are bind-mounted as volumes to the container if no keys are specified in the `.env` and should be blank so the server knows not to try to run in SSL/TLS mode.
