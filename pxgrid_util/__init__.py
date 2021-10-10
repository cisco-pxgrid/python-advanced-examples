
from . import _version
import logging

__version__ = _version.get_versions()['version']

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
