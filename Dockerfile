FROM python:latest

# Metadata
LABEL org.opencontainers.image.authors="ghostvr"

# ARG & ENV variables
ARG PORT=9091
ENV MERTIRCS_SERVER_PORT=$PORT
ENV USE_LOGIN_INFO_FROM_ENV=1

# Ports
EXPOSE $PORT/tcp

# Code
COPY code /usr/src/app
WORKDIR /usr/src/app
COPY pip-requirements.txt ./
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r ./pip-requirements.txt

CMD ["python", "./main.py"]
