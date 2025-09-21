#!/usr/bin/env python
"""
Simple simulation of a Sparkplug Edge Node with the ID edge-node-actuator-1. It interfaces

* One Device (actuator-1)
* One Device Metric (y) of type boolean.

The device is an actuator which can be controlled with the y metric. This could be the device being switched
on or off. This Edge Node subscribes to an MQTT broker.

This Edge Node will accept command from the Primary Host Application "digital-twin" only.
"""

import time
import logging
import pysparkplug as psp
from pysparkplug_builder import SparkplugGroup

logging.basicConfig(level=logging.DEBUG)


# Load definition of the sparkplug group from a file. The location of the config file is given by the
# environment variable SPARKPLUG_GROUP_CONFIG
group = SparkplugGroup()

# Create a particular node
edge_node_builder = group.edge_nodes["Edge_Node_Power_Switch"]

# The metric_builder is used to create and publish a new value of the given metric
metric_builder = edge_node_builder.devices["Power_Switch"].metrics["Device_Control/Switch_On"]

@edge_node_builder.devices["Power_Switch"].listener("Device_Control/Switch_On", psp.MessageType.DCMD)
def handle_switch_command(value):
    print("##################### SWITCH ON: ", value)

    # return new state -> get's published such that the whole network knows about it and is a way of
    # confirming the state change to the issuer of the command
    return value

# This handles the command message
@edge_node_builder.devices["Power_Switch"].cmd_callback
def callback(client: psp.Client, message: psp.Message) -> None:
    print("message", message)


# set initial state
edge_node_builder.devices["Power_Switch"].metrics["Device_Control/Switch_On"].value = True

edge_node = edge_node_builder.build()
try:
    edge_node.connect(blocking=True)
except KeyboardInterrupt:
    pass
finally:
    edge_node.disconnect()
