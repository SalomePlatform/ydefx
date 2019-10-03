import salome
import pylauncher
import os

_use_salome_servers = None

def _default():
  global _use_salome_servers
  if _use_salome_servers is None:
    try:
      salome.salome_init()
      _use_salome_servers = True
    except RuntimeError:
      _use_salome_servers = False

def forceSalomeServers():
  global _use_salome_servers
  if not _use_salome_servers:
    salome.salome_init()
  _use_salome_servers = True

def forceNoSalomeServers():
  global _use_salome_servers
  _use_salome_servers = False

def createSalomeParameters():
  _default()
  if _use_salome_servers:
    result = salome.JobParameters()
    result.resource_required = salome.ResourceParameters()
  else:
    result = pylauncher.JobParameters_cpp()
    result.resource_required = pylauncher.resourceParams()
  return result

_resourceManager = None
def getResourcesManager():
  global _resourceManager
  _default()
  if _resourceManager is None:
    if _use_salome_servers:
      _resourceManager = salome.lcc.getResourcesManager()
    else:
      catalog_path = os.environ.get("USER_CATALOG_RESOURCES_FILE", "")
      if not os.path.isfile(catalog_path):
        salome_path = os.environ.get("ROOT_SALOME_INSTALL", "")
        catalog_path = os.path.join(salome_path, "CatalogResources.xml")
      if not os.path.isfile(catalog_path):
        catalog_path = ""
      _resourceManager = pylauncher.ResourcesManager_cpp(catalog_path)
  return _resourceManager

_launcher = None
def getLauncher():
  global _launcher
  _default()
  if _launcher is None:
    if _use_salome_servers:
      _launcher = salome.naming_service.Resolve('/SalomeLauncher')
    else:
      _launcher = pylauncher.Launcher_cpp()
      _launcher.SetResourcesManager(getResourcesManager())
  return _launcher
