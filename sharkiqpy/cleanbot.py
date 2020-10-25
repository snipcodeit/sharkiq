import asyncio, sys
from sharkiqpy import get_ayla_api, OperatingModes, SharkIqVacuum, PowerModes, Properties
import secrets

class homeClean:
    def __init__(self,mode):
        self.ayla_api = get_ayla_api(secrets.USERNAME, secrets.PASSWORD)
        self.shark = asyncio.run(self.signin(mode))
        
    async def signin(self, mode) -> SharkIqVacuum:
        await self.ayla_api.async_sign_in()
        shark_vacs = await self.ayla_api.async_get_devices()
        self.shark = shark_vacs[0]
        
        switcher = {
            '1': self.start_eco,
            '2': self.start_nor,
            '3': self.start_max,
            '4': self.stop_clean
        }
        switcher[mode]()

    def start_eco(self):
        self.shark.async_set_power_mode(PowerModes.ECO)
        print('START ECO CLEAN')
        self.go()

    async def start_nor(self):
        await self.shark.async_set_power_mode(PowerModes.NORMAL)
        print('START NORMAL CLEAN')
        self.go()

    async def start_max(self):
        await self.shark.async_set_power_mode(PowerModes.MAX)
        print('START MAX CLEAN')
        self.go()
    
    async def stop_clean(self):
        await self.shark.async_set_operating_mode(OperatingModes.RETURN)
        print ('STOP CLEANING AND RETURN')

    def go(self):
        self.shark.async_set_operating_mode(OperatingModes.START)

if __name__ == "__main__":
    if (sys.argv[1]):
        homeClean(sys.argv[1])
    else:
        homeClean(secrets.PREF_MODE)



