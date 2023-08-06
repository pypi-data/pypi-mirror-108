
class Building():
    """Building with associated number of inputs and outputs, power consumption, overclock level"""
    name = ''
    input_num = 0
    output_num = 0
    base_power_use = 0
    overclock = 0

    def __init__(self, name='', input_num=0, output_num=0, base_power_use=0, overclock=0):
        """Read in from file, set building stats"""
        self.name = name
        self.input_num = input_num
        self.output_num = output_num
        self.base_power_use = base_power_use
        self.overclock = overclock

    def __str__(self):
        return '{} with {} inputs, {} outputs, {} MW of power use and overclock level of {}'.\
            format(self.name, self.input_num, self.output_num, self.base_power_use, self.overclock)
    
    def __repr__(self):
        return 'Building(name=\'{}\', input_num={}, output_num={}, base_power_use={}, overclock={})'.\
            format(self.name, self.input_num, self.output_num, self.base_power_use, self.overclock)

    def is_extactor(self):
        return self.input_num == 0

    def is_producer(self):
        return self.input_num != 0
    
    def get_base_power_use(self):
        return self.base_power_use

    def get_net_power_use(self):
        return self.base_power_use * self.get_power_multiplier()

    def get_overclock(self):
        return self.overclock

    def get_power_multiplier(self):
        # Needs actual formula, overclock power scaling is not linear
        return 1 + self.overclock*.5