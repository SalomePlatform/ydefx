#!/usr/bin/env python3
#from inspect import currentframe, getframeinfo
#from pathlib import Path

#filename = getframeinfo(currentframe()).filename
#parent = Path(filename).resolve().parent
import inspect
import pathlib

filename = inspect.getframeinfo(inspect.currentframe()).filename
parent = pathlib.Path(filename).resolve().parent
print(parent)
