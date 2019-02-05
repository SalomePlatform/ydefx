#include "MonoPyJob.hxx"
#include <py2cpp/py2cpp.hxx>

namespace ydefx
{
MonoPyJob::MonoPyJob()
: _pyStudy()
, _lastError()
, _waitDelay(10)
{
  py2cpp::PyFunction objConstructor;
  objConstructor.loadExp("pydefx", "PyStudy");
  _pyStudy = objConstructor();
}

MonoPyJob::~MonoPyJob()
{
}

std::string MonoPyJob::state()
{
  std::string result;
  _lastError = "";
  try
  {
    py2cpp::PyFunction pyFn;
    pyFn.loadExp(_pyStudy, "getJobState");
    py2cpp::pyResult(result) = pyFn();
  }
  catch(std::exception& e)
  {
    _lastError = "An error occured while retrieving job's state.\n";
    _lastError += e.what();
  }
  return result;
}

double MonoPyJob::progress()
{
  double result;
  py2cpp::PyFunction pyFn;
  _lastError = "";
  try
  {
    pyFn.loadExp(_pyStudy, "getProgress");
    py2cpp::pyResult(result) = pyFn();
  }
  catch(std::exception& e)
  {
    _lastError = "An error occured while retrieving job's progress.\n";
    _lastError += e.what();
  }
  return result;
}

std::string MonoPyJob::dump()
{
  std::string result;
  _lastError = "";
  try
  {
    py2cpp::PyFunction pyFn;
    pyFn.loadExp(_pyStudy, "dump");
    py2cpp::pyResult(result) = pyFn();
  }
  catch(std::exception& e)
  {
    _lastError = "An error occured while dumping the job.\n";
    _lastError += e.what();
  }
  return result;
}

bool MonoPyJob::launch()
{
  _lastError = "";
  try
  {
    py2cpp::PyFunction pyFn;
    pyFn.loadExp(_pyStudy, "launch");
    pyFn();
  }
  catch(std::exception& e)
  {
    _lastError = "An error occured while launching the job.\n";
    _lastError += e.what();
  }
  return _lastError.empty();
}

const std::string& MonoPyJob::lastError()
{
  return _lastError;
}

bool MonoPyJob::wait()
{
  _lastError = "";
  try
  {
    py2cpp::PyFunction pyFn;
    pyFn.loadExp(_pyStudy, "wait");
    pyFn(_waitDelay);
  }
  catch(std::exception& e)
  {
    _lastError = "An error occured while waiting the end of the job.\n";
    _lastError += e.what();
  }
  return _lastError.empty();
}

void MonoPyJob::configureWaitDelay(int seconds)
{
  _waitDelay = seconds;
}

}
