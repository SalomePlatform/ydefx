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
import csv
from enum import Enum

class SampleException(Exception):
  pass

class PointState(Enum):
  """
  Is the point evaluated?
  """
  NO    = 1
  YES   = 2
  ERROR = 3

class Sample:
  def __init__(self, input_names, output_names):
    """
    input_names  : gives the names and the order of input variables
    output_names : gives the names and the order of output variables
    """
    if len(input_names) < 1 :
      SampleException("A sample should have at least one input variable.")
    self._input_names  = input_names
    self._output_names = output_names
    self._input={}
    self._output={}   # {output_name:[output_values]}
    self._messages=[] # list. Possible values in the list:
                      #        None = point not evaluated,
                      #          "" = results available, no error
                      # "any string"= error message for that index.
  
  def __iter__(self):
    return Dico_iter(self._input)
  
  def inputIterator(self):
    """
    Iterate over input values.
    """
    return Dico_iter(self._input)

  def setInputValues(self, inputDict):
    if len(inputDict) != len(self._input_names):
      raise SampleException("Incorrect number of keys!")
    size = None
    for name in self._input_names:
      if size is None:
        size = len(inputDict[name])
      else:
        if size != len(inputDict[name]):
          raise SampleException("Inconsistency in input variable sizes!")
    self._input = inputDict
    # Fill all results with None
    self._messages = [ None for i in range(size)]
    self._output.clear()
    for name in self._output_names :
      self._output[name] = [ None for i in range(size)]

  def addResult(self, index, out_values, message):
    """
    Add results for index.
    """
    if message is None:
      message = ""
    if message :
      # case of error
      for name in self._output_names :
        self._output[name][index] = None
    else:
      for name in self._output_names :
        self._output[name][index] = out_values[name]
      
    self._messages[index] = message

  def getPointState(self, index):
    message = self._messages[index]
    if message is None:
      return PointState.NO
    elif message:
      return PointState.ERROR
    else:
      return PointState.YES

  def findFirstId(self, in_values):
    """
    Find the index of the first point in the sample which contains exactly the
    same input values as in in_values.
    in_values is a dictionary with {name : value} of input variables in one
    point.
    """
    if self._input_names is None or len(self._input_names) == 0 :
      raise SampleException("List of input variables not defined.")
    firstName = self._input_names[0]
    maxSize = len(self._input[firstName])
    curId = 0
    foundId = -1
    for curId in range(maxSize):
      if self.isValidId(self, curId, in_values) :
        foundId = curId
        break
    return foundId
    

  def isValidId(self, idToCheck, inputToCheck):
    """
    Verify the input values at the idToCheck position are exactly the same as
    the values in inputToCheck. Return True or False.
    """
    ok = True
    try:
      for name in self._input_names:
        if self._input[name][idToCheck] != inputToCheck[name] :
          ok = False
          break
    except:
      ok = False
    return ok

  def checkId(self, idToCheck, inputToCheck):
    """
    Verify the input values at the idToCheck position are exactly the same as
    the values in inputToCheck. Raise SampleException if it is not the case.
    """
    for name in self._input_names:
      if not name in self._input:
        raise SampleException(
          "Variable name {} expected and not found ".format(name))
      if self._input[name][idToCheck] != inputToCheck[name] :
        raise SampleException(
          "Expected value for variable {} is {} and found {}".format(name,
                                                  self._input[name][idToCheck],
                                                  inputToCheck[name]))

  def getInputNames(self):
    return self._input_names

  def getOutputNames(self):
    return self._output_names

  def progressRate(self):
    numberOfPoints = len(self._messages)
    unevaluatedPoints = self._messages.count(None)
    result = 0.0
    if(numberOfPoints > 0):
      result = 1.0 - unevaluatedPoints / numberOfPoints
    return result

  def __str__(self):
    result = ""
    for name in self._input_names:
      result += name+","
    for name in self._output_names:
      result += name+","
    result += "messages\n"
    for i in range(len(self._messages)):
      for name in self._input_names:
        result += repr(self._input[name][i]) +","
      for name in self._output_names:
        result += repr(self._output[name][i]) +","
      result += str(self._messages[i])+"\n"
    return result

class Dico_iter:
  """
  >>> si=Dico_iter({"x":[1,2,3], "y":["a","b","c"]})
  >>> for i in si:
  >>>   print(i)
  {'x': 1, 'y': 'a'}
  {'x': 2, 'y': 'b'}
  {'x': 3, 'y': 'c'}
  """
  def __init__(self, s):
    self.iters={}
    for k, v in s.items():
      self.iters[k] = iter(v)

  def __iter__(self):
    return self

  def __next__(self):
    result = {}
    for k,v in self.iters.items():
      result[k] = next(v)
    return result
