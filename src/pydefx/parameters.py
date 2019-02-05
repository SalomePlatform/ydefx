# -*- coding: utf-8 -*-
import salome
from . import configuration

class Parameters:
  def __init__(self, resource="localhost",
               nb_branches=None, salome_parameters=None):
    if salome_parameters is None :
      job_params = salome.JobParameters()
      job_params.job_type = "yacs_file"
      job_params.resource_required = salome.ResourceParameters()
      job_params.resource_required.name = resource
      job_params.job_name = "idefix_job"
      job_params.wckey = configuration.defaultWckey(resource)
      job_params.work_directory = configuration.defaultWorkingDir(resource)
      if nb_branches is None:
        nb_branches = configuration.defaultNbBranches(resource)
      job_params.resource_required.nb_proc = nb_branches
      self.nb_branches = nb_branches
      self.salome_parameters = job_params
    else:
      if nb_branches is None:
        nb_branches = salome_parameters.resource_required.nb_proc
      self.nb_branches = nb_branches
      self.salome_parameters = salome_parameters

  def configureResource(self, resource):
    self.salome_parameters.resource_required.name = resource
    self.salome_parameters.work_directory = configuration.defaultWorkingDir(
                                                                       resource)
    nb_branches = configuration.defaultNbBranches(resource)
    self.salome_parameters.resource_required.nb_proc = nb_branches
    self.nb_branches = nb_branches
    self.salome_parameters.wckey = configuration.defaultWckey(resource)

  def createResultDirectory(self, result_base_dir):
    self.salome_parameters.result_directory = configuration.newResultDirectory(result_base_dir)
