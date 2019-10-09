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
from . import salome_proxy
import tempfile
import pathlib

def defaultWorkingDir(resource):
  resManager = salome_proxy.getResourcesManager()
  resource_definition = resManager.GetResourceDefinition(resource)
  return resource_definition.working_directory

def defaultNbBranches(resource):
  resManager = salome_proxy.getResourcesManager()
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
    result = "P11N0:SALOME"
  return result

def availableResources():
  """ Return the list of resources defined in the current catalog."""
  resManager = salome_proxy.getResourcesManager()
  params     = salome_proxy.createSalomeParameters()
  params.resource_required.can_launch_batch_jobs = True
  # GetFittingResources returns a tuple if in no salome session mode.
  # Force to list for uniformity between the two modes.
  return list(resManager.GetFittingResources(params.resource_required))
