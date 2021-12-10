import pytest, yaml, os
from load_config import load_config

@pytest.fixture(scope="function")
def configs():
    with open(os.path.join(os.path.dirname(__file__),"config.yml"), "r") as stream:
        return yaml.safe_load(stream)