#group "Example Group" {
    oc_framework = softwareSystem "Online Characterization Framework" {

        broker = group "MQTT Broker" {
            sensor_topic = container "Sensor Topic" "Topic" "MQTT"
            actuator_topic = container "Actuator Topic" "Topic" "MQTT"
        }

        sensor_adapter = container "Edge Node Sensor" "Python" {
            reader = component "Reader" "Read data from sensor"
            publisher = component "Publisher" "MQTT client"
            reader -> publisher "dataflow"
        }

        actuator_adapter = container "Edge Node Power Switch" "Python" {
            writer = component "Writer" "Write data (i.e. commands) to actuator"
            subscriber = component "Subscriber" "MQTT client"
            subscriber -> writer "dataflow"
        }

        dt_adapter = container "Ditigal Twin" {
            mqtt_client = component "MQTT client"
            dt_client = component "DT client"

            mqtt_client -> dt_client "flow of sensor data"
            dt_client -> mqtt_client "flow of actuator data"
        }

        monitoring = container "Monitoring" {
            mqtt_client = component "MQTT client"
            analysis = component "Analysis"
            visualization = component "Visualization"
            notification = component "Notification"

            mqtt_client -> analysis "forward data"
            visualization -> analysis "fetch results"
            analysis -> notification "trigger"
        }

        # inter-container relations
        sensor_adapter.publisher -> sensor_topic "publish Temperature metric"

        actuator_adapter.subscriber -> actuator_topic "subscribe to Power Switch command"

        dt_adapter.mqtt_client -> sensor_topic "subscribe to Temperature metric"
        dt_adapter.mqtt_client -> actuator_topic "publish Power Switch command"

        monitoring.mqtt_client -> sensor_topic "subscribe"
        monitoring.mqtt_client -> actuator_topic "subscribe"

    }

#}
