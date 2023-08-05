"""The |pydwf.core.api.analog_in| module implements a single class: |AnalogIn|."""

# pylint: disable=too-many-lines

from typing import Tuple, List

import numpy as np

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.enum_types import (DwfTriggerLength, DwfTriggerSource, DwfTriggerType, DwfTriggerSlope,
                                             DwfAnalogInFilter, DwfAcquisitionMode, DwfState)
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.auxiliary.exceptions import PyDwfError
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class AnalogIn(DwfDevice_SubAPI):
    """The |AnalogIn| class provides access to the AnalogIn (oscilloscope) instrument of a
    |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its
        public |analogIn:link| attribute for access by the user.
    """

    # pylint: disable=too-many-public-methods

    def reset(self) -> None:
        """Reset all AnalogIn instrument parameters to default values.

        If auto-configuration is enabled at the device level, the reset operation is performed immediately;
        otherwise, an explicit call to the :py:meth:`configure` method is required.

        Raises:
            DwfLibraryError: There was an error while executing the *reset* operation.
        """
        result = self.lib.FDwfAnalogInReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self, reconfigure: bool, start: bool) -> None:
        """Configure the instrument and start or stop the acquisition operation.

        Parameters:
            reconfigure (bool): If True, the instrument settings are sent to the instrument.
                In addition, the auto-trigger timeout is reset.
            start (bool): If True, an acquisition is started. If False, an ongoing acquisition is stopped.

        Raises:
            DwfLibraryError: There was an error while executing the *configure* operation.
        """
        result = self.lib.FDwfAnalogInConfigure(self.hdwf, reconfigure, start)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerForce(self) -> None:
        """Force assertion of the instrument trigger.

        (To do: Figure out if this triggers the AnalogIn instrument or the AnalogIn trigger detector).

        Raises:
            DwfLibraryError: There was an error while executing the *triggerForce* operation.
        """
        result = self.lib.FDwfAnalogInTriggerForce(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self, read_data: bool) -> DwfState:
        """Check the status of the instrument.

        Executing this method initiates a status request to the AnalogIn instrument and receives its response.

        The following methods can be used to retrieve *AnalogIn* instrument status information
        as a result of this call, regardless of the value of *read_data*:

        * :py:meth:`~statusSamplesLeft`
        * :py:meth:`~statusTime`
        * :py:meth:`~statusSamplesValid`
        * :py:meth:`~statusIndexWrite`
        * :py:meth:`~statusAutoTriggered`
        * :py:meth:`~statusSample`
        * :py:meth:`~statusRecord`

        The following methods can be used to retrieve bulk data obtained from the *AnalogIn* instrument
        as a result of this call, but only if *read_data* is True:

        * :py:meth:`~statusData`
        * :py:meth:`~statusData2`
        * :py:meth:`~statusData16`
        * :py:meth:`~statusNoise`
        * :py:meth:`~statusNoise2`

        Arguments:
            read_data (bool): If True, read sample data from the instrument.

                For :py:attr:`~pydwf.core.auxiliary.enum_types.DwfAcquisitionMode.Single` acquisition mode,
                the data will be read only when the acquisition is finished.

        Returns:
            DwfState: The status of the AnalogIn instrument.

        Raises:
            DwfLibraryError: There was an error while executing the *status* operation.
        """
        c_status = typespec_ctypes.DwfState()
        result = self.lib.FDwfAnalogInStatus(self.hdwf, read_data, c_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        status_ = DwfState(c_status.value)
        return status_

    def statusSamplesLeft(self) -> int:
        """Retrieve the number of samples left in the acquisition, in samples.

        Returns:
            int: In case a finite-duration acquisition is active, the number of samples left in the acquisition.

        Raises:
            DwfLibraryError: There was an error while retrieving the number of samples left.
        """
        c_samples_left = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInStatusSamplesLeft(self.hdwf, c_samples_left)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samples_left = c_samples_left.value
        return samples_left

    def statusTime(self) -> Tuple[int, int, int]:
        """Retrieve the timestamp of the current status information.

        Returns:
            Tuple[int, int, int]: A three-element tuple, indicating the POSIX timestamp of the status request.
            The first element is the POSIX second, the second and third element are the numerator and denominator,
            respectively, of the fractional part of the second.

            In case :py:meth:`status` hasn't been called yet, this method will return zeroes
            for all three tuple elements.

        Raises:
            DwfLibraryError: There was an error while retrieving the status time.
        """
        c_sec_utc = typespec_ctypes.c_unsigned_int()
        c_tick = typespec_ctypes.c_unsigned_int()
        c_ticks_per_second = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfAnalogInStatusTime(self.hdwf, c_sec_utc, c_tick, c_ticks_per_second)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sec_utc = c_sec_utc.value
        tick = c_tick.value
        ticks_per_second = c_ticks_per_second.value
        return (sec_utc, tick, ticks_per_second)

    def statusSamplesValid(self) -> int:
        """Retrieve the number of valid acquired data samples.

        In :py:attr:`~pydwf.core.auxiliary.enum_types.DwfAcquisitionMode.Single` acquisition mode, valid samples are
        returned when :py:meth:`status` reports a result of :py:attr:`~pydwf.core.auxiliary.enum_types.DwfState.Done`.

        The actual number of samples transferred and reported back here is equal to max(16, :py:meth:`bufferSizeGet`).

        Returns:
            int: The number of valid samples.

        Raises:
            DwfLibraryError: There was an error while retrieving the number of valid samples.
        """
        c_samples_valid = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInStatusSamplesValid(self.hdwf, c_samples_valid)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samples_valid = c_samples_valid.value
        return samples_valid

    def statusIndexWrite(self) -> int:
        """Retrieve the buffer write index.

        This is needed in *ScanScreen* acquisition mode to display the scan bar.

        Returns:
            int: The buffer write index.

        Raises:
            DwfLibraryError: There was an error while retrieving the write index.
        """
        c_index_write = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInStatusIndexWrite(self.hdwf, c_index_write)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        index_write = c_index_write.value
        return index_write

    def statusAutoTriggered(self) -> bool:
        """Verify if the current acquisition is auto-triggered.

        Returns:
            bool: True if the current acquisition is auto-triggered, False otherwise.

        Raises:
            DwfLibraryError: There was an error while retrieving the auto-triggered state.
        """
        c_auto_triggered = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInStatusAutoTriggered(self.hdwf, c_auto_triggered)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        auto_triggered = bool(c_auto_triggered.value)
        return auto_triggered

    def statusSample(self, channel_index: int) -> float:
        """Get the last ADC conversion sample from the specified AnalogIn instrument channel, in Volts.

        Note:
            This value is updated even if the `status` method is called with argument False.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Returns:
            float: The most recent ADC value of this channel, in Volts.

        Raises:
            DwfLibraryError: There was an error while retrieving the sample value.
        """
        c_sample = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInStatusSample(self.hdwf, channel_index, c_sample)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sample = c_sample.value
        return sample

    def statusRecord(self) -> Tuple[int, int, int]:
        """Retrieve information about the recording process.

        Data loss occurs when the device acquisition is faster than the read process to the PC.

        If this happens, the device recording buffer is filled and data samples are overwritten.

        Corrupt samples indicate that the samples have been overwritten by the acquisition process during the
        previous read.

        In this case, try optimizing the loop process for faster execution or reduce the acquisition frequency or
        record length to be less than or equal to the device buffer size (i.e.,
        record_length is less than or equal to buffer_size / sample_frequency).

        Returns:
            Tuple[int, int, int]: A three-element tuple containing three counts for
                available*, *lost*, and *corrupt* data samples, in that order.

        Raises:
            DwfLibraryError: There was an error while retrieving the record status.
        """
        c_data_available = typespec_ctypes.c_int()
        c_data_lost = typespec_ctypes.c_int()
        c_data_corrupt = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInStatusRecord(
            self.hdwf,
            c_data_available,
            c_data_lost,
            c_data_corrupt)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        data_available = c_data_available.value
        data_lost = c_data_lost.value
        data_corrupt = c_data_corrupt.value
        return (data_available, data_lost, data_corrupt)

    def statusData(self, channel_index: int, count: int) -> np.ndarray:
        """Retrieve the acquired data samples from the specified AnalogIn instrument channel.

        This method returns samples as voltages, calculated from the raw, binary sample values as follows:

        .. code-block:: python

            voltages = analogIn.channelOffsetGet(channel_index) + \\
                       analogIn.channelRangeGet(channel_index) * (raw_samples / 65536.0)

        Note that the applied calibration is channel-dependent.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.
            count: int: The number of samples to retrieve.
        Returns:
            A 1D numpy array of floats, in Volts.

        Raises:
            DwfLibraryError: There was an error while retrieving the sample data.
        """
        samples = np.empty(count, dtype=np.float64)
        result = self.lib.FDwfAnalogInStatusData(
            self.hdwf,
            channel_index,
            samples.ctypes.data_as(typespec_ctypes.c_double_ptr),
            count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return samples

    def statusData2(self, channel_index: int, offset: int, count: int) -> np.ndarray:
        """Retrieve the acquired data samples from the specified AnalogIn instrument channel.

        This method returns samples as voltages, calculated from the raw, binary sample values as follows:

        .. code-block:: python

            voltages = analogIn.channelOffsetGet(channel_index) + \\
                       analogIn.channelRangeGet(channel_index) * (raw_samples / 65536.0)

        Note:
            The applied calibration is channel-dependent.

        Parameters:
            channel_index (int): The channel index, in the range 0 to :py:meth:`channelCount`-1.
            offset (int): Sample offset.
            count (int): Sample count.
        Returns:
            A 1D numpy array of floats, in Volts.

        Raises:
            DwfLibraryError: There was an error while retrieving the sample data.
        """
        samples = np.empty(count, dtype=np.float64)
        result = self.lib.FDwfAnalogInStatusData2(
            self.hdwf,
            channel_index,
            samples.ctypes.data_as(typespec_ctypes.c_double_ptr),
            offset,
            count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return samples

    def statusData16(self, channel_index: int, offset: int, count: int) -> np.ndarray:
        """Retrieve the acquired data samples from the specified AnalogIn instrument channel.

        This method returns raw, signed 16-bit samples.

        In case the ADC has less than 16 bits of raw resolution,
        least significant zero-bits are added to stretch the range to 16 bits.

        To convert these raw samples to voltages, use the following:

        .. code-block:: python

            voltages = analogIn.channelOffsetGet(channel_index) + \\
                       analogIn.channelRangeGet(channel_index) * (raw_samples / 65536.0)

        Parameters:
            channel_index (int): The channel index, in the range 0 to :py:meth:`channelCount`-1.
            offset (int): The sample offset to start copying from.
            count (int): The number of samples to retrieve.

        Returns:
            nd.array: A 1D numpy array of 16-bit signed integers.

        Raises:
            DwfLibraryError: There was an error while retrieving the sample data.
        """
        samples = np.empty(count, dtype=np.int16)
        result = self.lib.FDwfAnalogInStatusData16(
            self.hdwf,
            channel_index,
            samples.ctypes.data_as(typespec_ctypes.c_short_ptr),
            offset,
            count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return samples

    def statusNoise(self, channel_index: int, count: int) -> Tuple[np.ndarray, np.ndarray]:
        """Retrieve the acquired noise samples from the specified AnalogIn instrument channel.

        Parameters:
            channel_index (int): The channel index, in the range 0 to :py:meth:`channelCount`-1.
            count (int): Sample count.

        Returns:
            A two-element tuple; each element is a 1D numpy array of floats, in Volts.

            The first array contains the minimum values, the second element contains the maximum values.

        Raises:
            DwfLibraryError: There was an error while retrieving the noise data.
        """
        noise_min = np.empty(count, dtype=np.float64)
        noise_max = np.empty(count, dtype=np.float64)
        result = self.lib.FDwfAnalogInStatusNoise(
            self.hdwf,
            channel_index,
            noise_min.ctypes.data_as(typespec_ctypes.c_double_ptr),
            noise_max.ctypes.data_as(typespec_ctypes.c_double_ptr),
            count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return (noise_min, noise_max)

    def statusNoise2(self, channel_index: int, offset: int, count: int) -> Tuple[np.ndarray, np.ndarray]:
        """Retrieve the acquired data samples from the specified AnalogIn instrument channel.

        Parameters:
            channel_index (int): The channel index, in the range 0 to :py:meth:`channelCount`-1.
            offset (int): Sample offset.
            count (int): Sample count.

        Returns:
            A two-element tuple; each element is a 1D numpy array of floats, in Volts.

            The first array contains the minimum values, the second element contains the maximum values.

        Raises:
            DwfLibraryError: There was an error while retrieving the noise data.
        """
        noise_min = np.empty(count, dtype=np.float64)
        noise_max = np.empty(count, dtype=np.float64)
        result = self.lib.FDwfAnalogInStatusNoise2(
            self.hdwf,
            channel_index,
            noise_min.ctypes.data_as(typespec_ctypes.c_double_ptr),
            noise_max.ctypes.data_as(typespec_ctypes.c_double_ptr),
            offset,
            count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return (noise_min, noise_max)

    # Acquisition configuration:

    def recordLengthSet(self, record_duration: float) -> None:
        """Set the record length, in seconds.

        Note:
            This value is only used when the acquisition mode is configured as *Record*.

        Parameters:
            record_duration (float): The record duration to be configured, in seconds.

                A record duration of 0.0 (zero) seconds indicates a request for an arbitrary-length record acquisition.

        Raises:
            DwfLibraryError: There was an error while setting the record duration.
        """
        result = self.lib.FDwfAnalogInRecordLengthSet(self.hdwf, record_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def recordLengthGet(self) -> float:
        """Get the record length, in seconds.

        Note:
            This value is only used when the acquisition mode is configured as *Record*.

        Returns:
            float: The currently configured record length, in seconds.

            A record length of 0.0 (zero) seconds indicates a request for an arbitrary-length record acquisition.

        Raises:
            DwfLibraryError: There was an error while getting the record length.
        """
        c_record_duration = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInRecordLengthGet(self.hdwf, c_record_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        record_duration = c_record_duration.value
        return record_duration

    def frequencyInfo(self) -> Tuple[float, float]:
        """Retrieve the minimum and maximum configurable ADC sample frequency, in samples/second.

        Returns:
            Tuple[float, float]: The allowed sample frequency range (min, max), in samples/second.

        Raises:
            DwfLibraryError: There was an error while getting the allowed sample frequency range.
        """
        c_frequency_min = typespec_ctypes.c_double()
        c_frequency_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInFrequencyInfo(self.hdwf, c_frequency_min, c_frequency_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        frequency_min = c_frequency_min.value
        frequency_max = c_frequency_max.value
        return (frequency_min, frequency_max)

    def frequencySet(self, sample_frequency: float) -> None:
        """Set the ADC sample frequency of the AnalogIn instrument, in samples/second.

        Parameters:
            sample_frequency (float): Sample frequency, in samples/second.

        Raises:
            DwfLibraryError: There was an error while setting sample frequency.
        """
        result = self.lib.FDwfAnalogInFrequencySet(self.hdwf, sample_frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def frequencyGet(self) -> float:
        """Get the ADC sample frequency of the AnalogIn instrument, in samples/second.

        The ADC always runs at maximum frequency, but the method in which the samples are stored and transferred
        can be configured individually for each channel with the `channelFilterSet` method.

        Returns:
            float: The configured sample frequency, in samples/second.

        Raises:
            DwfLibraryError: There was an error while getting the sample frequency.
        """
        c_sample_frequency = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInFrequencyGet(self.hdwf, c_sample_frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sample_frequency = c_sample_frequency.value
        return sample_frequency

    def bitsInfo(self) -> int:
        """Get the fixed the number of bits used by the AnalogIn ADC.

        This number of bits can only be queried; it cannot be changed.

        Note:
            The Analog Discovery 2 uses an `Analog Devices AD9648
            <https://www.analog.com/media/en/technical-documentation/data-sheets/AD9648.pdf>`_ two-channel ADC.
            It converts 14-bit samples at a rate of up to 125 MHz. So for the Analog Discovery 2, this method
            always returns 14.

        Returns:
            int: The number of bits per sample for each of the AnalogIn channels.

        Raises:
            DwfLibraryError: There was an error while getting the number of bits.
        """
        c_num_bits = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInBitsInfo(self.hdwf, c_num_bits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        num_bits = c_num_bits.value
        return num_bits

    def bufferSizeInfo(self) -> Tuple[int, int]:
        """Returns the minimum and maximum allowable buffer size for the instrument, in samples.

        When using the *Record* acquisition mode, the buffer size should be left at the default value, which is equal
        to the maximum value. In other modes (e.g. *Single*), the buffer size determines the size of the
        acquisition window.

        Note:
            The maximum buffer size depends on the configuration that was selected while opening the device.

            For example, on the Analog Discovery 2, maximum AnalogIn buffer size can be 512, 2048, 8192, or 16384,
            depending on the configuration.

        Returns:
            Tuple[int, int]: A two-element tuple.
            The first element is the minimum buffer size, the second element is the maximum buffer size.

        Raises:
            DwfLibraryError: There was an error while getting the buffer size info.
        """
        c_buffer_size_min = typespec_ctypes.c_int()
        c_buffer_size_max = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInBufferSizeInfo(self.hdwf, c_buffer_size_min, c_buffer_size_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        buffer_size_min = c_buffer_size_min.value
        buffer_size_max = c_buffer_size_max.value
        return (buffer_size_min, buffer_size_max)

    def bufferSizeSet(self, buffer_size: int) -> None:
        """Adjust the AnalogIn instrument buffer size, expressed in samples.

        The actual buffer size configured will be clipped by the `bufferSizeInfo` values.

        The actual value configured can be read back by calling `bufferSizeGet`.

        Parameters:
            buffer_size (int): The requested buffer size, in samples.

        Raises:
            DwfLibraryError: There was an error while setting the buffer size.
        """
        result = self.lib.FDwfAnalogInBufferSizeSet(self.hdwf, buffer_size)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def bufferSizeGet(self) -> int:
        """Return the used AnalogIn instrument buffer size, in samples.

        Returns:
            int: The currently configured buffer size, in samples.

        Raises:
            DwfLibraryError: There was an error while getting the buffer size.
        """
        c_buffer_size = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInBufferSizeGet(self.hdwf, c_buffer_size)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        buffer_size = c_buffer_size.value
        return buffer_size

    def noiseSizeInfo(self) -> int:
        """Return the maximum noise buffer size for the AnalogIn instrument, in samples.

        Returns:
            The maximum noise buffer size, in samples.

        Raises:
            DwfLibraryError: There was an error while getting the noise buffer size info.
        """
        c_nSizeMax = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInNoiseSizeInfo(self.hdwf, c_nSizeMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        nSizeMax = c_nSizeMax.value
        return nSizeMax

    def noiseSizeSet(self, noise_buffer_size: int) -> None:
        """Enable or disable the noise buffer.

        This method determines if the noise buffer is enabled or disabled.

        Note:
            The name of this method and the type of its parameter (int) suggest that this function can be used
            to specify the size of the noise buffer, but that is not the case.

            Any non-zero value enables the noise buffer; a zero value disables it.

            If enabled, the noise buffer size as read by :py:meth:`noiseSizeGet` is always the size of the
            sample buffer as read by :py:meth:`bufferSizeGet` divided by 8.

        Parameters:
            noise_buffer_size (int): Whether to enable (non-zero) or disable (zero) the noise buffer.

        Raises:
            DwfLibraryError: There was an error while setting the noise buffer enabled/disabled state.
        """
        result = self.lib.FDwfAnalogInNoiseSizeSet(self.hdwf, int(noise_buffer_size))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def noiseSizeGet(self) -> int:
        """Return the currently configured noise buffer size for the AnalogIn instrument, in samples.

        This value is automatically adjusted according to the sample buffer size, divided by 8.
        For instance, setting the sample buffer size of 8192 implies a noise buffer size of 1024;
        setting the sample buffer size to 4096 implies noise buffer size will be 512.

        Returns:
            int: The currently active noise buffer size. Zero indicates that the noise buffer is disabled.

        Raises:
            DwfLibraryError: There was an error while getting the noise buffer size.
        """
        c_noise_buffer_size = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInNoiseSizeGet(self.hdwf, c_noise_buffer_size)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        noise_buffer_size = c_noise_buffer_size.value
        return noise_buffer_size

    def acquisitionModeInfo(self) -> List[DwfAcquisitionMode]:
        """Return the supported AnalogIn acquisition modes.

        Returns:
            List[DwfAcquisitionMode]: A list of acquisition modes supported by the AnalogIn instrument.

        Raises:
            DwfLibraryError: There was an error while getting the acquisition mode info.
        """

        c_acquisition_mode_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInAcquisitionModeInfo(self.hdwf, c_acquisition_mode_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        acquisition_mode_bitset = c_acquisition_mode_bitset.value
        acquisition_mode_list = [acquisition_mode for acquisition_mode in DwfAcquisitionMode
                                 if acquisition_mode_bitset & (1 << acquisition_mode.value)]
        return acquisition_mode_list

    def acquisitionModeSet(self, acquisition_mode: DwfAcquisitionMode) -> None:
        """Set the acquisition mode.

        Parameters:
            acquisition_mode (DwfAcquisitionMode): The acquisition mode to be configured.

        Raises:
            DwfLibraryError: There was an error while setting the acquisition mode.
        """
        result = self.lib.FDwfAnalogInAcquisitionModeSet(self.hdwf, acquisition_mode.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def acquisitionModeGet(self) -> DwfAcquisitionMode:
        """Get the currently configured acquisition mode.

        Returns:
            DwfAcquisitionMode: The acquisition mode currently configured.

        Raises:
            DwfLibraryError: There was an error while getting the acquisition mode.
        """
        c_acquisition_mode = typespec_ctypes.ACQMODE()
        result = self.lib.FDwfAnalogInAcquisitionModeGet(self.hdwf, c_acquisition_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        acquisition_mode = DwfAcquisitionMode(c_acquisition_mode.value)
        return acquisition_mode

    # Channel configuration:

    def channelCount(self) -> int:
        """Read the number of analog input channels.

        Returns:
            int: The number of analog input channels.

        Raises:
            DwfLibraryError: There was an error while retrieving the number of analog input channels.
        """
        c_channel_count = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInChannelCount(self.hdwf, c_channel_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_count = c_channel_count.value
        return channel_count

    def channelEnableSet(self, channel_index: int, enable: bool) -> None:
        """Enable or disable the specified analog input channel.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.
            enable: bool: Whether to enable (True) or disable (False) the specified channel.

        Raises:
            DwfLibraryError: There was an error while enabling or disabling the channel.
        """
        result = self.lib.FDwfAnalogInChannelEnableSet(self.hdwf, channel_index, enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelEnableGet(self, channel_index: int) -> bool:
        """Get the current enable/disable status of the specified AnalogIn channel.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Returns:
            bool: Channel is enabled (True) or disabled (False).

        Raises:
            DwfLibraryError: There was an error while getting the enabled/disabled state of the channel.
        """
        c_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInChannelEnableGet(self.hdwf, channel_index, c_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable = bool(c_enable.value)
        return enable

    def channelFilterInfo(self) -> List[DwfAnalogInFilter]:
        """Get a list of supported channel filter settings.

        Returns:
            List[DwfAnalogInFilter]: A list of possible channel filter settings.

        Raises:
            DwfLibraryError: There was an error while getting the channel filter info.
        """
        c_channel_filter_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInChannelFilterInfo(self.hdwf, c_channel_filter_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_filter_bitset = c_channel_filter_bitset.value
        channel_filter_list = [channel_filter for channel_filter in DwfAnalogInFilter
                               if channel_filter_bitset & (1 << channel_filter.value)]
        return channel_filter_list

    def channelFilterSet(self, channel_index: int, channel_filter: DwfAnalogInFilter) -> None:
        """Set the filter for a specified channel.

        Parameters:
            channel_index (int): The channel index, in the range 0 to :py:meth:`channelCount`-1.
            channel_filter (DwfAnalogInFilter): The channel filter mode to be selected.

        Raises:
            DwfLibraryError: There was an error while setting the channel filter.
        """
        result = self.lib.FDwfAnalogInChannelFilterSet(self.hdwf, channel_index, channel_filter.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelFilterGet(self, channel_index: int) -> DwfAnalogInFilter:
        """Get the channel filter setting.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Returns:
            DwfAnalogInFilter: The currently selected channel filter mode.

        Raises:
            DwfLibraryError: There was an error while getting the current channel filter setting.
        """
        c_channel_filter = typespec_ctypes.FILTER()
        result = self.lib.FDwfAnalogInChannelFilterGet(self.hdwf, channel_index, c_channel_filter)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_filter = DwfAnalogInFilter(c_channel_filter.value)
        return channel_filter

    def channelRangeInfo(self) -> Tuple[float, float, int]:
        """Report the possible voltage ranges of the analog input channels, in Volts.

        The values returned represent ideal values.
        The actual calibrated ranges are channel-dependent.

        See Also:
            The :py:meth:`channelRangeSteps` method returns essentially the same information
            in a different representation.

        Returns:
            Tuple[float, float, int]: The minimum range (Volts), maximum range (Volts),
            and number of different discrete channel settings of the |AnalogIn| instrument.

        Raises:
            DwfLibraryError: There was an error while getting the analog input range setting info.
        """
        c_voltsMin = typespec_ctypes.c_double()
        c_voltsMax = typespec_ctypes.c_double()
        c_nSteps = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInChannelRangeInfo(self.hdwf, c_voltsMin, c_voltsMax, c_nSteps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        voltsMin = c_voltsMin.value
        voltsMax = c_voltsMax.value
        # nSteps is retrieved as a double, but its value can always be expressed as an integer in Python.
        nSteps = round(c_nSteps.value)
        return (voltsMin, voltsMax, nSteps)

    def channelRangeSteps(self) -> List[float]:
        """Report the possible voltage ranges of the analog input channels, in Volts, as a list.

        The values returned represent ideal values.
        The actual calibrated ranges are channel-dependent.

        See Also:
            The :py:meth:`channelRangeInfo` method returns essentially the same information
            in a different representation.

        Returns:
            List[float]: A list of ranges, in Volts, representing the discrete
                channel range settings of the |AnalogIn| instrument.

        Raises:
            DwfLibraryError: there was an error while getting the list of analog input range settings.
        """
        c_rgVoltsStep = typespec_ctypes.c_double_array_32()
        c_nSteps = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInChannelRangeSteps(self.hdwf, c_rgVoltsStep, c_nSteps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        nSteps = c_nSteps.value
        rgVoltsStep = [c_rgVoltsStep[index] for index in range(nSteps)]
        return rgVoltsStep

    def channelRangeSet(self, channel_index: int, channel_range: float) -> None:
        """Set the range setting of the specified channel, in Volts.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.
            channel_range: float: The requested channel range, in Volts.

        Note:
            The actual range set will generally be different from the requested range.

        Note:
            Changing the channel range may also change the channel offset.

        Raises:
            DwfLibraryError: There was an error while setting the channel voltage range.
        """
        result = self.lib.FDwfAnalogInChannelRangeSet(self.hdwf, channel_index, channel_range)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelRangeGet(self, channel_index: int) -> float:
        """Get the range setting of the specified channel, in Volts.

        Together with the channel offset, this value can be used to transform raw binary ADC values into Volts.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Returns:
            float: The actual channel range, in Volts.

        Raises:
            DwfLibraryError: There was an error while setting the channel voltage range.
        """
        c_channel_range = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInChannelRangeGet(self.hdwf, channel_index, c_channel_range)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_range = c_channel_range.value
        return channel_range

    def channelOffsetInfo(self) -> Tuple[float, float, int]:
        """Get the possible channel offset settings, in Volts.

        Returns:
            Tuple[float, float, int]: The minimum channel offset (Volts), maximum channel offset (Volts),
                and number of steps.

        Raises:
            DwfLibraryError: There was an error while getting the channel offset info.
        """
        c_voltsMin = typespec_ctypes.c_double()
        c_voltsMax = typespec_ctypes.c_double()
        c_nSteps = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInChannelOffsetInfo(self.hdwf, c_voltsMin, c_voltsMax, c_nSteps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        voltsMin = c_voltsMin.value
        voltsMax = c_voltsMax.value
        nSteps = round(c_nSteps.value)
        return (voltsMin, voltsMax, nSteps)

    def channelOffsetSet(self, channel_index: int, channel_offset: float) -> None:
        """Set the channel offset, in Volts.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.
            channel_offset: float: The channel offset, in Volts.

        Note:
            The actual offset will generally be different from the requested offset.

        Note:
            Changing the channel offset may also change the channel range.

        Raises:
            DwfLibraryError: There was an error while setting the channel offset.
        """
        result = self.lib.FDwfAnalogInChannelOffsetSet(self.hdwf, channel_index, channel_offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelOffsetGet(self, channel_index: int) -> float:
        """Get the channel offset, in Volts.

        Together with the channel range, this value can be used to transform raw binary ADC values into Volts.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Returns:
            float: The currently active channel offset, in Volts.

        Raises:
            DwfLibraryError: There was an error while getting the current channel offset setting.
        """
        c_channel_offset = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInChannelOffsetGet(self.hdwf, channel_index, c_channel_offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_offset = c_channel_offset.value
        return channel_offset

    def channelAttenuationSet(self, channel_index: int, attenuation: float) -> None:
        """Set the channel attenuation setting.

        The channel attenuation is a dimensionless factor.

        This setting is normally used to compensate for probe attenuation.
        Many probes have two attenuation settings (e.g., ×1 and ×10).
        The value of this setting should correspond to the value of the probe, or 1 (the default)
        if a direct connection without attenuation is used.

        Note:
            Changing the channel attenuation will also change the channel offset and range.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.
            attenuation: float: The requested channel attenuation setting.
                If it is 0.0, the attenuation is set to 1.0 (the default) instead.

        Raises:
            DwfLibraryError: There was an error while setting the current channel attenuation.
        """
        result = self.lib.FDwfAnalogInChannelAttenuationSet(
            self.hdwf,
            channel_index,
            attenuation)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelAttenuationGet(self, channel_index: int) -> float:
        """Get the channel attenuation setting.

        The channel attenuation is a dimensionless factor.

        This setting is normally used to compensate for probe attenuation.
        Many probes have two attenuation settings (e.g., ×1 and ×10).
        The value of this setting should correspond to the value of the probe, or 1 (the default)
        if a direct connection without attenuation is used.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Returns:
            float: The channel attenuation setting.

        Raises:
            DwfLibraryError: There was an error while getting the current channel attenuation.
        """
        c_attenuation = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInChannelAttenuationGet(
            self.hdwf,
            channel_index,
            c_attenuation)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        attenuation = c_attenuation.value
        return attenuation

    def channelBandwidthSet(self, channel_index: int, bandwidth: float) -> None:
        """Set the channel bandwidth setting.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.
            bandwidth: float: The channel bandwidth setting, in Hz.

        Note:
            On the Analog Discovery 2, the channel bandwidth setting exists and can be set and retrieved,
            but the value has no effect.

        Raises:
            DwfLibraryError: There was an error while setting the channel bandwidth.
        """
        result = self.lib.FDwfAnalogInChannelBandwidthSet(self.hdwf, channel_index, bandwidth)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelBandwidthGet(self, channel_index: int) -> float:
        """Get the channel bandwidth setting.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Note:
            On the Analog Discovery 2, the channel bandwidth setting exists and can be set and retrieved,
            but the value has no effect.

        Returns:
            float: The channel bandwidth setting, in Hz.

        Raises:
            DwfLibraryError: There was an error while getting the current channel bandwidth.
        """
        c_bandwidth = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInChannelBandwidthGet(self.hdwf, channel_index, c_bandwidth)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        bandwidth = c_bandwidth.value
        return bandwidth

    def channelImpedanceSet(self, channel_index: int, impedance: float) -> None:
        """Set the channel impedance setting, in Ohms.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.
            impedance: float: channel impedance setting, in Ohms.

        Note:
            On the Analog Discovery 2, the channel impedance setting exists and can be set and retrieved,
            but the value has no effect.

        Raises:
            DwfLibraryError: There was an error while setting the current channel impedance.
        """
        result = self.lib.FDwfAnalogInChannelImpedanceSet(self.hdwf, channel_index, impedance)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelImpedanceGet(self, channel_index: int) -> float:
        """Get the channel impedance setting, in Ohms.

        Parameters:
            channel_index: int: The channel index, in the range 0 to :py:meth:`channelCount`-1.

        Note:
            On the Analog Discovery 2, the channel impedance setting exists and can be set and retrieved,
            but the value has no effect.

        Returns:
            float: The channel impedance setting, in Ohms.

        Raises:
            DwfLibraryError: There was an error while getting the current channel impedance.
        """
        c_impedance = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInChannelImpedanceGet(self.hdwf, channel_index, c_impedance)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        impedance = c_impedance.value
        return impedance

    # Trigger configuration:

    def triggerSourceInfo(self) -> List[DwfTriggerSource]:
        """Get analog-in trigger source info.

        Warning:
            This method is obsolete. Use the generic |DwfDevice.triggerInfo:link| method instead.

        Returns:
            List[DwfTriggerSource]: A list of trigger sources that can be selected.

        Raises:
            DwfLibraryError: There was an error while retrieving the trigger source information.
        """
        c_trigger_source_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInTriggerSourceInfo(self.hdwf, c_trigger_source_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source_bitset = c_trigger_source_bitset.value
        trigger_source_list = [trigger_source for trigger_source in DwfTriggerSource
                               if trigger_source_bitset & (1 << trigger_source.value)]
        return trigger_source_list

    def triggerSourceSet(self, trigger_source: DwfTriggerSource) -> None:
        """Set the trigger source.

        Parameters:
            trigger_source (DwfTriggerSource): The trigger source to be selected.

        Raises:
            DwfLibraryError: There was an error while setting the trigger source.
        """
        result = self.lib.FDwfAnalogInTriggerSourceSet(self.hdwf, trigger_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSourceGet(self) -> DwfTriggerSource:
        """Get the trigger source.

        Returns:
            DwfTriggerSource: The currently selected trigger source value.

        Raises:
            DwfLibraryError: There was an error while retrieving the active trigger source.
        """
        c_trigger_source = typespec_ctypes.TRIGSRC()
        result = self.lib.FDwfAnalogInTriggerSourceGet(self.hdwf, c_trigger_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source = DwfTriggerSource(c_trigger_source.value)
        return trigger_source

    def triggerPositionInfo(self) -> Tuple[float, float, int]:
        """Get trigger position info.

        Returns:
            Tuple[float, float, int]: The valid range of trigger positions that can be configured.

        Raises:
            DwfLibraryError: There was an error while retrieving the trigger position info.
        """
        c_trigger_position_min = typespec_ctypes.c_double()
        c_trigger_position_max = typespec_ctypes.c_double()
        c_trigger_position_num_steps = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerPositionInfo(
            self.hdwf,
            c_trigger_position_min,
            c_trigger_position_max,
            c_trigger_position_num_steps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        if not c_trigger_position_num_steps.value.is_integer():
            raise PyDwfError("Bad number of steps received.")

        trigger_position_min = c_trigger_position_min.value
        trigger_position_max = c_trigger_position_max.value
        trigger_position_num_steps = int(c_trigger_position_num_steps.value)

        return (trigger_position_min, trigger_position_max, trigger_position_num_steps)

    def triggerPositionSet(self, trigger_position: float) -> None:
        """Set the trigger position.

        In recording mode, the trigger position is the time, in seconds, relative to the position of the trigger event,
        of the first valid sample acquired. Negative values indicates times before the trigger time.

        For example, if the trigger should be in the middle of the acquisition window, this value should be
        set to -0.5 times the duration of the acquisition window.

        In Single acquisition mode, the trigger position is relative to the center of the acquisition window.

        Parameters:
            trigger_position (float): The trigger position to be configured, in seconds.

        Raises:
            DwfLibraryError: There was an error while setting the trigger position setpoint.
        """
        result = self.lib.FDwfAnalogInTriggerPositionSet(self.hdwf, trigger_position)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerPositionGet(self) -> float:
        """Get the trigger position.

        Returns:
            float: The currently configured trigger position, in seconds.

        Raises:
            DwfLibraryError: There was an error while getting the trigger position setpoint.
        """
        c_trigger_position = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerPositionGet(self.hdwf, c_trigger_position)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_position = c_trigger_position.value
        return trigger_position

    def triggerPositionStatus(self) -> float:
        """Get the current trigger position status.

        Returns:
            float: The current trigger position, in seconds.

        Raises:
            DwfLibraryError: There was an error while getting the trigger position status.
        """
        c_trigger_position = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerPositionStatus(self.hdwf, c_trigger_position)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_position = c_trigger_position.value
        return trigger_position

    def triggerAutoTimeoutInfo(self) -> Tuple[float, float, int]:
        """Get trigger auto-timeout info.

        Returns:
            Tuple[float, float, int]: The valid range of trigger auto-timeout values that can be configured.

        Raises:
            DwfLibraryError: There was an error while getting the trigger auto-timeout info.
        """
        c_secMin = typespec_ctypes.c_double()
        c_secMax = typespec_ctypes.c_double()
        c_nSteps = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerAutoTimeoutInfo(
            self.hdwf,
            c_secMin,
            c_secMax,
            c_nSteps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        if not c_nSteps.value.is_integer():
            raise PyDwfError("Bad auto-timeout info number of steps.")

        secMin = c_secMin.value
        secMax = c_secMax.value
        nSteps = int(c_nSteps.value)

        return (secMin, secMax, nSteps)

    def triggerAutoTimeoutSet(self, timeout_setting: float) -> None:
        """Set the trigger auto-timeout value.

        Parameters:
            timeout_setting (float): The auto timeout setting, in seconds.

        Raises:
            DwfLibraryError: There was an error while setting the trigger auto-timeout value.
        """
        result = self.lib.FDwfAnalogInTriggerAutoTimeoutSet(self.hdwf, timeout_setting)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerAutoTimeoutGet(self) -> float:
        """Get trigger auto-timeout value.

        Returns:
            float: The currently configured auto-timeout value, in seconds.

        Raises:
            DwfLibraryError: There was an error while getting the trigger auto-timeout value.
        """
        c_secTimeout = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerAutoTimeoutGet(self.hdwf, c_secTimeout)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secTimeout = c_secTimeout.value
        return secTimeout

    def triggerHoldOffInfo(self) -> Tuple[float, float, int]:
        """Get trigger holdoff info.

        The trigger holdoff setting is the minimum time (in seconds) for a trigger to be
        recognized after a previous trigger.

        Returns:
            Tuple[float, float, int]: The valid range of trigger holdoff values that can be configured.

        Raises:
            DwfLibraryError: There was an error while getting the trigger holdoff info.
        """
        c_secMin = typespec_ctypes.c_double()
        c_secMax = typespec_ctypes.c_double()
        c_nSteps = typespec_ctypes.c_double()

        result = self.lib.FDwfAnalogInTriggerHoldOffInfo(self.hdwf, c_secMin, c_secMax, c_nSteps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        if not c_nSteps.value.is_integer():
            raise PyDwfError("Bad trigger hold-time info number of steps.")

        secMin = c_secMin.value
        secMax = c_secMax.value
        nSteps = int(c_nSteps.value)

        return (secMin, secMax, nSteps)

    def triggerHoldOffSet(self, holdoff_setting: float) -> None:
        """Set trigger holdoff value.

        Parameters:
            holdoff_setting (float): The holdoff setting, in seconds.

        Raises:
            DwfLibraryError: There was an error while setting the trigger holdoff value.
        """
        result = self.lib.FDwfAnalogInTriggerHoldOffSet(self.hdwf, holdoff_setting)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerHoldOffGet(self) -> float:
        """Get trigger holdoff value.

        Returns:
            float: The currently configured trigger holdoff value, in seconds.

        Raises:
            DwfLibraryError: There was an error while getting the trigger holdoff value.
        """
        c_secHoldOff = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerHoldOffGet(self.hdwf, c_secHoldOff)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secHoldOff = c_secHoldOff.value
        return secHoldOff

    def triggerTypeInfo(self) -> List[DwfTriggerType]:
        """Get the trigger type info.

        Returns:
            List[DwfTriggerType]: A list of trigger types that can be configured.

        Raises:
            DwfLibraryError: There was an error while getting the trigger type info.
        """
        c_trigger_type_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInTriggerTypeInfo(self.hdwf, c_trigger_type_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_type_bitset = c_trigger_type_bitset.value
        trigger_type_list = [trigger_type for trigger_type in DwfTriggerType
                             if trigger_type_bitset & (1 << trigger_type.value)]
        return trigger_type_list

    def triggerTypeSet(self, trigger_type: DwfTriggerType) -> None:
        """Set the trigger type.

        Parameters:
            trigger_type (DwfTriggerType): The trigger type to be configured.

        Raises:
            DwfLibraryError: There was an error while setting the trigger type.
        """
        result = self.lib.FDwfAnalogInTriggerTypeSet(self.hdwf, trigger_type.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerTypeGet(self) -> DwfTriggerType:
        """Get the trigger type.

        Returns:
            DwfTriggerType: The currently configured trigger type.

        Raises:
            DwfLibraryError: There was an error while getting the trigger type.
        """
        c_trigger_type = typespec_ctypes.TRIGTYPE()
        result = self.lib.FDwfAnalogInTriggerTypeGet(self.hdwf, c_trigger_type)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_type = DwfTriggerType(c_trigger_type.value)
        return trigger_type

    def triggerChannelInfo(self) -> Tuple[int, int]:
        """Get |AnalogIn| trigger detector channel info.

        The |AnalogIn| trigger detector is sensitive to a specific channel.
        This method returns the range of valid analog input channels that can be configured
        as the |AnalogIn| trigger detector channel.

        Returns:
            Tuple[int, int]: A two-element tuple (min_channel_index, max_channel_index).

        Raises:
            DwfLibraryError: There was an error while getting the trigger channel info.
        """
        c_trigger_channel_index_min = typespec_ctypes.c_int()
        c_trigger_channel_index_max = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInTriggerChannelInfo(
            self.hdwf,
            c_trigger_channel_index_min,
            c_trigger_channel_index_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_channel_index_min = c_trigger_channel_index_min.value
        trigger_channel_index_max = c_trigger_channel_index_max.value
        return (trigger_channel_index_min, trigger_channel_index_max)

    def triggerChannelSet(self, trigger_channel_index: int) -> None:
        """Set |AnalogIn| trigger detector channel.

        This is the analog input channel that the |AnalogIn| trigger detector is sensitive to.

        Parameters:
            trigger_channel_index (int): The trigger channel to be selected.

        Raises:
            DwfLibraryError: There was an error while setting the trigger channel.
        """
        result = self.lib.FDwfAnalogInTriggerChannelSet(self.hdwf, trigger_channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerChannelGet(self) -> int:
        """Get |AnalogIn| trigger detector channel.

        This is the analog input channel that the |AnalogIn| trigger detector is sensitive to.

        Returns:
            int: The currently configured trigger channel.

        Raises:
            DwfLibraryError: There was an error while getting the trigger channel.
        """
        c_trigger_channel_index = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInTriggerChannelGet(self.hdwf, c_trigger_channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_channel_index = c_trigger_channel_index.value
        return trigger_channel_index

    def triggerFilterInfo(self) -> List[DwfAnalogInFilter]:
        """Get trigger filter info.

        Returns:
            List[DwfAnalogInFilter]: A list of filters that can be configured for the trigger.

        Raises:
            DwfLibraryError: There was an error while getting the trigger filter info.
        """
        c_trigger_filter_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInTriggerFilterInfo(self.hdwf, c_trigger_filter_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_filter_bitset = c_trigger_filter_bitset.value
        trigger_filter_list = [trigger_filter for trigger_filter in DwfAnalogInFilter
                               if trigger_filter_bitset & (1 << trigger_filter.value)]
        return trigger_filter_list

    def triggerFilterSet(self, trigger_filter: DwfAnalogInFilter) -> None:
        """Set |AnalogIn| trigger detector filter.

        Parameters:
            trigger_filter (DwfAnalogInFilter): The trigger filter to be selected.

        Raises:
            DwfLibraryError: There was an error while setting the trigger filter.
        """
        result = self.lib.FDwfAnalogInTriggerFilterSet(self.hdwf, trigger_filter.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerFilterGet(self) -> DwfAnalogInFilter:
        """Get |AnalogIn| trigger detector filter.

        Returns:
            int: The currently configured trigger filter.

        Raises:
            DwfLibraryError: There was an error while getting the trigger filter.
        """
        c_trigger_filter = typespec_ctypes.FILTER()
        result = self.lib.FDwfAnalogInTriggerFilterGet(self.hdwf, c_trigger_filter)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_filter = DwfAnalogInFilter(c_trigger_filter.value)
        return trigger_filter

    def triggerLevelInfo(self) -> Tuple[float, float, int]:
        """Get |AnalogIn| trigger detector level info, in Volts.

        Returns:
            Tuple[float, float, int]: The valid range of trigger level values that can be configured.

        Raises:
            DwfLibraryError: There was an error while getting the trigger level info.
        """
        c_voltsMin = typespec_ctypes.c_double()
        c_voltsMax = typespec_ctypes.c_double()
        c_nSteps = typespec_ctypes.c_double()

        result = self.lib.FDwfAnalogInTriggerLevelInfo(self.hdwf, c_voltsMin, c_voltsMax, c_nSteps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        if not c_nSteps.value.is_integer():
            raise PyDwfError("Bad trigger level info number of steps.")

        voltsMin = c_voltsMin.value
        voltsMax = c_voltsMax.value
        nSteps = int(c_nSteps.value)

        return (voltsMin, voltsMax, nSteps)

    def triggerLevelSet(self, trigger_level: float) -> None:
        """Set |AnalogIn| trigger detector level, in Volts.

        Parameters:
            trigger_level (float): The trigger level to be configured, in Volts.

        Raises:
            DwfLibraryError: There was an error while setting the trigger level.
        """
        result = self.lib.FDwfAnalogInTriggerLevelSet(self.hdwf, trigger_level)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerLevelGet(self) -> float:
        """Get |AnalogIn| trigger detector level, in Volts.

        Returns:
            float: The currently configured trigger level, in Volts.

        Raises:
            DwfLibraryError: There was an error while getting the trigger level.
        """
        c_trigger_level = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerLevelGet(self.hdwf, c_trigger_level)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_level = c_trigger_level.value
        return trigger_level

    def triggerHysteresisInfo(self) -> Tuple[float, float, int]:
        """Get |AnalogIn| trigger detector hysteresis info, in Volts.

        Returns:
            Tuple[float, float, int]: The valid range of trigger hysteresis values that can be configured.

        Raises:
            DwfLibraryError: There was an error while getting the trigger hysteresis info.
        """
        c_trigger_hysteresis_min = typespec_ctypes.c_double()
        c_trigger_hysteresis_max = typespec_ctypes.c_double()
        c_trigger_hysteresis_num_steps = typespec_ctypes.c_double()

        result = self.lib.FDwfAnalogInTriggerHysteresisInfo(
            self.hdwf,
            c_trigger_hysteresis_min,
            c_trigger_hysteresis_max,
            c_trigger_hysteresis_num_steps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        if not c_trigger_hysteresis_num_steps.value.is_integer():
            raise PyDwfError("Bad trigger hysteresis info number of steps.")

        trigger_hysteresis_min = c_trigger_hysteresis_min.value
        trigger_hysteresis_max = c_trigger_hysteresis_max.value
        trigger_hysteresis_num_steps = int(c_trigger_hysteresis_num_steps.value)

        return (trigger_hysteresis_min, trigger_hysteresis_max, trigger_hysteresis_num_steps)

    def triggerHysteresisSet(self, trigger_hysteresis: float) -> None:
        """Set |AnalogIn| trigger detector hysteresis, in Volts.

        Parameters:
            trigger_hysteresis (float): The trigger hysteresis to be configured, in Volts.

        Raises:
            DwfLibraryError: There was an error while setting the trigger hysteresis.
        """
        result = self.lib.FDwfAnalogInTriggerHysteresisSet(self.hdwf, trigger_hysteresis)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerHysteresisGet(self) -> float:
        """Get |AnalogIn| trigger detector trigger hysteresis, in Volts.

        Returns:
            float: The currently configured trigger hysteresis, in Volts.

        Raises:
            DwfLibraryError: There was an error while getting the trigger hysteresis.
        """
        c_trigger_hysteresis = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerHysteresisGet(self.hdwf, c_trigger_hysteresis)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_hysteresis = c_trigger_hysteresis.value
        return trigger_hysteresis

    def triggerConditionInfo(self) -> List[DwfTriggerSlope]:
        """Get |AnalogIn| trigger detector condition info.

        Raises:
            DwfLibraryError: There was an error while getting the trigger condition info.
        """
        c_trigger_condition_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInTriggerConditionInfo(
            self.hdwf,
            c_trigger_condition_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_condition_bitset = c_trigger_condition_bitset.value
        trigger_condition_list = [trigger_condition for trigger_condition in DwfTriggerSlope
                                  if trigger_condition_bitset & (1 << trigger_condition.value)]
        return trigger_condition_list

    def triggerConditionSet(self, trigger_condition: DwfTriggerSlope) -> None:
        """Set |AnalogIn| trigger detector condition.

        Parameters:
            trigger_condition (DwfTriggerSlope): The trigger condition to be configured.

        Raises:
            DwfLibraryError: there was an error while setting the trigger condition.
        """
        result = self.lib.FDwfAnalogInTriggerConditionSet(self.hdwf, trigger_condition.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerConditionGet(self) -> DwfTriggerSlope:
        """Get |AnalogIn| trigger detector condition.

        Returns:
            DwfTriggerSlope: The currently configured trigger condition.

        Raises:
            DwfLibraryError: There was an error while setting the trigger condition.
        """
        c_trigger_condition = typespec_ctypes.DwfTriggerSlope()
        result = self.lib.FDwfAnalogInTriggerConditionGet(self.hdwf, c_trigger_condition)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_condition = c_trigger_condition.value
        return DwfTriggerSlope(trigger_condition)

    def triggerLengthInfo(self) -> Tuple[float, float, int]:
        """Get |AnalogIn| trigger detector length info, in seconds.

        Returns:
            Tuple[float, float, int]: The valid range of trigger length values that can be configured.

        Raises:
            DwfLibraryError: There was an error while getting the trigger length info.
        """
        c_trigger_length_min = typespec_ctypes.c_double()
        c_trigger_length_max = typespec_ctypes.c_double()
        c_trigger_length_num_steps = typespec_ctypes.c_double()

        result = self.lib.FDwfAnalogInTriggerLengthInfo(self.hdwf, c_trigger_length_min, c_trigger_length_max,
                                                        c_trigger_length_num_steps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        if not c_trigger_length_num_steps.value.is_integer():
            raise PyDwfError("Bad trigger length info number of steps.")

        trigger_length_min = c_trigger_length_min.value
        trigger_length_max = c_trigger_length_max.value
        trigger_length_num_steps = int(c_trigger_length_num_steps.value)

        return (trigger_length_min, trigger_length_max, trigger_length_num_steps)

    def triggerLengthSet(self, trigger_length: float) -> None:
        """Set |AnalogIn| trigger detector length, in seconds.

        Parameters:
            trigger_length (float): The trigger length to be configured, in seconds.

        Raises:
            DwfLibraryError: There was an error while setting the trigger length.
        """
        result = self.lib.FDwfAnalogInTriggerLengthSet(self.hdwf, trigger_length)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerLengthGet(self) -> float:
        """Get |AnalogIn| trigger detector length, in seconds.

        Returns:
            float: The currently configured trigger length, in seconds.

        Raises:
            DwfLibraryError: There was an error while getting the trigger length.
        """
        c_trigger_length = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInTriggerLengthGet(self.hdwf, c_trigger_length)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_length = c_trigger_length.value
        return trigger_length

    def triggerLengthConditionInfo(self) -> List[DwfTriggerLength]:
        """Get |AnalogIn| trigger detector length condition info.

        Returns:
            List[DwfTriggerLength]: The valid trigger length condition values that can be selected.

        Raises:
            DwfLibraryError: There was an error while getting the trigger length condition info.
        """
        c_triglen_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogInTriggerLengthConditionInfo(self.hdwf, c_triglen_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        triglen_bitset = c_triglen_bitset.value
        triglen_list = [triglen for triglen in DwfTriggerLength if triglen_bitset & (1 << triglen.value)]
        return triglen_list

    def triggerLengthConditionSet(self, trigger_length_condition: DwfTriggerLength) -> None:
        """Set |AnalogIn| trigger detector length condition.

        Parameters:
            trigger_length_condition (DwfTriggerLength): The trigger length condition to be configured.

        Raises:
            DwfLibraryError: There was an error while setting the trigger length condition.
        """
        result = self.lib.FDwfAnalogInTriggerLengthConditionSet(
            self.hdwf,
            trigger_length_condition.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerLengthConditionGet(self) -> DwfTriggerLength:
        """Get |AnalogIn| trigger detector length condition.

        Returns:
            DwfTriggerLength: The currently configured trigger length condition.

        Raises:
            DwfLibraryError: There was an error while getting the trigger length condition.
        """
        c_trigger_length_condition = typespec_ctypes.TRIGLEN()
        result = self.lib.FDwfAnalogInTriggerLengthConditionGet(
            self.hdwf,
            c_trigger_length_condition)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_length_condition = DwfTriggerLength(c_trigger_length_condition.value)
        return trigger_length_condition

    def samplingSourceSet(self, sampling_source: DwfTriggerSource) -> None:
        """Set |AnalogIn| sampling source.

        Parameters:
            sampling_source (DwfTriggerSource): The sampling source to be configured.

        Raises:
            DwfLibraryError: There was an error while setting the sampling source.
        """
        result = self.lib.FDwfAnalogInSamplingSourceSet(self.hdwf, sampling_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def samplingSourceGet(self) -> DwfTriggerSource:
        """Get |AnalogIn| sampling source.

        Returns:
            DwfTriggerSource: The currently configured sampling source.

        Raises:
            DwfLibraryError: There was an error while getting the sampling source.
        """
        c_sampling_source = typespec_ctypes.TRIGSRC()
        result = self.lib.FDwfAnalogInSamplingSourceGet(self.hdwf, c_sampling_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sampling_source = DwfTriggerSource(c_sampling_source.value)
        return sampling_source

    def samplingSlopeSet(self, sampling_slope: DwfTriggerSlope) -> None:
        """Set |AnalogIn| sampling slope.

        Parameters:
            sampling_slope (DwfTriggerSlope): The sampling slope to be configured.

        Raises:
            DwfLibraryError: There was an error while setting the sampling slope.
        """
        result = self.lib.FDwfAnalogInSamplingSlopeSet(self.hdwf, sampling_slope.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def samplingSlopeGet(self) -> DwfTriggerSlope:
        """Get |AnalogIn| sampling slope.

        Returns:
            DwfTriggerSlope: The currently configured sampling slope.

        Raises:
            DwfLibraryError: There was an error while getting the sampling slope.
        """
        c_sampling_slope = typespec_ctypes.DwfTriggerSlope()
        result = self.lib.FDwfAnalogInSamplingSlopeGet(self.hdwf, c_sampling_slope)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sampling_slope = DwfTriggerSlope(c_sampling_slope.value)
        return sampling_slope

    def samplingDelaySet(self, sampling_delay: float) -> None:
        """Set |AnalogIn| sampling delay.

        Parameters:
            sampling_delay (float): The sampling delay to be configured, in seconds.

        Raises:
            DwfLibraryError: There was an error while setting the sampling delay.
        """
        result = self.lib.FDwfAnalogInSamplingDelaySet(self.hdwf, sampling_delay)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def samplingDelayGet(self) -> float:
        """Get |AnalogIn| sampling delay.

        Returns:
            float: The currently configured sampling delay, in seconds.

        Raises:
            DwfLibraryError: There was an error while getting the sampling delay.
        """
        c_sampling_delay = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogInSamplingDelayGet(self.hdwf, c_sampling_delay)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sampling_delay = c_sampling_delay.value
        return sampling_delay
