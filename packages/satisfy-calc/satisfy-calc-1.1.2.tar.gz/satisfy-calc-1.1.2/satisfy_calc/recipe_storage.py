from coproduct_recipes import Coproduct_Recipes
from recipe import Recipe
from item import Item

import jsonpickle as jp
from os import path

def save_recipes(recipes_list, filename='recipes.sc'):
    """
    Write Recipes to given filename for local storage.
    """
    # When file already present, wipe file, write new recipes
    if path.isfile(filename):
        print('Saved recipes file already exists. Overwriting.')
        erase_contents(filename)
        recipe_writer(filename, recipes_list, mode='a')

    # When file isn't present, make file, write new recipes
    else:
        print('Creating new recipes file for saving recipes.')
        recipe_writer(filename, recipes_list, mode='x')

def jsonify_recipes(coproduct_recipe_list):
    """
    Return Coproduct Recipe list encoded into a JSON format string.
    """
    return [jp.encode(coproduct_recipe) for coproduct_recipe in coproduct_recipe_list]

def recipe_writer(filename, recipes_list, mode):
    """
    Internal method for writing Recipes to given file.
    """
    try:
        # Write recipes to file in given mode
        with open(filename, mode) as recipes_file:
            for recipe_json in recipes_list:
                recipes_file.write(recipe_json)
                recipes_file.write('\n')

    except Exception:
        print('Problem writing to file.')
        # raise Exception

def erase_contents(filename):
    """
    Internal method for clearing the contents of given file.
    """
    try:
        # Clear contents of file
        open(filename, 'w').close()

    except Exception:
        print('Problem erasing file.')

def load_saved_recipes(filename):
    """
    Internal method for reading contens of given file.
    """
    contents = []
    
    try:
        # Read file line by line, recipe by recipe
        with open(filename, 'r') as recipes_file:
            contents = recipes_file.readlines()
        
        return contents

    except Exception:
        print('Problem reading recipes from file.')

def convert_loaded_recipes(loaded_recipes_list):
    """
    Return encoded recipes as list of Coproduct Recipe instances.
    """
    return [jp.decode(recipe) for recipe in loaded_recipes_list]

def save_recipes_locally(recipes_list, filename='recipes.sc'):
    """
    Write scraped recipes to given filename.
    """
    # Convert Coproduct_Recipes to JSON serializable
    jsonified_recipes = jsonify_recipes(recipes_list)

    # Write Corpoduct_Recipes to file
    save_recipes(jsonified_recipes, filename)

def read_saved_recipes(filename='recipes.sc'):
    """
    Read given filename to get all saved Coproduct Recipes instances.
    """
    # Read saved recipes from filename
    loaded_recipes = load_saved_recipes(filename)
    
    # Deserialize recipes to read in as Coproduct Recipes class
    loaded_recipes_deserialized = convert_loaded_recipes(loaded_recipes)

    return loaded_recipes_deserialized
