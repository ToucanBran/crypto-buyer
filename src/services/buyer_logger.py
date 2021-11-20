from io import TextIOWrapper
import logging, os, time, yaml, logging.config
from helpers import is_none_or_whitespace

class GMTFormatter(logging.Formatter):
    converter = time.gmtime

def read_config(f: TextIOWrapper):
    try:
        configs = yaml.safe_load(f.read())
        return configs
    except Exception as e:
        logging.basicConfig(level=logging.INFO)

def setup_logger():
    path = os.path.join(os.path.dirname(__file__), "log_configs.yaml")
    with open(path, 'r') as f:
        config = read_config(f)
        logging.config.dictConfig(config)

    return get_logger("buyer")

def get_logger(name):
    logger = logging.getLogger(name)
    level = os.environ.get("LOGLEVEL", "INFO") if not is_none_or_whitespace(os.environ.get("LOGLEVEL", "INFO")) else "INFO"
    logger.setLevel(level)
    return logger

