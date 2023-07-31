import logging
# TODO maybe can integrate into mqtt client 
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger(__name__)


def arrived_message(message):
    log.debug(
        f'Received message {message.payload} on topic {message.topic} with QoS {message.qos}'
    )
