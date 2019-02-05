#ifndef YDEFX_EXCEPTIONS_HXX
#define YDEFX_EXCEPTIONS_HXX
#include <string>

namespace ydefx
{
class Exception:public std::exception
{
public:
  Exception(const std::string& message);
  virtual const char* what() const noexcept;
private:
  std::string _message;
};

}

#endif // YDEFX_EXCEPTIONS_HXX
