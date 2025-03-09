#!/usr/bin/env python3

import asyncio
import logging
import json
import os

import pyemvue

from vue_exporter.vue_wrapper import VueWrapper
from vue_exporter.metrics_server import MetricsServer

_LOGGER = logging.getLogger(__name__)
_NAME = 'emporia-vue-exporter'

'''
  Entry point. Boiler plate stuff.
'''
async def main():
  # Logger
  logging.basicConfig(level=logging.INFO)

  # Get version info
  history_file_name = 'history.md'
  if os.path.exists(history_file_name):
    with open(history_file_name) as file:
      # Assuming 1st line of history file lookss like '### 0.1.0'
      _VERSION = file.readline().strip('\n').split()[1]
  else:
    _LOGGER.warning('history.md / version file not found. Unable to determine version number')
    _VERSION = 'unknown'

  # Print version info
  _LOGGER.info(f'Running {_NAME}: v{_VERSION}')

  # Get login.json
  login_file_name = 'secrets/login.json'

  if not os.path.exists(login_file_name):
    exit("No Login info found. Please provide login.json file")

  with open(login_file_name) as file:
    login_data = json.load(file)
  if 'username' not in login_data:
    exit('Error: no username')
  if 'password' not in login_data:
    exit('Error: no password')

  # Start the service
  _LOGGER.info('Starting service')
  token_file_name = 'secrets/token.json'
  await start_service(login_data['username'], login_data['password'], token_file_name)

  _LOGGER.info('Service stopped')

'''
  Start service
'''
async def start_service(username: str, password: str, token_storage_file: str):
  # Initialize metrics server
  port = os.environ.get('MERTIRCS_SERVER_PORT', 9090) # 9090 by default
  metrics_server = MetricsServer(port=port)

  # Login
  vue = pyemvue.PyEmVue()
  try:
    _LOGGER.info('Trying to log in with stored tokens')
    with open(token_storage_file) as file:
      token_data = json.load(file)
      vue.login(
        id_token=token_data['id_token'],
        access_token=token_data['access_token'],
        refresh_token=token_data['refresh_token'],
        token_storage_file=token_storage_file
      )
  except:
    _LOGGER.info(f'Logging in using username {username}')
    vue.login(username, password, token_storage_file=token_storage_file)

  # Initialzie Vue wrapper
  vue_wrapper = VueWrapper(vue)

  # Register vue handle with server
  metrics_server.register_vue_wrapper(vue_wrapper)

  _LOGGER.info('Starting metrics server')
  await metrics_server.run_app()

  await asyncio.sleep(1)


if __name__ == '__main__':
  asyncio.run(main())
