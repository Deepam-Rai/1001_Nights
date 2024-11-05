from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def get_timestamp():
    return f"{datetime.fromtimestamp(datetime.timestamp(datetime.now())).isoformat()}"
