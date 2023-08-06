_directions = [(1,0), (0,1), (-1,0), (0,-1)]

dir_names = ["east", "north","west", "south"]

from .models.world_model import print_success, print_error
import time as _time

class Robot():
    def __init__(self, index, robot_model, world):
        self.model = robot_model
        self.world_model = world.model
        self.world = world
        self.index = index
        self.collections = {}
        self.speed  = 0.5
 
    @property
    def x(self):
        return self.model.x
    
    @property
    def y(self):
        return self.model.y
    
    @property
    def dir(self):
        return self.model.orientation
    
    @dir.setter
    def dir(self, value):
        self.model.orientation = value

    @x.setter
    def x(self,value):
        self.model.x = value
    
    @y.setter
    def y(self, value):
        self.model.y = value
    
    def move(self, step=1):
        for x in range(step):
            self._move()
        self.world.js_call('move_to',[self.index, self.x, self.y])
        _time.sleep(self.speed)
    
    def _move(self):
        if self.front_is_clear():
            xx, yy = _directions[self.dir]
            self.x += xx
            self.y += yy
        else:
            print_error("Opps You Hit the walls") 
            self.world.js_call('error', ['Opps You Hit the wall'])
    
    def front_is_clear(self):
        return self.world_model.is_clear(self.x, self.y, self.dir)
    
    def turn_left(self):
        self.dir = (self.dir + 1) % 4
        self.world.js_call('turn_left', [self.index])
    
    def is_front_clear(self):
        return self.world_model.is_clear(self.x, self.y, self.dir)
    
    def right_is_clear(self):
        return self.world.model.is_clear(self.x, self.y, (self.dir + 3) % 4)
    
    def wall_on_right(self):
        return not self.right_is_clear()
    
    def wall_on_front(self):
        return not self.is_front_clear()
    
    def cell(self):
        return self.world_model.cells[self.x - 1][self.y - 1 ]

    def build_wall(self):
        
        if self.is_front_clear():
            self.cell().add_wall(self.dir, self.world.js_call)
        else:
            print_error("Wall Already exists")
            self.world.js_call("error", ["Wall already exists"])
    
    def remove_wall(self):
        if not self.is_front_clear():
            self.cell().remove_wall(self.dir, self.world.js_call)
        else:
            print_error("No Wall exists")
            self.world.js_call("error", ["No Wall exists"])


    def set_trace(self, color='red'):
        self.world.js_call('set_trace', [self.index, color])
    
    def set_speed(self, speed=0.1):
        self.speed = speed
        self.world.js_call('set_speed', [self.index, speed])
    
    def has_object(self, obj_name = None):
        objs = self.collections.values()
        if len(objs) > 0:
            if obj_name is None:
                return True
            else:
                fobjs = filter(lambda x, y: x == obj_name, objs)
                return sum(fobjs.values)
        else: 
            return False

    
    def on_object(self, obj_type=None):
        k = "{},{}".format(self.x,self.y)
        obj = self.world_model.objects.get(k, None)
        valid_type = True
        if obj is not None and obj_type is not None:
            obj_name = next(iter(obj))
            valid_type =  obj_name == obj_type

        return  obj is not None and valid_type and obj != self.collections.get(k, None) 
    
    def pick(self, obj_type=None):
        if self.on_object(obj_type):
            ck = "{},{}".format(self.x,self.y)
        
            obj = self.world_model.objects.get(ck, None)
            if obj is not None:
                for k, val in obj.items():
                    collection = self.collections.get(ck, {})
                    picked = collection.get(k, 0)
                    picked = picked + 1
                    collection[k] = picked
                    self.collections[ck] = collection
                    if val == picked:
                        self.world.js_call('remove_object', [self.x,self.y])
                    if val > picked:
                        self.world.js_call('update_object', [self.x, self.y, val - 1])
        else:
            print_error("No Items to Pick.")
            self.world.js_call('error', ["No Items to Pick"])

