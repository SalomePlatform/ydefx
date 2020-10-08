import pydefx
import os

myParams = pydefx.Parameters()
myParams.configureResource("localhost")
#myParams.createResultDirectory("/tmp")
myParams.nb_branches = 4
myParams.salome_parameters.resource_required.nb_proc = 1
#myParams.salome_parameters.result_directory=os.path.join(os.getcwd(),"runbasic")
#myParams.salome_parameters.work_directory="/scratch/I35256/workingdir/test_multijob/"
myParams.salome_parameters.work_directory=os.path.join(os.getcwd(),"runbasic")
myParams.salome_parameters.local_directory = os.getcwd()
#myParams.salome_parameters.in_files=["template_jdd.txt", "mysolver.py"]

#pyScript = os.path.join(os.getcwd(), "mystudy.py")
pyScript = """
def _exec(a,b):
  d = a / b
  return d
"""

myScript = pydefx.PyScript()
#myScript.loadFile(pyScript)
myScript.loadString(pyScript)

mySample = myScript.CreateEmptySample()
#mydata = {"x":range(10)}
mydata = {"a":[x // 10 for x in range(100)],
          "b":[x % 10 for x in range(100)]}
mySample.setInputValues(mydata)

myStudy = pydefx.LocalStudy(schemaBuilder=pydefx.LocalBuilder("lightexecutor"))
myStudy.createNewJob(myScript, mySample, myParams)
myStudy.launch()

myStudy.getJobState()
myStudy.wait()
print(myStudy.getResult())
print(myStudy.sample)
#print(myStudy.global_result)
