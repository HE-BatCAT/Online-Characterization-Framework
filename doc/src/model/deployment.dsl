testbed = deploymentEnvironment "Testbed" {
    broker = deploymentNode "Broker" "Mosquitto" "Docker Container" {
        sensor_topic = containerInstance oc_framework.sensor_topic {
        }
        actuator_topic = containerInstance oc_framework.actuator_topic {
        }
    }

    production_line = deploymentNode "Production Line" {
        sensor_depl = deploymentNode "Edge Node Temperature Sensor" "Docker Container" {
            sensor = softwareSystemInstance sensor {
            }
            sensor_adapter = containerInstance oc_framework.sensor_adapter
        }

        actuator_depl = deploymentNode "Edge Node Power Switch" "Docker Container" {
            actuator = softwareSystemInstance actuator {
            }
            actuator_adapter = containerInstance oc_framework.actuator_adapter
        }
    }

    dt_adapter = deploymentNode "Digital Twin" "Docker Container" {
        dt = containerInstance oc_framework.dt_adapter {
        }
    }
}
