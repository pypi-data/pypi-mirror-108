from recipe import Recipe
from item import Item

class Coproduct_Recipes():
    """
    Combines Recipe instances and common product name string.
    """

    def __init__(self, product_name: str, recipes_list: list):
        """
        Initialize instance with product name string and list of Recipe instances.
        """
        self._product_name = product_name
        self._recipes_list = recipes_list

    def __str__(self):
        """
        Return summary of instance using product name and number of recipes included.
        """
        num_recipes = self.num_recipes
        string = '{}: {} recipe'.format(self._product_name, num_recipes)

        if num_recipes > 1:
            return string + 's'
        else:
            return string
    
    def __repr__(self):
        """
        TODO
        """
        return self.__str__()

    def print_summary(self):
        """
        Prints all Recipe instances contained within Coproduct Recipe instance.
        """
        n = 1
        for recipe in self.recipes:
            print(str(n), '-', recipe.summary)
            n += 1

    @property
    def product(self):
        """
        Return product name string.
        """
        return self._product_name

    @product.setter
    def product(self, product):
        """
        Product name property setter.
        """
        self._product_name = product

    @property
    def recipes(self):
        """
        Return list of all included Recipe instances.
        """
        return self._recipes_list

    @recipes.setter
    def recipes(self, recipes):
        """
        Recipes property setter.
        """
        self._recipes = recipes

    @property
    def num_recipes(self):
        """
        Return number of included Recipe instances.
        """
        return len(self._recipes_list)

    @property
    def is_raw(self):
        """
        Return True if material is raw.
        """
        return self._recipes_list == []

    # def get_base_recipes(self):
    #     """
    #     Return list of all included base Recipe instances.
    #     TODO fix
    #     """
    #     return [recipe for recipe in self.recipes_list if not recipe.is_alternate()]
    
    # def get_alt_recipes(self):
    #     """
    #     Return list of all included alternate Recipe instances.
    #     TODO fix
    #     """
    #     return [recipe for recipe in self.recipes_list if recipe.is_alternate()]

    # def __len__(self):
    #     """
    #     TODO
    #     """
    #     return(self.num_recipes)

    # def __getitem__(self, key):
    #     return(self.recipes_list[key])