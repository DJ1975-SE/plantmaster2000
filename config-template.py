esphome_host="IPv4 of the ESP"
esphome_port=6053
esphome_api_password=""
esphome_api_encrkey="ESPHome API"

# Configure InfluxDB connection variables
influx_host = "IPv4 of the influx server" # influx serve
influx_port = 8086 # default port
influx_user = "user" # the user/password, with write access
influx_password = "pass"
influx_dbname = "database" # the influx database
# approx same interval as publishing
loopsleep = 300
verbose_info_in_db = False

# location is added as a tag to influx
location = "some string to make it easier"
sensornames = { ESPHOME_ID: {"name": "name of the sensor", "sensor": "type of sensor", "extra": "some additional info"}}
