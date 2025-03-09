FROM python:latest

# Metadata
LABEL org.opencontainers.image.authors="ghostvr"

# ARG & ENV variables
ENV METIRCS_SERVER_PORT=9090

# Ports
EXPOSE 9090/tcp

# Files setup
WORKDIR /usr/src/app
COPY code pip-requirements.txt history.md docker_init/login.json.init ./
RUN mkdir -p secrets
RUN mv login.json.init secrets/login.json

# Run initial setup
RUN pip install --upgrade setuptools && \
    pip install --no-cache-dir -r ./pip-requirements.txt

# Entry point
CMD ["python", "./main.py"]
