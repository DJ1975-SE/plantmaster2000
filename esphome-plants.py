#!/usr/bin/env python3

## plantmaster2k, sensor node

import config
import aioesphomeapi
import asyncio
import time
import pprint
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Create the InfluxDB client object 2.7
client = influxdb_client.InfluxDBClient(url=config.influxpm2k_url, token=config.influxpm2k_token, org=config.influxpm2k_org)
# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

def upload_to_influx(datadict,sensortype):
    iso = int(time.time())
    print(f"\t{bcolors.OKCYAN} Uploading" + str(datadict)+ f"{bcolors.ENDC}")
    pprint.pprint(datadict)
    for sensor,value in datadict.items():
        p = (
            influxdb_client.Point("data")
            .tag("collector", config.collectorname_pm2k)
            .tag("sensor", sensortype)
            .field(sensor,value)
#            .time(iso*1000)
        )
    pprint.pprint(iso*1000)
    write_api.write(bucket=config.influxpm2k_bucket, org=config.influxpm2k_org, record=p)

def get_influx_mavg(sensor_name,mavg_period):

#### THIS CODE IS NOT USED (yet), it should get a moving average of the moist level and use ESPHome switches/GPIOs which can control water pumps via relays.

#    query = 'select mean(\"' + sensor_name +  '\") from autogen.environment where time > now() - ' + mavg_period+ ' GROUP BY time(' + mavg_period + ') fill(null);'
#    result=client.query(query)
    # there will be 2 values returned, use the latter
#    for data in list(result.get_points()):
#        mavg=int(100 * data['mean'])
#    return mavg
    return 100

async def main():
    # Establish connection
    api = aioesphomeapi.APIClient(address=config.esphome_sensorhost, port=config.esphome_port, noise_psk=config.esphome_api_encrkey, password=config.esphome_api_password)
    await api.connect(login=True)
    print(f"{bcolors.OKBLUE}Connected to " + str(api.address) + ", version " + str(api.api_version) + f"{bcolors.ENDC}")
    # include software info and compilation date
    if (config.verbose_info_in_db == True):
        print(f"{bcolors.WARNING}Verbose info in database ON{bcolors.ENDC}")
        device_info = await api.device_info()
        verboseinfo = {"name":device_info.name, "mac_address":device_info.mac_address, "compilation_time":device_info.compilation_time, "project":device_info.project_name+ "v" + device_info.project_version}
    else:
        print(f"{bcolors.WARNING}Verbose info in database OFF{bcolors.ENDC}")
        verboseinfo = {}
    def change_callback(state):
        if (state.key in config.sensornames_triple):
                datadict={config.sensornames_triple[state.key]["name"]: state.state} | verboseinfo
                upload_to_influx(datadict,config.sensornames_triple[state.key]["sensor"])

    # Subscribe to the state changes
    await api.subscribe_states(change_callback)
    mavg=get_influx_mavg(config.moistsensor,"24h")
    # turn LED on or off based on mavg
    if mavg > config.water_threshold:
        print("Moving average is " + str(mavg) + " - running pump for " + str(config.water_pumptime) + " seconds")
        ledstate=True
    else:
        print("Moving average is " + str(mavg) + " - not running pump")
        ledstate=False
    for outputid in config.outputnames.keys():
        retval = await api.switch_command(key=outputid, state=ledstate)
        datadict={config.outputnames[outputid]["name"]:ledstate}
        upload_to_influx(datadict,config.outputnames[outputid]["sensor"])
    print("Sleepin for " + str(config.loopsleep - int((time.perf_counter() - s))))
    await asyncio.sleep(config.loopsleep - int(time.perf_counter() - s))
    await api.disconnect()

if __name__ == "__main__":
    while True:
        print(40 * ".")
        s = time.perf_counter()
        try:
            asyncio.run(main())
        except Exception as e:
            print("Failure: " + str(e) + " " + str(type(e)))
        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
        print(40 * "_")
