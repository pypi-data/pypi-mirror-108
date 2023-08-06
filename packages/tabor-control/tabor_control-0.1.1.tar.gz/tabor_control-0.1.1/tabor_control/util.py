"""Utility functionality for tabor awg interaction.

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

import socket
import logging
import dataclasses
from packaging import version

from typing import Iterator, Optional, Mapping, Tuple

BROADCAST = "255.255.255.255"
IDN_TEMPLATE = "{manuf_name},{model_name},{serial_nb},{fw_ver}"

module_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DeviceProperties:
    model_name: str
    fw_ver: version.Version
    serial_num: str

    num_parts: int        # number of instrument parts
    chan_per_part: int    # number of channels per part
    seg_quantum: int       # segment-length quantum
    min_seg_len: int      # minimal segment length
    max_arb_mem: int      # maximal arbitrary-memory (points per channel)
    min_dac_val: int         # minimal DAC value
    max_dac_val: int   # maximal DAC value
    max_num_segs: int     # maximal number of segments
    max_seq_len: int   # maximal sequencer-table length (# rows)
    min_seq_len: int         # minimal sequencer-table length (# rows)
    max_num_seq: int      # maximal number of sequencer-table
    max_aseq_len: int # maximal advanced-sequencer table length
    min_aseq_len: int  # minimal advanced-sequencer table length
    min_sclk: float      # minimal sampling-rate (samples/seconds)
    max_sclk: float   # maximal sampling-rate (samples/seconds)
    digital_support: bool   # is digital-wave supported?

    def as_dict(self):
        return dataclasses.asdict(self)


# WX2184 Properties
_wx2184_properties = {
    'model_name'      : 'WX2184', # the model name
    'fw_ver'          : 0.0,      # the firmware version
    'serial_num'      : '0'*9,    # serial number
    'num_parts'       : 2,        # number of instrument parts
    'chan_per_part'   : 2,        # number of channels per part
    'seg_quantum'     : 16,       # segment-length quantum
    'min_seg_len'     : 192,      # minimal segment length
    'max_arb_mem'     : 32 * 10**6,     # maximal arbitrary-memory (points per channel)
    'min_dac_val'     : 0,        # minimal DAC value
    'max_dac_val'     : 2**14-1,  # maximal DAC value
    'max_num_segs'    : 32E+3,    # maximal number of segments
    'max_seq_len'     : 48*1024,  # maximal sequencer-table length (# rows)
    'min_seq_len'     : 3,        # minimal sequencer-table length (# rows)
    'max_num_seq'     : 1000,     # maximal number of sequencer-table
    'max_aseq_len'    : 48*1024-2,# maximal advanced-sequencer table length
    'min_aseq_len'    : 3,        # minimal advanced-sequencer table length
    'min_sclk'        : 75e6,     # minimal sampling-rate (samples/seconds)
    'max_sclk'        : 2300e6,   # maximal sampling-rate (samples/seconds)
    'digital_support' : False,    # is digital-wave supported?
    }

# WX1284 Definitions
_wx1284_properties = {
    'model_name'      : 'WX1284', # the model name
    'fw_ver'          : 0.0,      # the firmware version
    'serial_num'      : '0'*9,    # serial number
    'num_parts'       : 2,        # number of instrument parts
    'chan_per_part'   : 2,        # number of channels per part
    'seg_quantum'     : 16,       # segment-length quantum
    'min_seg_len'     : 192,      # minimal segment length
    'max_arb_mem'     : 32 * 10**6,     # maximal arbitrary-memory (points per channel)
    'min_dac_val'     : 0,        # minimal DAC value
    'max_dac_val'     : 2**14-1,  # maximal DAC value
    'max_num_segs'    : 32 * 10**3,    # maximal number of segments
    'max_seq_len'     : 48*1024,  # maximal sequencer-table length (# rows)
    'min_seq_len'     : 3,        # minimal sequencer-table length (# rows)
    'max_num_seq'     : 1000,     # maximal number of sequencer-table
    'max_aseq_len'    : 48*1024-2,# maximal advanced-sequencer table length
    'min_aseq_len'    : 3,        # minimal advanced-sequencer table length
    'min_sclk'        : 75e6,     # minimal sampling-rate (samples/seconds)
    'max_sclk'        : 1250e6,   # maximal sampling-rate (samples/seconds)
    'digital_support' : False,    # is digital-wave supported?
    }

# WX2182C Definitions
_wx2182C_properties = {
    'model_name'      : 'WX2182C',# the model name
    'fw_ver'          : 0.0,      # the firmware version
    'serial_num'      : '0'*9,    # serial number
    'num_parts'       : 2,        # number of instrument parts
    'chan_per_part'   : 1,        # number of channels per part
    'seg_quantum'     : 16,       # segment-length quantum
    'min_seg_len'     : 192,      # minimal segment length
    'max_arb_mem'     : 32 * 10**6,     # maximal arbitrary-memory (points per channel)
    'min_dac_val'     : 0,        # minimal DAC value
    'max_dac_val'     : 2**14-1,  # maximal DAC value
    'max_num_segs'    : 32 * 10**3,    # maximal number of segments
    'max_seq_len'     : 48*1024,  # maximal sequencer-table length (# rows)
    'min_seq_len'     : 3,        # minimal sequencer-table length (# rows)
    'max_num_seq'     : 1000,     # maximal number of sequencer-table
    'max_aseq_len'    : 1000,     # maximal advanced-sequencer table length
    'min_aseq_len'    : 3,        # minimal advanced-sequencer table length
    'min_sclk'        : 10e6,     # minimal sampling-rate (samples/seconds)
    'max_sclk'        : 2.3e9,    # maximal sampling-rate (samples/seconds)
    'digital_support' : False,    # is digital-wave supported?
    }

# WX1282C Definitions
_wx1282C_properties = {
    'model_name'      : 'WX1282C',# the model name
    'fw_ver'          : 0.0,      # the firmware version
    'serial_num'      : '0'*9,    # serial number
    'num_parts'       : 2,        # number of instrument parts
    'chan_per_part'   : 1,        # number of channels per part
    'seg_quantum'     : 16,       # segment-length quantum
    'min_seg_len'     : 192,      # minimal segment length
    'max_arb_mem'     : 32 * 10**6,     # maximal arbitrary-memory (points per channel)
    'min_dac_val'     : 0,        # minimal DAC value
    'max_dac_val'     : 2**14-1,  # maximal DAC value
    'max_num_segs'    : 32 * 10**3,    # maximal number of segments
    'max_seq_len'     : 48*1024,  # maximal sequencer-table length (# rows)
    'min_seq_len'     : 3,        # minimal sequencer-table length (# rows)
    'max_num_seq'     : 1000,     # maximal number of sequencer-table
    'max_aseq_len'    : 1000,     # maximal advanced-sequencer table length
    'min_aseq_len'    : 3,        # minimal advanced-sequencer table length
    'min_sclk'        : 10e6,     # minimal sampling-rate (samples/seconds)
    'max_sclk'        : 1.25e9,   # maximal sampling-rate (samples/seconds)
    'digital_support' : False,    # is digital-wave supported?
    }

# dictionary of supported-models' properties
model_properties_dict = {
    'WX2184'  : _wx2184_properties,
    'WX2184C' : _wx2184_properties,
    'WX1284'  : _wx2184_properties,
    'WX1284C' : _wx2184_properties,
    'WX2182C' : _wx2182C_properties,
    'WX1282C' : _wx1282C_properties,
    }

# Maps SCPI data commands to file-type IDs
# (used by send_load_file_cmd())
_file_types_dict = {
    # Analog Wave Data:
    'TRACE:DATA' : 1,
    'TRAC:DATA'  : 1,
    'TRACE'      : 1,
    'TRAC'       : 1,

    # Digital Wave Data:
    'DIGITAL:DATA' : 2,
    'DIG:DATA'     : 2,

    # Segment Lengths List:
    'SEGMENT:DATA' : 3,
    'SEGM:DATA'    : 3,
    'SEGMENT'      : 3,
    'SEGM'         : 3,

    # Sequencer-Table (of the active sequencer):
    'SEQUENCE:DATA' : 4,
    'SEQ:DATA'      : 4,
    'SEQUENCE'      : 4,
    'SEQ'           : 4,

    # Sequencer-Lines (of all sequencers):
    'SEQUENCE:DATA:ALL' : 5,
    'SEQ:DATA:ALL'      : 5,
    'SEQUENCE:ALL'      : 5,
    'SEQ:ALL'           : 5,

    # Advanced-Sequencer Table:
    'ASEQUENCE:DATA' : 6,
    'ASEQ:DATA'      : 6,
    'ASEQUENCE'      : 6,
    'ASEQ'           : 6,

    # Pattern-Composer Fast (DC) Pattern Table:
    'PATTERN:COMPOSER:FAST:DATA' : 7,
    'PATTERN:COMPOSER:FAST'      : 7,
    'PATTERN:COMP:FAST:DATA'     : 7,
    'PATTERN:COMP:FAST'          : 7,
    'PATT:COMPOSER:FAST:DATA'    : 7,
    'PATT:COMPOSER:FAST'         : 7,
    'PATT:COMP:FAST:DATA'        : 7,
    'PATT:COMP:FAST'             : 7,

    # Pattern-Composer Linear Pattern Table
    'PATTERN:COMPOSER:LINEAR:DATA' : 8,
    'PATTERN:COMPOSER:LINEAR'      : 8,
    'PATTERN:COMPOSER:LIN:DATA'    : 8,
    'PATTERN:COMPOSER:LIN'         : 8,
    'PATTERN:COMP:LINEAR:DATA'     : 8,
    'PATTERN:COMP:LINEAR'          : 8,
    'PATTERN:COMP:LIN:DATA'        : 8,
    'PATTERN:COMP:LIN'             : 8,
    'PATT:COMPOSER:LINEAR:DATA'    : 8,
    'PATT:COMPOSER:LINEAR'         : 8,
    'PATT:COMPOSER:LIN:DATA'       : 8,
    'PATT:COMPOSER:LIN'            : 8,
    'PATT:COMP:LINEAR:DATA'        : 8,
    'PATT:COMP:LINEAR'             : 8,
    'PATT:COMP:LIN:DATA'           : 8,
    'PATT:COMP:LIN'                : 8,

    # Pattern Predefined Data:
    'PATTERN:PREDEFINED:DATA' : 9,
    'PATTERN:PRED:DATA'       : 9,
    'PATTERN:DATA'            : 9,
    'PATT:PREDEFINED:DATA'    : 9,
    'PATT:PRED:DATA'          : 9,
    'PATT:DATA'               : 9,

    # Digital-Pod Parameters
    'DIGITAL:PARAMETERS' : 10,
    'DIGITAL:PAR'        : 10,
    'DIG:PARAMETERS'     : 10,
    'DIG:PAR'            : 10,

    # ASK Table:
    'ASK:DATA' : 11,

    # FSK Table:
    'FSK:DATA' : 12,

    # FHOP Fixed-Time Table:
    'FHOPPING:FIXED:DATA' : 13,
    'FHOPPING:FIX:DATA'   : 13,
    'FHOP:FIXED:DATA'     : 13,
    'FHOP:FIX:DATA'       : 13,

    # FHOP Variable-Time Table:
    'FHOPPING:VARIABLE:DATA' : 14,
    'FHOPPING:VAR:DATA'      : 14,
    'FHOP:VARIABLE:DATA'     : 14,
    'FHOP:VAR:DATA'          : 14,

    # AHOP Fixed-Time Table:
    'AHOPPING:FIXED:DATA' : 15,
    'AHOPPING:FIX:DATA'   : 15,
    'AHOP:FIXED:DATA'     : 15,
    'AHOP:FIX:DATA'       : 15,

    # AHOP Variable-Time Table:
    'AHOPPING:VARIABLE:DATA' : 16,
    'AHOPPING:VAR:DATA'      : 16,
    'AHOP:VARIABLE:DATA'     : 16,
    'AHOP:VAR:DATA'          : 16,

    # PSK Table:
    'PSK:DATA' : 17,

    # PSK User-Defined Phases:
    'PSK:USER:DATA' : 18,

    # (N)QAM Table:
    'QAM:DATA' : 19,

    # (N)QAM User-Defined Constellation Table:
    'QAM:USER:DATA' : 20,

    # Firmware-Update File:
    'SYSTEM:FIRMWARE:DATA' : 21,
    'SYSTEM:FIRM:DATA'     : 21,
    'SYST:FIRMWARE:DATA'   : 21,
    'SYST:FIRM:DATA'       : 21,
    }


def _parse_max_arb_mem_from_opt_str(opt_str: str) -> Optional[int]:
    if opt_str.startswith('1M', 1):
        return 1 * 10**6
    elif opt_str.startswith('2M', 1):
        return 2 * 10**6
    elif opt_str.startswith('8M', 1):
        return 8 * 10**6
    elif opt_str.startswith('16M', 1):
        return 16 * 10**6
    elif opt_str.startswith('32M', 1):
        return 32 * 10**6
    elif opt_str.startswith('64M', 1):
        return 64 * 10**6
    elif opt_str.startswith('512K', 1):
        return 512 * 10**6
    elif opt_str.startswith('116') or opt_str.startswith('216') or opt_str.startswith('416'):
        return 16 * 10**6
    elif opt_str.startswith('132') or opt_str.startswith('232') or opt_str.startswith('432'):
        return 32 * 10**6
    elif opt_str.startswith('164') or opt_str.startswith('264') or opt_str.startswith('464'):
        return 64 * 10**6


def get_device_properties(idn_str: str, opt_str: str) -> DeviceProperties:
    """
    Args:
        idn_str: the instrument's answer to '*IDN?' query.
        opt_str: the instrument's answer to '*OPT?' query.

    Raises:
        ValueError if idn_str or opt_str does not belong to a supported instrument

    Returns:
        device properties
    """

    try:
        manufacturer_name, model_name, serial_number, fw_ver = idn_str.split(',')
    except ValueError as err:
        raise ValueError("Invalid IDN") from err

    try:
        prop_dict = model_properties_dict[model_name].copy()
    except KeyError as err:
        raise ValueError("Unknown model name", model_name) from err

    if model_name in ('WX2184', 'WX2184C', 'WX1284', 'WX1284C'):
        prop_dict['max_arb_mem'] = int(opt_str[2:4]) * 10**6
    else:
        parsed = _parse_max_arb_mem_from_opt_str(opt_str)
        if parsed is not None:
            prop_dict['max_arb_mem'] = parsed

    prop_dict['model_name'] = model_name
    prop_dict['serial_num'] = serial_number
    prop_dict['fw_ver'] = version.parse(fw_ver)

    return DeviceProperties(**prop_dict)


def udp_awg_instruments() -> Iterator[Tuple[str, str]]:
    """Using UDP list all broadcast reachable AWG-Instruments with LAN Interface.

    Returns:
         Mapping: Resource name -> IDN
    """
    UPFRMPORT = 7502
    FRMHEADERLEN = 22
    FRMDATALEN = 1024
    FLASHLINELEN = 32

    logger = module_logger.getChild('udp_awg_instruments')

    query_msg = bytearray([0xff] * FRMHEADERLEN)
    query_msg[0:4] = b'TEID'

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP) as udp_server_sock:
        # udp_server_sock.bind(("0.0.0.0", UDPSRVPORT))  # any IP-Address
        udp_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, FRMHEADERLEN + FRMDATALEN)
        udp_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

        # Send the query-message (to all)
        udp_server_sock.sendto(query_msg, (BROADCAST, UPFRMPORT))

        # Receive responses
        udp_server_sock.settimeout(2)
        while True:
            try:
                raw_data, (ip_addr, port) = udp_server_sock.recvfrom(FRMHEADERLEN + FRMDATALEN)
                resource_name = f"TCPIP::{ip_addr}::5025::SOCKET"
                logger.debug("Received answer from %s:%d: %r", ip_addr, port, raw_data)

                attrs = {}

                data = raw_data[FRMHEADERLEN:]
                while len(data) >= FLASHLINELEN and len(attrs) < 4:
                    line = data[:FLASHLINELEN]
                    data = data[FLASHLINELEN:]

                    op_code = line[:1]
                    attr = line[1:].rstrip(b'\x00')

                    if attr:
                        logger.debug("Attribute of %s with op code %s: %s", ip_addr, op_code, attr)

                    if op_code == b'D':
                        attrs['manuf_name'] = attr.decode('ascii')
                    if op_code == b'I':
                        attrs['model_name'] = attr.decode('ascii')
                    if op_code == b'S':
                        attrs['serial_nb'] = attr.decode('ascii')
                    if op_code == b'F':
                        attrs['fw_ver'] = attr.decode('ascii')

                if len(attrs) == 4:
                    yield resource_name, IDN_TEMPLATE.format(**attrs)
                else:
                    logger.info("Ignoring %s because it send %d != 4 attributes", resource_name, len(attrs))
            except socket.timeout:
                break


