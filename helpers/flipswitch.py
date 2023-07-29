import config
import aioesphomeapi
import asyncio
import pprint

async def main():
    """Connect to an ESPHome device and get details."""

    # Establish connection
    api = aioesphomeapi.APIClient(address=config.esphome_host, port=config.esphome_port, noise_psk=config.esphome_api_encrkey, password=config.esphome_api_password)
    await api.connect(login=True)

    # this is not how to use asynchro
    while True:
        for outputid in config.outputnames.keys():
            retval = await api.switch_command(key=outputid, state=False)
            await asyncio.sleep(1)
            retval = await api.switch_command(key=outputid, state=True)
            await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
