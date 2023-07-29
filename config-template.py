# we restart every now and then.
LIFETIMEITERATIONS=500

# they MUST have different names, otherwise they will have the same key
# use helper/getinfo.py to get the IDs.

esp32cams=[{"hostname": "esp32cam-sa-1", "ip": "192.168.1.101", "mqtttopic": "esp32cam-sa1","camkey": "##########"},
           {"hostname": "esp32cam-sa-2", "ip": "192.168.1.102", "mqtttopic": "esp32cam-sa2","camkey": "##########"},
           {"hostname": "esp32cam-sa-3", "ip": "192.168.1.103", "mqtttopic": "esp32cam-sa3","camkey": "##########"},
           {"hostname": "esp32cam-sa-4", "ip": "192.168.1.104", "mqtttopic": "esp32cam-sa4","camkey": "##########"},
           {"hostname": "esp32cam-sa-5", "ip": "192.168.1.105", "mqtttopic": "esp32cam-sa5","camkey": "##########"},
           {"hostname": "esp32cam-sa-6", "ip": "192.168.1.106", "mqtttopic": "esp32cam-sa6","camkey": "##########"}]

# This is the target when using the helper scripts
esphome_host="192.168.1.107"

# This is the IP being a sensor ndoe
esphome_sensorhost="192.168.1.107"
esphome_port=6053
esphome_api_keepalive=5
# this should be left empty
esphome_api_password=""
esphome_api_encrkey="the ESPHOME API encyption key"

# Configure InfluxDB connection variables
influx_host = "influx.example.org"
influx_port = 8086 				# default port
influx_user = "user" 				# need with write access
influx_password = "password"
influx_dbname = "dbname" 			# the database we created earlier

# Configure InfluxDB connection variables
influxpm2k_url = "http://influx.example.org:8086" # 2.7 version
influxpm2k_user = "user"
influxpm2k_password = "password"
influxpm2k_token = "influx API token for this bucket"
influxpm2k_org = "organization"
influxpm2k_dbname = "bucketname"
influxpm2k_bucket = "bucketname"

interval = 60 # Sample period in seconds
loopsleep = 300
verbose_info_in_db = False
water_threshold = 205
water_pumptime = 1
water_max_times = 10
water_max_period = 24

mqtt_brokerip = "192.168.1.108"
mqtt_brokerport = 1883
mqtt_user = "user"
mqtt_password = "password"
mqtt_wakeup_topicmain = "esp32camsleep/"
mqtt_wakeup_payload = "online2023"


mariadb_user = "user"
mariadb_password = "password"
mariadb_host = "192.168.1.109"
mariadb_database = "plantmaster2k"
software_version = "4.1.4 20230715"
disksave = False
mariadbsave = True

lightavgduration = "10m"
light_mavg_freq = 300
# discard image if avg mean is below this
light_threshold_neg = 10
#light_threshold_neg = -10

# must be multiple of 10, keep connection
# for this many seconds after requesting the photo,
# normal is 10-20 seconds
cam_postsleep = 60

# location will be used as a grouping tag later
location = "for influx"
collectorname_pm2k = "for influx"


# Names below based on plantmaster2k-sensor.yaml. first is ID which must be replaced
sensornames_triple = {
3672999868: {"name": "triplewhammy-esp32_sht21_temperature", "sensor": "sht21", "extra": ""},
3082284377: {"name": "triplewhammy-esp32_sht21_humidity", "sensor": "sht21", "extra": ""},
1315184542: {"name": "triplewhammy-esp32_bh1750_illuminance", "sensor": "bh1750", "extra": "" },
988808144: {"name": "ds18b20-[Dallas onesensor address, below 2 working examples]", "sensor": "ds18b20", "extra": "" },
988808147: {"name": "ds18b20-953ce10457bf4628", "sensor": "ds18b20", "extra": "" },
988808146: {"name": "ds18b20-943ce10457a80528", "sensor": "ds18b20", "extra": "" },
939579340: {"name": "[Find the ID using helpers/getinfo.py]-wifisignal", "sensor": "esp32", "extra": "" },
2564854287: {"name": "triplewhammy-esp32_ads1115_a0", "sensor": "ads1115", "extra": "" },
2564854286: {"name": "triplewhammy-esp32_ads1115_a1", "sensor": "ads1115", "extra": "" },
2564854285: {"name": "triplewhammy-esp32_ads1115_a2", "sensor": "ads1115", "extra": "" },
2564854284: {"name": "triplewhammy-esp32_ads1115_a3", "sensor": "ads1115", "extra": "" }
}
# for relay control, can be ignored
outputnames_triple = { 5237439: {"name": "triplewhammy-esp32-out-gpio16", "sensor": "GPIO", "extra": ""}}
# must match name above
moistsensor_triple = "triplewhammy-esp32_gpio32"
# must match name above
lightsensor_triple = "triplewhammy-esp32_bh1750_illuminance"
