#!/usr/bin/env python
"""
Simple simulation of a Sparkplug Edge Node with the ID Edge_Node_Temperature_Sensor. It interfaces

* One Device (Temperature_Sensor)
* One Device Metric (Temperature) of type float

The device is a sensor measuring the value of 'Temperature' with a framerate of 10/s and the data is being
published to a MQTT broker.
"""

import os
import time
import random
import logging
from pysparkplug_builder import SparkplugGroup

LOG_LEVEL=os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("sensor")

def read_sensor(n: int = 100000, fps: int = 1, value: float = 25.0):
    """
    Simulates reading values from a sensor.

    This generator function yields `n` sensor readings. The readings are spaced according to the specified
    frames per second (fps).

    Args:
        n (int, optional): Number of sensor readings to generate. Defaults to 100.
        fps (int, optional): Frames per second (readings per second). Controls the delay between each reading.
            Defaults to 10.
        value (float, optional): 
    Yields:
        float: A simulated sensor reading.

    Example:
        for reading in read_sensor(n=5, fps=2):
            print(reading)
    """
    _value = value
    for _ in range(n):
        yield _value
        time.sleep(1 / fps)
        _value += random.gauss(mu=-_value/10, sigma=value/5)


# Load definition of the sparkplug group from a file. The location of the config file is given by the
# environment variable SPARKPLUG_GROUP_CONFIG
group = SparkplugGroup()

# Create a particular node
edge_node_builder = group.edge_nodes["Edge_Node_Temperature_Sensor"]
edge_node = edge_node_builder.build()

# Connect to broker
edge_node.connect()

# The metric_builder is used to create and publish a new value of the given metric
metric_builder = edge_node_builder.devices["Temperature_Sensor"].metrics["Temperature"]

time.sleep(3)

# Read sensor data
try:
    for next_value in read_sensor():
        logger.info("publishing metric %s=%s", metric_builder.name, next_value)
        metrics = [
                metric_builder.build_value(next_value)
        ]

        # send data
        edge_node.update_device("Temperature_Sensor", metrics)


    # clean up
except KeyboardInterrupt:
    pass
finally:
    edge_node.deregister("Temperature_Sensor")
    edge_node.disconnect()
