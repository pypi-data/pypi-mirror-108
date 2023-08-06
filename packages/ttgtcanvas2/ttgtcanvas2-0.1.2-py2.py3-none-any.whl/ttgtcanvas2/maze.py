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
        self.model = WorldModel(self, kwargs)
        self.robots = [Robot(idx, x, self) for idx, x in enumerate(self.model.robots)]


        display(self)
        _time.sleep(1)

        self.js_call('draw_all', [
            self.model.rows, 
            self.model.cols, 
            self.model.walls,
            self.options.get("robots", []),
            self.model.objects
        ])
    
    def bot(self, bot_index=0):
        return self.robots[bot_index]
    
    def check(self, bot_index=0):
        val = self.model.check(self.bot(bot_index))
        if val:
            self.js_call('msg', ['Task Completed'])
        else:
            self.js_call('error', ["One Or More Goal are Not Completed."])
        return val

