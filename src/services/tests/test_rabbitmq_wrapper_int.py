from services.rabbitmq_wrapper import RabbitMqWrapper
import yaml

def test_given_validRabbitConfigurations_when_openChannelCalled_then_expectSuccessfulConnection(configs):
    wrapper = RabbitMqWrapper(configs["queue"])
    channel = wrapper.open_channel()
    opened = channel.is_open
    wrapper.close_connection()
    assert opened