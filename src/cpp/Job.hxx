#ifndef YDEFX_JOB_H
#define YDEFX_JOB_H
#include <string>

namespace ydefx
{

class Job
{
public:
  virtual ~Job(){}
  virtual std::string state()=0;
  virtual double progress()=0;
  virtual std::string dump()=0;
  virtual bool launch()=0; // return false when it fails
  virtual bool fetch()=0; // return false when it fails
  virtual const std::string& lastError()=0;
  virtual bool wait()=0; // Wait for the end of the job. Return false when it fails.
  virtual void configureWaitDelay(int seconds)=0;
};
}
#endif // YDEFX_JOB_H
