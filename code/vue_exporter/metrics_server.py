import asyncio
import json
import time
import logging

from aiohttp import web

from vue_exporter.vue_wrapper import VueWrapper

_LOGGER = logging.getLogger(__name__)

'''
  Metrics server that handles requests
'''
class MetricsServer:
  '''
    Initialize
  '''
  def __init__(
    self,
    port
  ) -> None:
    self._port = port
    self._app = None

  '''
    Register VueWrapper instance with this server
  '''
  def register_vue_wrapper(self, wrapper: VueWrapper):
    self._wrapper: VueWrapper = wrapper

  '''
    Entry point of server
  '''
  async def run_app(self):
    self._app = web.Application()
    self._app.add_routes([web.get('/status', self.handle_status)])
    self._app.add_routes([web.get('/data_json', self.handle_data_json)])
    self._app.add_routes([web.get('/metrics', self.handle_metrics)])

    runner = web.AppRunner(self._app)
    await runner.setup()

    site = web.TCPSite(runner, '0.0.0.0', self._port)
    await site.start()

    # Keep server running
    while True:
      await asyncio.sleep(36000)

  '''
    Status page
  '''
  async def handle_status(self, request):
    status = self._wrapper.get_device_info()
    text = json.dumps(status, indent=2)
    return web.Response(text=text)

  '''
    Get usage data in json format
  '''
  async def handle_data_json(self, request):
    metrics = self._wrapper.get_usage_all_metrics()
    text = json.dumps(metrics, indent=2)
    return web.Response(text=text)

  '''
    Metrics page
  '''
  async def handle_metrics(self, request):
    text = ''

    start_time = round(time.time() * 1000)

    device_info = self._wrapper.get_device_info()
    all_metrics = self._wrapper.get_usage_all_metrics()

    end_time = round(time.time() * 1000)
    _LOGGER.info(f'Query duration: {end_time - start_time} ms')

    for metric in all_metrics:
      for channel in metric['channel_usages']:
        channel_info = device_info[channel['device_id']]['channels'].get(channel['channel_num'])
        channel_name = channel_info['channel_name'] if channel_info else channel['channel_num']

        text += f'{metric['unit_name']} '
        text += '{'
        text += f'channel_num="{channel['channel_num']}", device_id="{channel['device_id']}", channel_name="{channel_name}"'
        text += '} '
        text += f'{channel['metric']}\n'
    return web.Response(text=text)
