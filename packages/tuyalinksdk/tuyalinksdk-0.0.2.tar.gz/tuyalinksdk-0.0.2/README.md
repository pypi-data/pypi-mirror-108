# Tuya IoT Device SDK for Python

- [Tuya IoT Device SDK for Python](#tuya-iot-device-sdk-for-python)
  - [Installation](#installation)
    - [Minimum Requirements](#minimum-requirements)
    - [Install from PyPI](#install-from-pypi)
    - [Install from source](#install-from-source)
  - [Examples](#examples)
- [License](#license)

## Installation

### Minimum Requirements
*   Python 3.6+

### Install from PyPI
```
python3 -m pip install tuyalinksdk
```

### Install from source
```
git clone https://github.com/tuya/tuya-iot-link-sdk-python.git
python3 -m pip install ./tuya-iot-link-sdk-python
```

## Examples

[Examples README](examples)

```python
from tuyalinksdk.client import TuyaClient

client = TuyaClient(productid='<PID>', uuid='<UUID>', authkey='<AUTHKEY>')

def on_connected():
    print('Connected.')

def on_dps(dps):
    print('DataPoints:', dps)
    client.push_dps(dps)

client.on_connected = on_connected
client.on_dps = on_dps
client.connect()
client.loop_start()
```

# License

This library is licensed under the MIT License.
