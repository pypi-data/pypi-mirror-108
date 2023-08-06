import logging

# from typing import Optional

# from thonny import ui_utils, get_workbench
from thonny.plugins.micropython import (
    BareMetalMicroPythonProxy,
    add_micropython_backend,
    BareMetalMicroPythonConfigPage,
)

# from thonny.ui_utils import show_dialog

logger = logging.getLogger(__name__)


class EmacMicropythonBackendProxy(BareMetalMicroPythonProxy):
    def get_node_label(self):
        if "cutipy" in self._welcome_text.lower():
            return "CutiPy"
        elif "mitipy" in self._welcome_text.lower():
            return "MitiPy"
        else:
            return "MicroPython Device"


class EmacMicropythonBackendConfigPage(BareMetalMicroPythonConfigPage):
    @property
    def allow_webrepl(self):
        return False


def load_plugin():
    add_micropython_backend(
        "EMAC MicroPython",
        EmacMicropythonBackendProxy,
        "Micropython (EMAC CutiPy/MitiPy)",
        EmacMicropythonBackendConfigPage,
        bare_metal=True,
        sort_key="37",
    )
