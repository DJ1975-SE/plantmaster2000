# plantmaster2000
ESPHome / Grafana / MariaDB based environment for documenting plants. If you have 3 of them, for example.

# Principle
* ESP32-CAM running ESPHome code.
* Python script polling sensors and uploading status to Grafana
* Python script polling camera and uploading image + snapshot of sensors to MariaDB
* Output pin goes high when python script decides water is needed

# Using
* clone repo
* based on secrets-template.yaml and config-template.py, create the files secrets.yaml (for ESPHome) and config.py (for Python)

# Info
* This code can very likely not be usable unless it is inspected and modified to your specific use case.
* Much information in the config file is only to tag the measurments in the database properly, for the code itself it does not matter what type of sensor it is or the name of it.

# TODO
* robustness when connecting
* ESPHome - camera takes constant images and use a lot of power
