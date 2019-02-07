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
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(ydefx)

SET (CMAKE_CXX_STANDARD 11)
ENABLE_TESTING()
SET(BUILD_SHARED_LIBS TRUE)

OPTION(YDEFX_BUILD_GUI "Generate widgets" ON)

SET(CONFIGURATION_ROOT_DIR $ENV{CONFIGURATION_ROOT_DIR} CACHE PATH "Path to the Salome CMake configuration files")
IF(EXISTS ${CONFIGURATION_ROOT_DIR})
  LIST(APPEND CMAKE_MODULE_PATH "${CONFIGURATION_ROOT_DIR}/cmake")
  INCLUDE(SalomeMacros)
ELSE()
  MESSAGE(FATAL_ERROR "We absolutely need the Salome CMake configuration files, please define CONFIGURATION_ROOT_DIR !"
)
ENDIF()

SET(KERNEL_ROOT_DIR $ENV{KERNEL_ROOT_DIR} CACHE PATH "Path to Salome KERNEL")
IF( EXISTS ${KERNEL_ROOT_DIR} )
  LIST(APPEND CMAKE_MODULE_PATH "${KERNEL_ROOT_DIR}/salome_adm/cmake_files")
ELSE()
  MESSAGE(FATAL_ERROR "We absolutely need Salome KERNEL, please define KERNEL_ROOT_DIR")
ENDIF()
FIND_PACKAGE(SalomeKERNEL REQUIRED)
ADD_DEFINITIONS(${KERNEL_DEFINITIONS} )
INCLUDE_DIRECTORIES(${KERNEL_INCLUDE_DIRS})

SET(YACS_ROOT_DIR $ENV{YACS_ROOT_DIR} CACHE PATH "Path to Salome YACS")
IF( EXISTS ${YACS_ROOT_DIR} )
  LIST(APPEND CMAKE_MODULE_PATH "${YACS_ROOT_DIR}/salome_adm/cmake_files")
ELSE()
  MESSAGE(FATAL_ERROR "We absolutely need Salome YACS, please define YACS_ROOT_DIR")
ENDIF()
FIND_PACKAGE(SalomeYACS REQUIRED)
ADD_DEFINITIONS(${YACS_DEFINITIONS})
INCLUDE_DIRECTORIES(${YACS_INCLUDE_DIRS})

SET(PY2CPP_ROOT_DIR $ENV{PY2CPP_ROOT_DIR} CACHE PATH "Path to py2cpp")
IF( EXISTS ${PY2CPP_ROOT_DIR} )
  LIST(APPEND CMAKE_MODULE_PATH "${PY2CPP_ROOT_DIR}/lib/cmake/py2cpp")
ELSE()
  MESSAGE(FATAL_ERROR "We absolutely need py2cpp, please define PY2CPP_ROOT_DIR")
ENDIF()
FIND_PACKAGE(Py2cpp REQUIRED)

IF(YDEFX_BUILD_GUI)
  FIND_PACKAGE(Qt5Widgets CONFIG REQUIRED)
ENDIF(YDEFX_BUILD_GUI)

SET(SALOME_INSTALL_PYTHON "${SALOME_INSTALL_PYTHON}" CACHE PATH "Install Python files")

ADD_SUBDIRECTORY(src)
