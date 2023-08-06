"""The |pydwf.core.api.analog_out| module implements a single class: |AnalogOut|."""

# pylint: disable=too-many-lines

from typing import Tuple, List

import numpy as np

from pydwf.core.dwf_device_subapi import AbstractDwfDeviceSubApi

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.enum_types import (DwfTriggerSource, DwfAnalogOutFunction, DwfState,
                                             DwfAnalogOutNode, DwfTriggerSlope, DwfAnalogOutMode, DwfAnalogOutIdle)
from pydwf.core.auxiliary.constants import RESULT_SUCCESS


class AnalogOut(AbstractDwfDeviceSubApi):
    """The |AnalogOut| class provides access to the analog output (signal generator) instrument of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its
        public |analogOut:link| attribute for access by the user.
    """

    # pylint: disable=too-many-public-methods

    ####################################################################################################################
    #                                                                                                                  #
    #                                               INSTRUMENT CONTROL                                                 #
    #                                                                                                                  #
    ####################################################################################################################

    def reset(self, channel_index: int) -> None:
        """Reset the |AnalogOut| instrument.

        Raises:
            DwfLibraryError: An error occurred while executing the *reset* operation.
        """
        result = self.lib.FDwfAnalogOutReset(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self, channel_index: int, start: bool) -> None:
        """Configure the |AnalogOut| instrument.

        Parameters:
            channel_index (int): The output channel to configure. Specify -1 to configure all channels.
            start (int): Whether to start/stop the instrument:

               * 0: Stop instrument.
               * 1: Start instrument.
               * 3: Apply settings; do not change instrument state.

        Raises:
            DwfLibraryError: An error occurred while executing the *configure* operation.
        """
        result = self.lib.FDwfAnalogOutConfigure(self.hdwf, channel_index, start)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self, channel_index: int) -> DwfState:
        """Get |AnalogOut| instrument channel state.

        Executing this method initiates a status request to the |AnalogOut| instrument and receives its response.

        Parameters:
            channel_index (int): The output channel for which to get the status.

        Returns:
            DwfState: The status of the |AnalogOut| instrument channel.

        Raises:
            DwfLibraryError: An error occurred while executing the *status* operation.
        """
        c_status = typespec_ctypes.DwfState()
        result = self.lib.FDwfAnalogOutStatus(self.hdwf, channel_index, c_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        status = DwfState(c_status.value)
        return status

    ####################################################################################################################
    #                                                                                                                  #
    #                                                    CHANNEL COUNT                                                 #
    #                                                                                                                  #
    ####################################################################################################################

    def count(self) -> int:
        """Count the number of analog output channels.

        Returns:
            int: The number of analog output channels.

        Raises:
            DwfLibraryError: An error occurred while retrieving the number of analog output channels.
        """
        c_channel_count = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutCount(self.hdwf, c_channel_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_count = c_channel_count.value
        return channel_count

    ####################################################################################################################
    #                                                                                                                  #
    #                                               PER-CHANNEL CONFIGURATION                                          #
    #                                                                                                                  #
    ####################################################################################################################

    def masterSet(self, channel_index: int, master_channel_index: int) -> None:
        """Set master status.

        Sets the state machine master of the channel generator.

        Parameters:
            channel_index (int): The output channel for which to set the master setting.
                Specify -1 to set all channels.
            master_channel_index (int): The master channel index.

        Raises:
            DwfLibraryError: An error occurred while setting the value.
        """
        result = self.lib.FDwfAnalogOutMasterSet(self.hdwf, channel_index, master_channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def masterGet(self, channel_index: int) -> int:
        """Get master status.

        Parameters:
            channel_index (int): The output channel for which to get the status.

        Returns:
            int: The index of the master channel which the channel is configured to follow.

        Raises:
            DwfLibraryError: An error occurred while getting the value.
        """
        c_master_channel_index = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutMasterGet(self.hdwf, channel_index, c_master_channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        master_channel_index = c_master_channel_index.value
        return master_channel_index

    def modeSet(self, channel_index: int, mode: DwfAnalogOutMode) -> None:
        """Set analog output mode.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            mode (DwfAnalogOutMode): The mode.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutModeSet(self.hdwf, channel_index, mode.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def modeGet(self, channel_index: int) -> DwfAnalogOutMode:
        """Get analog output mode.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            DwfAnalogOutMode: The currently configured analog output mode.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_mode = typespec_ctypes.DwfAnalogOutMode()
        result = self.lib.FDwfAnalogOutModeGet(self.hdwf, channel_index, c_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        mode = DwfAnalogOutMode(c_mode.value)
        return mode

    def idleInfo(self, channel_index: int) -> List[DwfAnalogOutIdle]:
        """Get idle info.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            List[DwfAnalogOutIdle]: A list of options for the channel behavior when idle.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_idle_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutIdleInfo(self.hdwf, channel_index, c_idle_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        idle_bitset = c_idle_bitset.value
        idle_list = [idle for idle in DwfAnalogOutIdle if idle_bitset & (1 << idle.value)]
        return idle_list

    def idleSet(self, channel_index: int, idle: DwfAnalogOutIdle) -> None:
        """Set idle behavior.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            idle (DwfAnalogOutIdle): The idle setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutIdleSet(self.hdwf, channel_index, idle.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def idleGet(self, channel_index: int) -> DwfAnalogOutIdle:
        """Get idle behavior.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            DwfAnalogOutIdle: The idle behavior.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_idle = typespec_ctypes.DwfAnalogOutIdle()
        result = self.lib.FDwfAnalogOutIdleGet(self.hdwf, channel_index, c_idle)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        idle = DwfAnalogOutIdle(c_idle.value)
        return idle

    def runInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get run duration range, in seconds.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The range of allowed run-time, in seconds.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_secMin = typespec_ctypes.c_double()
        c_secMax = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutRunInfo(self.hdwf, channel_index, c_secMin, c_secMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secMin = c_secMin.value
        secMax = c_secMax.value
        return (secMin, secMax)

    def runSet(self, channel_index: int, run_duration: float) -> None:
        """Set run duration, in seconds.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            run_duration (float): The run duration, in seconds.
                Specify 0 for a run of indefinite length.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutRunSet(self.hdwf, channel_index, run_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def runGet(self, channel_index: int) -> float:
        """Get run-time, in seconds.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The currently active run setting, in seconds.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_run_duration = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutRunGet(self.hdwf, channel_index, c_run_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        run_duration = c_run_duration.value
        return run_duration

    def runStatus(self, channel_index: int) -> float:
        """Get run status.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The current run status, in seconds.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_secRun = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutRunStatus(self.hdwf, channel_index, c_secRun)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secRun = c_secRun.value
        return secRun

    def waitInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get wait info.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The range of configurable wait durations.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_secMin = typespec_ctypes.c_double()
        c_secMax = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutWaitInfo(self.hdwf, channel_index, c_secMin, c_secMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secMin = c_secMin.value
        secMax = c_secMax.value
        return (secMin, secMax)

    def waitSet(self, channel_index: int, wait_duration: float) -> None:
        """Set wait state duration, in seconds.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            wait_duration (float): The wait duration, in seconds.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutWaitSet(self.hdwf, channel_index, wait_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def waitGet(self, channel_index: int) -> float:
        """Get wait state duration in seconds.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The currently configured wait duration.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_wait_duration = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutWaitGet(self.hdwf, channel_index, c_wait_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        wait_duration = c_wait_duration.value
        return wait_duration

    def repeatInfo(self, channel_index: int) -> Tuple[int, int]:
        """Get repeat info.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[int, int]: The range of configurable repeat values.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_nMin = typespec_ctypes.c_int()
        c_nMax = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatInfo(self.hdwf, channel_index, c_nMin, c_nMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        nMin = c_nMin.value
        nMax = c_nMax.value
        return (nMin, nMax)

    def repeatSet(self, channel_index: int, repeat: int) -> None:
        """Set repeat setting.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            repeat (int): The repeat count. If 0, repeat indefinitely.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutRepeatSet(self.hdwf, channel_index, repeat)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def repeatGet(self, channel_index: int) -> int:
        """Get repeat setting.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            int: The currently configured repeat value. 0 means: repeat indefinitely.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_repeat = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatGet(self.hdwf, channel_index, c_repeat)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat = c_repeat.value
        return repeat

    def repeatStatus(self, channel_index: int) -> int:
        """Get repeat status.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            int: The current repeat value.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_repeat_status = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatStatus(self.hdwf, channel_index, c_repeat_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat_status = c_repeat_status.value
        return repeat_status

    def limitationInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get limitation info.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The range of limitation values that can be configured.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_limitation_min = typespec_ctypes.c_double()
        c_limitation_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutLimitationInfo(self.hdwf, channel_index, c_limitation_min, c_limitation_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        limitation_min = c_limitation_min.value
        limitation_max = c_limitation_max.value
        return (limitation_min, limitation_max)

    def limitationSet(self, channel_index: int, limitation: float) -> None:
        """Set limitation value.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            limitation (float): The limitation value, in [V] or [A].

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutLimitationSet(self.hdwf, channel_index, limitation)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def limitationGet(self, channel_index: int) -> float:
        """Get limitation value (in Volts or Amps).

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The currently configured limitation.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_limitation = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutLimitationGet(self.hdwf, channel_index, c_limitation)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        limitation = c_limitation.value
        return limitation

    def customAMFMEnableSet(self, channel_index: int, enable: bool) -> None:
        """Set custom AM/FM enable status.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            enable (bool): The custom AM/FM enable setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutCustomAMFMEnableSet(self.hdwf, channel_index, int(enable))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def customAMFMEnableGet(self, channel_index: int) -> bool:
        """Get custom AM/FM enable status.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            bool: The custom AM/FM enable state.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutCustomAMFMEnableGet(self.hdwf, channel_index, c_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable = bool(c_enable.value)
        return enable

    ####################################################################################################################
    #                                                                                                                  #
    #                                           PER-CHANNEL TRIGGER CONFIGURATION                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def triggerSourceInfo(self) -> List[DwfTriggerSource]:
        """Get analog out trigger source info.

        Warning:
            This method is obsolete. Use the generic |DwfDevice.triggerInfo:link| method instead.

        Returns:
            List[DwfTriggerSource]: The list of DwfTriggerSource values that can be configured.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_trigger_source_info_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutTriggerSourceInfo(self.hdwf, c_trigger_source_info_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source_info_bitset = c_trigger_source_info_bitset.value
        trigger_source_info_list = [trigger_source for trigger_source in DwfTriggerSource
                                    if trigger_source_info_bitset & (1 << trigger_source.value)]
        return trigger_source_info_list

    def triggerSourceSet(self, channel_index: int, trigger_source: DwfTriggerSource) -> None:
        """Set trigger source.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            trigger_source (DwfTriggerSource): The trigger source to be selected.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutTriggerSourceSet(
            self.hdwf,
            channel_index,
            trigger_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSourceGet(self, channel_index: int) -> DwfTriggerSource:
        """Get trigger source.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            DwfTriggerSource: The currently configured trigger source.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_trigger_source = typespec_ctypes.DwfTriggerSource()
        result = self.lib.FDwfAnalogOutTriggerSourceGet(self.hdwf, channel_index, c_trigger_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source = DwfTriggerSource(c_trigger_source.value)
        return trigger_source

    def triggerSlopeSet(self, channel_index: int, trigger_slope: DwfTriggerSlope) -> None:
        """Set trigger slope.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            trigger_slope (DwfTriggerSlope): The trigger slope to be selected.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutTriggerSlopeSet(
            self.hdwf,
            channel_index,
            trigger_slope.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSlopeGet(self, channel_index: int) -> DwfTriggerSlope:
        """Get trigger slope.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            DwfTriggerSlope: The currently configured trigger slope setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_trigger_slope = typespec_ctypes.DwfTriggerSlope()
        result = self.lib.FDwfAnalogOutTriggerSlopeGet(self.hdwf, channel_index, c_trigger_slope)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_slope = DwfTriggerSlope(c_trigger_slope.value)
        return trigger_slope

    def repeatTriggerSet(self, channel_index: int, repeat_trigger_flag: bool) -> None:
        """Set repeat trigger setting.

        This setting determines if a new trigger must precede all runs, or only the first one.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            repeat_trigger_flag (bool): The trigger repeat flag.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutRepeatTriggerSet(self.hdwf, channel_index, repeat_trigger_flag)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def repeatTriggerGet(self, channel_index: int) -> bool:
        """Get repeat trigger setting.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            bool: The currently configured repeat trigger setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_repeat_trigger_flag = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatTriggerGet(
            self.hdwf,
            channel_index,
            c_repeat_trigger_flag)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat_trigger_flag = bool(c_repeat_trigger_flag.value)
        return repeat_trigger_flag

    ####################################################################################################################
    #                                                                                                                  #
    #                                                  NODE ENUMERATION                                                #
    #                                                                                                                  #
    ####################################################################################################################

    def nodeInfo(self, channel_index: int) -> List[DwfAnalogOutNode]:
        """Get a list of valid node channel nodes.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            List[DwfAnalogOutNode]: The valid nodes for this channel.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_node_info_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodeInfo(self.hdwf, channel_index, c_node_info_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        node_info_bitset = c_node_info_bitset.value
        node_info_list = [node for node in DwfAnalogOutNode if node_info_bitset & (1 << node.value)]
        return node_info_list

    ####################################################################################################################
    #                                                                                                                  #
    #                                                  NODE CONFIGURATION                                              #
    #                                                                                                                  #
    ####################################################################################################################

    def nodeEnableSet(self, channel_index: int, node: DwfAnalogOutNode, enable: bool) -> None:
        """Enabled or disable a channel node.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            enable (bool): The enable flag.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodeEnableSet(self.hdwf, channel_index, node.value, enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeEnableGet(self, channel_index: int, node: DwfAnalogOutNode) -> bool:
        """"Get channel node enabled state.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            bool: The enable setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodeEnableGet(self.hdwf, channel_index, node.value, c_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable = bool(c_enable.value)
        return enable

    def nodeFunctionInfo(self, channel_index: int, node: DwfAnalogOutNode) -> List[DwfAnalogOutFunction]:
        """Get channel node waveform shape function info.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            List[DwfAnalogOutFunction]: The available node waveform shape functions.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_func_bitset = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfAnalogOutNodeFunctionInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_func_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        func_bitset = c_func_bitset.value
        func_list = [func for func in DwfAnalogOutFunction if func_bitset & (1 << func.value)]
        return func_list

    def nodeFunctionSet(self, channel_index: int, node: DwfAnalogOutNode, func: DwfAnalogOutFunction) -> None:
        """Set channel node waveform shape function.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            func (DwfAnalogOutFunction): The waveform shape function to be configured.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodeFunctionSet(self.hdwf, channel_index, node.value, func.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeFunctionGet(self, channel_index: int, node: DwfAnalogOutNode) -> DwfAnalogOutFunction:
        """Get channel node waveform shape function.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            DwfAnalogOutNode: The currently configured waveform shape function.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_func = typespec_ctypes.DwfAnalogOutFunction()
        result = self.lib.FDwfAnalogOutNodeFunctionGet(self.hdwf, channel_index, node.value, c_func)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        func = DwfAnalogOutFunction(c_func.value)
        return func

    def nodeFrequencyInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get channel node frequency info, in Hz.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            Tuple[float, float]: The range of valid frequencies, in Hz.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_frequency_min = typespec_ctypes.c_double()
        c_frequency_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeFrequencyInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_frequency_min,
            c_frequency_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        frequency_min = c_frequency_min.value
        frequency_max = c_frequency_max.value
        return (frequency_min, frequency_max)

    def nodeFrequencySet(self, channel_index: int, node: DwfAnalogOutNode, frequency: float) -> None:
        """Set channel node frequency, in Hz.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            frequency (float): The frequency, in Hz.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodeFrequencySet(
            self.hdwf,
            channel_index,
            node.value,
            frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeFrequencyGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get channel node frequency, in Hz.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            float: The currently configured frequency, in Hz.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_frequency = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeFrequencyGet(
            self.hdwf,
            channel_index,
            node.value,
            c_frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        frequency = c_frequency.value
        return frequency

    def nodeAmplitudeInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get channel node amplitude range, in Volts.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            Tuple[float, float]: The range of allowed amplitude values, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_amplitude_min = typespec_ctypes.c_double()
        c_amplitude_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeAmplitudeInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_amplitude_min,
            c_amplitude_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude_min = c_amplitude_min.value
        amplitude_max = c_amplitude_max.value
        return (amplitude_min, amplitude_max)

    def nodeAmplitudeSet(self, channel_index: int, node: DwfAnalogOutNode, amplitude: float) -> None:
        """Set channel node amplitude, in Volts.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            amplitude (float): The amplitude to be configured, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodeAmplitudeSet(
            self.hdwf,
            channel_index,
            node.value,
            amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeAmplitudeGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get channel node amplitude, in Volts.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            float: The currently configured channel amplitude, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_amplitude = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeAmplitudeGet(
            self.hdwf,
            channel_index,
            node.value,
            c_amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude = c_amplitude.value
        return amplitude

    def nodeOffsetInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get channel node valid offset range, in Volts.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            Tuple[float, float]: The range of valid node offsets, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_offset_min = typespec_ctypes.c_double()
        c_offset_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeOffsetInfo(self.hdwf, channel_index, node.value, c_offset_min, c_offset_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset_min = c_offset_min.value
        offset_max = c_offset_max.value
        return (offset_min, offset_max)

    def nodeOffsetSet(self, channel_index: int, node: DwfAnalogOutNode, offset: float) -> None:
        """Set channel node offset, in Volts.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            offset (float): The channel offset to be configured, in Volt.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodeOffsetSet(self.hdwf, channel_index, node.value, offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeOffsetGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get channel node offset, in Volts.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            float: The currently configured node offset.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_offset = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeOffsetGet(self.hdwf, channel_index, node.value, c_offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset = c_offset.value
        return offset

    def nodeSymmetryInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get channel node symmetry info.

        The *symmetry* value alters the waveform shape function of the node.

        The *symmetry* value ranges from 0 to 100 for most waveform shape functions, except for the
        :py:attr:`~pydwf.core.auxiliary.enum_types.DwfAnalogOutFunction.SinePower` function,
        where it ranges from -100 to 100.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            Tuple[float, float]: The range of valid symmetry settings.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_symmetry_min = typespec_ctypes.c_double()
        c_symmetry_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeSymmetryInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_symmetry_min,
            c_symmetry_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry_min = c_symmetry_min.value
        symmetry_max = c_symmetry_max.value
        return (symmetry_min, symmetry_max)

    def nodeSymmetrySet(self, channel_index: int, node: DwfAnalogOutNode, symmetry: float) -> None:
        """Set channel node symmetry value.

        The *symmetry* value alters the waveform shape function of the node.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            symmetry (float): The symmetry setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodeSymmetrySet(
            self.hdwf,
            channel_index,
            node.value,
            symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeSymmetryGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get channel node symmetry setting.

        The *symmetry* value alters the waveform shape function of the node.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            float: The currently configured channel node symmetry value.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_symmetry = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeSymmetryGet(
            self.hdwf,
            channel_index,
            node.value,
            c_symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry = c_symmetry.value
        return symmetry

    def nodePhaseInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get channel node phase range, in degrees.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            Tuple[float, float]: The range of valid channel node phase values, in degrees.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_phase_min = typespec_ctypes.c_double()
        c_phase_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodePhaseInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_phase_min,
            c_phase_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase_min = c_phase_min.value
        phase_max = c_phase_max.value
        return (phase_min, phase_max)

    def nodePhaseSet(self, channel_index: int, node: DwfAnalogOutNode, phase: float) -> None:
        """Set channel node phase, in degrees.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            phase (float): The phase setting, in degrees.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodePhaseSet(
            self.hdwf,
            channel_index,
            node.value,
            phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodePhaseGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get channel node phase, in degrees.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            float: The currently configured node phase value, in degrees.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_phase = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodePhaseGet(
            self.hdwf,
            channel_index,
            node.value,
            c_phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase = c_phase.value
        return phase

    ####################################################################################################################
    #                                                                                                                  #
    #                                                NODE DATA MANAGEMENT                                              #
    #                                                                                                                  #
    ####################################################################################################################

    def nodeDataInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get channel node data info, in samples.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            Tuple[float, float]: The range of valid values.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_samples_min = typespec_ctypes.c_int()
        c_samples_max = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodeDataInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_samples_min,
            c_samples_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samples_min = c_samples_min.value
        samples_max = c_samples_max.value
        return (samples_min, samples_max)

    def nodeDataSet(self, channel_index: int, node: DwfAnalogOutNode, data: np.ndarray) -> None:
        """Set channel node data.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            data (np.ndarray): The data.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """

        double_data = data.astype(np.float64)

        result = self.lib.FDwfAnalogOutNodeDataSet(
            self.hdwf,
            channel_index,
            node.value,
            double_data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(double_data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodePlayStatus(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[int, int, int]:
        """Get channel node play status.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.

        Returns:
            Tuple[int, int, int]: The status counts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_data_free = typespec_ctypes.c_int()
        c_data_lost = typespec_ctypes.c_int()
        c_data_corrupted = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodePlayStatus(
            self.hdwf,
            channel_index,
            node.value,
            c_data_free,
            c_data_lost,
            c_data_corrupted)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        data_free = c_data_free.value
        data_lost = c_data_lost.value
        data_corrupted = c_data_corrupted.value
        return (data_free, data_lost, data_corrupted)

    def nodePlayData(self, channel_index: int, node: DwfAnalogOutNode, data: np.ndarray) -> None:
        """Configure channel node play data.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            node (DwfAnalogOutNode): The channel node.
            data (np.ndarray): The data.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutNodePlayData(
            self.hdwf,
            channel_index,
            node.value,
            data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    ####################################################################################################################
    #                                                                                                                  #
    #                                            CARRIER CONFIGURATION (OBSOLETE)                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def enableSet(self, channel_index: int, enable: bool) -> None:
        """Enable or disable the specified |AnalogOut| channel.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeEnableSet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            enable (bool): The enable setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutEnableSet(self.hdwf, channel_index, enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def enableGet(self, channel_index: int) -> bool:
        """Get the current enable/disable status of the specified |AnalogOut| channel.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeEnableGet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            bool: The enable state of the channel.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutEnableGet(self.hdwf, channel_index, c_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable = bool(c_enable.value)
        return enable

    def functionInfo(self, channel_index: int) -> List[DwfAnalogOutFunction]:
        """Get |AnalogOut| channel waveform shape function info.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeFunctionInfo` method instead.

        Returns:
            List[DwfAnalogOutFunction]: The valid waveform shape functions.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_function_info_bitset = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfAnalogOutFunctionInfo(self.hdwf, channel_index, c_function_info_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        function_info_bitset = c_function_info_bitset.value
        function_info_list = [function_ for function_ in DwfAnalogOutFunction
                              if function_info_bitset & (1 << function_.value)]
        return function_info_list

    def functionSet(self, channel_index: int, func: DwfAnalogOutFunction) -> None:
        """Set |AnalogOut| channel waveform shape function.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeFunctionSet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            func (DwfAnalogOutFunction): The waveform shape function to use.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutFunctionSet(self.hdwf, channel_index, func.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def functionGet(self, channel_index: int) -> DwfAnalogOutFunction:
        """Get |AnalogOut| channel waveform shape function.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeFunctionGet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            List[DwfAnalogOutFunction]: The currently configured function.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_func = typespec_ctypes.DwfAnalogOutFunction()
        result = self.lib.FDwfAnalogOutFunctionGet(self.hdwf, channel_index, c_func)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        func = DwfAnalogOutFunction(c_func.value)
        return func

    def frequencyInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get |AnalogOut| channel valid frequency range, in Hz.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeFrequencyInfo` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The valid frequency range, in Hz.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_hzMin = typespec_ctypes.c_double()
        c_hzMax = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutFrequencyInfo(self.hdwf, channel_index, c_hzMin, c_hzMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        hzMin = c_hzMin.value
        hzMax = c_hzMax.value
        return (hzMin, hzMax)

    def frequencySet(self, channel_index: int, frequency: float) -> None:
        """Set |AnalogOut| channel frequency, in Hz.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeFrequencySet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            frequency (float): The frequency to use.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutFrequencySet(self.hdwf, channel_index, frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def frequencyGet(self, channel_index: int) -> float:
        """Get |AnalogOut| channel frequency, in Hz.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeFrequencyGet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The currently configured frequency, in Hz.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_hzFrequency = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutFrequencyGet(self.hdwf, channel_index, c_hzFrequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        hzFrequency = c_hzFrequency.value
        return hzFrequency

    def amplitudeInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get |AnalogOut| channel amplitude range info.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeAmplitudeInfo` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The range of valid amplitudes, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_amplitude_min = typespec_ctypes.c_double()
        c_amplitude_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutAmplitudeInfo(self.hdwf, channel_index, c_amplitude_min, c_amplitude_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude_min = c_amplitude_min.value
        amplitude_max = c_amplitude_max.value
        return (amplitude_min, amplitude_max)

    def amplitudeSet(self, channel_index: int, amplitude: float) -> None:
        """Set |AnalogOut| channel amplitude.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeAmplitudeSet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            amplitude (float): The amplitude, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutAmplitudeSet(self.hdwf, channel_index, amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def amplitudeGet(self, channel_index: int) -> float:
        """Get |AnalogOut| channel amplitude.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeAmplitudeGet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The currently configured amplitude, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_amplitude = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutAmplitudeGet(self.hdwf, channel_index, c_amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude = c_amplitude.value
        return amplitude

    def offsetInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get |AnalogOut| channel offset range info, in Volts.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeOffsetInfo` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The valid range of offset values, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_offset_min = typespec_ctypes.c_double()
        c_offset_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutOffsetInfo(self.hdwf, channel_index, c_offset_min, c_offset_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset_min = c_offset_min.value
        offset_max = c_offset_max.value
        return (offset_min, offset_max)

    def offsetSet(self, channel_index: int, offset: float) -> None:
        """Set |AnalogOut| channel offset, in Volts.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeOffsetSet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            offset (float): The channel offset, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutOffsetSet(self.hdwf, channel_index, offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def offsetGet(self, channel_index: int) -> float:
        """Get |AnalogOut| channel offset, in Volts.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeOffsetGet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The valid offset value, in Volts.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_offset = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutOffsetGet(self.hdwf, channel_index, c_offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset = c_offset.value
        return offset

    def symmetryInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get |AnalogOut| channel symmetry setting range.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeSymmetryInfo` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The range of valid symmetry settings.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_symmetry_min = typespec_ctypes.c_double()
        c_symmetry_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutSymmetryInfo(self.hdwf, channel_index, c_symmetry_min, c_symmetry_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry_min = c_symmetry_min.value
        symmetry_max = c_symmetry_max.value
        return (symmetry_min, symmetry_max)

    def symmetrySet(self, channel_index: int, symmetry: float) -> None:
        """Set |AnalogOut| channel symmetry setting.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeSymmetrySet` method instead.

        Parameters:
            channel_index (int):  The |AnalogOut| channel.
            symmetry (float): The channel symmetry setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutSymmetrySet(self.hdwf, channel_index, symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def symmetryGet(self, channel_index: int) -> float:
        """Get |AnalogOut| channel symmetry setting.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeSymmetryGet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The currently configured symmetry setting.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_symmetry = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutSymmetryGet(self.hdwf, channel_index, c_symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry = c_symmetry.value
        return symmetry

    def phaseInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get |AnalogOut| channel phase range, in degrees.

        Warning:
            This method is obsolete. Use the :py:meth:`nodePhaseInfo` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[float, float]: The range of valid phase values, in degrees.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_phase_min = typespec_ctypes.c_double()
        c_phase_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutPhaseInfo(self.hdwf, channel_index, c_phase_min, c_phase_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase_min = c_phase_min.value
        phase_max = c_phase_max.value
        return (phase_min, phase_max)

    def phaseSet(self, channel_index: int, phase: float) -> None:
        """Set |AnalogOut| channel phase, in degrees.

        Warning:
            This method is obsolete. Use the :py:meth:`nodePhaseSet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            phase (float): The phase setting, in degrees.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfAnalogOutPhaseSet(self.hdwf, channel_index, phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def phaseGet(self, channel_index: int) -> float:
        """Get |AnalogOut| channel phase, in degrees.

        Warning:
            This method is obsolete. Use the :py:meth:`nodePhaseGet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            float: The currently configured phase, in degrees.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_phase = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutPhaseGet(self.hdwf, channel_index, c_phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase = c_phase.value
        return phase

    ####################################################################################################################
    #                                                                                                                  #
    #                                          CARRIER DATA MANAGEMENT (OBSOLETE)                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def dataInfo(self, channel_index: int) -> Tuple[int, int]:
        """Get data buffer info.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeDataInfo` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[int, int]: The data range.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_num_samples_min = typespec_ctypes.c_int()
        c_num_samples_max = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutDataInfo(self.hdwf, channel_index, c_num_samples_min, c_num_samples_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        num_samples_min = c_num_samples_min.value
        num_samples_max = c_num_samples_max.value
        return (num_samples_min, num_samples_max)

    def dataSet(self, channel_index: int, data: np.ndarray) -> None:
        """Set carrier data.

        Warning:
            This method is obsolete. Use the :py:meth:`nodeDataSet` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            data (np.ndarray): The data.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """

        double_data = data.astype(np.float64)

        result = self.lib.FDwfAnalogOutDataSet(
            self.hdwf,
            channel_index,
            double_data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(double_data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def playStatus(self, channel_index: int) -> Tuple[int, int, int]:
        """Get play status.

        Warning:
            This method is obsolete. Use the :py:meth:`nodePlayStatus` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.

        Returns:
            Tuple[int, int, int]: The play status.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_data_free = typespec_ctypes.c_int()
        c_data_lost = typespec_ctypes.c_int()
        c_data_corrupted = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutPlayStatus(
            self.hdwf,
            channel_index,
            c_data_free,
            c_data_lost,
            c_data_corrupted)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        data_free = c_data_free.value
        data_lost = c_data_lost.value
        data_corrupted = c_data_corrupted.value
        return (data_free, data_lost, data_corrupted)

    def playData(self, channel_index: int, data: np.ndarray) -> None:
        """Play data.

        Warning:
            This method is obsolete. Use the :py:meth:`nodePlayData` method instead.

        Parameters:
            channel_index (int): The |AnalogOut| channel.
            data (np.ndarray): The data.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """

        double_data = data.astype(np.float64)

        result = self.lib.FDwfAnalogOutPlayData(
            self.hdwf,
            channel_index,
            double_data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(double_data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
