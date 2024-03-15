FROM python:3.12-bookworm

WORKDIR /usr/src/app

# Copy GUnicorn config
COPY docker/app/gunicorn.conf.py ./

# Copy start script
COPY docker/app/start_production.sh ./
RUN chmod +x start_production.sh

# Copy & install requirements
COPY docker/app/requirements.txt ./production_requirements.txt
RUN pip install --no-cache-dir -r production_requirements.txt

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Starting command
ENTRYPOINT '/usr/src/app/start_production.sh'
