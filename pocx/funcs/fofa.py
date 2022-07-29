import httpx
import json
import base64
from loguru import logger
import urllib3
import ssl

try:
    ssl_context = httpx.create_ssl_context()
except:
    ssl_context = ssl.create_default_context()
ssl_context.options ^= ssl.OP_NO_TLSv1  # Enable TLS 1.0 back

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
httpx._config.DEFAULT_CIPHERS += ":ALL:@SECLEVEL=1"


class Fofa():
    @logger.catch(level='ERROR')
    def __init__(self):
        """

        Initialize the Fofa API.

        """
        self.key = ''
        self.email = ''
        self.domain = ''

    @logger.catch(level='ERROR')
    def set_config(self, api_key: str, api_email: str, domain: str = 'fofa.info'):
        """

        Setting the configuration for the Fofa API.

        :param api_key: the fofa api key
        :param api_email: the fofa account email
        :param domain: the fofa domain
        :return:
        """
        self.key = api_key
        self.email = api_email
        self.domain = domain

    @logger.catch(level='ERROR')
    def _grammar_b64(self, grammar: str):
        """

        Transform the grammar to base64.

        :param grammar: the fofa search grammar
        :return: the base64 grammar
        """
        b64 = base64.b64encode(grammar.encode()).decode()
        for i in range(b64.count('=')):
            b64.replace('=', '%3D')
        return b64

    @logger.catch(level='ERROR')
    def _search(self, grammar: str, page: int = 1, size: int = 100):
        """

        The core method for searching the fofa.

        :param grammar: the search grammar
        :param page: the page to search
        :param size: the size of the page
        :return: the search results
        """
        b64 = self._grammar_b64(grammar)
        furl = f'https://{self.domain}/api/v1/search/all?email={self.email}&key={self.key}&qbase64={b64}&{grammar}&page={page}&size={size}'
        try:
            assets = httpx.get(furl).content.decode('utf-8')
        except Exception as _:
            assets = httpx.get(furl, verify=ssl_context).content.decode('utf-8')
        result = json.loads(assets)
        if not result['error']:
            return result
        logger.error(f'Fofa API error: {result["errmsg"]}')
        return None

    @logger.catch(level='ERROR')
    def assets(self, grammar: str, page: int = 1, size: int = 100):
        """

        Gain the assets from the fofa.

        :param grammar: the search grammar
        :param page: the page to search
        :param size: the size of the page
        :return: the fofa assets
        """
        results = self._search(grammar, page, size)
        targets = []
        if not results:
            return targets
        for asset in results['results']:
            target = asset[0] if 'http' in asset[0] else (f'https://{asset[1]}:{asset[2]}' if int(asset[2]) == 443 else f'http://{asset[1]}:{asset[2]}')
            targets.append(target)
        return list(set(targets))

    @logger.catch(level='ERROR')
    def asset_counts(self, grammar: str):
        """

        Get the asset counts from the fofa, which search the given grammar.

        :param grammar: the search grammar
        :return: the asset counts
        """
        results = self._search(grammar, 1, 1)
        if not results:
            return 0
        return results['size']

    @logger.catch(level='ERROR')
    def asset_pages(self, grammar: str, size: int = 100):
        """

        Get the asset pages from the fofa, which search the given grammar.

        :param grammar: the search grammar
        :param size: the size of the page
        :return: the pages of the asset counts
        """
        results = self._search(grammar, 1, 1)
        if not results:
            return 1
        all_counts = results['size']
        if all_counts >= 10000:
            logger.warning(f"Fofa's asset counts is {all_counts}, which is too much, so we only search the first 10000.")
            count = 10000 % size
            pages = 10000 // size if count == 0 else 10000 // size + 1
        else:
            count = results['size'] % size
            pages = all_counts // size if count == 0 else all_counts // size + 1
        return pages
