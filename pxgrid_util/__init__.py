
from . import _version
import logging

__version__ = _version.get_versions()['version']

import urllib
import base64
from urllib.parse import urlparse
from .config import Config
from .create_account_config import CreateAccountConfig
from .pxgrid import PXGridControl
from .ws_stomp import WebSocketStomp


logger = logging.getLogger(__name__)


def create_override_url(config: Config, discovered_url: str) -> str:
    logger.info('Overriding discovered service host with %s', config.discovery_override)
    o = urlparse(discovered_url)
    netloc_array = o.netloc.split(':')
    new_netloc = config.discovery_override
    if len(netloc_array) > 1:
        new_netloc += ':' + netloc_array[1]
    o = o._replace(netloc=new_netloc)
    new_url = o.geturl()
    logger.info('New URL %s', new_url)
    return new_url


def query(config, secret, url, payload):
    handler = urllib.request.HTTPSHandler(context=config.ssl_context)
    opener = urllib.request.build_opener(handler)
    rest_request = urllib.request.Request(url=url, data=str.encode(payload))
    rest_request.add_header('Content-Type', 'application/json')
    rest_request.add_header('Accept', 'application/json')
    b64 = base64.b64encode((config.node_name + ':' + secret).encode()).decode()
    rest_request.add_header('Authorization', 'Basic ' + b64)
    rest_response = opener.open(rest_request)
    return rest_response.read().decode()


