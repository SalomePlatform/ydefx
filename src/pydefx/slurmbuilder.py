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
import os

class SlurmBuilder:
  def __init__(self, executor = None, pointEval = None, mainJob = None):
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    install_root_directory = pathlib.Path(filename).resolve().parent
    install_files_directory = os.path.join(install_root_directory, "slurm")

    if executor is None:
      executor = os.path.join(install_files_directory, "executor.py")
    self.executor = executor

    if pointEval is None:
      pointEval = os.path.join(install_files_directory, "pointeval.py")
    self.pointEval = pointEval

    if mainJob is None:
      mainJob = os.path.join(install_files_directory, "mainjob.py")
    self.mainJob = mainJob

  def getMainJob(self):
    return self.mainJob

  def getExecutor(self):
    return self.executor

  def getPointEval(self):
    return self.pointEval

  def getPluginName(self):
    basename = os.path.basename(self.executor)
    if not basename.endswith(".py"):
      raise Exception("File name {} does not end with '.py'.".format(
                                                                 self.executor))
    return basename[:-3]
