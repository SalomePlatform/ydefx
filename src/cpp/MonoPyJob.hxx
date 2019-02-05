#ifndef YDEFX_MONOPYJOB_HXX
#define YDEFX_MONOPYJOB_HXX
#include "Job.hxx"
#include <py2cpp/PyPtr.hxx>

namespace ydefx
{
class MonoPyJob : public Job
{
public:
  MonoPyJob();
  virtual ~MonoPyJob();
  virtual std::string state();
  virtual double progress();
  virtual std::string dump();
  virtual bool launch(); // return false when it fails
  virtual bool fetch()=0; // return false when it fails
  virtual const std::string& lastError();
  virtual bool wait(); // Wait for the end of the job. Return false when it fails.
  virtual void configureWaitDelay(int seconds);
protected:
  py2cpp::PyPtr _pyStudy;
  std::string _lastError;
  int _waitDelay;
};

}

#endif //YDEFX_MONOPYJOB_HXX
