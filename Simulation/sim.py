from creation import Material
from creation import Recipe
from creation import Machine
from creation import Inventory

class Sim:
    def __init__(self, time_naught=None, time_step=None, materials=None, machines=None, recipes=None):
        self.materials = materials or []
        self.machines = machines or []
        self.recipes = recipes or []

        self.itime = time_naught if time_naught is not None else 0
        self.dt = time_step if time_step is not None else 1
        self.time = self.itime

        """We have to do all of the """

    def update_state(self):
        for machine in self.machines:
            machine.process()  # Process the machine for the current time step


    def add(self, material=None, machine=None, recipe=None):
        self.materials.append(material)
        self.machines.append(machine)
        self.recipes.append(recipe)

    def step(self):
        # Perform a single step of the simulation
        self.update_state()
        self.time += self.dt

        # when we implement stochastic events, these should go here I think

    def run(self, steps):
        # Run the simulation for a specified number of steps
        for t in range(steps):
            self.step()
            

sim = Sim()
iron_ore = Material("Iron_ore")
iron_ingot = Material("Iron_ingot")
gear = Material("Gear")

smelter = Machine("Smelter")
gear_cutter = Machine("Gear_cutter")
robot_maker = Machine("Robot_maker")

iron_ingot_recipe = Recipe("Iron_ingot", inputs={iron_ore: 1}, outputs={iron_ingot: 1}, process_time=5)
gear_recipe = Recipe("Gear", inputs={iron_ingot: 2}, outputs={gear: 1}, process_time=10)
robot_recipe = Recipe("Robot", inputs={gear: 5, iron_ingot: 10}, outputs={"Robot": 1}, process_time=20)


sim.add(material=iron_ore, machine=smelter, recipe=iron_ingot_recipe)
sim.add(material=iron_ingot, machine=gear_cutter, recipe=gear_recipe)
sim.add(material=gear, machine=robot_maker, recipe=robot_recipe)


sim.machines[0].add_recipe(iron_ingot_recipe)  # Add the Iron_ingot recipe to the Smelter
sim.machines[0].add_material(iron_ore, 10)  # Add some Iron_ore to the Smelter's inventory
print(f"Initial inventory of {sim.machines[0].name}: {sim.machines[0].inventory.items}")
sim.machines[0].start_processing(sim.machines[0].recipes[0])  # Start processing the Iron_ingot recipe in the Smelter
sim.run(steps=10)