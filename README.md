<!--
SPDX-FileCopyrightText: Copyright (C) 2025 IndiScale GmbH <info@indiscale.com>
SPDX-FileCopyrightText: Copyright (C) 2025 Timm Fitschen <t.fitschen@indiscale.com>

SPDX-License-Identifier: MIT
-->

# Testbed of the BatCAT Online Characterization Framework

See a video demonstration on youtube: https://youtu.be/OiTLQB4YK3Y

## Requirements

This was tested with the following configuration

* Linux (Fedora 41) - Mac and Windows are not tested
* Bash==5.2.26
* Git==2.49.0
* Python==3.13, recent pip==25.2
* Docker==28.1.1

The required python packages are listed in [requirements.txt](./requirements.txt).

## Setup

### Environment

> Note: You need a github account with SSH setup and read permissions for the `HE-BatCAT/Pysparkplug-Builder`

* Initialize a virtual environment (recommended):
  ```shell
  python -m venv .venv
  source .venv/bin/activate
  ```
* Install development requirements from `dev-requirements.txt`:
  ```shell
  pip install -r requirements.txt
  ```

## Start the Testbed

This will
* start a Mosquitto MQTT broker
* start two Sparkplug Edge Nodes (i.e. MQTT clients) with a single Device each:
    * one simulates a temperature sensor
    * one simulates an actuator, a power switch
* start a "Digital Twin", a MQTT client which listens on the temperature sensor and send a command to the
  actuator

You'll need AT LEAST four shell tabs/windows.

### 1. Start MQTT Broker (Mosquitto)

Run

```
docker compose up mosquitto
```

### 2. Start the Digital Twin (Python Script)

Run

```
./digital_twin/digital_twin.py
```

### 3. Start the Actuator Edge Node

Run

```
./actuator/actuator.py
```

### 4. Start the Sensor

Run

```
./sensor/sensor.py
```

### Watch

* All components will log verbosely what is happening.
* Look at the output of the digital twin for a line that goes:
  ```
  INFO:digital_twin_adapter:######## Send command: Device_Control/Switch_On=False
  ```
* Look at the output of the actuator for a line that goes:
  ```
  INFO:actuator:######## Received command: Device_Control/Switch_On=False
  ```

## Contact

* (Lead) Timm Fitschen <mailto:t.fitschen@indiscale.com>

## License

This software and all files are licensed under the [MIT License](./LICENSES/MIT.txt) unless expressly stated otherwise.
You can also obtain a copy of the license under <https://opensource.org/license/MIT>.

## Copyright

* Copyright (C) 2025 Timm Fitschen <mailto:t.fitschen@indiscale.com>
* Copyright (C) 2025 IndiScale GmbH <mailto:info@indiscale.com>
