# plantmaster2000
ESPHome / Grafana / MariaDB based environment for documenting plants. If you have 3 of them, for example.

## Principle
* ESP32-CAM(s) running ESPHome code, taking pictures.
* ESP32 running ESPHome code, publishing I2C Sensor information, GPIO control etc.
* Python script calling back on state changes, poll sensors and upload data to Influx 2 instance
* Python script calling back on cameras waking up from deepsleep, and uploading image + snapshot of sensors to MariaDB

# Using
* clone repo
* based on secrets-template.yaml and config-template.py, create the files secrets.yaml (for ESPHome) and config.py (for Python)
* based on camera1.yaml/camera2.yaml create the config for the camera(s)
* (create venv, figure out python dependencies and solving them with pip etc)
* ```esphome compile camera1.yaml, esphome upload camera1.yaml``` or if you wish ```esphome run camera1.yaml``` and your camera(s) are complete
* ```python esphome-plants.py``` which will connect to influx and the central node. It subscribes to the ESPHome sensors and uploads the results to an Influx bucket
* ```python cam-mqtt-trigger.py``` which connects to MariaDB, MQTT and influx. It connects directly to cameras when they wake up (knowing when by snooping on MQTT wakeup messages), asks for an image and uploads it to the MariaDB DB.
* (for later) the web interface to the images
* (for later) the template / grafana dashboards 


# Info
* This code can very likely not be usable unless it is inspected and modified to your specific use case.
* Much information in the config file is only to tag the measurments in the database properly, for the code itself it does not matter what type of sensor it is or the name of it.
* It can very likely be made to work with influx 1








# TODO
* polishing
