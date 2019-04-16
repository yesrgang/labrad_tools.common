class AFG3xxx(object):
    _visa_address = None
    _source = None

    _frequency_range = None
    _amplitude_range = None
    _amplitude_units = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'visa' not in globals():
            global visa
            import visa
        rm = visa.ResourceManager()
        self._inst = rm.open_resource(self._visa_address)

    @property
    def state(self):
        command = 'OUTP{}?'.format(self.source)
        ans = self._inst.query(command)
        if ans == 'ON':
            state = True
        else:
            state = False
        return state
    
    @state.setter
    def state(self, state):
        command = 'OUTP{}:STAT {}'.format(self.source, int(bool(state)))
        self._inst.write(command)

    @property
    def frequency(self):
        command = 'SOUR{}:FREQ?'.format(self.source)
        ans = self._inst.query(command)
        return float(ans)
    
    @frequency.setter
    def frequency(self, frequency):
        frequency = sorted([min(self.frequency_range), 
            max(self.frequency_range), frequency])[1]
        command = 'SOUR{}:FREQ {}'.format(self.source, frequency)
        self._inst.write(command)
    
    @property
    def start_frequency(self):
        command = 'SOUR{}:FREQ:STAR?'.format(self.source)
        ans = self._inst.query(command)
        return float(ans)
    
    @start_frequency.setter
    def start_frequency(self, frequency):
        frequency = sorted([min(self.frequency_range), 
            max(self.frequency_range), frequency])[1]
        command = 'SOUR{}:FREQ:STAR {}'.format(self.source, frequency)
        self._inst.write(command)
    
    @property
    def stop_frequency(self):
        command = 'SOUR{}:FREQ:STOP?'.format(self.source)
        ans = self._inst.query(command)
        return float(ans)
    
    @stop_frequency.setter
    def stop_frequency(self, frequency):
        frequency = sorted([min(self.frequency_range), 
            max(self.frequency_range), frequency])[1]
        command = 'SOUR{}:FREQ:STOP {}'.format(self.source, frequency)
        self._inst.write(command)
    
    @property
    def amplitude(self):
        command = 'SOUR{}:VOLT?'.format(self.source)
        ans = self._inst.query(command)
        return float(ans)
    
    @amplitude.setter
    def amplitude(self, amplitude):
        amplitude = sorted([min(self.amplitude_range), 
            max(self.amplitude_range), amplitude])[1]
        command = 'SOUR{}:VOLT {}'.format(self.source, amplitude)
        self._inst.write(command)
        
    @property
    def offset(self):
        command = 'SOUR{}:VOLT:OFFS?'.format(self.source)
        ans = self._inst.query(command)
        return float(ans)
    
    @offset.setter
    def offset(self, offset):
        command = 'SOUR{}:VOLT:OFFS {}'.format(self.source, offset)
        self._inst.write(command)

