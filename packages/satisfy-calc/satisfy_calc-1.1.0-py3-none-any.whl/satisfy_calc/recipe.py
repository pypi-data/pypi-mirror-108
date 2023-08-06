from item import Item
from re import sub

class Recipe():
    """
    Combines up to 4 Item instances to output up to 2 Item instances.
    """

    def __init__(self, recipe_name: bool, inputs_list: list, outputs_list: list, building: str, is_alternate: bool):
        """
        Initialize instance with name string, input Item instances list, 
        output Item instances list, building name, whether is an alternate recipe.
        """
        self._recipe_name = recipe_name
        self._inputs = inputs_list
        self._outputs = outputs_list
        self._building = building
        self._is_alternate = is_alternate

    def __str__(self):
        """
        Return all details of Recipe.
        """
        return f'Recipe name: {self.name}\nInputs: {self.input_names}\nOutputs: {self.output_names}\nMade in: {self.building}\nIs alt. recipe: {self.is_alt}\n'
    def __repr__(self):
        """
        Return Recipe name.
        """
        return f'Recipe for {self.name}'

    def scale_by(self, multiplier):
        """
        Scale inputs and outputs according to multiplier.
        """
        self.scale_inputs_by(multiplier)
        self.scale_outputs_by(multiplier)

    def scale_inputs_by(self, multiplier):
        """
        Scale inputs of recipe according to multiplier.
        """
        self._inputs = [inp.scale_by(multiplier) for inp in self._inputs]

    def scale_outputs_by(self, multiplier):
        """
        Scale inputs of recipe according to multiplier.
        """
        self._outputs = [outp.scale_by(multiplier) for outp in self._outputs]

    @property
    def summary(self):
        """
        Return summary of the Recipe instance.
        """
        return '[{}] made from {}'.format(self.name, self.list_formatter(self.input_names))

    def list_formatter(self, l):
        return '[' + ', '.join(l) + ']'

    @property
    def name(self):
        """
        Return Recipe instance name.
        """
        return self._recipe_name

    @name.setter
    def name(self, name):
        self._recipe_name = name
    
    @property
    def is_raw(self):
        """
        Return True if the item is a raw material (not craftable/no inputs).
        """
        return self._inputs is None

    @property
    def input_items(self):
        """
        Return all inputs as list of Item instances.
        """
        return self._inputs

    @input_items.setter
    def input_items(self, input_items):
        self._inputs = input_items

    @property
    def input_names(self):
        """
        Return all inputs as list of item name strings.
        """
        return [inp.name for inp in self._inputs]

    @property
    def input_rates(self):
        """
        Return all inputs as list of item rates.
        """
        return [inp.rate for inp in self._inputs]

    @property
    def output_items(self):
        """
        Return all outputs as list of Item instances.
        """
        return self._outputs

    @output_items.setter
    def output_items(self, output_items):
        self._outputs = output_items

    @property
    def output_names(self):
        """
        Return all outputs as list of item names.
        """
        return [outp.name for outp in self._outputs]

    @property
    def output_rates(self):
        """
        Return all outputs as list of item rates.
        """
        return [outp.rate for outp in self._outputs]

    @property
    def building(self):
        """
        Return building name.
        """
        return self._building

    @building.setter
    def building(self, building):
        self._building = building

    @property
    def is_base(self):
        """
        Return whether recipe is unlocked by default.
        """
        return self._is_alternate == False

    @property
    def is_alt(self):
        """
        Return whether recipe is locked by default.
        """
        return self._is_alternate

    @is_alt.setter
    def is_alt(self, is_alternate):
        self._is_alternate = is_alternate

    def get_output_rate_for(self, output_name):
        return self.output_rates[self.output_names.index(output_name)]
        
    def get_input_item_from_name(self, item_name: str):
        """
        Return Item instance from self.inputs given item name.
        """
        return [inp for inp in self.input_items if item_name == inp.name][0]

    def get_output_item_from_name(self, item_name: str):
        """
        Return Item instance from self.outputs given item name.
        """
        return [outp for outp in self.output_items if item_name == outp.name][0]

    def get_ratio(self, inp: str, outp: str):
        """
        Return input/output ratio given one input, one output item name.
        """
        if inp is None:
            return None
        else:
            return self.get_input_item_from_name(inp).rate /\
                self.get_output_item_from_name(outp).rate
    
    def get_ratio_rev(self, inp: str, outp: str):
        """
        Return output/input ratio given one input, one output item name.
        """
        if inp is None:
            return None
        else:
            return self.get_output_item_from_name(outp).rate /\
                self.get_input_item_from_name(inp).rate
