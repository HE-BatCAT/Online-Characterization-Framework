#!/usr/bin/env python
"""
Simple simulation of a Sparkplug Edge Node with the ID Edge_Node_Power_Switch. It interfaces

* One Device (Power_Switch)
* One Device Metric (Device_Control/Switch_On) of type boolean.

This Edge Node subscribes to an MQTT broker.
"""
import os
import time
import logging
import pysparkplug as psp
from pysparkplug_builder import SparkplugGroup

LOG_LEVEL=os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("actuator")


# Load definition of the sparkplug group from a file. The location of the config file is given by the
# environment variable SPARKPLUG_GROUP_CONFIG
group = SparkplugGroup()

# Create a particular node
edge_node_builder = group.edge_nodes["Edge_Node_Power_Switch"]

# The metric_builder is used to create and publish a new value of the given metric
metric_builder = edge_node_builder.devices["Power_Switch"].metrics["Device_Control/Switch_On"]

@edge_node_builder.devices["Power_Switch"].listener("Device_Control/Switch_On", psp.MessageType.DCMD)
def handle_switch_command(value):
    logger.info("######## Received command: %s=%s", metric_builder.name, value)

    # return new state -> get's published such that the whole network knows about it and is a way of
    # confirming the state change to the issuer of the command
    return value

# set initial state
edge_node_builder.devices["Power_Switch"].metrics["Device_Control/Switch_On"].value = True


edge_node = edge_node_builder.build()
logger.info("Initial value %s=%s",
    edge_node_builder.devices["Power_Switch"].metrics["Device_Control/Switch_On"].name,
    edge_node_builder.devices["Power_Switch"].metrics["Device_Control/Switch_On"].value)
try:
    edge_node.connect(blocking=True)
except KeyboardInterrupt:
    pass
finally:
    edge_node.disconnect()
