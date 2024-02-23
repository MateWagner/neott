import os
import yaml


def parse_config_yml():
    # Define the relative path to the config.yml file
    CONFIG_FILE_RELATIVE_PATH = "../config.yml"

    # Get the absolute path of the directory containing this script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Load the configuration from the config.yml file
    return yaml.safe_load(open(os.path.join(script_directory, CONFIG_FILE_RELATIVE_PATH), encoding="utf-8"))


conf = parse_config_yml()
# neopixel constans
NUM_PIXEL = conf['NEOPIXEL']['NUM_PIXEL']
ORDER = conf['NEOPIXEL']['ORDER']
PIN = conf['NEOPIXEL']['PIN']

# mqtt constans
HOST = conf['MQTT']['HOST']
PORT = conf['MQTT']['PORT']
KEEP_ALIVE = conf['MQTT']['KEEP_ALIVE']
ROOT_TOPIC = conf['MQTT']['ROOT_TOPIC']
USER = conf['MQTT']['USER']
PASS = conf['MQTT']['PASS']


# dev
DEBUG = conf['DEV']['DEBUG']

