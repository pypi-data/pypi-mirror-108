"""
Module: 'onewire' on micropython-cutipy-1.14-128
"""
# MCU: {'ver': '1.14-128', 'port': 'cutipy', 'arch': 'armv7emsp', 'sysname': 'cutipy', 'release': '1.14.0', 'name': 'micropython', 'mpy': 7685, 'version': '1.14.0', 'machine': 'EMAC-CutiPy with STM32F407', 'build': '128', 'nodename': 'cutipy', 'platform': 'cutipy', 'family': 'micropython'}
# Stubber: 1.3.9


class OneWire:
    ""
    MATCH_ROM = 85
    SEARCH_ROM = 240
    SKIP_ROM = 204

    def _search_rom():
        pass

    def crc8():
        pass

    def readbit():
        pass

    def readbyte():
        pass

    def readinto():
        pass

    def reset():
        pass

    def scan():
        pass

    def select_rom():
        pass

    def write():
        pass

    def writebit():
        pass

    def writebyte():
        pass


class OneWireError:
    ""


_ow = None
