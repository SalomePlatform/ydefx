#include "StudyGeneralTest.hxx"
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

void SampleTest::fullStudy()
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
    CPPUNIT_ASSERT(studyFunction.errors().empty());
    const std::list<std::string>& inputs = studyFunction.inputNames();
    CPPUNIT_ASSERT(std::find(inputs.begin(), inputs.end(), "a")!=inputs.end());
    CPPUNIT_ASSERT(std::find(inputs.begin(), inputs.end(), "b")!=inputs.end());
    const std::list<std::string>& outputs = studyFunction.outputNames();
    CPPUNIT_ASSERT(std::find(outputs.begin(), outputs.end(), "d")
                                                              != outputs.end());
    
    ydefx::Sample<double> sample;
    std::vector<double> a_vals = {1.1, 2.2, 3.4, 5.5};
    std::vector<double> b_vals = {2.2, 4.4, 6.8, 11};
    sample.inputs<double>().set("a", a_vals);
    sample.inputs<double>().set("b", b_vals);
    sample.outputs<double>().addName("d");

    ydefx::Launcher l;
    ydefx::Job* myJob = l.submitMonoPyJob(studyFunction, sample, jobParams);
    CPPUNIT_ASSERT(myJob);
    CPPUNIT_ASSERT(l.lastError().empty());
    std::string jobDump = myJob->dump();
    CPPUNIT_ASSERT(myJob->lastError().empty());
    std::string jobState = myJob->state();
    CPPUNIT_ASSERT(myJob->lastError().empty());
    CPPUNIT_ASSERT(jobState == "QUEUED" || jobState == "RUNNING"
                   || jobState == "FINISHED");
    double progress = myJob->progress();
    CPPUNIT_ASSERT(progress >= 0.0 && progress <= 1.0 );
    CPPUNIT_ASSERT(myJob->lastError().empty());
    bool ok = myJob->wait();
    CPPUNIT_ASSERT(ok);
    CPPUNIT_ASSERT(myJob->lastError().empty());
    jobState = myJob->state();
    CPPUNIT_ASSERT(jobState == "FINISHED");
    progress = myJob->progress();
    CPPUNIT_ASSERT(progress == 1.0);
    ok = myJob->fetch();
    CPPUNIT_ASSERT(ok);
    CPPUNIT_ASSERT(myJob->lastError().empty());
    std::vector<double> expectedResult = {0.5, 0.5, 0.5, 0.5};
    const std::vector<double>& result = sample.outputs<double>().get("d");
    CPPUNIT_ASSERT(expectedResult == result);
    delete myJob;
  }
  Py_Finalize();
}

CPPUNIT_TEST_SUITE_REGISTRATION( SampleTest );
#include "TestMain.cxx"
