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

## Testing

To test the production containers, after building, create a .env file of the following sort:
``` env
SECRET_KEY="CHANGE THIS"
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE="<Strict/Lax/None>"
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


### TODO: Database persistence & Document volume used for such a purpose