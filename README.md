![grafana_screenshot](https://github.com/DJ1975-SE/plantmaster2000/blob/main/presentation/grafana-example.png)

# plantmaster2000
ESPHome / MQTT / Grafana / MariaDB based environment for documenting plants. If you have 3 of them, for example.

Idea is that this setup should be controllable / integrateable with Homeassistant as well, which might be a better idea than this standalone setup.

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
* install esphome, browse over the docs
* ```esphome compile camera1.yaml, esphome upload camera1.yaml``` or if you wish ```esphome run camera1.yaml``` and your camera(s) are complete
* ```esphome compile plantmaster2k-sensor.yaml, esphome upload plantmaster2k-sensor.yaml``` or if you wish ```esphome run plantmaster2k-sensor.yaml``` and your sensor node is complete (1 sensor node per 3 or 4 plants is needed)
* ```python esphome-plants.py``` which will connect to influx and the central node. It subscribes to the ESPHome sensors and uploads the results to an Influx bucket
* ```python cam-mqtt-trigger.py``` which connects to MariaDB, MQTT and influx. It connects directly to cameras when they wake up (knowing when by snooping on MQTT wakeup messages), asks for an image and uploads it to the MariaDB DB.
* (for later) the web interface to the images
* (for later) the template / grafana dashboards 


# Info
* This code can very likely not be usable unless it is inspected and modified to your specific use case.
* Much information in the config file is only to tag the measurments in the database properly, for the code itself it does not matter what type of sensor it is or the name of it.
* It can probably be made to work with influx 1 by someone knowing what they do.
* you might need to press CTRL-C several times to break, due to the async and parallel code
* you can change the name of the sensor from double, triplewhammy etc. it has no meaning or sense.
* the only integration between the two python programse is through the sensor names in the config file, no magic.
* if the MQTT server is restarted etc you need to restart the whole thing. That is why the scripts have a limited run length and restart after x iterations.
* if the cameras are located within a grow tent, you might need to move the AP a lot closer since the reflection material also seems to affect radio waves. I had unexpectedly good results using hostapd and a TP-Link TL-WN722N USB stick as an AP


# TODO
* documentation / fritzing etc
* polishing
