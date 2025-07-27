from ..api import objects, materials
import random

class ProceduralGenerator:
    """
    Handles procedural generation tasks based on high-level commands.
    """
    def __init__(self, config):
        self.config = config

    def execute(self, command):
        """Executes a procedural generation command."""
        if command['task'] == 'create_random_cubes':
            self.create_random_cubes(**command['params'])

    def create_random_cubes(self, count=10, area_size=20):
        """Creates a number of cubes in a random layout."""
        for i in range(count):
            location = (random.uniform(-area_size, area_size),
                        random.uniform(-area_size, area_size),
                        random.uniform(0, area_size / 2))
            objects.create_primitive('CUBE', location=location)