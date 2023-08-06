from .robot_model import RobotModel

from IPython.display import HTML as html_print
from IPython.display import display

def cstr(s, color='black'):
    return "<text style=color:{}>{}</text>".format(color, s)

def print_success(msg):
    if msg is not None:
        display(html_print(cstr("✓ {}".format(msg), color="green"))) 

def print_error(error):
    if error is not None:
        display(html_print(cstr("✗ {}".format(error), color="red")))


class WorldModel():
    def __init__(self, ui,kwargs):
        self.walls = kwargs.get('walls', {})
        self.robots_config = kwargs.get('robots', [])
        self.goals = kwargs.get('goal', {})
        self.objects = kwargs.get('objects', {})
        self.ui = ui
        self.added_walls = {}
        self.errors = []
        self.set_dimensions(kwargs)
        self.init_robots(self.robots_config)


    def init_robots(self, robots=[]):
        self.robots = [RobotModel(robot) for robot in robots]

    def set_dimensions(self, options={}):
        self.rows = options.get('rows',10)
        self.cols = options.get('cols', 10)
    
    def dimensions(self):
        return [self.rows, self.cols]
    
    def is_clear(self, x, y, dir):
        return not self.is_wall(x,y, dir) and not self.is_border(x, y, dir)
    
    def add_wall(self, x, y, dir):
        key = "{},{}".format(x,y)
        val = self.walls.get(key,[])
        val.append(dir)
        self.walls[key] = val
        self.added_walls[key] = val
        self.ui.js_call('add_wall', [x,y, dir])

    
    def is_wall(self, x, y, dir):
        wall =  self.walls.get("{},{}".format(x,y), [])
        if dir == 0 and "east" in wall:
            return True 
        if dir == 1 and "north" in wall: #north
            return True 

        wall =  self.walls.get("{},{}".format(x - 1 , y), [])
        if dir == 2 and "east" in wall:
            return True 

        wall =  self.walls.get("{},{}".format(x,y -1), [])
        if dir == 3 and "north" in wall: #south
            return True 
        return False

    def is_border(self, x,y, dir):
        if dir == 0 and x == self.cols : #east
            return True 
        if dir == 1 and y == self.rows : #north
            return True 
        if dir == 2 and x - 1 == 0 : #west
            return True 
        if dir == 3 and y - 1 == 0 : #south
            return True 
        return False
    
    def check(self, bot):
        msg = self.position_goals_msg()
        sucess = True
        if not self.valid_position(bot):
            print_error(msg)
            sucess = False
        else:
            print_success(msg)

        msg = self.wall_goals_msg()
        if not self.all_walls_builded(bot):
            print_error(msg)
            sucess = False
        else:
            print_success(msg)

        msg = self.objects_goals_msg()
        if not self.all_objects_collected(bot):
            print_error(msg)
            sucess = False
        else:
            print_success(msg)
            
        return sucess

    def position_goals_msg(self):
        msg = None
        final_position = self.goals.get('possible_final_positions', self.goals.get('position', None))
        if final_position is None: 
            return None
        if isinstance(final_position, dict):
            msg = "Reached Final Position: {},{}".format(final_position.get("x"),final_position.get("y"))
        else:
            msg = "Reached One Of the Final Position: {}".format(' or '.join([ "{},{}".format(x,y) for x,y in final_position]))
        return msg
    
    def wall_goals_msg(self):
        walls = self.goals.get('walls', None)
        if walls is None: 
            return None
        return "Build walls at:  {}".format(' or '.join(walls.keys()))
    
    def objects_goals_msg(self):
        objects = self.goals.get('objects', None)
        if objects is None:
            return None
        return "Picked objects at: {}".format(' or '.join(objects.keys()))

    def valid_position(self, bot):
        final_position = self.goals.get('possible_final_positions', self.goals.get('position', None))
        if final_position is None: 
            return True
        
        if isinstance(final_position, dict):
            return final_position.get("x") == bot.x and final_position.get("y") == bot.y
        else:
            coord = [bot.x, bot.y]
            return coord in final_position
    

    def all_walls_builded(self, bot):
        walls = self.goals.get('walls', None)
        if walls is None: 
            return True
        return all(sorted(self.added_walls.get(k, [])) == sorted(v) for k, v in walls.items())
    
    def all_objects_collected(self, bot):
        objects = self.goals.get('objects', None)
        if objects is None:
            return True
        return bot.collections == objects
            


    

