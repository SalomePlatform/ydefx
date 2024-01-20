# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024 EDF
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

class StudyException(Exception):
  """
  Root of exceptions raised by a study.
  """
  def __init__(self, message):
    super().__init__(message)

class StudyUseException(StudyException):
  """
  Exception used when there is a bad utilisation of the study - functions called
  in a wrong order.
  """
  def __init__(self, message):
    super().__init__(message)

class StudyRunException(StudyException):
  """
  Exception used when there is a problem when running the study.
  """
  def __init__(self, message):
    super().__init__(message)
