import httpx
import subprocess
from loguru import logger
from snow_flake import IdWorker


class Ceye():
    @logger.catch(level="ERROR")
    def __init__(self):
        """

        Initialize the ceye object.

        """
        self.id_worker = IdWorker(0, 0)
        self.api_token = ''
        self.identifier = ''

    @logger.catch(level='ERROR')
    def set_config(self, api_token: str, identifier: str):
        """

        Set the configuration of the ceye object.

        :param api_token: The api token of the ceye.
        :param identifier: The identifier url address of the ceye.
        :return:
        """
        self.api_token = api_token
        self.identifier = identifier

    @logger.catch(level='ERROR')
    def generate_payload_id(self):
        """

        Generate a unique id for the payload.

        :return: The unique id of string type.
        """
        return str(self.id_worker.get_id())

    @logger.catch(level='ERROR')
    def verify(self, pid: str, verify_type: str='dns'):
        """

        Verify the payload.

        :param pid: The unique id of the payload.
        :param verify_type: The type of the verification, http or dns.
        :return: The bool result of the verification.
        """
        verify_url = f'http://api.ceye.io/v1/records?token={self.api_token}&type={verify_type}&filter={pid}'
        result = httpx.get(verify_url).json()
        if not result['data']:
            logger.error(f'{pid} not found in Ceye')
            return False
        logger.success(f'{pid} found in Ceye')
        logger.success(f'The ceye records are: \n{result["data"]}')
        return True
