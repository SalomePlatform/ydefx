#ifndef YDEFX_TMONOPYJOB_HXX
#define YDEFX_TMONOPYJOB_HXX
#include "JobParametersProxy.hxx"
#include "MonoPyJob.hxx"
#include "Sample.hxx"
#include "SamplePyConversions.hxx"
#include "PyStudyFunction.hxx"
#include <py2cpp/py2cpp.hxx>

namespace ydefx
{
template <class ...Ts>
class TMonoPyJob : public MonoPyJob
{
public:
  //! Create a new job.
  TMonoPyJob(const PyStudyFunction& fnScript,
             Sample<Ts...>& sample,
             const JobParametersProxy& params)
  : MonoPyJob()
  , _sample(sample)
  {
    if(_lastError.empty()) // no errors during parent contruction
    {
      try
      {
        py2cpp::PyPtr pySample = createPySample(sample);
        py2cpp::PyFunction pyFn;
        pyFn.loadExp(_pyStudy, "createNewJob");
        pyFn(fnScript.content(), pySample, params);
      }
      catch(std::exception& e)
      {
        _lastError = "An error occured while creating the job.\n";
        _lastError += e.what();
      }
    }
  }

  //! Connect to an existing job.
  TMonoPyJob(const std::string& jobDump, Sample<Ts...>& sample)
  : MonoPyJob()
  , _sample(sample)
  {
    if(_lastError.empty()) // no errors during parent contruction
    {
      try
      {
        py2cpp::PyFunction pyFn;
        pyFn.loadExp(_pyStudy, "loadFromString");
        pyFn(jobDump);
      }
      catch(std::exception& e)
      {
        _lastError = "An error occured while creating the job.\n";
        _lastError += e.what();
      }
    }
  }
  
  virtual ~TMonoPyJob(){}
  virtual bool fetch()
  {
    _lastError = "";
    try
    {
      py2cpp::PyFunction pyFn;
      pyFn.loadExp(_pyStudy, "getResult");
      fetchResults(_pyStudy.getAttr("sample"), _sample);
    }
    catch(std::exception& e)
    {
      _lastError = "An error occured while fetching the results.\n";
      _lastError += e.what();
    }
    return _lastError.empty();
  }

  const Sample<Ts...>& getSample()const{return _sample;}

private:
  Sample<Ts...>& _sample;
};

}

#endif //YDEFX_TMONOPYJOB_HXX
