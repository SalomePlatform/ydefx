#ifndef YDEFX_YACSSTUDYFUNCTION_H
#define YDEFX_YACSSTUDYFUNCTION_H
#include "StudyFunction.hxx"
namespace ydefx
{
//TODO not implemented!
class YacsStudyFunction :  StudyFunction
{
public:
  YacsStudyFunction();
  virtual ~YacsStudyFunction();
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
#endif // YDEFX_YACSSTUDYFUNCTION_H
