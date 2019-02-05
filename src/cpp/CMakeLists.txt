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
                          $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
                          $<INSTALL_INTERFACE:include>)

INSTALL(TARGETS ydefx DESTINATION lib)
INSTALL(TARGETS ydefx EXPORT Findydefx LIBRARY DESTINATION lib)
INSTALL(FILES ${ydefx_HEADERS} DESTINATION include/ydefx)
INSTALL(EXPORT Findydefx DESTINATION lib/cmake/ydefx)

ADD_SUBDIRECTORY(Test)
