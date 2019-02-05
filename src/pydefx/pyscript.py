# -*- coding: utf-8 -*-
# Copyright (C) 2019  EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
from . import sample

class PyScriptException(Exception):
  pass

class PyScript:
  def __init__(self):
    self.script = ""

  def loadFile(self,path):
    with open(path, "r") as f:
      self.script = f.read()

  def loadString(self, script):
    self.script = script

  def saveFile(self, path):
    with open(path, "w") as f:
      f.write(self.script)

  def getAllProperties(self):
    """
    functions,errors = myscript.getAllProperties()
    print(errors)      # list of syntax errors in the script
    for f in functions:
      print(f.name)    # function name
      print(f.inputs)  # list of input variable names
      print(f.outputs) # list of output variable names
      print(f.errors)  # list of py2yacs errors in the function
      print(f.imports) # list of import statements in the function
    """
    import py2yacs
    return py2yacs.get_properties(self.script)

  def getFunctionProperties(self, fname):
    """
    Properties of the _exec function:
    fn_properties, errors = myscript.getExecProperties("_exec")
    fn_properties.name    : "_exec"
    fn_properties.inputs  : list of input variable names
    fn_properties.outputs : list of output variable names
    fn_properties.errors  : list of py2yacs errors in the function
    fn_properties.imports : list of import statements in the function
    errors                : list of syntax errors in the script
    fn_properties is None if the "_exec" function does not exist.
    """
    functions,errors = self.getAllProperties()
    fn_properties = next((f for f in functions if f.name == fname), None)
    return fn_properties, errors

  def CreateEmptySample(self):
    """
    Create a sample with input and output variable names set.
    """
    fn = "_exec"
    fn_properties, errors = self.getFunctionProperties(fn)
    if len(errors) > 0:
      error_string = "global errors:\n"
      error_string += '\n'.join(errors)
      raise PyScriptException(error_string)
    if fn_properties is None:
      raise PyScriptException("Function {} not found!".format(fn))
    if len(fn_properties.errors) > 0:
      error_string = "Errors in function {}:\n".format(fn)
      error_string += '\n'.join(fn_properties.errors)
      raise PyScriptException(error_string)
    return sample.Sample(fn_properties.inputs, fn_properties.outputs)
    
