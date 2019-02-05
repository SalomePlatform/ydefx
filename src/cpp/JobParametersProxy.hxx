#ifndef YDEFX_JOBPARAMETERSPROXY_H
#define YDEFX_JOBPARAMETERSPROXY_H
#include <py2cpp/PyPtr.hxx>
#include <string>
#include <list>
#include <map>

namespace ydefx
{
class JobParametersProxy;
}
namespace py2cpp
{
PyObject * toPy(const ydefx::JobParametersProxy& jp);
}

#include <py2cpp/py2cpp.hxx>

namespace ydefx
{
class JobParametersProxy
{
public:
  JobParametersProxy();

  std::string job_name()const;
  void job_name(const std::string& v);
  
  std::string job_type()const;
  void job_type(const std::string& v);
  
  std::string job_file()const;
  void job_file(const std::string& v);
  
  std::string pre_command()const;
  void pre_command(const std::string& v);
  
  std::string env_file()const;
  void env_file(const std::string& v);
  
  std::list<std::string> in_files()const;
  void add_in_files(const std::list<std::string>& pathList);
  void in_files(const std::list<std::string>& pathList);

  std::string work_directory()const;
  void work_directory(const std::string& v);
  
  std::string local_directory()const;
  void local_directory(const std::string& v);
  
  std::string result_directory()const;
  void result_directory(const std::string& v);
  
  std::string maximum_duration()const;
  void maximum_duration(const std::string& v);
  
  // ResourceParameters
  std::string resource_name()const;
  void resource_name(const std::string& name);

  int nb_proc()const;
  void nb_proc(int v);
  
  int mem_mb()const;
  void mem_mb(int v);
  
  int nb_node()const;
  void nb_node(int v);
  
  int nb_proc_per_node()const;
  void nb_proc_per_node(int v);
  
  std::string queue()const;
  void queue(const std::string& v);
  
  std::string partition()const;
  void partition(const std::string& v);
  
  bool exclusive()const;
  void exclusive(bool v);
  
  unsigned int mem_per_cpu()const;
  void mem_per_cpu(unsigned int v);
  
  std::string wckey()const;
  void wckey(const std::string& v);
  
  std::string extra_params()const;
  void extra_params(const std::string& v);
  
  unsigned int nb_branches()const;
  void nb_branches(unsigned int v);
  
  /*!
   * Set the resource and the default values associated with that resource:
   * work_directory, nb_branches, nb_proc and wckey.
   */
  void configureResource(const std::string& resourceName);
  //! create a new result directory as a subdirectory of the given path.
  void createResultDirectory(const std::string& basePath);
  friend PyObject * py2cpp::toPy(const JobParametersProxy& jp);

private:
  py2cpp::PyPtr _pyParameters;
private:
  std::string getAttrString(const std::string& attributeName)const;
  void setAttr(const std::string& attributeName, const std::string& value);
  int getResAttr(const std::string& attributeName)const;
  void setResAttr(const std::string& attributeName, int value);
};
}
#endif // YDEFX_JOBPARAMETERSPROXY_H
