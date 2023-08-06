from coproduct_recipes import Coproduct_Recipes as CR
from building import Building
from recipe import Recipe
from item import Item

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import re

def get_recipe_name(table_td):
    """
    Return name of recipe from Soup.
    """
    return str(table_td.contents[0])

def get_recipe_rate(string):
    """
    Return item input/output rate from string.
    """
    return float(re.match('[0-9]*[.]*[0-9]*', string).group(0))

def get_input_output(table_td):
    """
    Return list of items and rates from given table.
    """
    items_list = []
    rates_list = []

    while table_td:
        try:
            items_list.append(table_td.div.div.a.get('title'))
            rates_list.append(get_recipe_rate(table_td.div.next_sibling.string))
            
        except:
            break
        table_td = table_td.next_sibling

    return [items_list, rates_list]

def get_recipe_inputs(table_td):
    """
    Return list of all input names, list of all input rates.
    """
    return get_input_output(table_td)

def get_recipe_outputs(table_td):
    """
    Return list of all output names, list of all output rates.
    """
    return get_input_output(table_td)

def get_building(table_td):
    """
    Return the building recipe is made in.
    """
    try:
        return table_td.span.a.get('title')
    
    except:
        return None

def get_prereq(table_td):
    """
    Return what prerequisite exists for recipe unlock.
    """
    return str(table_td.span.text)

def get_is_alternate(table_td):
    """
    Return if the recipe is an alternate recipe (locked by default).
    """
    return True if table_td.br else False

def extract_product(extension: str):
    """
    Return full product name from URL extension.
    """
    return re.search('[a-zA-Z_-]+$', extension)[0]

def get_recipe_rows(recipe_soup):
    """
    Return non-header rows from crafting table on the item's Wiki page soup.
    """
    # Get all rows for recipe page
    try:
        crafting_table = recipe_soup.find_all(class_='wikitable')[0]
    except:
        raise Exception('Problem parsing wiki page soup.')

    crafting_rows = crafting_table.find_all('tr')

    # Select all non-header rows
    non_header_rows = crafting_rows[1:]

    return non_header_rows

def get_all_URLs_to_scrape(extensions_list):
    """
    Return list of full item URLs for scraping.
    """   
    base_URL = 'https://satisfactory.fandom.com'

    return [base_URL + extension for extension in extensions_list]

def itemify_components(names, rates):
    """
    Return Item instances list given names and rates.
    TODO: include other item forms besides 'solid' if necessary
    """
    return [Item(i, 'solid', r) for i, r in zip(names, rates)]

def scrape_recipe_page(recipes_soup):
    """
    Return Coproduct Recipes list for given Wiki page Soup.
    """
    # Select all non-header rows
    select_rows = get_recipe_rows(recipes_soup)

    # Define function-internal lists
    final_recipe_list = []
    temp_inputs = []
    temp_irates = []
    temp_outputs = []
    temp_orates = []

    # For each row in table (besides column names)
    for i in range(len(select_rows)):

        # Get first row's input item names and rates listed on HTML structure with 'class' attr
        if select_rows[i].has_attr('class'):

            # Get name for recipe, always index 0
            recipe_name = get_recipe_name(select_rows[i].find_all('td')[0])

            # Get if recipe is alt, always index 0
            recipe_is_alt = get_is_alternate(select_rows[i].find_all('td')[0])

            # Get primary row input values. always index 1+
            inps, irts = get_recipe_inputs(select_rows[i].find_all('td')[1])
            temp_inputs = inps
            temp_irates = irts

            # Get proper index for building info location in row
            if len(temp_inputs) < 2:
                building_index = 2

            else:
                building_index = 3

            # If exists, get first row's secondary inputs listed on HTML structure with no 'class' attr
            try:
                if not select_rows[i+1].has_attr('class'):

                    # Append secondary row input values to primary ones
                    inps, rts = get_recipe_inputs(select_rows[i+1].find_all('td')[0])
                    temp_inputs += inps
                    temp_irates += rts

            except:
                pass

            # Get building info
            recipe_building = get_building(select_rows[i].find_all('td')[building_index])

            # Get outputs for recipe, one index up from building
            outs, orts = get_recipe_outputs(select_rows[i].find_all('td')[building_index+1])
            temp_outputs = outs
            temp_orates = orts

            # Get prereqs for recipe
            # recipe_prereqs = get_prereq()
        
        # If hit row with no primary values, skip
        else:
            continue

        # Arrange items and rates into correct classes
        inputs = itemify_components(temp_inputs, temp_irates)
        outputs = itemify_components(temp_outputs, temp_orates)

        # Add to list of recipes for the page
        final_recipe_list.append(Recipe(recipe_name, inputs, outputs, recipe_building, recipe_is_alt))

    return final_recipe_list

def underscore_2_space(string: str):
    """
    Return string with underscores replaced by spaces.
    """
    return re.sub('[_]', ' ', string)

def get_recipe_soup(recipe_URL: str):
    """
    Return Soup of given URL.
    """
    # Get HTML of recipe page
    recipe_page = requests.get(recipe_URL)
    
    # Only parse and soup-ify the recipes table
    only_recipe_table = SoupStrainer(class_='wikitable')

    recipe_soup = BeautifulSoup(recipe_page.content, 'html.parser', parse_only=only_recipe_table)

    return recipe_soup

def get_all_coproduct_recipes(extensions_list: list):
    """
    Return Coproduct Recipes list for all recipes on the Wiki.
    """
    # Get list of item name URLs, convert to full URLs for scraping.
    all_item_URLs = get_all_URLs_to_scrape(extensions_list)

    # Get Soup list from all item URLs.
    all_recipe_soups = [get_recipe_soup(recipe_page) for recipe_page in all_item_URLs]

    # Scrape recipes from all Soups.
    all_recipe_lists = [scrape_recipe_page(recipe_soup) for recipe_soup in all_recipe_soups]

    # Make CR list from extensions and Recipe instances.
    all_coproduct_recipes = [CR(underscore_2_space(extract_product(extension)), recipe_list) for extension, recipe_list in zip(extensions_list, all_recipe_lists)]

    # Add Water, Fuel as a resource because it is missing
    all_coproduct_recipes.append(CR('Water', []))

    return all_coproduct_recipes
