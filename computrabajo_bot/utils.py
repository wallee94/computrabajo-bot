import logging

logger = logging.getLogger(__name__)


class ComputrabajoStatusCodeError(IOError):
    pass


def catch_exceptions(func):
    """
    wrapper to validate that the page_id argument exists in the ES database
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ComputrabajoStatusCodeError as e:
            logger.error('ERROR: %s', e.args)

    return wrapper