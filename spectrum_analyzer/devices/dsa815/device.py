import numpy as np
import re
import struct
import vxi11

from device_server.device import DefaultDevice


class DSA815(DefaultDevice):
    vxi11_address = None

    trace_index = None

    def initialize(self, config):
        super(DSA815, self).initialize(config)
        self.vxi11 = vxi11.Instrument(self.vxi11_address)
        self.vxi11.write(':format:trace:data REAL')

    def set_trace(self, value):
        pass

    def get_trace(self):
        command = ':TRACe:DATA? TRACE{}'.format(self.trace_index)
        response = self.vxi11.ask_raw(command)
        header = response[:11]
        body = response[11:-1]
        num_bytes = int(header[2:])
        trace = struct.unpack('{}f'.format(num_bytes / 4), body)
        return trace
   
    def get_frequency_range(self):
        start = self.vxi11.ask(':SENSe:FREQuency:STARt?')
        stop = self.vxi11.ask(':SENSe:FREQuency:STOP?')
        return [float(start), float(stop)]

    def set_frequency_range(self, value):
        start_command = ':SENSe:FREQuency:STARt {}'.format(min(value))
        stop_command = ':SENSe:FREQuency:STOP {}'.format(max(value))
        self.vxi11.write(start_command)
        self.vxi11.write(stop_command)

    def get_amplitude_scale(self):
        scale = self.vxi11.ask(':DISPlay:WINdow:TRACe:Y:SCALe:PDIVision?')
        return float(scale)
 
    def set_amplitude_scale(self, value):
        scale_command = ':DISPlay:WINdow:TRACe:Y:SCALe:PDIVision {}'.format(value)
        self.vxi11.write(scale_command)
    
    def get_amplitude_offset(self):
        offset = self.vxi11.ask(':DISPlay:WINdow:TRACe:Y:SCALe:RLEVel?')
        return float(offset)
 
    def set_amplitude_offset(self, value):
        offset_command = ':DISPlay:WINdow:TRACe:Y:SCALe:RLEVel {}'.format(value)
        self.vxi11.write(offset_command)
   
    def set_resolution_bandwidth(self, value):
        command = ':SENSe:BANDwidth:RESolution {}'.format(value)
        self.vxi11.write(command)

    def get_resolution_bandwidth(self):
        command = ':SENSe:BANDwidth:RESolution?'
        resolution_bandwidth = self.vxi11.ask(command)
        return resolution_bandwidth
