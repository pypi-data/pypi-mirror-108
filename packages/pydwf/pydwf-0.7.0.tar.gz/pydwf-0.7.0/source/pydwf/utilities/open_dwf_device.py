"""Implementation of the |pydwf.utilities.open_dwf_device| function."""

from typing import Optional, Callable, Dict, Any

from pydwf.core.dwf_library import DwfLibrary
from pydwf.core.dwf_device import DwfDevice
from pydwf.core.auxiliary.enum_types import DwfEnumConfigInfo, DwfEnumFilter
from pydwf.core.auxiliary.exceptions import PyDwfError


def open_dwf_device(dwf: DwfLibrary,
                    enum_filter: Optional[DwfEnumFilter] = None,
                    serial_number: Optional[str] = None,
                    configuration_fitness_func: Optional[Callable[[Dict[str, Any]], Optional[int]]] = None
                    ) -> DwfDevice:
    """Open a device identified by its serial number, optionally selecting a preferred configuration.

    This is a three-step process:

    1. The first step this function performs is to select a device for opening.

       To do this, all available Digilent Waveforms devices are enumerated. For this initial enumeration process
       the *enum_filter* parameter is used, if given.

       Then, if the *serial_number* parameter is given, the list will be filtered to exclude devices whose serial
       numbers do not match.

       If the list that remains has a single device, this device will be used. If not, a |PyDwfError| is reported.

    2. The next step is to select a configuration for the device.

       If no *configuration_fitness_func* is provided, the first (default) configuration will be used.

       If a *configuration_fitness_func* is provided, it should be a function (or lambda expression) that takes a
       single parameter *configuration_info*, which is a dictionary with string keys that correspond to the names
       of each possible |DwfEnumConfigInfo:link| entry, and values that correspond to the value of that parameter
       for a specific configuration.

       The function should return *None* if the configuration is entirely unsuitable, or otherwise an integer score
       that reflects the 'desirability' or 'fitness' score of that particular configuration for the task at hand.

       The *open_dwf_device* function will go through all available device configurations, construct a dictionary
       of all parameters that describe the configuration, call the *configuration_fitness_func* with that dictionary,
       and examine the score value it returns. If multiple suitable device configurations are found (i.e., the
       *configuration_fitness_func* does not return None), it will select the configuration with the highest score.

       This may all sounds pretty complicated, but in practice this parameter is quite easy to define for most common
       use-cases.

       As an example, to select a configuration that maximizes the analog input buffer size, simply use this:

       .. code-block:: python

          def fitness_func(config_parameters):
              return config_parameters["AnalogInBufferSize"]

          with open_dwf_device(dwf, configuration_fitness_func = fitness_func) as device:
              use_device_with_big_analog_in_buffer(device)

    3. As a final step, the selected device is opened using the selected device configuration, and the |DwfDevice:link|
       instance is returned.

    Note:
        This method takes several seconds to complete.

    Parameters:
        dwf (DwfLibrary): The |DwfLibrary:link| used to open the device.
        serial_number (str): The serial number of the device to be opened.
            Digilent Waveforms device serial numbers consist of 12 hexadecimal digits.
        configuration_fitness_func (Optional[Callable[[Dict[str, Any]]):
            A function to score the preferred configuration of the selected device.
            See the description above for details.
        enum_filter (Optional[DwfEnumFilter]):
            An optional filter to limit the device enumeration to certain device types.
            In None, enumerate all devices.

    Returns:
        DwfDevice: The |DwfDevice:link| created as a result of this call.

    Raises:
        PyDwfError: could not select a unique candidate device, or no usable configuration detected.
    """

    if enum_filter is None:
        enum_filter = DwfEnumFilter.All

    # The dwf.deviceEnum.enumerateDevices() function builds an internal table of connected devices
    # that can be queried using other dwf.deviceEnum methods.
    num_devices = dwf.deviceEnum.enumerateDevices(enum_filter)

    # We do the explicit conversion to list to make sure the variable is a list of integers, not a range.
    candidate_devices = list(range(num_devices))

    if serial_number is not None:

        candidate_devices = [device_index for device_index in candidate_devices
                             if dwf.deviceEnum.serialNumber(device_index) == serial_number]

        if len(candidate_devices) == 0:
            raise PyDwfError("No Digilent Waveforms device found in device class '{}' with serial number '{}'.".format(
                enum_filter.name, serial_number))

        if len(candidate_devices) > 1:
            # Multiple devices found with a matching serial number; this should not happen!
            raise PyDwfError("Multiple Digilent Waveforms devices found with serial number '{}'.".format(
                serial_number))

    else:

        if len(candidate_devices) == 0:
            raise PyDwfError("No Digilent Waveforms devices found in device class '{}'.".format(enum_filter.name))

        if len(candidate_devices) > 1:
            raise PyDwfError(
                "Multiple Digilent Waveforms devices found (serial numbers: {});"
                " specify a serial number to select one.".format(
                    ", ".join(dwf.deviceEnum.serialNumber(device_index) for device_index in candidate_devices)))

    # We now have a single candidate device left.

    assert len(candidate_devices) == 1

    device_index = candidate_devices[0]

    if configuration_fitness_func is None:
        # If no 'configuration_fitness_func' was specified, just return the first one.
        return dwf.deviceControl.open(device_index)

    # The caller specified a 'configuration_fitness_func'.
    # We will examine all configuration and pick the one that has the highest fitness.

    num_config = dwf.deviceEnum.enumerateConfigurations(device_index)

    best_configuration_index = None
    best_configuration_fitness = None

    for configuration_index in range(num_config):

        configuration_info = {
            configuration_parameter.name:
                dwf.deviceEnum.configInfo(configuration_index, configuration_parameter)
            for configuration_parameter in DwfEnumConfigInfo}

        configuration_fitness = configuration_fitness_func(configuration_info)

        if configuration_fitness is None:
            continue

        if best_configuration_index is None or configuration_fitness > best_configuration_fitness:
            best_configuration_index = configuration_index
            best_configuration_fitness = configuration_fitness

    if best_configuration_index is None:
        raise PyDwfError("No acceptable configuration was found.")

    return dwf.deviceControl.open(device_index, best_configuration_index)
