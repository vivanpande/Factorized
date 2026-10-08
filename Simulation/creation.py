class Material:
    # A class to represent materials, the building block of manufacturing in this game
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
    # a class for recipes, which are the instructions for how to make materials or machines from other materials
    def __init__(self, name, inputs, outputs, process_time=None, active_recipe=None, specifications=None):
        # A recipe has a name, inputs, and outputs
        # inputs and outputs should be dictionaries with material names as keys and quantities as values
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.specifications = specifications or {} # basically if only one machine can make this
        self.process_time = process_time

        self.active_recipes = []  # Track the currently active recipe

class Machine:
    """a class for machines, which are the things that make materials or other machines from recipes
    Eventually, we need to create a way to upgrade machines, so we need to have more specifications
    """
    def __init__(self, name, recipes=None, specifications=None, inventory=None, x=None, y=None, transport=None):
        # A machine has a name and can have multiple recipes
        self.name = name
        self.recipes = recipes or []
        self.specifications = specifications or {} # properties/things the machine can do
        self.transport = transport or []  # a list of transports that the machine can use to move materials in and out of its inventory


        self.busy = False  # Indicates if the machine is currently processing a recipe
        self.active_recipe = None  # Track the currently active recipe
        self.process_time = 0  # Total time required for the current recipe

        self.inventory = inventory or Inventory()  # Each machine has its own inventory, so we can add materials to it to queue
        
        # positional variables for the machine in the world, so we can place it in a 2D space
        self.x = x
        self.y = y

    def place_machine(self, x, y):
        #TODO: Add logic to check if the position is valid (e.g., not occupied by another machine)
        #TODO: Also, add logic to add a making/creating time for the machine (no auto installs)
        self.x = x
        self.y = y

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def add_material(self, material, amount):
        self.inventory.add(material, amount)

    def get_recipes(self):
        return self.recipes

    def __str__(self):
        return f"Machine: {self.name}, Recipes: {[recipe.name for recipe in self.recipes]}, Specifications: {self.specifications}"

    # assumes machine can only make one thing, can't run in parallel
    def start_processing(self, recipe):
        if recipe in self.recipes and not self.busy and all(self.inventory.get(material) >= amount for material, amount in recipe.inputs.items()):
            self.busy = True
            self.process_time = recipe.process_time
            for material, amount in recipe.inputs.items():
                self.inventory.remove(material, amount)  # Remove input materials from inventory
                print("we removed from machine inv correctly")
            print("machine started processing")
            self.active_recipe = recipe  # Set the active recipe

        else:
            raise ValueError(f"Recipe {recipe.name} not available for machine {self.name}")
        
    def process(self):
        if self.busy:
            self.process_time -= 1  # Assuming each step reduces the process time by 1
            if self.process_time <= 0:
                self.busy = False
                for material, amount in self.active_recipe.outputs.items():
                    self.inventory.add(material, amount)
                print(f"Machine {self.name} has finished processing recipe {self.active_recipe.name}. Outputs added to inventory.")
                if transport := self.transport:
                    for t in transport:

                        #TODO: This code is only true in this basic sim, since we need to implement a way to check if the materials
                        #being transported are what we actually want and the directionality of the transporting
                        for material, amount in self.inventory.items():
                            t.transfer(material, amount)
            print(f"Machine {self.name} is processing recipe {self.active_recipe.name}. Time remaining: {self.process_time}")

class Repository:
    # a class for a repository, which is a place in the world where materials can be retrieved
    def __init__(self, materials=None, specifications=None, x=None, y=None):
        self.materials = materials or {}
        self.x = x
        self.y = y
        """ specifications is a dictionary that contains information about the repository, like the quality of materials it outputs, how likely it is to find materials there, etc
        For example, it could have keys like "quality", "rarity", "capacity", etc. and the values would be the corresponding information about the repository.
        We want to procedurally generate different repositories throughout the world at a micro scale
        The quality of a repository should include what materials it outputs and the chance per tick of mining to obtain them (we want it to be stochastic to model the world better)
        Repositories should also be able to be refined or depleted, so we want to have the quality be subject to change
        Maybe for gameplay purposes, we should have them refill themselves automatically?

        A more realistic and perhaps better approach is for them to have a finite amount, and then new repositories get added
        ^^ I think we'll implement this late stages, but for now we'll just have them be infinite and have a quality that can be refined or depleted
        """
        self.specifications = specifications or {}

    def add_material(self, material):
        self.materials[material.name] = material

        
class Inventory:
    """Inventory will be a general class for machine, silo, and player inventories. It will be a dictionary, where items are values and positions are keys
    Methods to move items around in the inventory will need to be implemented so we can easily transfer this to graphics"""
    def __init__(self):
        self.items = {}

    def add(self, material, amount):
        self.items[material] = self.items.get(material, 0) + amount  # adding the amount to the existing amount of the material in the inventory, or initializing it if it doesn't exist yet

    def remove(self, material, amount):
        if self.items.get(material, 0) >= amount:
            self.items[material] -= amount
        if self.items[material] == 0:
            del self.items[material]
        else:
            self.items[material] = 0 # If not enough material, set to 0

    #TODO: implement a method to check if inventory is too full (maybe at a certain number of items or a weight/size limit)

    def get(self, material):
        return self.items.get(material, 0)


    class Transport:
        """Transport is a class for transporting materials between machines, repositories, and other locations in the world. 
        It will have a source and destination, a capacity, and a speed. It will also have specifications for how it operates, 
        like whether it can transport certain materials or not (so like LNG would need a special transport, and transporting 
        by sea would be special too)
        
        The reason we make this a class and not a function is because we want to have these specifications and properties so we can change and access them as we go
        We can have building blocks like conveyer belts that will have one specification, and then we can have more complex transports like trucks that will have more 
        specifications and properties
        
        I think one of the use things we want to have is like a conveyer belt with a "if next to two machines, transport automatically to the other" kind of chain that the player assigns"""

        def __init__(self, source, destination, capacity, speed, specifications=None):
            self.source = source
            self.destination = destination
            self.capacity = capacity
            self.speed = speed
            self.specifications = specifications or {}
            self.rate = capacity * speed  # rate of transport is capacity times speed

        def transfer(self, material, amount):
            if self.source.inventory.get(material) >= amount and amount <= self.capacity:
                self.source.inventory.remove(material, amount)
                self.destination.inventory.add(material, amount)
            else:
                raise ValueError(f"Not enough {material.name} in source inventory or amount exceeds capacity.")

        

    
