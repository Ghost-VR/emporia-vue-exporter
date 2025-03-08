import pyemvue
from pyemvue.enums import Scale, Unit

'''
  Basically a wrapper around pyemvue so things are processed in a more civialized way.
'''
class VueWrapper:
  '''
    Initialier
  '''
  def __init__(
    self,
    vue_instance: pyemvue.PyEmVue
  ) -> None:
    self._vue: pyemvue.PyEmVue = vue_instance

    # Propagate stuff
    devices = self._vue.get_devices()
    self._device_gids = []
    self._device_info = {}

    # Note: each device will show up as 2 instances in get_devices() function.
    for device in devices:
      if not device.device_gid in self._device_gids:
        self._device_gids.append(device.device_gid)
        self._device_info[device.device_gid] = device
      else:
        self._device_info[device.device_gid].channels += device.channels

  '''
    Get device / channel info
  '''
  def get_device_info(self):
    devices = {}
    # Iterate devices
    for device_id, device_inst in self._device_info.items():
      device = {
        'device_id': device_id,
        'model': device_inst.model,
        'device_name': device_inst.device_name,
        'display_name': device_inst.display_name,
        'channels': {}
      }
      # Iterate channels
      for channel_inst in device_inst.channels:
        channel = {
          'channel_num': channel_inst.channel_num,
          'channel_name': channel_inst.name
        }
        device['channels'][channel_inst.channel_num] = (channel)
      devices[device_id] = device
    return devices

  '''
    Get metrics of a single type
  '''
  def get_usage_single_metric(self, unit_name: str='V'):
    if unit_name == 'V':
      unit_name = 'voltage_volt'
      unit = Unit.VOLTS.value
      scale = 1
    elif unit_name == 'A':
      unit_name = 'current_ampere'
      unit = Unit.AMPHOURS.value
      scale = 3600
    elif unit_name == 'W':
      unit_name = 'power_watt'
      unit = Unit.KWH.value
      scale = 1000 * 3600

    raw_usage = self._vue.get_device_list_usage(
      deviceGids=self._device_gids,
      instant=None,
      scale=Scale.SECOND.value,
      unit=unit
    )

    channel_usages = []

    for device_id, device_usage_inst in raw_usage.items():
      for channel_num, channel_usage_inst in device_usage_inst.channels.items():
        channel = {
          'device_id': device_id,
          'channel_num': channel_num,
          'metric': channel_usage_inst.usage * scale
        }
        channel_usages.append(channel)

    return {
      'unit_name': unit_name,
      'channel_usages': channel_usages
    }

  '''
    Get all metrics
  '''
  def get_usage_all_metrics(self):
    voltage_metric = self.get_usage_single_metric('V')
    current_metric = self.get_usage_single_metric('A')
    power_metric = self.get_usage_single_metric('W')

    return [
      voltage_metric, current_metric, power_metric
    ]
