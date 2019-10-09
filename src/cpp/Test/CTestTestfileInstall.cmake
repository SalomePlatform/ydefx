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

SET(TEST_NAME ${COMPONENT_NAME}_SampleTest)
ADD_TEST(${TEST_NAME} python ${SALOME_TEST_DRIVER} ${TIMEOUT} ./SampleTest)
SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES
                                  LABELS "${COMPONENT_NAME}"
                    )

SET(TEST_NAME ${COMPONENT_NAME}_StudyGeneralTest)
ADD_TEST(${TEST_NAME} python ${SALOME_TEST_DRIVER} ${TIMEOUT} ./StudyGeneralTest)
SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES
                                  LABELS "${COMPONENT_NAME}"
                    )

SET(TEST_NAME ${COMPONENT_NAME}_StudyRestartTest)
ADD_TEST(${TEST_NAME} python ${SALOME_TEST_DRIVER} ${TIMEOUT} ./StudyRestartTest)
SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES
                                  LABELS "${COMPONENT_NAME}"
                    )

SET(TEST_NAME ${COMPONENT_NAME}_NoSession_SampleTest)
ADD_TEST(${TEST_NAME} ./SampleTest)
SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES
                                  LABELS "${COMPONENT_NAME}"
                    )

SET(TEST_NAME ${COMPONENT_NAME}_NoSession_StudyGeneralTest)
ADD_TEST(${TEST_NAME} ./StudyGeneralTest)
SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES
                                  LABELS "${COMPONENT_NAME}"
                    )

SET(TEST_NAME ${COMPONENT_NAME}_NoSession_StudyRestartTest)
ADD_TEST(${TEST_NAME} ./StudyRestartTest)
SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES
                                  LABELS "${COMPONENT_NAME}"
                    )
