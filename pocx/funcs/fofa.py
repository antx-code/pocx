import requests
import json
import base64
from loguru import logger

class Fofa():
    @logger.catch(level='ERROR')
    def __init__(self, ):
        self.key = ''
        self.email = ''

    @logger.catch(level='ERROR')
    def set_config(self, api_key: str, api_email: str):
        self.key = api_key
        self.email = api_email

    @logger.catch(level='ERROR')
    def _grammar_b64(self, grammar: str):
        b64 = base64.b64encode(grammar.encode()).decode()
        for i in range(b64.count('=')):
            b64.replace('=', '%3D')
        return b64

    @logger.catch(level='ERROR')
    def _search(self, grammar: str, page: int = 1, size: int = 100):
        b64 = self._grammar_b64(grammar)
        furl = f'https://fofa.info/api/v1/search/all?email={self.email}&key={self.key}&qbase64={b64}&{grammar}&page={page}&size={size}'
        try:
            assets = requests.get(furl).content.decode('utf-8')
            return json.loads(assets)
        except Exception as e:
            logger.error(e)
            return None

    @logger.catch(level='ERROR')
    def assets(self, grammar: str, page: int = 1, size: int = 100):
        results = self._search(grammar)
        if not results:
            return None
        return results['results']

    @logger.catch(level='ERROR')
    def asset_counts(self, grammar: str):
        results = self._search(grammar)
        if not results:
            return None
        return results['size']
