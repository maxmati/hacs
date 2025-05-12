import aiohttp


class Burak:

    def __init__(self, host: str, slave_id: int, user: str, password: str):
        self._host = host
        self._slave_id = slave_id

    @property
    def slave(self) -> int:
        return self._slave_id

    async def channels(self) -> [str]:
        status = await self._get_status()
        return status["led_brightness"].keys()

    async def _get_status(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._host}/slaves/{self._slave_id}") as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data

    async def set_brightness(self, channel: str, brightness: int):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._host}/slaves/{self._slave_id}/led/{channel}/{brightness}") as resp:
                resp.raise_for_status()

    async def get_brightness(self, channel: str):
        status = await self._get_status()
        return status["led_brightness"][channel]

    async def set_output(self, channel: str, state: bool):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._host}/slaves/{self._slave_id}/{channel}/{state}") as resp:
                resp.raise_for_status()

    async def get_output(self, channel: str):
        status = await self._get_status()
        return status[f"{channel}_enabled"]
