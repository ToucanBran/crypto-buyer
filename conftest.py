import pytest, yaml
from load_config import load_config

@pytest.fixture(scope="function")
def configs():
    with open("config.yml", "r") as stream:
        return yaml.safe_load(stream)