import unittest
import os
import time

class TestYdefx(unittest.TestCase):
  def test_errors(self):
    """
    Test errors in study script.
    """
    import pydefx

    myScript = pydefx.PyScript()
    myScript.loadString("a=5")
    self.assertIn("not accepted statement", myScript.getErrors())
    
    myScript.loadString("n'importe quoi!")
    self.assertIn("SyntaxError", myScript.getErrors())

    myScript.loadString("")
    self.assertIn("Function _exec not found", myScript.getErrors())
    
    with self.assertRaises(pydefx.pyscript.PyScriptException):
      mySample = myScript.CreateEmptySample()

  def test_availableResources(self):
    import pydefx
    lr = pydefx.configuration.availableResources()
    self.assertIn('localhost', lr) 

if __name__ == '__main__':
    unittest.main()
