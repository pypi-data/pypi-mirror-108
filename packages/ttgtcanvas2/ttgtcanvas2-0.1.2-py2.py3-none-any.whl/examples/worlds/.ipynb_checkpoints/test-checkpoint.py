#!/usr/bin/env python
# coding: utf-8
import json

def load_world():
    f = open('./worlds/test.json', "r")
    data= json.loads(f.read())
    f.close()
    return data



