
class Item():
    """Any Extracted item or item made in a production building"""

    def __init__(self, name: str, form: str, rate: float):
        self._name = name
        self._form = form
        self._rate = rate

    def __str__(self):
        return f'{self._rate}/min {self._name}.'

    def __repr__(self):
        return f'Item(name=\'{self._name}\', form=\'{self._form}\', rate={self._rate})'
        
    # For when/if form is added
    #return 'Item(name=\'{}\', form=\'{}\', rate={})'.format(self.name, self.form, self.rate)

    def __add__(self, other):
        """
        Return the combined Item instance.
        """
        return Item(self._name, self._form, self._rate + other._rate)
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, form: str):
        self._form = form

    @property
    def rate(self):
        return float(self._rate)

    @rate.setter
    def rate(self, rate: float):
        self._rate = rate

    @property
    def is_solid(self):
        return self._form == 'solid'

    @property
    def is_liquid(self):
        return self._form == 'liquid'
    
    @property
    def is_gas(self):
        return self._form == 'gas'

    def scale_by(self, multiplier: float):
        return Item(self._name, self._form, self._rate * multiplier)

    # def simple_str(self):
    #     return '{}x {}'.format(self._rate, self._name)

# test_item = Item('test_item', 'solid', 120)
# print(test_item)