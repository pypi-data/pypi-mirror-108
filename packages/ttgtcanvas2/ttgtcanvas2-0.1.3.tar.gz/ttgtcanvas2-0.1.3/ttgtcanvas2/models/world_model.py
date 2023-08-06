from .robot_model import RobotModel
from .world_parser import WorldParser

from IPython.display import HTML as html_print
from IPython.display import display

import os.path
import json

from .goal import class_list, Goal 

def cstr(s, color='black'):
    return "<text style=color:{}>{}</text>".format(color, s)

def print_success(msg, color="green"):
    if msg is not None:
        display(html_print(cstr("✓ {}".format(msg), color=color))) 

def print_error(error):
    if error is not None:
        display(html_print(cstr("✗ {}".format(error), color="red")))


class WorldModel():
    def __init__(self, path=None, initFn= None):
        self.walls = {}
        self.objects = {}
        self.robots = []
        self.added_walls = []
        self.errors = []
        self.goals = []
        self.description= None
        self.rows = 10
        self.cols = 10

        if path is not None:
            data = self.load_json(path)
            self.parser = WorldParser(self, data)
        
        if initFn is not None and callable(initFn):
            initFn(self)
    
    def load_json(self, path):
        f = open(path, "r")
        data = json.loads(f.read())
        f.close()
        return data
    
    def js_call(self, call_js_fn=None, method_name=None, params=[]):
        if call_js_fn is not None and callable(call_js_fn):
            call_js_fn(method_name, params)
    
    def set_dimensions(self, rows = 10, cols = 10):
        self.rows = rows
        self.cols = cols
    
    def add_description(self, desc):
        self.description = desc
    
    def add_wall(self, xy, direction, call_js=None):
        val = self.walls.get(xy,[])

        if direction in ["north", "east"]:
            val.append(direction)
        else:
            raise "Invalid wall direction"

        self.walls[xy] = val
        if call_js is not None:
            x, y = xy.split("-")
            self.added_walls[xy] = val
            self.js_call('add_wall', [x, y, dir])
    
    def add_object(self, pos, obj_name, val):
        obj = {}
        obj[obj_name] = val
        self.objects[pos] = obj

    def add_robot(self, x, y, orientation, traceColor):
        self.robots.append(RobotModel(x, y , orientation, traceColor))
    
    def add_goal(self, goal):
        if isinstance(goal, tuple(class_list.values())):
            self.goals.append(goal)
        else:
            raise "Not a valid goal class"

    def _add_goal(self, goal_type,  config):        
        goal = Goal.load(goal_type, config)
        self.add_goal(goal)


    def dimensions(self):
        return [self.rows, self.cols]
    
    def is_clear(self, x, y, dir):
        return not self.is_wall(x,y, dir) and not self.is_border(x, y, dir)

    
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
        sucess = True
        for goal in self.goals:
            if not goal.is_completed(bot, self):
                sucess = False
                print_error(goal.msg())
            
        return sucess

    def render_all(self, js_call=None):
        self.js_call(js_call, 'draw_all', [
            self.rows,
            self.cols,
            self.walls,
            [r.toJSON() for r in self.robots],
            self.objects
        ])


    

