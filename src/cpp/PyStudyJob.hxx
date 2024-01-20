// Copyright (C) 2019-2024 EDF
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
#ifndef YDEFX_PYSTUDYJOB_HXX
#define YDEFX_PYSTUDYJOB_HXX
#include "Job.hxx"
#include <py2cpp/PyPtr.hxx>

namespace ydefx
{
class PyStudyJob : public Job
{
public:
  PyStudyJob(const std::string& pymodule_name, const std::string& pyclass_name);
  PyStudyJob(py2cpp::PyPtr& pyStudyObj);
  PyStudyJob();
  virtual ~PyStudyJob();
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

#endif //YDEFX_PYSTUDYJOB_HXX
