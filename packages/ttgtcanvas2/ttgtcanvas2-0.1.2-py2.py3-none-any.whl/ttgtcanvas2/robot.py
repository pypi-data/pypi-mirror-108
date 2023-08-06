_directions = [(1,0), (0,1), (-1,0), (0,-1)]

dir_names = ["east", "north","west", "south"]

from .models.world_model import print_success, print_error

class Robot():
    def __init__(self, index, robot_model, world):
        self.model = robot_model
        self.world_model = world.model
        self.world = world
        self.index = index
        self.collections = {}
 
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
    
    def wall_in_front(self):
        return not self.is_front_clear()

    def build_wall(self):
        if self.world_model.is_clear(self.x, self.y, self.dir):
            if self.dir == 0:
                self.world_model.add_wall(self.x, self.y, "east")
            if self.dir == 1:
                self.world_model.add_wall(self.x, self.y, "north")
            if self.dir == 2:
                self.world_model.add_wall(self.x - 1, self.y, "east")
            if self.dir == 3:
                self.world_model.add_wall(self.x, self.y - 1, "north")
        else:
            print_error("Wall Already exists")
            self.world.js_call("error", ["Wall already exists"])

    def set_trace(self, color='red'):
        self.world.js_call('set_trace', [self.index, color])
    
    def on_object(self):
        k = "{},{}".format(self.x,self.y)
        obj  = self.world_model.objects.get(k, None)
        return  obj is not None and obj != self.collections.get(k, None)
    
    def pick(self):
        if self.on_object():
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

