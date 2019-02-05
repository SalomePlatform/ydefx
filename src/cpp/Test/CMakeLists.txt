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
FIND_PACKAGE(CppUnit REQUIRED)

# additional include directories
INCLUDE_DIRECTORIES(
  ${CPPUNIT_INCLUDE_DIRS}
  ${CMAKE_CURRENT_SOURCE_DIR}/..
)

# libraries to link to
SET(_link_LIBRARIES
  ${CPPUNIT_LIBRARIES}
  py2cpp
  ydefx
)

SET(Test_SOURCES
    SampleTest.cxx
)

ADD_EXECUTABLE(SampleTest ${Test_SOURCES})
TARGET_LINK_LIBRARIES(SampleTest ${_link_LIBRARIES})
ADD_TEST(YdefxSampleTest SampleTest)
SET_TESTS_PROPERTIES(YdefxSampleTest PROPERTIES ENVIRONMENT
                    "PYTHONPATH=${CMAKE_SOURCE_DIR}/src:$ENV{PYTHONPATH}")

ADD_EXECUTABLE(StudyGeneralTest StudyGeneralTest.cxx)
TARGET_LINK_LIBRARIES(StudyGeneralTest ${_link_LIBRARIES})
ADD_TEST(YdefxStudyGeneralTest StudyGeneralTest)
SET_TESTS_PROPERTIES(YdefxStudyGeneralTest PROPERTIES ENVIRONMENT
                    "PYTHONPATH=${CMAKE_SOURCE_DIR}/src:$ENV{PYTHONPATH}")

ADD_EXECUTABLE(StudyRestartTest StudyRestartTest.cxx)
TARGET_LINK_LIBRARIES(StudyRestartTest ${_link_LIBRARIES})
ADD_TEST(YdefxStudyRestartTest StudyRestartTest)
SET_TESTS_PROPERTIES(YdefxStudyRestartTest PROPERTIES ENVIRONMENT
                    "PYTHONPATH=${CMAKE_SOURCE_DIR}/src:$ENV{PYTHONPATH}")
