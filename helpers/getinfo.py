import config
import aioesphomeapi
import asyncio
import pprint

async def main():
    """Connect to an ESPHome device and get details."""

    # Establish connection
    api = aioesphomeapi.APIClient(address=config.esphome_host, port=config.esphome_port, noise_psk=config.esphome_api_encrkey, password=config.esphome_api_password)
    await api.connect(login=True)

    # Get API version of the device's firmware
    print(api.api_version)

    # Show device details
    device_info = await api.device_info()
    print(device_info)

    # List all entities of the device
    entities = await api.list_entities_services()

    # entities is a tuple of dictionaries of sensors (and then cameras?)
    for entity in entities[0]:
        print(40 * "*")
        print(entity.unique_id + " / " + str(entity.key) + " : " + entity.device_class)
        print(str(entity) + "\n")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
