class Material:
    def __init__(self, name, properties=None):
        # A material has a name and properties
        # properties should be a list or dictionary with useful information (like radiactivity, flammability, stuff that impacts how it would get treated basically)
        self.name = name
        self.properties = properties or {}

    def get_properties(self):
        return {
            "name": self.name,
            **self.properties
        }
        

    def __str__(self):
        return f"Material: {self.name}, Properties: {self.properties}"

class Recipe:
    def __init__(self, name, inputs, outputs, process_time=None, specifications=None):
        # A recipe has a name, inputs, and outputs
        # inputs and outputs should be dictionaries with material names as keys and quantities as values
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.specifications = specifications or {} # basically if only one machine can make this
        self.process_time = process_time

class Machine:
    def __init__(self, name, recipes=None, specifications=None, inventory=None):
        # A machine has a name and can have multiple recipes
        self.name = name
        self.recipes = recipes or []
        self.specifications = specifications or {} # properties/things the machine can do
        self.busy = False  # Indicates if the machine is currently processing a recipe
        self.process_time = 0  # Total time required for the current recipe
        self.inventory = inventory or Inventory()  # Each machine has its own inventory, so we can add materials to it to queue

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def get_recipes(self):
        return self.recipes

    def __str__(self):
        return f"Machine: {self.name}, Recipes: {[recipe.name for recipe in self.recipes]}, Specifications: {self.specifications}"
    
    def start_processing(self, recipe):
        if recipe in self.recipes and not self.busy and all(self.inventory.get(material) >= amount for material, amount in recipe.inputs.items()):
            self.busy = True
            self.process_time = recipe.process_time
            self.inventory.remove_materials(recipe.inputs)  # Remove input materials from inventory

        else:
            raise ValueError(f"Recipe {recipe.name} not available for machine {self.name}")

        
class Inventory:
    def __init__(self):
        self.items = {}

    def add(self, material, amount):
        self.items[material] = self.items.get(material, 0) + amount #adding the amount to the existing amount of the material in the inventory, or initializing it if it doesn't exist yet

    def remove(self, material, amount):
        if self.items.get(material, 0) >= amount:
            self.items[material] -= amount
        if self.items[material] == 0:
            del self.items[material]
        else:
            self.items[material] = 0  # If not enough material, set to 0

    #TODO: implement a method to check if inventory is too full (maybe at a certain number of items or a weight/size limit)

    def get(self, material):
        return self.items.get(material, 0)

    
