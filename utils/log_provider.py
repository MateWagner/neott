import logging
# TODO maybe can integrate into mqtt client
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger(__name__)


def arrived_message(message):
    log.debug('Received message %s on topic %s with QoS %s',
              message.payload, message.topic, message.qos)
