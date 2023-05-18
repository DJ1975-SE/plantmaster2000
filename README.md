# plantmaster2000
ESPHome / Grafana / MariaDB based environment for documenting plants. If you have 3 of them, for example.

# Principle
* ESP32-CAM running ESPHome code.
* Python script polling sensors and uploading status to Grafana
* Python script polling camera and uploading image + snapshot of sensors to MariaDB
* Output pin goes high when python script decides water is needed

