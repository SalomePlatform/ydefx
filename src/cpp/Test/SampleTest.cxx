#include "SampleTest.hxx"
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

void SampleTest::pointState()
{
  ydefx::Sample<double, int> mySample;
  CPPUNIT_ASSERT(mySample.maxSize() == 0);
  std::vector<int> int_vals = {1, 7, 42};
  mySample.inputs<int>().set("toto", int_vals);
  mySample.outputs<double>().addName("lili");
  for(unsigned int i = 0; i < 5; ++i)
    CPPUNIT_ASSERT(mySample.pointState(i)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.maxSize() == 3);
  mySample.errors().resize(3);
  mySample.errors()[1] = "Error detected!";
  CPPUNIT_ASSERT(mySample.pointState(0)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(1)==ydefx::ExecutionState::ERROR);
  CPPUNIT_ASSERT(mySample.pointState(2)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(3)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.maxSize() == 3);

  mySample.outputs<double>().set("lili", 0, 4.5);
  CPPUNIT_ASSERT(mySample.pointState(0)==ydefx::ExecutionState::DONE);
  CPPUNIT_ASSERT(mySample.pointState(1)==ydefx::ExecutionState::ERROR);
  CPPUNIT_ASSERT(mySample.pointState(2)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(3)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.maxSize() == 3);

  mySample.outputs<double>().set("lili", 5, 42.3);
  CPPUNIT_ASSERT(mySample.pointState(0)==ydefx::ExecutionState::DONE);
  CPPUNIT_ASSERT(mySample.pointState(1)==ydefx::ExecutionState::ERROR);
  CPPUNIT_ASSERT(mySample.pointState(2)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(3)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(4)==ydefx::ExecutionState::NOTEXECUTED);
  // no input defined for n°5 => not executed
  // TODO: add a new state: incomplete
  CPPUNIT_ASSERT(mySample.pointState(5)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.maxSize() == 3);
  
  mySample.inputs<int>().set("toto", 5, 7);
  CPPUNIT_ASSERT(mySample.pointState(4)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(5)==ydefx::ExecutionState::DONE);
  CPPUNIT_ASSERT(mySample.maxSize() == 6);

  mySample.outputs<double>().set("lili", 4, 23.5);
  CPPUNIT_ASSERT(mySample.pointState(4)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.maxSize() == 6);

  mySample.unset("lili", 5);
  CPPUNIT_ASSERT(mySample.pointState(0)==ydefx::ExecutionState::DONE);
  CPPUNIT_ASSERT(mySample.pointState(1)==ydefx::ExecutionState::ERROR);
  CPPUNIT_ASSERT(mySample.pointState(2)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(3)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(4)==ydefx::ExecutionState::NOTEXECUTED);
  CPPUNIT_ASSERT(mySample.pointState(5)==ydefx::ExecutionState::NOTEXECUTED);

  CPPUNIT_ASSERT(mySample.outputs<double>().maxSize() == 4);
}

void SampleTest::pyConversions()
{
  ydefx::Sample<double, int, std::string> mySample;
  std::vector<int> int_vals = {1, 7, 42};
  Py_Initialize();
  {
    // Test inputs
    py2cpp::PyPtr pyObj(inputToPy(mySample));
    CPPUNIT_ASSERT(pyObj.repr() == "{}");
    mySample.inputs<int>().set("toto", int_vals);
    pyObj.reset(inputToPy(mySample));
    CPPUNIT_ASSERT(pyObj.repr() == "{'toto': [1, 7, 42]}");
    std::vector<double> double_vals = {1.5, 3.2, 7.5};
    mySample.inputs<double>().set("dval", double_vals);
    pyObj.reset(inputToPy(mySample));
    ydefx::Sample<double, int, std::string> frompySample;
    frompySample.inputs<int>().addName("toto");
    frompySample.inputs<double>().addName("dval");
    py2cpp::ConversionCheck check(inputFromPy(pyObj.get(), frompySample));
    CPPUNIT_ASSERT(check);
    CPPUNIT_ASSERT(double_vals == frompySample.inputs<double>().get("dval"));
    CPPUNIT_ASSERT(int_vals == frompySample.inputs<int>().get("toto"));
    
    // Test outputs
    pyObj.reset(outputToPy(mySample));
    CPPUNIT_ASSERT(pyObj.repr() == "{}");
    check.reset();
    check.addError(outputFromPy(pyObj.get(), frompySample));
    CPPUNIT_ASSERT(check);
    CPPUNIT_ASSERT(0 == frompySample.allOutputNames().size());
    CPPUNIT_ASSERT(double_vals == frompySample.inputs<double>().get("dval"));
    CPPUNIT_ASSERT(int_vals == frompySample.inputs<int>().get("toto"));
    mySample.outputs<double>().addName("dout");
    mySample.outputs<double>().set("dout", 1, 1.5);
    pyObj.reset(outputToPy(mySample));
    frompySample.outputs<double>().addName("dout");
    check.addError(outputFromPy(pyObj.get(), frompySample));
    CPPUNIT_ASSERT(check);
    CPPUNIT_ASSERT(1.5 == frompySample.outputs<double>().get("dout", 1));
    CPPUNIT_ASSERT(frompySample.outputs<double>().isSet("dout",1));
    CPPUNIT_ASSERT(!frompySample.outputs<double>().isSet("dout",0));
    CPPUNIT_ASSERT(!frompySample.outputs<double>().isSet("dout",2));

    mySample.outputs<std::string>().addName("strout");
    mySample.outputs<std::string>().set("strout", 1, "myvalue");
    pyObj.reset(outputToPy(mySample));
    frompySample.outputs<std::string>().addName("strout");
    check.addError(outputFromPy(pyObj.get(), frompySample));
    CPPUNIT_ASSERT(check);
    CPPUNIT_ASSERT(1.5 == frompySample.outputs<double>().get("dout", 1));
    CPPUNIT_ASSERT(frompySample.outputs<double>().isSet("dout",1));
    CPPUNIT_ASSERT(!frompySample.outputs<double>().isSet("dout",0));
    CPPUNIT_ASSERT(!frompySample.outputs<double>().isSet("dout",2));
    CPPUNIT_ASSERT(frompySample.outputs<std::string>().get("strout", 1)
                   == "myvalue");
    CPPUNIT_ASSERT(frompySample.outputs<std::string>().isSet("strout",1));
    CPPUNIT_ASSERT(!frompySample.outputs<std::string>().isSet("strout",0));
    CPPUNIT_ASSERT(!frompySample.outputs<std::string>().isSet("strout",2));
  }
  Py_Finalize();
}

void SampleTest::pyConversionsErrors()
{
  Py_Initialize();
  {
    ydefx::Sample<double> resultSample;
    std::vector<double> double_vals = {1.5, 3.2, 7.5};
    ydefx::Sample<std::vector<double> > vectSample;
    // errors on input variables
    vectSample.inputs<std::vector<double> >().addName("p1");
    vectSample.inputs<std::vector<double> >().set("p1", 0, double_vals);
    py2cpp::PyPtr pyObj(inputToPy(vectSample));
    resultSample.inputs<double>().addName("noname");
    py2cpp::ConversionCheck check;
    check.addError(inputFromPy(pyObj.get(), resultSample));
    // The error contains the name of the unfound key.
    CPPUNIT_ASSERT(check.getMessage().find("noname")!= std::string::npos);
    resultSample.clear();
    resultSample.inputs<double>().addName("p1");
    check.reset();
    check.addError(inputFromPy(pyObj.get(), resultSample));
    // The error contains the name of the type "double" which fails to be
    // converted.
    CPPUNIT_ASSERT(check.getMessage().find("double")!= std::string::npos);
    ydefx::Sample<std::vector<int> > vectIntSample;
    vectIntSample.inputs<std::vector<int> >().addName("p1");
    check.reset();
    check.addError(inputFromPy(pyObj.get(), vectIntSample));
    CPPUNIT_ASSERT(check.getMessage().find("int")!= std::string::npos);
    CPPUNIT_ASSERT(check.getMessage().find("std::vector")!= std::string::npos);
    py2cpp::PyPtr notADict(py2cpp::toPy(42));
    check.reset();
    check.addError(inputFromPy(notADict.get(), vectIntSample));
    CPPUNIT_ASSERT(check.getMessage().find("Sample input")!= std::string::npos);

    // errors on output variables
    resultSample.outputs<double>().addName("o1");
    check.reset();
    check.addError(outputFromPy(pyObj.get(), resultSample));
    CPPUNIT_ASSERT(check.getMessage().find("o1")!= std::string::npos);

    vectSample.outputs<std::vector<double> >().addName("o1");
    vectSample.outputs<std::vector<double> >().set("o1", 0, double_vals);
    pyObj.reset(outputToPy(vectSample));
    check.reset();
    check.addError(outputFromPy(pyObj.get(), resultSample));
    CPPUNIT_ASSERT(check.getMessage().find("double")!= std::string::npos);

    check.reset();
    check.addError(outputFromPy(notADict.get(), resultSample));
    CPPUNIT_ASSERT(check.getMessage().find("Sample output")!= std::string::npos);
  }
  Py_Finalize();
}

void SampleTest::params()
{
  Py_Initialize();
  {
    try
    {
    ydefx::JobParametersProxy jpp;
    CPPUNIT_ASSERT(jpp.resource_name() == "localhost");
    CPPUNIT_ASSERT(jpp.job_type() == "yacs_file");
    std::list<std::string> testList = {"toto", "titi","tata"};
    jpp.in_files(testList);
    CPPUNIT_ASSERT(jpp.in_files() == testList);
    std::list<std::string> addList = {"zozo", "zizi"};
    jpp.add_in_files(addList);
    CPPUNIT_ASSERT(jpp.in_files() == std::list<std::string>({"toto", "titi",
                                     "tata", "zozo", "zizi"}));
    jpp.env_file("a");
    jpp.exclusive(true);
    jpp.extra_params("b");
    jpp.job_file("c");
    jpp.job_name("d");
    jpp.job_type("e");
    jpp.local_directory("fi");
    jpp.maximum_duration("dur");
    jpp.mem_mb(5);
    jpp.mem_per_cpu(42);
    jpp.nb_branches(18);
    jpp.nb_node(15);
    jpp.nb_proc(13);
    jpp.nb_proc_per_node(12);
    jpp.partition("gg");
    jpp.pre_command("pc");
    jpp.queue("qq");
    jpp.resource_name("rn");
    jpp.result_directory("rd");
    jpp.wckey("wk");
    jpp.work_directory("wd");
    CPPUNIT_ASSERT(jpp.env_file() == "a");
    CPPUNIT_ASSERT(jpp.exclusive());
    CPPUNIT_ASSERT(jpp.extra_params() == "b");
    CPPUNIT_ASSERT(jpp.job_file() == "c");
    CPPUNIT_ASSERT(jpp.job_name() == "d");
    CPPUNIT_ASSERT(jpp.job_type() == "e");
    CPPUNIT_ASSERT(jpp.local_directory() == "fi");
    CPPUNIT_ASSERT(jpp.maximum_duration() == "dur");
    CPPUNIT_ASSERT(jpp.mem_mb() == 5);
    CPPUNIT_ASSERT(jpp.mem_per_cpu() == 42);
    CPPUNIT_ASSERT(jpp.nb_branches() == 18);
    CPPUNIT_ASSERT(jpp.nb_node() == 15);
    CPPUNIT_ASSERT(jpp.nb_proc() == 13);
    CPPUNIT_ASSERT(jpp.nb_proc_per_node() == 12);
    CPPUNIT_ASSERT(jpp.partition() == "gg");
    CPPUNIT_ASSERT(jpp.pre_command() == "pc");
    CPPUNIT_ASSERT(jpp.queue() == "qq");
    CPPUNIT_ASSERT(jpp.resource_name() == "rn");
    CPPUNIT_ASSERT(jpp.result_directory() == "rd");
    CPPUNIT_ASSERT(jpp.wckey() == "wk");
    CPPUNIT_ASSERT(jpp.work_directory() == "wd");
    }
    catch(std::exception& e)
    {
      std::cout << e.what();
      CPPUNIT_FAIL("Unexpected exception!");
    }
  }
  Py_Finalize();
}

CPPUNIT_TEST_SUITE_REGISTRATION( SampleTest );
#include "TestMain.cxx"
