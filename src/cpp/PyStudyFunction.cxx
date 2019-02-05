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
#include "PyStudyFunction.hxx"
#include <fstream>
#include <sstream>
#include <py2yacs.hxx>

namespace ydefx
{
PyStudyFunction::PyStudyFunction()
: _content()
, _input()
, _output()
, _errors()
{
  _errors.push_back("Function \"_exec\" not found!");
}

PyStudyFunction::~PyStudyFunction(){}

void PyStudyFunction::loadFile(const std::string& path)
{
  std::ifstream infile(path.c_str());
  std::stringstream buffer;
  buffer << infile.rdbuf();
  loadString(buffer.str());
}

void PyStudyFunction::loadString(const std::string& value)
{
  _content = value;
  _input.clear();
  _output.clear();
  _errors.clear();
  // TODO: use py2yacs
  Py2yacs p2y;
  p2y.load(value);
  if(p2y.getGlobalErrors().size() == 0)
  {
    const std::list<FunctionProperties>& fn_prop = p2y.getFunctionProperties();
    std::list<FunctionProperties>::const_iterator prop_it = fn_prop.begin();
    while(prop_it != fn_prop.end() && prop_it->_name != "_exec")
      ++ prop_it;
    if(prop_it != fn_prop.end() && prop_it->_errors.empty())
    {
      for(const std::string& name: prop_it->_input_ports)
        _input.push_back(name);
      for(const std::string& name: prop_it->_output_ports)
        _output.push_back(name);
    }
  }
  // TODO: deal with the errors
}

void PyStudyFunction::save(const std::string& path)
{
  std::ofstream outfile(path.c_str());
  outfile << _content;
}

const std::string& PyStudyFunction::content()const
{
  return _content;
}

const std::list<std::string>& PyStudyFunction::inputNames()const
{
  return _input;
}

const std::list<std::string>& PyStudyFunction::outputNames()const
{
  return _output;
}

const std::list<std::string>& PyStudyFunction::errors()const
{
  return _errors;
}

}
