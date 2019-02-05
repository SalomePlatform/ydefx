// Copyright (C) 2019  EDF R&D
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
//
// See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
//
#include "StudyRestartTest.hxx"
#include "../Launcher.hxx" // possible conflict with KERNEL/Launcher/Launcher.hxx
#include <algorithm>

void SampleTest::setUp()
{
}

void SampleTest::tearDown()
{
}

void SampleTest::cleanUp()
{
}

void SampleTest::studyTest()
{
  Py_Initialize();
  {
    ydefx::JobParametersProxy jobParams;
    jobParams.configureResource("localhost");
    jobParams.createResultDirectory("/tmp");

    std::string pyScript = 
"def _exec(a, b):\n"
"  d = a / b\n"
"  return d\n";
    ydefx::PyStudyFunction studyFunction;
    studyFunction.loadString(pyScript);

    ydefx::Sample<double> sample;
    std::vector<double> a_vals = {1.1, 2.2, 3.4, 5.5};
    std::vector<double> b_vals = {2.2, 4.4, 6.8, 11};
    sample.inputs<double>().set("a", a_vals);
    sample.inputs<double>().set("b", b_vals);
    sample.outputs<double>().addName("d");

    ydefx::Launcher l;
    ydefx::Job* myJob = l.submitMonoPyJob(studyFunction, sample, jobParams);
    std::string jobDump = myJob->dump();
    delete myJob;

    ydefx::Job* restoredJob = l.connectJob(jobDump, sample);
    CPPUNIT_ASSERT(restoredJob);
    CPPUNIT_ASSERT(l.lastError().empty());
    bool ok = restoredJob->wait();
    CPPUNIT_ASSERT(ok);
    double progress = restoredJob->progress();
    CPPUNIT_ASSERT(progress == 1.0);
    ok = restoredJob->fetch();
    CPPUNIT_ASSERT(ok);
    std::vector<double> expectedResult = {0.5, 0.5, 0.5, 0.5};
    const std::vector<double>& result = sample.outputs<double>().get("d");
    CPPUNIT_ASSERT(expectedResult == result);
    CPPUNIT_ASSERT(restoredJob->lastError().empty());
    delete restoredJob;
  }
  Py_Finalize();
}

CPPUNIT_TEST_SUITE_REGISTRATION( SampleTest );
#include "TestMain.cxx"
