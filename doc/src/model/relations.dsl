# Put inter-group relations here

oc_framework.sensor_adapter.reader -> sensor "fetch data"
oc_framework.actuator_adapter.writer -> actuator "operate"
oc_framework.dt_adapter.dt_client -> digital_twin.actionable_model "push sensor data, receive actuator data"

dkms.mqtt_client -> oc_framework.sensor_topic "subscribe"
dkms.mqtt_client -> oc_framework.actuator_topic "subscribe"

operator -> oc_framework.monitoring.visualization "view"
oc_framework.monitoring.notification -> operator "notify"
