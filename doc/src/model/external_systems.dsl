dkms = softwareSystem "BatCAT DKMS" "Extern" "Extern" {
    mqtt_client = container "MQTT client"
}

digital_twin = softwareSystem "BatCAT Digital Twin Platform" "Extern" "Extern" {
    actionable_model = container "Actionable Model T3.6" {
    }
}

sensor = softwareSystem "Sensor" "Extern" {
    tags "Device, Extern"
}

actuator = softwareSystem "Actuator" "Extern" {
    tags "Device, Extern"
}
