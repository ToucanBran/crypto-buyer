import yaml
from helpers import is_none_or_whitespace
from gate_api import ApiClient, Configuration, SpotApi

class SpotApiWrapper:
    def __init__(self, exchange_configs):
        self.configs = exchange_configs
        self._spot_api = None

    @property
    def spot_api(self) -> SpotApi:
        if self._spot_api is None:
            client = self.load_gateio_creds()
            self._spot_api = SpotApi(ApiClient(client))
        return self._spot_api

    def load_gateio_creds(self) -> Configuration:
        if not 'api' in self.configs or not 'secret' in self.configs:
            raise Exception("Missing credentials")
        if is_none_or_whitespace(self.configs['api']) or is_none_or_whitespace(self.configs['secret']):
            raise Exception("Missing credentials")
        return Configuration(key=self.configs['api'], secret=self.configs['secret'])