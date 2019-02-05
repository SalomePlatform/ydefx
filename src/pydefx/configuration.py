import salome
import tempfile
import pathlib

def defaultWorkingDir(resource):
  resManager= salome.lcc.getResourcesManager()
  resource_definition = resManager.GetResourceDefinition(resource)
  return resource_definition.working_directory

def defaultNbBranches(resource):
  resManager= salome.lcc.getResourcesManager()
  resource_definition = resManager.GetResourceDefinition(resource)
  ret = resource_definition.nb_node
  if ret < 1:
    ret = 1
  return ret

def defaultBaseDirectory():
  """Return the default path to the root of any new result directory."""
  return str(pathlib.Path.home())

def newResultDirectory(basedir=None):
  """ A new directory is created and the path is returned."""
  if basedir is None :
    basedir = defaultBaseDirectory()
  return tempfile.mkdtemp(prefix='idefix',dir=basedir)

def defaultWckey(resource="localhost"):
  result = ""
  if resource != "localhost":
    result = "P11U5:CARBONES"
  return result

