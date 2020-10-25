import asyncio, sys
from sharkiqpy import get_ayla_api, OperatingModes, SharkIqVacuum, PowerModes, Properties
import configparser

parser = configparser.ConfigParser()
parser.read('../secrets.ini')  

class homeClean:
    def __init__(self,mode):
        self.ayla_api = get_ayla_api(parser.get('login','USERNAME'), parser.get('login','PASSWORD'))
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
        await self.shark.async_update()
        await switcher[mode]()
        return self.shark

    async def start_eco(self):
        await self.shark.async_set_power_mode(PowerModes.ECO)
        print('START ECO CLEAN')
        await self.go()

    async def start_nor(self):
        await self.shark.async_set_power_mode(PowerModes.NORMAL)
        print('START NORMAL CLEAN')
        await self.go()

    async def start_max(self):
        await self.shark.async_set_power_mode(PowerModes.MAX)
        print('START MAX CLEAN')
        await self.go()
    
    async def stop_clean(self):
        await self.shark.async_set_operating_mode(OperatingModes.RETURN)
        print ('STOP CLEANING AND RETURN')

    async def go(self):
        await self.shark.async_set_operating_mode(OperatingModes.START)

if __name__ == "__main__":
    arg_names = ['file','mode']
    args = dict(zip(arg_names, sys.argv))
    if (args.get('mode')):
        homeClean(sys.argv[1])
    else:
        homeClean(parser.get('mode','PREF_MODE'))



