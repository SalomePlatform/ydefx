#ifndef YDEFX_STUDYFUNCTION_H
#define YDEFX_STUDYFUNCTION_H
#include <string>
#include <list>

namespace ydefx
{
class StudyFunction
{
public:
  virtual ~StudyFunction(){}
  virtual void loadFile(const std::string& path)=0;
  virtual void loadString(const std::string&)=0;
  virtual void save(const std::string& path)=0;
  virtual const std::string& content()const=0;
  virtual const std::list<std::string>& inputNames()const=0;
  virtual const std::list<std::string>& outputNames()const=0;
  virtual const std::list<std::string>& errors()const=0;
  std::list<std::string> datafiles;
};
}
#endif // YDEFX_STUDYFUNCTION_H
