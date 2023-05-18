#!/usr/bin/env python3
import aioesphomeapi
import asyncio
import time
import pprint
from influxdb import InfluxDBClient
# config file contain all settings
import config

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

# Create the InfluxDB client object
client = InfluxDBClient(config.influx_host, config.influx_port, config.influx_user, config.influx_password, config.influx_dbname)

def upload_to_influx(datadict,sensortype):
    iso = int(time.time())
    data = [{"measurement": "environment","tags": {"collector": config.location, "sensor": sensortype,},"time": iso, "fields": datadict}]
    print(f"\t{bcolors.OKCYAN} Uploading" + str(data)+ f"{bcolors.ENDC}")
#    client.write_points(data, time_precision='s')

def get_influx_mavg(sensor_name,mavg_period):
    query = 'select mean(\"' + sensor_name +  '\") from autogen.environment WHERE time > now() - ' + mavg_period+ ' GROUP BY time(' + mavg_period + ') fill(null);'
    result=client.query(query)
    # there will be 2 values returned, use the latter
    for data in list(result.get_points()):
        mavg=int(100 * data['mean'])
    return mavg

def should_we_water(moving_avg, plantid):
    print(str(config.mavg_period) + " moving average is " + str(moving_avg) + " of " + str(config.water_threshold))
    # how many times did we water the last x hours
    query = 'select count(\"' + config.outputswitch + '\") from autogen.environment WHERE time > now() - ' + config.mavg_period + ' AND \"' + config.outputswitch + '\" = True;'
    # there is only one result, probably better ways to do this
    result=client.query(query)
    for data in list(result.get_points()):
        countlastperiod=data['count']
    print("We have watered " + str(countlastperiod) + " of " + str(config.water_max_times) + " times in the last " + str(config.water_max_period) + " hours")
    if moving_avg > config.water_threshold:
        if countlastperiod <= config.water_max_times:
            print("Have not yet watered " + str(config.water_max_times) + " in the last " + str(config.water_max_period) + " hours, turning on pump")
            pumpstate=True
        else:
            print("Have already watered " + str(config.water_max_times) + " in the last " + str(config.water_max_period) + " hours, leaving pump off")
            pumpstate=False
    else:
        print("No water needed, leaving pump off")
        pumpstate=False

    for outputid in config.outputnames.keys():
        datadict={config.outputnames[outputid]["name"]:pumpstate}
        upload_to_influx(datadict,config.outputnames[outputid]["sensor"])

    return pumpstate

def run_pump(length, plantid):
    return False


async def main():
    # Establish connection
    api = aioesphomeapi.APIClient(address=config.esphome_host, port=config.esphome_port, noise_psk=config.esphome_api_encrkey, password=config.esphome_api_password)
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
        if (state.key in config.sensornames):
                datadict={config.sensornames[state.key]["name"]: state.state} | verboseinfo
                upload_to_influx(datadict,config.sensornames[state.key]["sensor"])

    # Subscribe to the state changes, callback function is called in the background
    await api.subscribe_states(change_callback)

    # get the average moist level for the last period
    mavg=get_influx_mavg(config.moistsensor,config.mavg_period)

    # check if we should add more water based on waterings / day
    if should_we_water(mavg,config.plant1):
        run_pump(config.water_pumptime,config.plant1)
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
