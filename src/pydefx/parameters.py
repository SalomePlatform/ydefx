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
