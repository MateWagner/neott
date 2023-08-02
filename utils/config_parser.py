import os
import yaml
conf = yaml.safe_load(open("config.yml"))
# print(conf['NEOPIXEL']['PIN'])
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

# print(ROOT_TOPIC + '/dsa')
