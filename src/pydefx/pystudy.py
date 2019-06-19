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
import inspect
import pathlib
import tempfile
import os
import salome
import json
from . import samplecsvmanager
from . import parameters
from . import configuration
from . import defaultschemabuilder

def defaultSampleManager():
  return samplecsvmanager.SampleManager()

class PyStudy:
  JOB_DUMP_NAME = "jobDump.xml"
  def __init__(self, sampleManager=None, schemaBuilder=None):
    self.job_id = -1
    if sampleManager is None:
      self.sampleManager = defaultSampleManager()
    else:
      self.sampleManager = sampleManager
    if schemaBuilder is None:
      self.schemaBuilder = defaultschemabuilder.DefaultSchemaBuilder()
    else:
      self.schemaBuilder = schemaBuilder

  # Study creation functions
  def createNewJob(self, script, sample, params):
    """
    Create a new job out of those parameters:
    script : script / pyscript type
    sample : sample to be evaluated (Sample class)
    params : job submission parameters (Parameters class)
    The result directory will contain all the files needed for a launch and a
    job is created but not launched.
    """
    self.sample = sample
    self.params = params
    self.params.salome_parameters.job_type = self.jobType()
    tmp_workdir = self.params.salome_parameters.result_directory
    schema_path, extra_files = self._prepareDirectoryForLaunch(tmp_workdir,
                                                               script)

    self.params.salome_parameters.in_files.extend(extra_files)
    self.params.salome_parameters.job_file = schema_path
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    self.job_id = launcher.createJob(self.params.salome_parameters)
    return self.job_id

  def loadFromDirectory(self, path):
    """
    Recover a study from a result directory where a previous study was launched.
    """
    self.sample = self.sampleManager.loadSample(path)
    job_string = loadJobString(path)
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    self.job_id = launcher.restoreJob(job_string)
    if job_id >= 0:
      salome_params = launcher.getJobParameters(job_id)
      self.params = parameters.Parameters(salome_parameters=salome_params)
      self.getResult()
    return self.job_id

  def loadFromString(self, jobstring):
    """
    Recover a study from a string which contains the description of the job.
    This string can be obtained by launcher.dumpJob.
    """
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    self.job_id = launcher.restoreJob(jobstring)
    self.params = None
    self.sample = None
    if self.job_id >= 0:
      salome_params = launcher.getJobParameters(self.job_id)
      self.params = parameters.Parameters(salome_parameters=salome_params)
      #TODO: sampleManager should be loaded from result_directory
      self.sample = self.sampleManager.loadSample(
                                                 salome_params.result_directory)
      self.getResult()
    else:
      raise Exception("Failed to restore the job.")

  def loadFromId(self, jobid):
    """
    Connect the study to an already created job.
    The result directory of the job must be already prepared for launch.
    """
    if jobid < 0:
      return
    self.job_id = jobid
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    salome_params = launcher.getJobParameters(job_id)
    self.params = parameters.Parameters(salome_parameters=salome_params)
    #TODO: sampleManager should be loaded from result_directory
    self.sample = self.sampleManager.loadSample(salome_params.result_directory)
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
    """
    Try to get the result file and if it was possible the results are loaded in
    the sample.
    An exception may be thrown if it was not possible to get the file.
    """
    if self.job_id < 0 :
      raise Exception("Cannot get the results if the job is not created!")
    launcher = salome.naming_service.Resolve('/SalomeLauncher')
    state = launcher.getJobState(self.job_id)
    tmp_workdir = self.params.salome_parameters.result_directory
    searchResults = False
    errorIfNoResults = False
    errorMessage = ""
    if state == "CREATED" :
      raise Exception("Cannot get the results if the job is not launched!")
    elif state ==  "QUEUED" or state == "IN_PROCESS":
      # no results available at this point. Try again later! Not an error.
      searchResults = False
    elif state == "FINISHED" :
      # verify the return code of the execution
      searchResults = True
      if(launcher.getJobWorkFile(self.job_id, "logs/exit_code.log", tmp_workdir)):
        exit_code_file = os.path.join(tmp_workdir, "exit_code.log")
        exit_code = ""
        if os.path.isfile(exit_code_file):
          with open(exit_code_file) as myfile:
            exit_code = myfile.read()
            exit_code = exit_code.strip()
        if exit_code == "0" :
          errorIfNoResults = True # we expect to have full results
        else:
          errorMessage = "An error occured during the execution of the YACS schema."
      else:
        errorMessage = "Failed to get the exit code of the YACS schema execution."

    elif state == "RUNNING" or state == "PAUSED" or state == "ERROR" :
      # partial results may be available
      searchResults = True
    elif state == "FAILED":
      # We may have some partial results because the job could have been
      # canceled or stoped by timeout.
      searchResults = True
      errorMessage = "Job execution failed!"
    if searchResults :
      if 1 == launcher.getJobWorkFile(self.job_id,
                                      self.sampleManager.getResultFileName(),
                                      tmp_workdir):
        try:
          self.sampleManager.loadResult(self.sample, tmp_workdir)
        except Exception as err:
          if errorIfNoResults:
            raise err
      elif errorIfNoResults:
        errorMessage = "The job is finished but we cannot get the result file!"
    if len(errorMessage) > 0 :
      warningMessage = """
The results you get may be incomplete or incorrect.
For further details, see {}/logs directory on {}.""".format(
                          self.params.salome_parameters.work_directory,
                          self.params.salome_parameters.resource_required.name)
      errorMessage += warningMessage
      raise Exception(errorMessage)
    return self.sample

  def resultAvailable(self):
    """
    Try to get the result and return True in case of success with no exception.
    In case of success the results are loaded in the sample.
    """
    resultFound = False
    try:
      self.getResult()
      resultFound = True
    except:
      resultFound = False
    return resultFound

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
    if not self.resultAvailable():
      return 0.0
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

  def _prepareDirectoryForLaunch(self, result_directory, script):
    """
    result_directory : path to a result working directory.
    script : script / pyscript type
    return:
      yacs_schema_path: path to the yacs schema (xml file).
      extra_in_files: list of files to add to salome_parameters.in_files
    """
    if not os.path.exists(result_directory):
      os.makedirs(result_directory)
    # export sample to result_directory
    inputFiles = self.sampleManager.prepareRun(self.sample, result_directory)

    # export nbbranches
    configpath = os.path.join(result_directory, "idefixconfig.json")
    dicconfig = {}
    dicconfig["nbbranches"]  = self.params.nb_branches
    dicconfig["studymodule"] = "idefixstudy"
    dicconfig["sampleIterator"] = self.sampleManager.getModuleName()
    with open(configpath, "w") as f:
      json.dump(dicconfig, f, indent=2)
    studypath = os.path.join(result_directory, "idefixstudy.py")
    with open(studypath, "w") as f:
      f.write(script.script)
    schema_path, extra_files = self.schemaBuilder.buildSchema(result_directory)

    extra_files.extend([configpath, studypath])
    extra_files.extend(inputFiles)
    return schema_path, extra_files

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

