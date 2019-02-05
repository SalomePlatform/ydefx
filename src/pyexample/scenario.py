# -*- coding: utf-8 -*-
import pydefx
import os

myParams = pydefx.Parameters(resource="localhost",nb_branches=2);
#wd = os.path.join(myParams.salome_parameters.work_directory, "minifixtest")
#myParams.salome_parameters.local_directory = "/toto/titi/tata"

myScript = pydefx.PyScript()
myScript.loadFile("scenario_study.py")

mySample = myScript.CreateEmptySample()
print(mySample.getInputNames())
print(mySample.getOutputNames())

mySample.setInputValues({ "x":[0.1, 0.2, 0.3, 0.4, 0.5],
                          "y":[1.0, 2.0, 3.0, 4.0, 5.0],
                          "z":["a", "b", "c", "d", "e"]})

myStudy = pydefx.PyStudy(myScript.script, mySample, myParams)
myStudy.run()
