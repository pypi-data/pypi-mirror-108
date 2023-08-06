#!/usr/bin/python

from recipe_storage import read_saved_recipes, load_saved_recipes, save_recipes_locally
from fetch_recipes import get_all_coproduct_recipes
from fetch_item_names import get_all_item_URLs
from tree import CraftingTree

import sys

def main():

    def help():
        HELP_STRING = ('Satisfy-calc use guide:\n'
                    '1. "update" or -u: to update local recipe files. Advisable after an update drops.\n'
                    '2. "calc" or -c: followed by \'Item Name\' Item Rate to calculate crafting chain for an ingredient. '
                    'e.g. ./satisfy-calc.py -c \'Iron Ingot\' 60\n'
                    '3. "help" or -h: to bring up this information.')
        print(HELP_STRING)

    def update_local():
        all_item_URLs = get_all_item_URLs()
        all_recipes = get_all_coproduct_recipes(all_item_URLs)
        save_recipes_locally(all_recipes)

    def calc():
        CRs = read_saved_recipes('recipes.sc')
        tree = CraftingTree(*args, CRs)
        tree.traverse()

    opts = [opt for opt in sys.argv[1:] if opt.startswith('-')]
    args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]

    if 'help' in args or '-h' in opts:
        help()
    elif 'update' in args or '-u' in opts:
        print('Updating locally saved recipes... ')
        update_local()
    elif 'calc' in args or '-c' in opts:
        print('Begin crafting tree calculation... \nPlease select what recipe to use at each step: \n')
        calc()
    else:
        raise SystemExit('Try -h or --help.')

if __name__ == '__main__':
    main()
    
