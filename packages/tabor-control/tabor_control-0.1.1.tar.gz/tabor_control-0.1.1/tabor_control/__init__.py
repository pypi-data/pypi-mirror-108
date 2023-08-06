"""
    tabor_control - Interact with arbitrary waveform generators from Tabor-Electronics Ltd.
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

    Partially derived from pyte16 by 2016 Tabor-Electronics Ltd. distributed under GPL 2
    http://www.taborelec.com/
"""

from typing import Sequence, Tuple, cast
import socket
import enum
import warnings
import struct

import numpy as np

from pyvisa import ResourceManager
from pyvisa.resources import Resource, MessageBasedResource
import pyvisa.constants as vc


__version__ = "0.1.1"


TABLE_ENTRY_FORMAT = struct.Struct('< L H B x')
TABLE_ENTRY_DTYPE = np.dtype([('repeats', '<u4'), ('segment_no', '<u2'), ('jump_flag', '|u1')], align=True)
assert TABLE_ENTRY_FORMAT.size == TABLE_ENTRY_DTYPE.itemsize == 8
assert [TABLE_ENTRY_FORMAT.unpack(bytes(range(1, 9)))] == np.frombuffer(bytes(range(1, 9)), dtype=TABLE_ENTRY_DTYPE).tolist()


class ParanoiaLevel(enum.Enum):
    NONE = 0
    OPC = 1
    SYST_ERR = 2


def init_vi_inst(vi: Resource,
                 timeout_msec: int = 30000,
                 read_buff_size_bytes: int = 4096,
                 write_buff_size_bytes: int = 4096):
    """Initialize the given Instrument VISA Session"""

    vi.timeout = int(timeout_msec)
    vi.visalib.set_buffer(vi.session, vc.VI_READ_BUF, int(read_buff_size_bytes))
    vi.visalib.set_buffer(vi.session, vc.VI_WRITE_BUF, int(write_buff_size_bytes))
    vi.read_termination = '\n'
    vi.write_termination = '\n'
    intf_type = vi.get_visa_attribute(vc.VI_ATTR_INTF_TYPE)
    if intf_type in (vc.VI_INTF_USB, vc.VI_INTF_GPIB, vc.VI_INTF_TCPIP, vc.VI_INTF_ASRL):
        vi.set_visa_attribute(vc.VI_ATTR_WR_BUF_OPER_MODE, vc.VI_FLUSH_ON_ACCESS)
        vi.set_visa_attribute(vc.VI_ATTR_RD_BUF_OPER_MODE, vc.VI_FLUSH_ON_ACCESS)
        if intf_type == vc.VI_INTF_TCPIP:
            vi.set_visa_attribute(vc.VI_ATTR_TERMCHAR_EN, vc.VI_TRUE)  # vc.VI_FALSE
        elif intf_type == vc.VI_INTF_ASRL:
            vi.set_visa_attribute(vc.VI_ATTR_ASRL_BAUD, 115200)
            vi.set_visa_attribute(vc.VI_ATTR_ASRL_END_OUT, 0)
            vi.set_visa_attribute(vc.VI_ATTR_ASRL_END_IN, 2)
    vi.clear()


def _validate_syst_err_answer(query_str, syst_err: str):
    try:
        err_num, err_txt = syst_err.split(',')
        err_num = int(err_num)
    except (ValueError, TypeError):
        warnings.warn(IllformedAnswer(query_str, syst_err))
    else:
        if err_num != 0:
            warnings.warn(SystErr(query_str, err_num, err_txt))


def open_session(resource_name: str, resource_manager: ResourceManager = None, extra_init=True) -> MessageBasedResource:
    """Open VISA Session (optionally prompt for resource name).

    The `resource_name` can be either:
        1. Full VISA Resource-Name (e.g. 'TCPIP::192.168.0.170::5025::SOCKET')
        2. IP-Address (e.g. '192.168.0.170')
    """

    if resource_manager is None:
        resource_manager = ResourceManager()

    try:
        packed_ip = socket.inet_aton(resource_name)
    except OSError:
        pass
    else:
        resource_name = f"TCPIP::{socket.inet_ntoa(packed_ip)}::5025::SOCKET"

    vi = resource_manager.open_resource(resource_name)
    if extra_init:
        init_vi_inst(vi)

    return vi


def send_cmd(vi: MessageBasedResource, cmd_str: str, paranoia_level: ParanoiaLevel = ParanoiaLevel.OPC):
    """

    Args:
        vi:
        cmd_str:
        paranoia_level:

    Raises:
        ValueError: If '?' is in cmd_str

    Returns:

    """
    paranoia_level = ParanoiaLevel(paranoia_level)
    if '?' in cmd_str:
        raise ValueError("? in command string. Use send_query.")
    cmd_str = cmd_str.rstrip()
    cmd_list = [cmd_str] if cmd_str else []

    if paranoia_level == ParanoiaLevel.NONE:
        vi.write(cmd_str)

    elif paranoia_level == ParanoiaLevel.OPC:
        cmd_list.append('*OPC?')
        query = ';'.join(cmd_list)
        opc = vi.query(query)

        if opc != '1':
            warnings.warn(OPCWarning(query, opc))

    elif paranoia_level == ParanoiaLevel.SYST_ERR:
        cmd_list.append(':SYST:ERR?')
        query = ';'.join(cmd_list)
        syst_err = vi.query(query)
        _validate_syst_err_answer(query, syst_err)

    else:
        raise ValueError("Unhandled paranoia level")


def _pre_download_binary_data(vi, bin_dat_size=None):
    '''Pre-Download Binary-Data

    :param vi: `pyvisa` instrument.
    :param bin_dat_size: the binary-data-size in bytes (can be omitted)
    :returns: the max write-chunk size (in bytes) and the original time-out (in msec)
    '''
    orig_timeout = vi.timeout

    max_chunk_size = vi.write_buff_size if hasattr(vi, 'write_buff_size') else 4096

    try:
        intf_type = vi.get_visa_attribute(vc.VI_ATTR_INTF_TYPE)
        if intf_type == vc.VI_INTF_GPIB:
            _ = vi.write("*OPC?")
            for _ in range(2000):
                status_byte = vi.stb
                if (status_byte & 0x10) == 0x10:
                    break
            _ = vi.read()
            max_chunk_size = min(max_chunk_size, 30000)
            if bin_dat_size is not None and orig_timeout < bin_dat_size / 20:
                vi.timeout = int(bin_dat_size / 20)
        else:
            max_chunk_size = min(max_chunk_size, 256000)
    except:
        pass

    return orig_timeout, max_chunk_size


def _write_binary_data(vi: MessageBasedResource, prefix: str, data: bytes, paranoia_level: ParanoiaLevel):
    paranoia_level = ParanoiaLevel(paranoia_level)

    assert isinstance(data, bytes)

    data_len = f"{len(data)}"
    header = f'{prefix}#{len(data_len)}{data_len}'.encode()

    written = vi.write_raw(header)
    if written != len(header):
        raise RuntimeError("Binary header not completely written. Probably unrecoverable error.")

    # TODO: do we need manual chunked writing here?
    written = vi.write_raw(data)
    if written != len(data):
        raise RuntimeError("Binary data not completely written. Probably unrecoverable error.")

    if paranoia_level == ParanoiaLevel.NONE:
        pass

    elif paranoia_level == ParanoiaLevel.OPC:
        opc = vi.query('*OPC?')
        if opc != '1':
            warnings.warn(OPCWarning('*OPC?', opc))

    else:
        query = ':SYST:ERR?'
        syst_err = vi.query(query)
        _validate_syst_err_answer(query, syst_err)


def write_waveform_data(vi: MessageBasedResource, data: np.ndarray, paranoia_level: ParanoiaLevel = ParanoiaLevel.OPC):
    if not (isinstance(data, np.ndarray) and data.dtype.char != np.uint16):
        raise TypeError("Must be a numpy array of unsigned 16 bit integers")

    if not (data.ndim == 1 and data.size >= 192 and data.size % 16 == 0):
        raise ValueError("Data must have the correct dimensions")

    b_data = data.tobytes()
    _write_binary_data(vi, ':TRAC:DATA', b_data, paranoia_level)


def write_segment_lengths(vi, segment_lengths: np.ndarray, paranoia_level: ParanoiaLevel = ParanoiaLevel.OPC):
    if not (isinstance(segment_lengths, np.ndarray) and segment_lengths.dtype == np.uint32):
        raise TypeError("Segment lengths must be a numpy array of unsigned 32 bit integers")

    if not (segment_lengths.ndim == 1):
        raise ValueError("Segment lengths must be a one dimensional array.")

    b_data = segment_lengths.tobytes()
    _write_binary_data(vi, ':SEGM:DATA', b_data, paranoia_level)


def _write_table(vi: MessageBasedResource, prefix: str, table: Sequence[Tuple[int, int, int]],
                 paranoia_level: ParanoiaLevel):
    table_entry_format = TABLE_ENTRY_FORMAT
    entry_size = table_entry_format.size

    table_len = len(table)
    b_data = bytearray(table_len * entry_size)

    for pos, (repeats, seg_nb, jump_flag) in enumerate(table):
        table_entry_format.pack_into(b_data, pos * entry_size, repeats, seg_nb, jump_flag)

    _write_binary_data(vi, prefix, data=bytes(b_data), paranoia_level=paranoia_level)


def _read_table(vi: MessageBasedResource, query_cmd: str) -> np.ndarray:
    data_raw = cast(np.ndarray, vi.query_binary_values(query_cmd, datatype='B', container=np.array))
    return data_raw.view(TABLE_ENTRY_DTYPE)


def write_sequencer_table(vi, sequencer_table: Sequence[Tuple[int, int, int]],
                          paranoia_level: ParanoiaLevel = ParanoiaLevel.OPC):
    """Write Sequencer-Table to Instrument

    The sequencer-table, `seq_table`, is a list of 3-tuples
    of the form: (<repeats>, <segment no.>, <jump-flag>)

    Example:
        >>> # Create Sequencer-Table:
        >>> repeats = [ 1, 1, 100, 4, 1 ]
        >>> seg_nb = [ 2, 3, 5, 1, 4 ]
        >>> jump = [ 0, 0, 1, 0, 0 ]
        >>> my_sequencer_table = zip(repeats, seg_nb, jump)
        >>>
        >>> # Select sequence no. 1:
        >>>  _ = vi.ask(':SEQ:SELect 1; *OPC?')
        >>>
        >>> # Download the sequencer-table:
        >>> tabor_control.write_sequencer_table(vi, sequencer_table)
    """
    _write_table(vi, ':SEQ:DATA', sequencer_table, paranoia_level=paranoia_level)


def read_sequencer_table(vi: MessageBasedResource) -> np.ndarray:
    return _read_table(vi, ':SEQ:DATA?')


def write_advanced_sequencer_table(vi, advanced_sequencer_table: Sequence[Tuple[int, int, int]],
                                   paranoia_level: ParanoiaLevel = ParanoiaLevel.OPC):
    """Download Advanced-Sequencer-Table to Instrument

    The advanced-sequencer-table, `adv_seq_table`, is a list of 3-tuples
    of the form: (<repeats>, <sequence no.>, <jump-flag>)
    """

    _write_table(vi, ':ASEQ:DATA', table=advanced_sequencer_table, paranoia_level=paranoia_level)


def read_advanced_sequencer_table(vi: MessageBasedResource) -> np.ndarray:
    return _read_table(vi, ':ASEQ:DATA?')


class TaborWarning(RuntimeWarning):
    pass


class OPCWarning(TaborWarning):
    """Warning emitted if answer to OPC is not '1'"""

    def __init__(self, query_str, answer):
        super().__init__(query_str, answer)

    @property
    def query_str(self):
        return self.args[0]

    @property
    def answer(self):
        return self.args[1]

    def __str__(self):
        return f"Received {self.answer!r} as an answer on {self.query_str!r} instead of '1'"


class SystErr(TaborWarning):
    """Emitted if :SYST:ERR? returns a non 0 status code"""
    def __init__(self, query_str, status_code, error_description):
        super().__init__(query_str, status_code, error_description)

    @property
    def query_str(self):
        return self.args[0]

    @property
    def status_code(self) -> int:
        return self.args[1]

    @property
    def error_description(self) -> int:
        return self.args[2]

    def __str__(self):
        return f"Received {self.status_code}, {self.error_description} as an answer on {self.query_str!r} instead of '0, \"No Error\"'"


class IllformedAnswer(TaborWarning):
    """Received an answer in an unexpected format."""
    def __init__(self, query_str, answer):
        super().__init__(query_str, answer)


warnings.simplefilter("error", OPCWarning)
warnings.simplefilter("error", IllformedAnswer)
