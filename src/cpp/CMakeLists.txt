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
ADD_DEFINITIONS(${YACS_DEFINITIONS})
INCLUDE_DIRECTORIES(${YACS_INCLUDE_DIRS})

SET(ydefx_SOURCES
  PyStudyFunction.cxx
  JobParametersProxy.cxx
  Exceptions.cxx
  MonoPyJob.cxx
)

SET(ydefx_HEADERS
  PyStudyFunction.hxx
  StudyFunction.hxx
  JobParametersProxy.hxx
  Sample.hxx
  SamplePyConversions.hxx
  Exceptions.hxx
  MonoPyJob.hxx
  TMonoPyJob.hxx
  Job.hxx
  Launcher.hxx
)

SET(ydefx_LINK
  py2yacslib
  py2cpp
)

ADD_LIBRARY(ydefx ${ydefx_SOURCES})
TARGET_LINK_LIBRARIES(ydefx ${ydefx_LINK})
TARGET_INCLUDE_DIRECTORIES(ydefx PUBLIC
                          $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src/cpp>
                          $<INSTALL_INTERFACE:include>)

INSTALL(TARGETS ydefx DESTINATION lib)
INSTALL(TARGETS ydefx EXPORT Findydefx LIBRARY DESTINATION lib)
INSTALL(FILES ${ydefx_HEADERS} DESTINATION include/ydefx)
INSTALL(EXPORT Findydefx DESTINATION lib/cmake/ydefx)

ADD_SUBDIRECTORY(Test)
