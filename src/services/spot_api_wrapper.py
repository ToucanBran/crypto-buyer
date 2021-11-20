import yaml
from gate_api import ApiClient, Configuration, Order, SpotApi

class SpotApiWrapper:
    def __init__(self, configs):
        self.configs = configs

    def get_spot_api(self) -> SpotApi:
        if self.spot_api is not None:
            return self.spot_api
        client = self.load_gateio_creds()
        self.spot_api = SpotApi(ApiClient(client))

    def load_gateio_creds(self) -> Configuration:
        return Configuration(key=self.configs['api'], secret=self.configs['secret'])