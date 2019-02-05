#ifndef YDEFX_PYSTUDYFUNCTION_H
#define YDEFX_PYSTUDYFUNCTION_H
#include "StudyFunction.hxx"
namespace ydefx
{
class PyStudyFunction :  StudyFunction
{
public:
  PyStudyFunction();
  virtual ~PyStudyFunction();
  virtual void loadFile(const std::string& path);
  virtual void loadString(const std::string&);
  virtual void save(const std::string& path);
  virtual const std::string& content()const;
  virtual const std::list<std::string>& inputNames()const;
  virtual const std::list<std::string>& outputNames()const;
  virtual const std::list<std::string>& errors()const;
private:
  std::string _content;
  std::list<std::string> _input;
  std::list<std::string> _output;
  std::list<std::string> _errors;
};
}
#endif // YDEFX_PYSTUDYFUNCTION_H
