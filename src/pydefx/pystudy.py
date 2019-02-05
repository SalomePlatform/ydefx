# -*- coding: utf-8 -*-
import inspect
import pathlib
import tempfile
import os
import salome
import json
from . import samplecsvmanager
from . import parameters
from . import configuration

def defaultSampleManager():
  return samplecsvmanager.SampleManager()

def prepareDirectoryForLaunch(sample, result_directory, nb_branches, script,
                                 sampleManager=None):
  """
  sample : Sample type
  result_directory : path to a result working directory.
  nb_branches : int
  script : string
  return:
    extra_in_files: list of files to add to salome_parameters.in_files
    yacs_schema_path: path to the yacs schema (xml file).
  """
  if sampleManager is None:
    sampleManager = defaultSampleManager()
  # export sample to result_directory
  inputFiles = sampleManager.prepareRun(sample, result_directory)
  # export nbbranches
  configpath = os.path.join(result_directory, "idefixconfig.json")
  dicconfig = {}
  dicconfig["nbbranches"]  = nb_branches
  dicconfig["studymodule"] = "idefixstudy"
  dicconfig["sampleIterator"] = sampleManager.getModuleName()
  with open(configpath, "w") as f:
    json.dump(dicconfig, f, indent=2)
  studypath = os.path.join(result_directory, "idefixstudy.py")
  with open(studypath, "w") as f:
    f.write(script)
  # find generic schema
  filename = inspect.getframeinfo(inspect.currentframe()).filename
  install_directory = pathlib.Path(filename).resolve().parent
  yacs_schema_path = os.path.join(install_directory, "schemas",
                                  "idefix_pyschema.xml")
  plugin_path = os.path.join(install_directory, "schemas", "plugin.py")
  # create salome params
  extra_in_files = []
  extra_in_files.extend([configpath, studypath, plugin_path])
  extra_in_files.extend(inputFiles)
  return extra_in_files, yacs_schema_path

class PyStudy:
  JOB_DUMP_NAME = "jobDump.xml"
  def __init__(self):
    self.job_id = -1

  # Study creation functions
  def createNewJob(self, script, sample, params, sampleManager=None):
    """
    Create a new job out of those parameters:
    script : string
    sample : sample to be evaluated (Sample class)
    params : job submission parameters (Parameters class)
    The result directory will contain all the files needed for a launch and a
    job is created but not launched.
    """
    self.sample = sample
    self.params = params
    self.params.salome_parameters.job_type = self.jobType()
    if sampleManager is None:
      self.sampleManager = defaultSampleManager()
    else:
      self.sampleManager = sampleManager
    tmp_workdir = self.params.salome_parameters.result_directory
    extra_in_files, yacs_schema_path = prepareDirectoryForLaunch(self.sample,
                                                        tmp_workdir,
                                                        self.params.nb_branches,
                                                        script,
                                                        self.sampleManager)
    self.params.salome_parameters.in_files.extend(extra_in_files)
    self.params.salome_parameters.job_file = yacs_schema_path
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    self.job_id = launcher.createJob(self.params.salome_parameters)
    return self.job_id

  def loadFromDirectory(self, path, sampleManager=None):
    """
    Recover a study from a result directory where a previous study was launched.
    """
    if sampleManager is None:
      sampleManager = defaultSampleManager()
    self.sampleManager = sampleManager
    self.sample = sampleManager.loadSample(path)
    job_string = loadJobString(path)
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    self.job_id = launcher.restoreJob(job_string)
    if job_id >= 0:
      salome_params = launcher.getJobParameters(job_id)
      self.params = parameters.Parameters(salome_parameters=salome_params)
      self.getResult()
    return self.job_id

  def loadFromString(self, jobstring, sampleManager=None):
    """
    Recover a study from a string which contains the description of the job.
    This string can be obtained by launcher.dumpJob.
    """
    if sampleManager is None:
      sampleManager = defaultSampleManager()
    self.sampleManager = sampleManager
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    self.job_id = launcher.restoreJob(jobstring)
    self.params = None
    self.sample = None
    if self.job_id >= 0:
      salome_params = launcher.getJobParameters(self.job_id)
      self.params = parameters.Parameters(salome_parameters=salome_params)
      self.sample = sampleManager.loadSample(salome_params.result_directory)
      self.getResult()
    else:
      raise Exception("Failed to restore the job.")

  def loadFromId(self, jobid, sampleManager=None):
    """
    Connect the study to an already created job.
    The result directory of the job must be already prepared for launch.
    """
    if jobid < 0:
      return
    if sampleManager is None:
      sampleManager = defaultSampleManager()
    self.sampleManager = sampleManager
    self.job_id = jobid
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    salome_params = launcher.getJobParameters(job_id)
    self.params = parameters.Parameters(salome_parameters=salome_params)
    self.sample = sampleManager.loadSample(salome_params.result_directory)
    self.script = None
    return

  # launch parameters functions
  def jobType(self):
    return "yacs_file"

  # TODO: may be deprecated
  def createDefaultParameters(self, resource="localhost",
                              nb_branches=None,
                              result_base_dir=None):
    """
    Create the Parameters structure and the result directory.
    The result directory created here is needed by the job.
    """
    newParams = parameters.Parameters(resource, nb_branches)
    newParams.salome_parameters.job_type = self.jobType()
    newParams.salome_parameters.job_name = "idefix_job"
    newParams.salome_parameters.result_directory = configuration.newResultDirectory(result_base_dir)
    return newParams

  # Job management functions
  def launch(self):
    """
    The job should have been already created.
    """
    if self.job_id < 0 :
      raise Exception("Nothing to launch! Job is not created!")
    tmp_workdir = self.params.salome_parameters.result_directory
    # run the job
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    launcher.launchJob(self.job_id)
    #save the job
    job_string = launcher.dumpJob(self.job_id)
    jobDumpPath = os.path.join(tmp_workdir, PyStudy.JOB_DUMP_NAME)
    with open(jobDumpPath, "w") as f:
      f.write(job_string)

  def getResult(self):
    if self.job_id < 0 :
      raise Exception("Cannot get the results if the job is not created!")
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    state = launcher.getJobState(self.job_id)
    if state == "CREATED" :
      raise Exception("Cannot get the results if the job is not launched!")
    tmp_workdir = self.params.salome_parameters.result_directory
    if 1 == launcher.getJobWorkFile(self.job_id,
                                    self.sampleManager.getResultFileName(),
                                    tmp_workdir):
      self.sampleManager.loadResult(self.sample, tmp_workdir)
    return self.sample

  def getJobState(self):
    if self.job_id < 0:
      return "NOT_CREATED"
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    return launcher.getJobState(self.job_id)

  def getProgress(self):
    if self.job_id < 0:
      return 0.0
    state = self.getJobState()
    if state == "CREATED" or state == "QUEUED" :
      return 0.0
    self.getResult();
    return self.sample.progressRate()

  def dump(self):
    if self.job_id < 0 :
      raise Exception("Cannot dump the job if it is not created!")
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    return launcher.dumpJob(self.job_id)

  def wait(self, sleep_delay=10):
    """ Wait for the end of the job """
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    job_id = self.job_id
    jobState = launcher.getJobState(job_id)
    import time
    while jobState=="QUEUED" or jobState=="IN_PROCESS" or jobState=="RUNNING" :
      time.sleep(sleep_delay)
      jobState = launcher.getJobState(job_id)


### Deprecated!!!!
def dumpJob(result_directory, jobString):
  """
  Save the jobString to a file into result_directory.
  result_directory is a string representing a path to a directory.
  jobString is a string representing the serialization of a job.
  Use loadJobString for reloading the string saved here.
  """
  jobDumpPath = os.path.join(result_directory, PyStudy.JOB_DUMP_NAME)
  with open(jobDumpPath, "w") as f:
    f.write(job_string)

def loadJobString(result_directory):
  """
  Return the jobString saved by the dumpJob function into a directory.
  Use dumpJob for saving a the string.
  """
  jobDumpPath = os.path.join(result_directory, PyStudy.JOB_DUMP_NAME)
  with open(jobDumpPath, "r") as f:
    job_string = f.read()
  return job_string

