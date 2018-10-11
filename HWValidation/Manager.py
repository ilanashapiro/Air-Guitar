
import re
import sys
import json
import time
import struct
try:
    import readline
except ImportError:
    import pyreadline as readline
import threading
from collections import OrderedDict, namedtuple
import os

import serial
import serial.tools.list_ports

#Runs on Raspberry Pi and communicates w/ arduino manager network

COMM_INITIAL                   = 0
COMM_WAITING_FOR_CHANGE_STATE  = 1
COMM_WAITING_FOR_EVENT_STATE   = 2
COMM_WAITING_FOR_EVENT_EVENT   = 3
COMM_WAITING_FOR_VALUE_STATE   = 4
COMM_WAITING_FOR_VALUE_ID      = 5
COMM_WAITING_FOR_VALUE_VALUE   = 6
COMM_WAITING_FOR_DEBUG_SETTING = 7
COMM_WAITING_FOR_HEARTBEAT_ID  = 8

State = namedtuple('State', ('name', 'id', 'devices'))
DeviceState = namedtuple('DeviceState', ('values', 'events'))
WireValue = namedtuple('WireValue',('type','changed','value'))

class Manager():

    INT_TY_RE = re.compile(r"^(u?)int(8|16|32)_t$")
    STRUCT_SIZE_MAPPING = {
        '8': 'b',
        '16': 'h',
        '32': 'i',
    }
    
    @staticmethod
    def ty_to_struct(ty):
        if ty == 'bool':
            return '?'

        m = Manager.INT_TY_RE.match(ty)
        if m is None:
            return ValueError("bad type???")

        size = Manager.STRUCT_SIZE_MAPPING[m.group(2)]
        return '<' + (size.upper() if m.group(1) == 'u' else size)

    @staticmethod
    def parse_val(ty, s):
        if ty == 'bool':
            if s in ('True', 'true'):
                return chr(1)
            elif s in ('False', 'false'):
                return chr(0)
            else:
                raise ValueError("%r is not a bool" % s)
        elif 'int' in ty:
            return struct.pack(Manager.ty_to_struct(ty), int(s))
        else:
            raise ValueError("unknown type %r" % ty)

    def __init__(self,*args):
        if len(args) == 3:
            (self.build_id, self.hardware_states, self.port) = args
        else:
            try:
                hardware = json.load(open("hardware.json"))
                master = min((int(name[4:]), serial) for (name, serial) in hardware['AMIBs'].items())[1]
                master_serial = master['serialNumber']
            except (IOError, ValueError, IndexError, KeyError):
                print("Non-existent or invalid hardware.json file")
                sys.exit(1)
            connected = False
            for port in serial.tools.list_ports.comports():
                if port.serial_number == master_serial:
                    self.port = serial.Serial(port.device, 9600)
                    connected = True
                    break
            if not connected:
                print("Master AMIB not connected")
                sys.exit(2)
            self.build_id = 776775290
            self.hardware_states = [State(name='IDLE', id=0, devices={'master': DeviceState(values=OrderedDict(), events=[]), 'tablet': DeviceState(values=OrderedDict(), events=[])}), State(name='PISTON', id=1, devices={'master': DeviceState(values=OrderedDict([('encodedChord', WireValue(type='uint32_t', changed=False, value=None))]), events=['playFChord', 'playBbChord', 'playD5Chord', 'playAbChord', 'playDbChord', 'playCChord', 'playeChord', 'playaChord', 'retractAll', 'engageMuteBar', 'disengageMuteBar']), 'tablet': DeviceState(values=OrderedDict([('testVal', WireValue(type='uint16_t', changed=False, value=None))]), events=[])})]

        time.sleep(1)
        self.state = COMM_INITIAL
        self.port.write(b"\x05")
        if self.port.read(1) != b'\x05':
            comm_error()
        
        its_build_id = struct.unpack("<I", self.port.read(4))[0]
        if its_build_id != self.build_id:
            print("Mismatching build IDs: expected {} but got {}, exiting".format(self.build_id, its_build_id))
            sys.exit(3)

        self.port.write(b"\x06")
        if self.port.read(1) != b'\x06':
            comm_error()

        self.buf           = []
        self.pending_value = None
        self.thread        = threading.Thread(target=self.handle_byte)
        self.thread.daemon = True
        self.cur_state = self.hardware_states[ord(self.port.read(1))]
    
    def comm_error():
        print("Communications error, exiting...")
        sys.exit(2)

    def handle_byte(self):
        try:
            s = self.port.read(1)
        except serial.SerialException:
            return

        while s != '':
            b = ord(s)
            self.buf.append(b)
            if self.state == COMM_INITIAL:
                if b == 2:
                    self.state = COMM_WAITING_FOR_VALUE_STATE
                else:
                    # ??
                    self.state = COMM_INITIAL
                    self.buf = []
            elif self.state == COMM_WAITING_FOR_VALUE_STATE:
                self.state = COMM_WAITING_FOR_VALUE_ID
            elif self.state == COMM_WAITING_FOR_VALUE_ID:
                state = self.hardware_states[self.buf[1]]
                #just gets value with id that matches buf[2]
                self.pending_value = next((name, wire_val) for (i, (name, wire_val)) in enumerate(state.devices['tablet'].values.items()) if i == self.buf[2])
                self.state = COMM_WAITING_FOR_VALUE_VALUE
            elif self.state == COMM_WAITING_FOR_VALUE_VALUE:
                name, wire_val = self.pending_value
                sty = Manager.ty_to_struct(wire_val.type)
                if struct.calcsize(sty) == len(self.buf) - 3:#Wait for buffer to fill up with entire value. Keep looping in this state until full.
                    oldVal = state.devices['tablet'].values[name].value
                    state.devices['tablet'].values[name] = state.devices['tablet'].values[name]._replace(value = struct.unpack(sty, bytes(self.buf[3:]))[0]) #udpdate received value
                    if oldVal != state.devices['tablet'].values[name].value: 
                        state.devices['tablet'].values[name] = state.devices['tablet'].values[name]._replace(changed= True)
                    else:
                        state.devices['tablet'].values[name] = state.devices['tablet'].values[name]._replace(changed = False)
                    self.state = COMM_INITIAL
                    self.buf = []
            else:
                raise ValueError("???")

            try:
                s = self.port.read(1)
            except serial.SerialException:
                pass

    def start(self):
        self.thread.start()

    def set_state(self,name):
        self.cur_state = next(state for state in self.hardware_states if state.name == name)
        self.port.write(('\x00' + chr(self.cur_state.id)).encode('utf8'))

    def set_value(self,value_name, value):
        for id, (name, ty) in enumerate(self.cur_state.devices['master'].values.items()):
            if name == value_name:
                break
            else:
                raise ValueError('No such value % r' % value_name)

        value = Manager.parse_val(ty, value)
        self.port.write(('\x02' + chr(self.cur_state.id) + chr(id) + value).encode('utf8'))

    def set_event(self,name):
        id = self.cur_state.devices['master'].events.index(name)
        self.port.write(('\x01' + chr(self.cur_state.id) + chr(id)).encode('utf8'))

    def get_value(self,name):
        return self.cur_state.devices['tablet'].values[name]
