from abc import ABCMeta, abstractmethod
from loguru import logger
import httpx
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
httpx._config.DEFAULT_CIPHERS += ":ALL:@SECLEVEL=1"


class BasicPoc(metaclass=ABCMeta):
    @logger.catch(level='ERROR')
    def __init__(self) -> None:
        self.mode = 'Synchronous Mode'
        self.name = "BasicPoc"
        self.cve = ''
        self.example = ''
        self.session = httpx.Client(verify=False)
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
        logger.info(f'Testing {self.name} with {self.mode}.')

    @logger.catch(level='ERROR')
    def set_headers(self, headers: dict = None):
        if headers is not None:
            self.session.headers = headers

    @logger.catch(level='ERROR')
    def request(self, url: str, method: str = 'get', timeout: int = 10, **kwargs) -> httpx.Response:
        try:
            resp = self.session.request(method, url, timeout=timeout, **kwargs)
        except Exception as e:
            logger.error(f'[-] Run Poc [{self.cve} - {self.name}] Connection Error => {url} was not reachable.')
            resp = None
        return resp

    @logger.catch(level='ERROR')
    def get(self, url: str, **kwargs) -> httpx.Response:
        return self.request(url, method='get', **kwargs)

    @logger.catch(level='ERROR')
    def post(self, url: str, **kwargs) -> httpx.Response:
        return self.request(url, method='post', **kwargs)

    @logger.catch(level='ERROR')
    def put(self, url: str, **kwargs) -> httpx.Response:
        return self.request(url, method='put', **kwargs)

    @logger.catch(level='ERROR')
    def head(self, url: str, **kwargs) -> httpx.Response:
        return self.request(url, method='head', **kwargs)

    @logger.catch(level='ERROR')
    def delete(self, url: str, **kwargs) -> httpx.Response:
        return self.request(url, method='delete', **kwargs)

    @abstractmethod
    @logger.catch(level='ERROR')
    def poc(self, target: str) -> bool:
        pass

    @logger.catch(level='ERROR')
    def run(self, target):
        targets = [target] if isinstance(target, str) else target

        for target in targets:
            self.poc(target)
