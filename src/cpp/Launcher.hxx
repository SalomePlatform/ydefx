#ifndef YDEFX_LAUNCHER_H
#define YDEFX_LAUNCHER_H

#include "TMonoPyJob.hxx"

namespace ydefx
{
class Job;
class Launcher
{
public:
  Launcher():_lastError(){}
  const std::string& lastError()const{return _lastError;}

  /*!
   * Create and submit a new job.
   * Return nullptr in case of failure. Check the error with lastError().
   */
  template <class ...Ts>
  Job* submitMonoPyJob(const PyStudyFunction& fnScript,
                       Sample<Ts...>& sample,
                       const JobParametersProxy& params);

  /*!
   * Connect to an already created job.
   * Return nullptr in case of failure. Check the error with lastError().
   */
  template <class ...Ts>
  Job* connectJob(const std::string& jobDump, Sample<Ts...>& sample);

  template <class ...Ts>
  Job* submitMultiPyJob(const PyStudyFunction& fn,
                        Sample<Ts...>& sample,
                        const JobParametersProxy& params);

private:
  std::string _lastError;
};

////////////////////////////////////////////////////////////////////////////////
// Template implementations
////////////////////////////////////////////////////////////////////////////////

template <class ...Ts>
Job* Launcher::submitMonoPyJob(const PyStudyFunction& fnScript,
                    Sample<Ts...>& sample,
                    const JobParametersProxy& params)
{
  Job* result = nullptr;
  _lastError = "";
  try
  {
    result = new TMonoPyJob<Ts...>(fnScript, sample, params);
  }
  catch(std::exception& e)
  {
    if(result != nullptr)
      delete result;
    result = nullptr;
    _lastError = e.what();
    return result;
  }

  if(!result->launch())
  {
    _lastError = "Failed to submit job.\n";
    _lastError  += result->lastError();
    delete result;
    result = nullptr;
  }
  return result;
}

template <class ...Ts>
Job* Launcher::connectJob(const std::string& jobDump,
                      Sample<Ts...>& sample)
{
  Job* result = nullptr;
  _lastError = "";
  try
  {
    result = new TMonoPyJob<Ts...>(jobDump, sample);
  }
  catch(std::exception& e)
  {
    if(result != nullptr)
      delete result;
    result = nullptr;
    _lastError = e.what();
  }

  return result;
}

template <class ...Ts>
Job* Launcher::submitMultiPyJob(const PyStudyFunction& fn,
                      Sample<Ts...>& sample,
                      const JobParametersProxy& params)
{
  // TODO
  _lastError = "Not implemented!";
  return nullptr;
}

}
#endif // YDEFX_LAUNCHER_H
