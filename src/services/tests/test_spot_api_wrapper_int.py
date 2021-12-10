import pytest
from services.spot_api_wrapper import SpotApiWrapper


def test_given_spotapiwrapperWithValidCredentials_when_spotApiPropertyUsed_expectSpotApi(configs):
    wrapper = SpotApiWrapper(configs["exchange"])
    s = wrapper.spot_api
    assert s is not None

@pytest.mark.parametrize("configs", [{ "api": "", "secret": "" }, {}, { "api": "dddd", "secret": "" }, { "api": "", "secret": "ddddd" }, { "api": "" }, { "secret": "" }])
def test_given_spotapiwrapperWithInvalidCredentials_when_spotApiPropertyUsed_expectException(configs):
    
    wrapper = SpotApiWrapper(configs)
    with pytest.raises(Exception):
        wrapper.spot_api