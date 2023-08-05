#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Indresh Vishwakarma.
# Distributed under the terms of the Modified BSD License.

from ipywidgets import DOMWidget
from traitlets import Unicode
from ._frontend import module_name, module_version

import time as _time
from datetime import datetime
import json



from .models import WorldModel, RobotModel
from .robot import Robot


class Maze(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('MazeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('MazeView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    current_call  = Unicode('{}').tag(sync=True)
    method_return = Unicode('{}').tag(sync=True)


    def js_call(self, method_name, params): 
        # print("calling method: " + method_name)
        cb = datetime.now().strftime('%f')
        self.current_call = json.dumps({'method_name': method_name, 'params': params, 'cb': cb})
    
    def __init__(self, kwargs):
        super(Maze, self).__init__()
        self.options = kwargs
        self.model = WorldModel(kwargs)
        self.robots = [Robot(x) for x in self.model.robots]


        display(self)
        _time.sleep(1)

        self.js_call('draw_all', [
            self.model.rows, 
            self.model.cols, 
            self.model.walls,
            self.options.get("robots", [])
        ])
    
    def bot(self, bot_index=0):
        return self.robots[bot_index]



    
    # def __init__(self, **kwargs):
    #     super(Maze, self).__init__(**kwargs)
    #     options = {"avenues": 10, "streets": 10, "beepers": {}, "walls": [], "robot": (8, 1, 'E', 0), "flags": []}
    #     options.update(kwargs)

    #     self._beepers = options["beepers"]
    #     self._flags = options["flags"]
    #     self.av = options["avenues"]
    #     self.st = options["streets"]
    #     self.robot = options["robot"] 
    #     self.width = self.av * 50
    #     self.height = self.st * 50
    #     self.num_cols = 2*self.av + 1
    #     self.num_rows = 2*self.st + 1
    #     self.walls = options["walls"]
    #     self._bot = None
    #     for (col, row) in self.walls:
    #         if not (col+row) % 2:
    #             raise RuntimeError("Wall in impossible position (%d, %d)." % (col,row))
    #     self.borders = []
    #     self.set_borders()
        
    #     display(self)
    #     _time.sleep(1)

    #     self.init()

    # def set_borders(self):
    #     """The world is surrounded by a continuous wall.  This function
    #         sets the corresponding "wall" or "border" based on the world's
    #         dimensions."""
    #     for col in range(1, self.num_cols-1, 2):
    #         if (col, 0) not in self.borders:
    #             self.borders.append( (col, 0) )
    #         if (col, self.num_rows) not in self.borders:
    #             self.borders.append( (col, self.num_rows-1) )
    #         for row in range(1, self.num_rows-1, 2):
    #             if (0, row) not in self.borders:
    #                 self.borders.append( (0, row) )
    #             if (self.num_cols, row) not in self.borders:
    #                 self.borders.append( (self.num_cols-1, row) )
    
    # def cr2xy(self, col, row):
    #     x = self.left + self.ts * col
    #     y = self.bottom - self.ts * row
    #     return x, y
    
    # def toggle_wall(self, col, row):
    #     """This function is intended for adding or removing a
    #         wall from a GUI world editor."""
    #     if (col+row) % 2 :  # safety check
    #         if (col, row) in self.walls: # toggle value
    #             self.walls.remove((col, row))
    #         else:
    #             self.walls.append((col, row))
    #     else:
    #         raise RuntimeError("Wall in impossible position (%d, %d)." % (col,row))

    # def is_clear(self, col, row):
    #     """Returns True if there is no wall or border here."""
    #     return not ((col, row) in self.walls or (col, row) in self.borders)
    
    # def _create_beeper(self, av, st):
    #     num = self.beepers[(av, st)]
    #     bp = _Beeper(self, 0.6 * self.ts, av, st, num)
    #     self.beeper_icons[(av, st)] = bp
    #     return bp
        


    # def init(self, src='./robot-design.svg'):
    #     self.beepers = self._beepers.copy()
    #     self.flags = self._flags.copy()
    #     self.total_flags = self.flags_count()
    #     self.total_beepers = self.beepers_count()
    #     self.beeper_icons = {}
    #     tsx =  self.width / (self.num_cols + 2)
    #     tsy =  self.height / (self.num_rows + 2)
    #     self.ts = min(tsx, tsy)
    #     self.left = 2 * self.ts
    #     self.right = self.left + 2 * self.ts * self.av
    #     self.bottom = self.height - 2 * self.ts
    #     self.top = self.bottom - 2 * self.ts * self.st


    #     #UI Add layer
    #     ##Add Beepers
    #     _beepers = []
    #     for (av, st) in self.beepers:
    #         _beeper = self._create_beeper(av, st)
    #         _beepers.append({'key':[av, st], 'value': _beeper.num})
        
    #     self.js_call('draw_grid', [self.width, self.height, self.av, self.st,  self.ts, self.walls, _beepers, self.flags, self.robot])

    #     self.init_robot(src)
    #     # add_robot
    #     return self

    # def move_to(self, rindex , x, y):
    #     self.js_call('move_to', [rindex, x,y])
    #     _time.sleep(0.1)
    #     if self._bot.on_flag():
    #         self._bot.pick_flag()

    # def add_point(self, rindex ,  x, y):
    #     self.js_call('add_point', [rindex, x,y])
    
    # ##init robot
    # def init_robot(self, src):
    #     avenue, street, orientation, beepers = self.robot
    #     self.js_call('add_robot', [0, src, avenue, street,'E', beepers])
    #     self._bot  =  self._bot or Robot()
    #     self._bot.init(self, avenue, street, 'E', beepers, 0)
    #     self.js_call('init_robot', [0])
    #     self._bot._update_pos()

    #     if _to_rotate[orientation] > 0 :
    #         for x in range(_to_rotate[orientation]):
    #             self._bot.turn_left()
    #     return self._bot

    # def bot(self):
    #     return self._bot

    # def remove_trace(self, rindex):
    #     self.js_call("remove_trace", [rindex])
    
    # def set_pause(self, rindex,  delay):
    #     self.js_call('set_pause', [rindex, delay])
    
    # def set_trace(self, rindex, x,y, color):
    #     self.js_call('set_trace', [rindex, x, y, color])
    
    # def set_number(self, beeper):
    #     self.js_call('set_beeper_number', [beeper.av, beeper.st, beeper.num])

    # def rotate_left(self, rindex):
    #     self.js_call('rotate_left', [rindex])

    # def beepers_count(self):
    #     return len(self.beepers)

    # def flags_count(self):
    #     return len(self.flags)
    
    # def check(self):
    #     ret = (self.beepers_count() == 0) and (self.flags_count() == 0)
    #     if ret == True:
    #         self.js_call('success_msg', ["Congrats, Task Completed."])
    #     else:
    #         self.js_call('failed_msg', ["Oops, Task Failed."])
    #     return ret

    # def add_beeper(self, av, st):
    #     x, y = self.cr2xy(2 * av - 1, 2 * st - 1)
    #     """Add a single beeper."""
    #     if (av, st) in self.beepers:
    #         self.beepers[(av, st)] += 1
    #         bp = self.beeper_icons[(av,st)]
    #         bp.set_number(self.beepers[(av, st)])
    #         self.js_call('update_beeper', [av, st, self.beepers[(av, st)]])
    #     else:
    #         self.beepers[(av, st)] = 1
    #         self._create_beeper(av, st)
    #         self.js_call('add_beeper', [av, st, x, y, self.beepers[(av, st)]])

    # def remove_beeper(self, av, st):
    #     """Remove a beeper (does nothing if no beeper here)."""
    #     x, y = self.cr2xy(2 * av - 1, 2 * st - 1)
        
    #     if (av, st) in self.beepers:
    #         self.beepers[(av, st)] -= 1
    #     if self.beepers[(av, st)] == 0:
    #         del self.beepers[(av, st)]
    #         del self.beeper_icons[(av,st)]
    #         self.js_call('remove_beeper', [av, st])
    #     else:
    #         bp = self.beeper_icons[(av,st)]
    #         bp.set_number(self.beepers[(av, st)])
    #         self.js_call('update_beeper', [av, st, self.beepers[(av, st)]])
    

    # def remove_flag(self, av, st):
    #     if (av, st) in self.flags:
    #         _flag_index = self.flags.index((av, st))
    #         self.flags.pop(_flag_index)
    #         self.js_call('remove_flag', [av, st])
    
    # def add_flag(self, av, st):
    #     x, y = self.cr2xy(2 * av - 1, 2 * st - 1)
    #     if not ((av, st) in self.flags):
    #         self.flags.append((av, st))
    #         self.js_call('add_flag', [av, st, x, y])

