#!/usr/bin/env python
# coding: utf-8
import json
from ttgtcanvas2 import WorldModel, Maze

def init(world):
    print("details")

def generate_maze():
    world =  WorldModel('./worlds/test.json', init)
    return Maze(world)
    



