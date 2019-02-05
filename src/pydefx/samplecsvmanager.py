# Copyright (C) 2019  EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
import csv
import inspect
import os
import pathlib
from .samplecsviterator import SampleIterator
from . import samplecsviterator
from . import sample

class SampleManager:
  def __init__(self):
    pass

  def prepareRun(self, sample, directory):
    """
    Create a dump of the sample in the given directory.
    Return a list of files to add to the input files list of the job.
    """
    datapath = os.path.join(directory, SampleIterator.DATAFILE)
    with open(datapath, 'w', newline='') as csvfile:
      writer = csv.DictWriter(csvfile,
                              fieldnames=sample.getInputNames(),
                              quoting=csv.QUOTE_NONNUMERIC )
      writer.writeheader()
      writer.writerows(sample.inputIterator())
    
    outnamespath = os.path.join(directory, SampleIterator.OUTPUTNAMESFILE)
    with open(outnamespath, 'w') as outputfile:
      for v in sample.getOutputNames():
        outputfile.write(v+'\n')
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    install_directory = pathlib.Path(filename).resolve().parent
    iteratorFile = os.path.join(install_directory, "samplecsviterator.py")
    return [datapath,
            outnamespath,
            iteratorFile
            ]

  def loadResult(self, sample, directory):
    """ The directory should contain a file with the name given by
    getResultFileName. The results are loaded from that file to the sample.
    Return the modified sample.
    """
    datapath = os.path.join(directory, SampleIterator.RESULTFILE)
    with open(datapath, newline='') as datafile:
      data = csv.DictReader(datafile, quoting=csv.QUOTE_NONNUMERIC)
      for elt in data:
        index = int(elt[SampleIterator.IDCOLUMN]) # float to int
        input_vals = {}
        for name in sample.getInputNames():
          input_vals[name] = elt[name]
        output_vals = {}
        for name in sample.getOutputNames():
          output_vals[name] = elt[name]
        try:
          sample.checkId(index, input_vals)
        except Exception as err:
          extraInfo = "Error on processing file {} index number {}:".format(
                                                datapath,       str(index))
          raise Exception(extraInfo + str(err))
        sample.addResult(index, output_vals, elt[SampleIterator.ERRORCOLUMN])
    return sample

  def loadSample(self, directory):
    """ The directory should contain the files created by prepareRun. A new
    sample object is created and returned from those files.
    This function is used to recover a previous run.
    """
    outputnamesfile = os.path.join(directory, SampleIterator.OUTPUTNAMESFILE)
    outputnames = samplecsviterator._loadOutputNames(outputnamesfile)
    inputFilePath = os.path.join(directory, SampleIterator.DATAFILE)
    with open(inputFilePath) as datafile:
      data = csv.DictReader(datafile, quoting=csv.QUOTE_NONNUMERIC)
      inputvalues = {}
      for name in data.fieldnames:
        inputvalues[name] = []
      for line in data:
        for name in data.fieldnames:
          inputvalues[name].append(line[name])
    result = sample.Sample(data.fieldnames, outputnames)
    result.setInputValues(inputvalues)
    return result
        

  def getModuleName(self):
    """
    Return the module name which contains the class SampleIterator.
    """
    return "samplecsviterator"
  
  def getResultFileName(self):
    return SampleIterator.RESULTFILE
