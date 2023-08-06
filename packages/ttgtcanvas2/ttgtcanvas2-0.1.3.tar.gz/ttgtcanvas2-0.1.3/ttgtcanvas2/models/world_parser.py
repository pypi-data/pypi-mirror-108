import random
from .goal import Goal
class WorldParser:

    def __init__(self, world, config):
        self.world = world
        self.config = config
        #parse files
        self.parse_dimensions()
        self.parse_walls()
        self.parse_robots()
        self.parse_objects()
        self.parse_goals()
        self.parse_description()

    def parse_dimensions(self):
        self.world.set_dimensions(self.config["rows"], self.config["cols"])

    def parse_walls(self):
        walls = self.config.get("walls", {})
        for pos, wall in walls.items():
            for direction in wall:
                self.world.add_wall(pos, direction)

    def parse_objects(self):
        objects = self.config.get('objects', {})
        for pos, obj in objects.items():
            for obj_name, val in obj.items():
                parsed_val = self.parse_val(val)
                self.world.add_object(pos, obj_name, parsed_val)

    def parse_val(self, value):
        if isinstance(value, list):
            #eg [1,3,5]
            return random.choice(value)
        elif isinstance(value, str) and "-" in value:
            #eg "1-10"
            min_val, max_val = map(int, value.split("-"))
            return random.randint(min_val, max_val)
        else:
            return int(value)

    def parse_robots(self):
        robots = self.config.get('robots', [])
        for robot in robots:
            x = robot.get('x')
            y = robot.get('y')
            positions = robot.get('possible_initial_positions', None)
            if positions is not None and isinstance(positions, list) and len(positions) > 0:
                x, y = random.choice(positions)
            
            self.world.add_robot(x, y, robot.get('_orientation', 0), robot.get('_traceColor', 'red'))


    def parse_goals(self):
        goals = self.config.get('goal', {})

        self.add_position_goal(goals)
        self.add_wall_goals(goals.get('walls', {}))
        self.add_object_goals(goals.get('objects',{}))

    def add_position_goal(self, goals):
        position_goal = goals.get('possible_final_positions', [])
        if len(position_goal) > 0:
            x,y = random.choice(position_goal)
            self.world._add_goal('position', {"x": x, "y": y})
        elif goals.get('position', None) is not None:
            self.world._add_goal('position', goals.get('position', None))
    
    def add_wall_goals(self, walls = {}):
        for xy, wall in walls.items():
            self.world._add_goal('wall', {"xy": xy , "walls": wall})
        
    
    def add_object_goals(self, objects = {}):
        for xy, obj in objects.items():
            for obj_name, val in obj.items():
                self.world._add_goal('object', {"xy": xy, "val": val, "obj_name": obj_name})

    def parse_description(self):
        self.world.add_description(self.config.get("description"))


