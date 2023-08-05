"""The |pydwf.core.dwf_device| module implements a single class: |DwfWaveformsDevice|."""

from typing import List, TYPE_CHECKING

from pydwf.core.auxiliary.enum_types import DwfTriggerSource, DwfTriggerSlope, DwfParameter
from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS

from pydwf.core.api.analog_in import AnalogIn
from pydwf.core.api.analog_out import AnalogOut
from pydwf.core.api.digital_in import DigitalIn
from pydwf.core.api.digital_out import DigitalOut
from pydwf.core.api.analog_io import AnalogIO
from pydwf.core.api.digital_io import DigitalIO
from pydwf.core.api.digital_uart import DigitalUart
from pydwf.core.api.digital_can import DigitalCan
from pydwf.core.api.digital_spi import DigitalSpi
from pydwf.core.api.digital_i2c import DigitalI2c
from pydwf.core.api.analog_impedance import AnalogImpedance

if TYPE_CHECKING:
    # The DwfLibrary types is needed while type-checking (mypy).
    from pydwf.core.dwf_library import DwfLibrary
    import ctypes


class DwfDevice:
    """The |DwfDevice| represents a single Digilent Waveforms test and measurement device.

    Attention:

        Users of |pydwf| should not create instances of this class directly.

        Use |DwfLibrary.deviceControl.open:link| or |pydwf.utilities.open_dwf_device:link| to obtain a valid
        |DwfDevice| instance.

    The main test and measurement functionality of a Digilent Waveforms device is provided as
    multiple sub-interfaces (instruments, protocols, and measurements). To access those,
    use one of the eleven attributes described below.

    .. rubric:: |DwfDevice| attributes

    Attributes:

        analogIn (AnalogIn):
            Provides access analog input (oscilloscope) functionality.
        analogOut (AnalogOut):
            Provides access to the analog output (waveform generator) functionality.
        analogIO (AnalogIO):
            Provides access to the analog I/O (voltage source, monitoring) functionality.
        analogImpedance (AnalogImpedance):
            Provides access to the analog impedance measurement functionality.
        digitalIn (DigitalIn):
            Provides access to the dynamic digital input (logic analyzer) functionality.
        digitalOut (DigitalOut):
            Provides access to the dynamic digital output (pattern generator) functionality.
        digitalIO (DigitalIO):
            Provides access to the static digital I/O functionality.
        digitalUart (DigitalUart):
            Provides access to the UART protocol functionality.
        digitalCan (DigitalCan):
            Provides access to the CAN protocol functionality.
        digitalSpi (DigitalSpi):
            Provides access to the SPI protocol functionality.
        digitalI2c (DigitalI2c):
            Provides access to the I2C protocol functionality.

    .. rubric:: |DwfDevice| methods
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, dwf: 'DwfLibrary', hdwf: int) -> None:
        """Initialize a DwfDevice with the specified DWF handle value.

        This method is used by the |DwfLibrary.device.open| method to initialize a |DwfDevice| immediately after
        successfully opening a Digilent Waveforms device using the low-level C API.

        User programs should not initialize |DwfDevice| instances themselves, but leave that to |pydwf| instead.

        Parameters:
            dwf (DwfLibrary):
                The |DwfLibrary| instance used to make calls to the underlying library.
            hdwf (int):
                The device to open.
        """

        self._dwf = dwf
        self._hdwf = hdwf

        # Initialize sub-API instances and assign them to attributes.

        self.analogIn = AnalogIn(self)
        self.analogOut = AnalogOut(self)
        self.analogIO = AnalogIO(self)
        self.analogImpedance = AnalogImpedance(self)
        self.digitalIn = DigitalIn(self)
        self.digitalOut = DigitalOut(self)
        self.digitalIO = DigitalIO(self)
        self.digitalUart = DigitalUart(self)
        self.digitalCan = DigitalCan(self)
        self.digitalSpi = DigitalSpi(self)
        self.digitalI2c = DigitalI2c(self)

    def __enter__(self):
        """Context manager entry method."""
        return self

    def __exit__(self, *dummy):
        """Context manager exit method."""
        self.close()

    @property
    def dwf(self) -> 'DwfLibrary':
        """Return the |DwfLibrary| instance.

        This property is intended for internal |pydwf| use.

        :meta private:
        """
        return self._dwf

    @property
    def hdwf(self) -> int:
        """Return the HDWF handle of the device.

        This property is intended for internal |pydwf| use.

        :meta private:
        """
        return self._hdwf

    @property
    def lib(self) -> 'ctypes.CDLL':
        """Return the |ctypes| shared library instance used to access the DWF library.

        This property is intended for internal |pydwf| use.

        :meta private:
        """
        return self._dwf.lib

    def close(self) -> None:
        """Close the device.

        This method should be called when access to the device is no longer needed.

        Once this function returns, the |DwfDevice| can no longer be used.

        Raises:
            DwfLibraryError: The device cannot be closed.
        """
        result = self.lib.FDwfDeviceClose(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def autoConfigureSet(self, auto_configure: int) -> None:
        """Enable or disable the auto-configuration setting of the device.

        When this setting is enabled, the device is automatically configured every time an instrument parameter is set.

        This adds latency to every *Set* function; just as much latency as calling the corresponding *configure*
        method directly afterward.

        With value 3, configuration will be applied dynamically, without stopping the instrument.

        Parameters:
            auto_configure (int): Specify auto-configuration setting.

                Possible values for this option:

                * 0: disable;
                * 1: enable;
                * 3: dynamic.

        Raises:
            DwfLibraryError: The value cannot be set.
        """
        result = self.lib.FDwfDeviceAutoConfigureSet(self.hdwf, auto_configure)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def autoConfigureGet(self) -> int:
        """Return the auto-configuration setting of the device.

        Returns:
            The auto-configure setting

            Possible values:

            * 0: disable;
            * 1: enable;
            * 3: dynamic.

        Raises:
            DwfLibraryError: The value cannot be retrieved.
        """

        c_auto_configure = typespec_ctypes.c_int()
        result = self.lib.FDwfDeviceAutoConfigureGet(self.hdwf, c_auto_configure)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        auto_configure = c_auto_configure.value
        return auto_configure

    def reset(self) -> None:
        """Reset all device and instrument parameters to default values.

        The new settings are effectuated immediately if auto-configuration is enabled.

        Raises:
            DwfLibraryError: The device cannot be reset.
        """
        result = self.lib.FDwfDeviceReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def enableSet(self, enable: bool) -> None:
        """Enable or disable the device.

        Parameters:
            enable (bool): True for enable, False for disable.

        Raises:
            DwfLibraryError: The device's enabled state cannot be set.
        """
        result = self.lib.FDwfDeviceEnableSet(self.hdwf, enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerInfo(self) -> List[DwfTriggerSource]:
        """Return the supported trigger source options for the global trigger bus.

        Returns:
            List[DwfTriggerSource]: A list of available trigger sources.

        Raises:
            DwfLibraryError: The list of supported trigger sources cannot be retrieved.
        """
        c_trigger_source_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDeviceTriggerInfo(self.hdwf, c_trigger_source_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source_bitset = c_trigger_source_bitset.value
        trigger_source_list = [trigger_source for trigger_source in DwfTriggerSource
                               if trigger_source_bitset & (1 << trigger_source.value)]
        return trigger_source_list

    def triggerSet(self, pin_index: int, trigger_source: DwfTriggerSource) -> None:
        """Configure the trigger I/O pin with a specific trigger source option.

        Parameters:
            pin_index (int): The pin_index to configure.
            trigger_source (DwfTriggerSource): The trigger source to select.

        Raises:
            DwfLibraryError: The trigger source cannot be set.
        """
        result = self.lib.FDwfDeviceTriggerSet(self.hdwf, pin_index, trigger_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerGet(self, pin_index: int) -> DwfTriggerSource:
        """Return the selected trigger source for a trigger I/O pin.

        The trigger source can be 'none', an internal instrument, or an external trigger.

        Parameters:
            pin_index (int): The pin for which to obtain the selected trigger source.

        Returns:
           DwfTriggerSource: The trigger source setting for the selected pin.

        Raises:
            DwfLibraryError: The trigger source cannot be retrieved.
        """
        c_trigger_source = typespec_ctypes.TRIGSRC()
        result = self.lib.FDwfDeviceTriggerGet(self.hdwf, pin_index, c_trigger_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source = DwfTriggerSource(c_trigger_source.value)
        return trigger_source

    def triggerPC(self) -> None:
        """Generate one pulse on the PC trigger line.

        Raises:
            DwfLibraryError: The PC trigger line cannot be pulsed.
        """
        result = self.lib.FDwfDeviceTriggerPC(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSlopeInfo(self) -> List[DwfTriggerSlope]:
        """Return the supported trigger slope options.

        Returns:
            List[DwfTriggerSlope]: A list of supported trigger slope values.

        Raises:
            DwfLibraryError: The trigger slope options cannot be retrieved.
        """
        c_slope_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDeviceTriggerSlopeInfo(self.hdwf, c_slope_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        slope_bitset = c_slope_bitset.value
        slope_list = [slope for slope in DwfTriggerSlope if slope_bitset & (1 << slope.value)]
        return slope_list

    def paramSet(self, parameter: DwfParameter, value: int) -> None:
        """Set a device parameter.

        Parameters:
            parameter (DwfParameter): The device parameter to set.
            value (int): The value to assign to the parameter.

        Raises:
            DwfLibraryError: The specified device parameter cannot be set.
        """
        result = self.lib.FDwfDeviceParamSet(self.hdwf, parameter.value, value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def paramGet(self, parameter: DwfParameter) -> int:
        """Retrieve a device parameter.

        Parameters:
            parameter (DwfParameter): The device parameter to retrieve.

        Returns:
            int: The integer value of the parameter.

        Raises:
            DwfLibraryError: The specified device parameter cannot be retrieved.
        """
        c_value = typespec_ctypes.c_int()
        result = self.lib.FDwfDeviceParamGet(self.hdwf, parameter.value, c_value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        value = c_value.value
        return value
