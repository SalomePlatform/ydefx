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
