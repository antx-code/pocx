from abc import ABCMeta, abstractmethod
from loguru import logger
import asyncio
import httpx
import urllib3
urllib3.disable_warnings()


class AioPoc(metaclass=ABCMeta):
    @logger.catch(level='ERROR')
    def __init__(self) -> None:
        self.mode = 'Asynchronous Mode'
        self.name = "AioPoc"
        self.example = ""
        self.session = httpx.AsyncClient(verify=False)
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}

    @logger.catch(level='ERROR')
    def set_headers(self, headers: dict = None):
        if headers is not None:
            self.session.headers = headers

    @logger.catch(level='ERROR')
    async def aio_request(self, url: str, method: str = 'get', timeout: int = 10, **kwargs) -> httpx.Response:
        try:
            resp = await self.session.request(method, url, timeout=timeout, **kwargs)
        except httpx.RequestError as e:
            logger.error(f'[-] Run Poc[{self.name}] => {url} Error:\n\t{e}')
            resp = None
        return resp

    @logger.catch(level='ERROR')
    async def aio_get(self, url: str, **kwargs) -> httpx.Response:
        return await self.aio_request(url, method='get', **kwargs)

    @logger.catch(level='ERROR')
    async def aio_post(self, url: str, **kwargs) -> httpx.Response:
        return await self.aio_request(url, method='post', **kwargs)

    @logger.catch(level='ERROR')
    async def aio_put(self, url: str, **kwargs) -> httpx.Response:
        return await self.aio_request(url, method='put', **kwargs)

    @logger.catch(level='ERROR')
    async def aio_head(self, url: str, **kwargs) -> httpx.Response:
        return await self.aio_request(url, method='head', **kwargs)

    @logger.catch(level='ERROR')
    async def aio_delete(self, url: str, **kwargs) -> httpx.Response:
        return await self.aio_request(url, method='delete', **kwargs)

    @abstractmethod
    @logger.catch(level='ERROR')
    async def poc(self, target: str) -> bool:
        pass

    @logger.catch(level='ERROR')
    def run(self, target):
        logger.info(f'testing {self.name} with {self.mode}.')

        targets = [target] if isinstance(target, str) else target

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*[self.poc(target) for target in targets]))
