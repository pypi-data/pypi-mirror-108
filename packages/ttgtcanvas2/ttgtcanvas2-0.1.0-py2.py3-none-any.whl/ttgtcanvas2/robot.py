class Robot():
    def __init__(self, robot_model):
        self.model = robot_model
 
    @property
    def x(self):
        return self.model.x
    
    @property
    def y(self):
        return self.model.y

    @x.setter
    def x(self,value):
        self.model.x = value
    
    @y.setter
    def y(self, value):
        self.model.y = value