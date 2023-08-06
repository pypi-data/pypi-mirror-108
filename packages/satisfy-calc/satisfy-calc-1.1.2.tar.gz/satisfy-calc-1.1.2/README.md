## Satisfy-Calc

### Introduction:

`satisfy-calc` is a command line utility for calculating and visualizing crafting trees in [Satisfactory Game](https://www.satisfactorygame.com/) by [Coffee Stain Studios](https://www.coffeestainstudios.com/) written in Python. This utility is intended to aid users in the construction of complex production lines utilizing all available base and alternate recipes, or for users simply wanting to check their own designs for efficiency and correctness.

### Quick Use Guide:

1. On first use, invoke `python -m satisfy-calc update` to get all up to date recipes. Repeat this step after game updates.
   **Note:** This might take around a minute, and requires an active internet connection.
2. After the recipes are fetched, invoke `python -m satisfy-calc calc <Item Name> <Item Rate>` to get the crafting tree.
   **Note:** Use single or double quotes around item names that have multiple words in them e.g. `'Iron Plate' 20` instead of just `Iron Plate 20`.

### Detailed Use Guide:

`satisfy-calc` currently has 2 operating modes:

**1. Updating locally stored recipes:**

Invoked through `python -m satisfy-calc update` or `python -m satisfy-calc -u`, this mode will acquire all recipes currently in use within the game if none exist locally, or update the locally stored recipes if already present.

Recipes are fetched from the [Satisfactory Wiki](https://satisfactory.fandom.com/wiki/Satisfactory_Wiki), and therefore are subject to changes during/after updates that affect recipe contents and/or add new recipes. The fetched recipes are stored locally under the package install directory as a text file.

The use of this mode is recommended after any update that has new recipes and during the first use of the utility in order to generate the initial file locally.

`satisfy-calc` is not intended to allow for simple recipe browsing, as the recipe tables found on the Wiki provide a more intuitive visual representation for recipes.

**2. Calculating crafting tree for a given input item and desired rate of production:**

Invoked through `python -m satisfy-calc calc <Item Name> <Item Rate>` or `python -m satisfy-calc -c <Item Name> <Item Rate>`, this mode will calculate the individual requirements to craft the given item at the given rate. Rate units for any item is assumed to be items/min for solids and m3/min for liquids and gases.

Upon invocation the utility will start formulating a tree structure, rooted on the specified item and given rate. The tree will add new branches for each ingredient required to craft the specified item. This process will repeat until each branch concludes in a form of raw input that can be extracted from the world, such as Ore or Crude Oil. At each such step, the user will be asked to provide their recipe of choice from a suitable list of recipes that can be utilized in the production of the necessary item.

Each step can be broken down into several parts:
- Item name that needs to be produced at given rate through the user-selected recipe.
- All byproducts of the user-selected recipe as well as the rate at which they will be produced, if applicable.
- Name and number of buildings to carry out the crafting of the user-selected recipe. 
  **Note:** If the item is Ore or other raw input, the necessary rate of extraction from the world will be listed instead.

### Usage Example:

Upon the invocation of the following line:
`python -m satisfy-calc calc 'Iron Plate' 30`

The following output will follow, and the user will be prompted to make a recipe selection:
```
Begin crafting tree calculation... 
Please select what recipe to use at each step: 

1 - [Iron Plate] made from [Iron Ingot]
2 - [Coated Iron Plate] made from [Iron Ingot, Plastic]
3 - [Steel Coated Plate] made from [Steel Ingot, Plastic]
Enter recipe # to use: _
```

Because the crafting process does not end after a single step, the user will be prompted again:
```
Begin crafting tree calculation... 
Please select what recipe to use at each step: 

1 - [Iron Plate] made from [Iron Ingot]
2 - [Coated Iron Plate] made from [Iron Ingot, Plastic]
3 - [Steel Coated Plate] made from [Steel Ingot, Plastic]
Enter recipe # to use: 1

1 - [Iron Ingot] made from [Iron Ore]
2 - [Pure Iron Ingot] made from [Iron Ore, Water]
3 - [Iron Alloy Ingot] made from [Iron Ore, Copper Ore]
Enter recipe # to use: _
```

In both cases the first recipe from the list was selected, and the crafting tree is constructed automatically after all necessary recipes have been selected:
```
Begin crafting tree calculation... 
Please select what recipe to use at each step: 

1 - [Iron Plate] made from [Iron Ingot]
2 - [Coated Iron Plate] made from [Iron Ingot, Plastic]
3 - [Steel Coated Plate] made from [Steel Ingot, Plastic]
Enter recipe # to use: 1

1 - [Iron Ingot] made from [Iron Ore]
2 - [Pure Iron Ingot] made from [Iron Ore, Water]
3 - [Iron Alloy Ingot] made from [Iron Ore, Copper Ore]
Enter recipe # to use: 1

 30/min Iron Plate.
 Made in 1.50x Constructor.

        L_ 45.0/min Iron Ingot.
           Made in 1.50x Smelter.

                L_ 45.0/min Iron Ore.
                   Mine/Extract resource from the world.
```
The produced crafting tree that can be read as follows:

1. Extract 45 Iron Ore/min from the world.
2. Use 1.5 Smelters to smelt the 45 Iron Ore/min into 45 Iron Ingot/min.
3. Use 1.5 Constructors to craft 45 Iron Ingot/min into 30 Iron Plate/min.

**Note:** The 1.5 [Building] notation is used to denote the use of 1.5 times the full production capacity of a single building instance. For example:

- One Smelter overclocked to 150%
- One Smelter at 100%, one Smelter downclocked to 50%
- Two Smelters downclocked to 75%
- Any other mathematically equivalent solution

can be used to satisfy the rate requirement.

### Future Plans:

1. Reuse of recipes already selected by the user during the crafting tree. 
   - This will likely be the default behavior of the utility. 
   - A command line flag will be made available for users wishing to construct more complex factories, and will be asked to make a selection for every encountered recipe.
2. Saving of generated crafting trees locally, and being able to fetch and see saved trees freely.
3. Addition of item transport guidelines such as the Mk. of conveyors or pipes required for each connection.
4. Scaling of crafting trees according to user-selected input constraints. 
   - For example, if a generated crafting tree requires a larger amount of resources than what the user is able to provide, the crafting tree will be able to be entirely adjusted based on the specified resource.
5. Optimization of crafting trees towards minimizing either power use or any chosen input the user considers limiting. 
   - This includes the use of alternate recipes that will either remove the chosen input or maximally reduce the amount the chosen input used.
6. Walkthrough mode to select what recipes should be offered during crafting tree construction, to allow the users to select their favorite recipes once and not have to worry about making numerous selections during the construction of each crafting tree.
7. And in typical software development fashion, more tests and overall polish.

### Update History:

- Version 1.0.0 released.
