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
