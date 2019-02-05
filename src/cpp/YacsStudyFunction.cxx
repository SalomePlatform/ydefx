#include "YacsStudyFunction.hxx"
#include <fstream>
#include <sstream>
namespace ydefx
{
YacsStudyFunction::YacsStudyFunction()
: _content()
, _input()
, _output()
, _errors()
{
  _errors.push_back("Function \"_exec\" not found!");
}

YacsStudyFunction::~YacsStudyFunction(){}

void YacsStudyFunction::loadFile(const std::string& path)
{
  std::ifstream infile(path.c_str());
  std::stringstream buffer;
  buffer << infile.rdbuf();
  loadString(buffer.str());
}

void YacsStudyFunction::loadString(const std::string& value)
{
  _content = value;
  _input.clear();
  _output.clear();
  _errors.clear();
  // TODO: use YACS
}

void YacsStudyFunction::save(const std::string& path)
{
  std::ofstream outfile(path.c_str());
  outfile << _content;
}

const std::string& YacsStudyFunction::content()const
{
  return _content;
}

const std::list<std::string>& YacsStudyFunction::inputNames()const
{
  return _input;
}

const std::list<std::string>& YacsStudyFunction::outputNames()const
{
  return _output;
}

const std::list<std::string>& YacsStudyFunction::errors()const
{
  return _errors;
}

}
