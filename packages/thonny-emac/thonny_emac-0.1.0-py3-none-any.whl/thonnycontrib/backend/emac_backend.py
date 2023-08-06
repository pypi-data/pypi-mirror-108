# import datetime
import logging

# from textwrap import dedent, indent

from thonny.plugins.micropython.bare_metal_backend import BareMetalMicroPythonBackend

logger = logging.getLogger(__name__)


class EmacBareMetalBackend(BareMetalMicroPythonBackend):
    def _get_flash_prefix():
        return "/flash/"
