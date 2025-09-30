#!/usr/bin/env python
import logging
import pysparkplug as psp
from pysparkplug_builder import SparkplugGroup, settings as sparkplug_settings
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.domain.write_precision import WritePrecision


logger = logging.getLogger("monitor")
logging.basicConfig(level=logging.DEBUG)

group = SparkplugGroup()
server_id = group.default_server_id

bucket = "BatCAT"
url="http://foras:8184"


class Broker:
    host = group.servers[server_id].host
    port = group.servers[server_id].port
    keepalive = 60


class Settings:

    client_id = "monitor"
    transport_config = psp.TLSConfig(**group.servers[server_id].tls_config.model_dump()) if group.servers[server_id].tls_config is not None else None
    broker = Broker()
    retry = True

    group_id = group.group_id

    # SENSOR
    edge_node_sensor = group.edge_nodes["Edge_Node_Temperature_Sensor"]
    sensor = edge_node_sensor.devices["Temperature_Sensor"]
    temperature = sensor.metrics["Temperature"]

    # ACTUATOR
    edge_node_actuator = group.edge_nodes["Edge_Node_Power_Switch"]
    actuator = edge_node_actuator.devices["Power_Switch"]
    switch_on = actuator.metrics["Device_Control/Switch_On"]

    username = sparkplug_settings.sparkplug_username
    password = sparkplug_settings.sparkplug_password


settings = Settings()

client = influxdb_client.InfluxDBClient(
    url=url,
    #token=token,
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)


# Message(
#         topic=Topic(
#                     group_id='batcat-testbed-1-v0.1',
#                     message_type=<MessageType.DBIRTH: 'DBIRTH'>,
#                     edge_node_id='Edge_Node_Temperature_Sensor',
#                     device_id='Temperature_Sensor',
#                     sparkplug_host_id=None),
#         payload=DBirth(timestamp=1758712420326,
#                        seq=1,
#                        metrics=(
#                                 Metric(
#                                        timestamp=1758712420324,
#                                        name='Temperature',
#                                        datatype=<DataType.FLOAT: 9>,
#                                        metadata=None,
#                                        value=None,
#                                        alias=None,
#                                        is_historical=False,
#                                        is_transient=False,
#                                        is_null=True),
#                                 )
#                        ),
#         qos=<QoS.AT_MOST_ONCE: 0>,
#         retain=0)

# Message(
#   topic=Topic(
#       group_id='batcat-testbed-1-v0.1',
#       message_type=<MessageType.NBIRTH: 'NBIRTH'>,
#       edge_node_id='Edge_Node_Power_Switch',
#       device_id=None, sparkplug_host_id=None),
#       payload=NBirth(
#           timestamp=1759087357056,
#           seq=0,
#           metrics=(
#               Metric(
#                   timestamp=1759087357054,
#                   name='bdSeq',
#                   datatype=<DataType.INT64: 4>,
#                   metadata=None,
#                   value=0,
#                   alias=None,
#                   is_historical=False,
#                   is_transient=False,
#                   is_null=False),)), qos=<QoS.AT_MOST_ONCE: 0>, retain=0)


def callback(client: psp.Client, message: psp.Message) -> None:
    if message.topic.message_type in [ psp.MessageType.DDATA, psp.MessageType.NDATA ]:

        p = influxdb_client.Point("measurement").tag("edge_node",
                                                     message.topic.edge_node_id).tag("message_type",
                                                                                     str(message.topic.message_type)).tag("device_id",
                                                                                                                          message.topic.device_id)
        p.time(message.payload.timestamp, write_precision=WritePrecision.MS)
        print("TIMESTAMP: ", message.payload.timestamp, type(message.payload.timestamp))
        for metric in message.payload.metrics:
            p.field(metric.name, metric.value)

        write_api.write(bucket=bucket, org="None", record=p)

    elif message.topic.message_type in [ psp.MessageType.NBIRTH, psp.MessageType.DBIRTH, psp.MessageType.DDEATH, psp.MessageType.NDEATH ]:
        p = influxdb_client.Point("status")
        p.time(message.payload.timestamp, write_precision=WritePrecision.MS)
        if message.topic.message_type == psp.MessageType.NBIRTH:
            p.field("status", "online")
            p.tag("endi", message.topic.edge_node_id)
        elif message.topic.message_type == psp.MessageType.NDEATH:
            p.field("status", "offline")
            p.tag("endi", message.topic.edge_node_id)
        elif message.topic.message_type == psp.MessageType.DBIRTH:
            p.field("status", "online")
            p.tag("endi", f"{message.topic.edge_node_id}.{message.topic.device_id}")
        elif message.topic.message_type == psp.MessageType.DDEATH:
            p.field("status", "offline")
            p.tag("endi", f"{message.topic.edge_node_id}.{message.topic.device_id}")
        write_api.write(bucket=bucket, org="None", record=p)
    elif message.topic.message_type == psp.MessageType.DCMD:
        p = influxdb_client.Point("cmd")
        p.time(message.payload.timestamp, write_precision=WritePrecision.MS)
        p.tag("endi", f"{message.topic.edge_node_id}.{message.topic.device_id}")
        for metric in message.payload.metrics:
            if metric.name == settings.switch_on.name:
                p.field("on", metric.value)
        write_api.write(bucket=bucket, org="None", record=p)
    else:
        print(message)


TOPIC = psp.Topic(group_id="#")

client = psp.Client(client_id="Monitor", username=settings.username, password=settings.password, transport_config=settings.transport_config)
client.subscribe(TOPIC, psp.QoS.AT_LEAST_ONCE, callback)

try:
    client.connect(host=settings.broker.host, port=settings.broker.port, blocking=True)
except KeyboardInterrupt:
    pass
finally:
    client.disconnect()
