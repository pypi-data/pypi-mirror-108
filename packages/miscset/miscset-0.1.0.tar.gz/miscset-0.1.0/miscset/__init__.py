# miscset


"""Miscellaneous tools."""


import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


version = (0, 1, 0)
version_string = "{}.{}.{}".format(*version)


from .io import Parsable
from . import dt
from . import io
from . import sh

