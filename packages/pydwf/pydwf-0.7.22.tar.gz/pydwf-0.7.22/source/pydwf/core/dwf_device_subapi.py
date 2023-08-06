"""The *pydwf.core.dwf_device_subapi* module implements a single class: *AbstractDwfDeviceSubApi*."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydwf.core.dwf_device import DwfDevice


class AbstractDwfDeviceSubApi:
    """Abstract base class for the sub-API class members of a |DwfDevice:link|."""

    def __init__(self, device: 'DwfDevice'):
        self._device = device

    @property
    def device(self):
        """Return the device."""
        return self._device

    @property
    def hdwf(self):
        """Return the HDWF device handle."""
        return self.device.hdwf

    @property
    def dwf(self):
        """Return the library."""
        return self.device.dwf

    @property
    def lib(self):
        """Return the |ctypes:link| library."""
        return self.dwf.lib
