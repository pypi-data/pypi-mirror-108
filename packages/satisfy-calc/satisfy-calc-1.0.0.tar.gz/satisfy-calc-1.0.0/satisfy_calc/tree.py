from item import Item
from recipe import Recipe
from coproduct_recipes import Coproduct_Recipes

all_requirements = []

class CraftingTree():

    def __init__(self, product_name: str, product_rate: float, coproduct_recipes_list: list):
        """
        Initialize tree with target item name and desired production rate.
        """
        init_item = Item(product_name, 'solid', product_rate)
        self._coproduct_recipes_list = coproduct_recipes_list
        self._root_node = CraftingNode(init_item, self._coproduct_recipes_list, 0)
        # self._tree_height = 0
        # self._all_reqs = []

        self.calc()

    @property
    def root(self):
        return self._root_node

    @root.setter
    def root(self, root):
        self._root_node = root

    @property
    def recipes_list(self):
        return self._coproduct_recipes_list

    @root.setter
    def recipes_list(self, recipes_list):
        self._coproduct_recipes_list = recipes_list
    
    @property
    def tree_height(self):
        return self._tree_height
    
    @property
    def reqs(self):
        return self._all_reqs

    def calc(self):
        self.root.calc()

    def traverse(self):
        self.root.traverse()


class CraftingNode():

    MAX_CHILDREN = 4

    def __init__(self, init_item: Item, coproduct_recipes_list: list, level: int):
        """
        Initialize node using Item class definition.
        """
        self.coproduct_recipes_list = coproduct_recipes_list
        self.num_buildings = 0.0
        self.goal = init_item
        self.byproducts = []
        self.children = []
        self.level = level
        self.recipe = ''

    def __str__(self):
        return('Crafting node for {} at {}/min.'.format(self.goal.name, self.goal.rate))

    def __repr__(self):
        return('CraftingNode(Item({}, \'solid\', {}))'.format(self.goal.name, self.goal.rate))

    def display(self):
        """
        Print summary of CraftingNode, as part of CraftingTree.
        """
        # Set spacer strings for the following text
        align_str_header = '\t'*self.level
        align_str_body = '\t'*self.level
        
        # Exception for first node printed (root)
        if self.level > 0:
            align_str_header = '\t'*self.level + 'L_'
            align_str_body = '\t'*(self.level) + '  '

        # Display input names and required rates
        self.display_header(align_str_header)

        # Display names and rates of byproducts if any
        self.display_byproduct(align_str_body)

        # Display building / to extract
        self.display_building(align_str_body)

        # Print whitespace separator
        self.spacer()

    def display_header(self, align_str):
        """
        Print header of current CraftingNode.
        """
        print(align_str, self.unpack_list())

    def display_byproduct(self, align_str):
        """
        Print byproduct section of current CraftingNode.
        """
        if self.byproducts:
            print(align_str, 'Byproduct: {}'.format(self.byproducts[0]))

    def display_building(self, align_str):
        """
        Print building section of current CraftingNode.
        """
        if self.recipe:
            if self.recipe._building:
                print(align_str, 'Made in {:.2f}x {}.'.format(self.num_buildings, self.recipe.building))
            else:
                raise Exception('Recipe exists with no building.')
        else:
            print(align_str, 'Mine/Extract resource from the world.')

    def spacer(self):
        print()

    def unpack_list(self):
        """
        Return appropriate print method from Item instace of self.goal.
        """
        return self.goal.__str__()

    def user_recipe_select(self, potential_recipes):
        """
        Offer user choice of which recipe to use for the crafting step.
        """
        # Check for edge cases
        if potential_recipes.num_recipes == 0:
            return None

        if potential_recipes.num_recipes == 1:
            return potential_recipes.recipes[0]
        
        # If no edge case, display options
        potential_recipes.print_summary()

        # Prompt user for resonable selection
        try:
            selected_idx = int(input('Enter recipe # to use: '))
        except ValueError as err:
            selected_idx = int(input('Enter valid recipe # to use: '))
        
        self.spacer()
        while selected_idx > potential_recipes.num_recipes or selected_idx < 0:
            selected_idx = int(input('Enter valid recipe # to use: '))

        # Return the Recipe at the adjusted index (1-indexed)
        return potential_recipes.recipes[selected_idx-1]
    
    @property
    def num_children(self):
        """
        Return number of children a node already has.
        """
        return len(self.children)

    def add_child(self, new_child):
        """
        Add a child to node. Handles max amount of children already existing.
        """
        if self.num_children < self.MAX_CHILDREN:
            self.children.append(new_child)
        
        else:
            raise Exception('Max number of allowed children ({}) exceeded.'.format(self.MAX_CHILDREN))
    
    def get_suitable_recipes(self, desired_output):
        """
        Return the CRs instance containing Recipes for the desired output.
        """
        for coproduct_recipe in self.coproduct_recipes_list:
            if desired_output == coproduct_recipe.product:
                return coproduct_recipe
        
        return None
        
    def calc(self):
        """
        Take root node of tree, with user assistance, compute the crafting requirements and build the tree.
        """
        # Find appropriate recipes
        suitable_recipe = self.get_suitable_recipes(self.goal.name)

        # If recipe for desired goal exists
        if suitable_recipe:

            # If a non-raw recipe has been returned, calculate production requirements
            if suitable_recipe.recipes:

                # Ask user for which recipe to use
                self.recipe = self.user_recipe_select(suitable_recipe)
                all_inputs = self.recipe.input_items
                all_output_names = self.recipe.output_names

                # Build crafting tree for each input for recipe
                for inp in all_inputs:

                    # Calculate the requirements for the step
                    multiplier = self.recipe.get_ratio(inp.name, self.goal.name)

                    # Calculate number of buildings required for the step
                    self.num_buildings = self.goal.rate / self.recipe.get_output_rate_for(self.goal.name)

                    # Set goal for next child
                    next_goal = Item(inp.name, inp.form, self.goal.rate * multiplier)

                    # Add next steps as child CraftingNode
                    self.add_child(CraftingNode(next_goal, self.coproduct_recipes_list, self.level+1))

                # Find and report byproducts for the step if present
                if len(all_output_names) > 1:

                    # Remove step goal from outputs list
                    all_output_names.remove(self.goal.name)

                    # Convert output names to output Item instances
                    all_output_items = [self.recipe.get_output_item_from_name(output) for output in all_output_names]

                    # Scale byproduct rates appropriately
                    self.byproducts = [output.scale_by(self.num_buildings) for output in all_output_items]

                # Recurse
                for child in self.children:
                    child.calc()

            # Otherwise, end branch
            else:
                # print('Reached leaf node.')
                all_requirements.append(self.goal)

        # When no recipe for requested component exists
        else:
            raise Exception('No match for desired output in any available recipe.', self.goal.name)

    def traverse(self):
        """
        Print CraftingNodes as tree is being traversed depth-first.
        """
        self.display()

        for child in self.children:
            child.traverse()
