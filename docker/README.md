# Docker Build Process

Docker-Compose is used to create two containers--

- **app**  
    This includes a GUnicorn WSGI server and the BingoSurvey Flask app.
- **db**  
    This is just a MySQL container connected to BingoSurvey-App.

