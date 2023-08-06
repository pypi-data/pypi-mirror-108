"""This module provides an object oriented abstraction.

    Copyright (C) 2021 Simon Humpohl

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Partially derived from teawg by 2016 Tabor-Electronics Ltd. distributed under GPL 2
    http://www.taborelec.com/
"""
from typing import Optional, Sequence, Tuple

from packaging import version
import numpy as np

import pyvisa.util
from pyvisa.resources import MessageBasedResource
import pyvisa.constants as vc

import tabor_control
from tabor_control import ParanoiaLevel
from tabor_control.util import get_device_properties, DeviceProperties


class TEWXAwg:
    """Tabor-Electronics WX-Instrument Controller"""

    def __init__(self, visa_instr: MessageBasedResource, paranoia_level: ParanoiaLevel):
        self._visa_inst = visa_instr
        self._dev_props: Optional[DeviceProperties] = None
        self._resource_name = None
        self._paranoia_level = ParanoiaLevel(paranoia_level)
        self._simulator_read_workaround = None

        if visa_instr is not None:
            self._resource_name = visa_instr.resource_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def supports_basic_reading(self) -> bool:
        return self.model_name.lower() in ('wx2184', 'wx2184c', 'wx1284', 'wx1284c') and self.fw_ver >= version.Version('3')

    def open(self, resource_name=None):
        self.close()

        if resource_name is not None:
            self._resource_name = resource_name

        if self._resource_name is not None:
            self._visa_inst = tabor_control.open_session(self._resource_name, extra_init=True)

    def close(self):
        """Close Connection and forget saved properties"""
        if self._visa_inst is not None:
            try:
                self._visa_inst.close()
            except pyvisa.errors.Error:
                pass
        self._visa_inst = None
        self._dev_props = None
        self._simulator_read_workaround = None

    @property
    def visa_inst(self) -> MessageBasedResource:
        return self._visa_inst

    @property
    def resource_name(self):
        return self._resource_name

    @property
    def dev_properties(self) -> DeviceProperties:
        '''Get dictionary of the device properties '''
        if self._dev_props is None:
            idn = self._visa_inst.query('*IDN?')
            opt = self._visa_inst.query('*OPT?')

            self._dev_props = get_device_properties(idn, opt)
        return self._dev_props

    @property
    def model_name(self) -> str:
        return self._dev_props.model_name

    @property
    def fw_ver(self) -> version.Version:
        """Firmware version"""
        return self._dev_props.fw_ver

    @property
    def is_simulator(self) -> bool:
        """True if IP address is localhost"""
        if self.visa_inst and self.visa_inst.interface_type == vc.InterfaceType.tcpip:
            return '127.0.0.1' in self.visa_inst.resource_name or 'localhost' in self.visa_inst.resource_name
        return False

    @property
    def paranoia_level(self) -> ParanoiaLevel:
        """Get the (default) paranoia-level"""
        return self._paranoia_level

    @paranoia_level.setter
    def paranoia_level(self, value: ParanoiaLevel):
        """Set the (default) paranoia-level"""
        self._paranoia_level = ParanoiaLevel(value)

    def send_cmd(self, cmd_str: str, paranoia_level=None):
        '''Send the given command to the instrument

        :param cmd_str: the command string (SCPI statement).
        :param paranoia_level: the paranoia-level (overrides the default one)
        '''
        if paranoia_level is None:
            paranoia_level = self._paranoia_level
        else:
            paranoia_level = ParanoiaLevel(paranoia_level)

        if self._simulator_read_workaround is None:
            workaround = self.is_simulator
        else:
            workaround = self._simulator_read_workaround

        tabor_control.send_cmd(self._visa_inst, cmd_str, paranoia_level)
        if workaround and paranoia_level == ParanoiaLevel.NONE:
            empty_str = self._visa_inst.read()
            assert empty_str == '', ("This workaround expects an empty response after each command that is not a query."
                                     " The simulator does this in some versions. It is controlled by the attribute "
                                     "_simulator_read_workaround. Actual response was: %r" % empty_str)

    def send_query(self, query_str) -> str:
        """Send the given query to the instrument and read the response

        :param query_str: the query string (SCPI statement).
        :returns: the instrument's response."""
        return self._visa_inst.query(query_str)

    def write_segment_data(self, waveform_data: np.ndarray, paranoia_level=None):
        if paranoia_level is None:
            paranoia_level = self._paranoia_level
        tabor_control.write_waveform_data(self._visa_inst, waveform_data, paranoia_level)

    def read_segment_data(self) -> np.ndarray:
        """Read data of active segment.

        Raises:
            ReadNotSupported if unsupported

        Returns:

        """
        if self.supports_basic_reading():
            dat = self._visa_inst.query_binary_values(':TRAC:DATA?', datatype='H', container=np.array)
            return np.asarray(dat, dtype=np.uint16)
        else:
            raise ReadNotSupported(self.dev_properties)

    def write_segment_lengths(self, segment_lengths: np.ndarray, paranoia_level: ParanoiaLevel = None):
        if paranoia_level is None:
            paranoia_level = self.paranoia_level
        tabor_control.write_segment_lengths(self._visa_inst,
                                            segment_lengths=segment_lengths,
                                            paranoia_level=paranoia_level)

    def write_sequencer_table(self, sequencer_table: Sequence[Tuple[int, int, int]],
                              paranoia_level: ParanoiaLevel = None):
        if paranoia_level is None:
            paranoia_level = self.paranoia_level
        tabor_control.write_sequencer_table(self._visa_inst, sequencer_table, paranoia_level)

    def read_sequencer_table(self):
        """Read the active sequencer table (of the active part).

        Returns:
            numpy structured array with dtype tabor_control.TABLE_ENTRY_DTYPE
        """
        if not self.supports_basic_reading():
            raise ReadNotSupported(self.dev_properties)
        else:
            return tabor_control.read_sequencer_table(self._visa_inst)

    def write_advanced_sequencer_table(self, advanced_sequencer_table: Sequence[Tuple[int, int, int]],
                                       paranoia_level: ParanoiaLevel = None):
        if paranoia_level is None:
            paranoia_level = self.paranoia_level
        tabor_control.write_advanced_sequencer_table(self._visa_inst, advanced_sequencer_table, paranoia_level)

    def read_advanced_sequencer_table(self) -> np.ndarray:
        """Read the advanced sequencer table (of the active part).

        Raises:
            ReadNotSupported if the device cannot be read from
        Returns:
            numpy structured array with dtype tabor_control.TABLE_ENTRY_DTYPE
        """
        if not self.supports_basic_reading():
            raise ReadNotSupported(self.dev_properties)
        else:
            return tabor_control.read_advanced_sequencer_table(self._visa_inst)


class ReadNotSupported(RuntimeError):
    """Raised if a read is attempted on a device that does not support it"""
