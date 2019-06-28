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
import numbers
import pickle
from . import sample

class SampleManager:
  DATAFILE = "idefixdata.csv"
  OUTPUTNAMESFILE = "idefixoutputnames.csv"
  RESULTDIR = "idefixresult" # directory which contains all the result files
  RESULTFILE = "idefixresult.csv" # main result file - values for every point
  GLOBALFILE = "idefixglobal"     # global result - one value for the whole simulation
  ERRORCOLUMN = "idefix_error"
  IDCOLUMN ="idefix_id"
  ESCAPE_CHAR = "@"   # prefix a value that needs particular save/load procedure
  PICK_CHAR = "p"     # @p : csv value saved in another file using pickle
  def __init__(self):
    self.datafile = None
    self.result_file = None
    pass

  # Functions used by the study
  def prepareRun(self, sample, directory):
    """
    Create a dump of the sample in the given directory.
    sample: Sample object.
    directory: path to a local working directory where all the working files are
               copied. This directory should be already created.
    Return a list of files to add to the input files list of the job.
    """
    datapath = os.path.join(directory, SampleManager.DATAFILE)
    with open(datapath, 'w', newline='') as csvfile:
      writer = csv.DictWriter(csvfile,
                              fieldnames=sample.getInputNames(),
                              quoting=csv.QUOTE_NONNUMERIC )
      writer.writeheader()
      writer.writerows(sample.inputIterator())

    outnamespath = os.path.join(directory, SampleManager.OUTPUTNAMESFILE)
    with open(outnamespath, 'w') as outputfile:
      for v in sample.getOutputNames():
        outputfile.write(v+'\n')
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    return [datapath,
            outnamespath,
            filename
            ]

  def loadResult(self, sample, directory):
    """
    The directory should contain a RESULTDIR directory with the result files.
    The results are loaded into the sample.
    Return the modified sample.
    """
    resultdir = os.path.join(directory, SampleManager.RESULTDIR)
    datapath = os.path.join(resultdir, SampleManager.RESULTFILE)
    with open(datapath, newline='') as datafile:
      data = csv.DictReader(datafile, quoting=csv.QUOTE_NONNUMERIC)
      for elt in data:
        index = int(elt[SampleManager.IDCOLUMN]) # float to int
        input_vals = {}
        for name in sample.getInputNames():
          input_vals[name] = elt[name]
        output_vals = {}
        for name in sample.getOutputNames():
          output_vals[name] = self.decodeOutput(elt[name], resultdir)
        try:
          sample.checkId(index, input_vals)
        except Exception as err:
          extraInfo = "Error on processing file {} index number {}:".format(
                                                datapath,       str(index))
          raise Exception(extraInfo + str(err))
        sample.addResult(index, output_vals, elt[SampleManager.ERRORCOLUMN])
    return sample

  def loadSample(self, directory):
    """ The directory should contain the files created by prepareRun. A new
    sample object is created and returned from those files.
    This function is used to recover a previous run.
    """
    sampleIt = self.initInputIterator(directory)
    inputvalues = {}
    for name in self.inputnames:
      inputvalues[name] = []
    for newid, values in sampleIt:
      for name in self.inputnames:
        inputvalues[name].append(values[name])
    
    result = sample.Sample(self.inputnames, self.outputnames)
    result.setInputValues(inputvalues)
    self.terminate()
    return result

  def getModuleName(self):
    """
    Return the module name which contains the class SampleManager.
    """
    return __name__
  
  def getResultFileName(self):
    """
    Name of the file or directory which contains the result and needs to be
    copied from the remote computer.
    """
    return SampleManager.RESULTDIR

  # Functions used by the optimizerloop plugin
  def initInputIterator(self, directory=None):
    """
    Iterate over the input values read from the csv file.
    """
    if directory:
      datapath = os.path.join(directory, SampleManager.DATAFILE)
      outputnamespath = os.path.join(directory, SampleManager.OUTPUTNAMESFILE)
      self.directory = directory
    else:
      datapath = SampleManager.DATAFILE
      outputnamespath = SampleManager.OUTPUTNAMESFILE
      self.directory = None

    self.datafile = open(datapath, newline='')
    data     = csv.DictReader(self.datafile, quoting=csv.QUOTE_NONNUMERIC)
    self.inputnames = data.fieldnames
    self.outputnames = _loadOutputNames(outputnamespath)
    return InputSampleIterator(data)

  def writeHeaders(self):
    """
    This function can be called after initInputIterator and before the first
    call to addResult in order to write the names of the parameters in the
    result file.
    """
    if self.directory:
      resultdir = os.path.join(self.directory, SampleManager.RESULTDIR)
      outputnamespath = os.path.join(self.directory,
                                     SampleManager.OUTPUTNAMESFILE)
    else:
      resultdir = SampleManager.RESULTDIR
      outputnamespath = SampleManager.OUTPUTNAMESFILE
    os.makedirs(resultdir, exist_ok=True)
    resultpath = os.path.join(resultdir, SampleManager.RESULTFILE)
    result_columns = [SampleManager.IDCOLUMN]
    result_columns.extend(self.inputnames)
    result_columns.extend(self.outputnames)
    result_columns.append(SampleManager.ERRORCOLUMN)
    self.result_file = open(resultpath, 'w', newline='')
    self.result_csv = csv.DictWriter( self.result_file,
                                      fieldnames=result_columns,
                                      quoting=csv.QUOTE_NONNUMERIC )
    self.result_csv.writeheader()
    self.result_file.flush()

  def addResult(self, currentId, currentInput, currentOutput, currentError):
    """
    You need to call initInputIterator and writeHeaders before the first call
    of this function.
    currentId : int value
    currentInput : dictionary {"input name":value}
    currentOutput : result returned by _exec.  Can be a tuple, a simple value or
    None in case of error.
    currentError : string or None if no error
    """
    currentRecord = {}
    currentRecord[SampleManager.IDCOLUMN] = currentId
    for name in self.inputnames:
      currentRecord[name] = currentInput[name]
    if currentError is None:
      if len(self.outputnames) == 1 :
        outputname = self.outputnames[0]
        currentRecord[outputname] = self.codeOutput(currentOutput,
                                                    currentId,
                                                    outputname)
      elif len(self.outputnames) > 1 :
        outputIter = iter(currentOutput)
        for name in self.outputnames:
          currentRecord[name]=self.codeOutput(next(outputIter), currentId, name)
    else:
      for name in self.outputnames:
        currentRecord[name] = None
    currentRecord[SampleManager.ERRORCOLUMN] = currentError
    self.result_csv.writerow(currentRecord)
    self.result_file.flush()

  def terminate(self):
    """
    Call this function at the end of the simulation in order to close every
    open files.
    """
    if not self.datafile is None:
      self.datafile.close()
      self.datafile = None
    if not self.result_file is None:
      self.result_file.close()
      self.result_file = None

  # Read and write results (output parameters)
  def codeOutput(self, value, currentId, name):
    """
    Define how a value should be saved.
    value: object to be saved - value of a parameter
    currentId: number of the current line (current point).
    name: name of the parameter (name of the column in the csv file).
    return: string to be saved in the csv file.
    """
    res = None
    if isinstance(value, numbers.Number):
      res = value
    elif isinstance(value, str):
      res = value
      if res[0:1] == SampleManager.ESCAPE_CHAR :
        res = SampleManager.ESCAPE_CHAR + res
    else:
      file_name = "idefixresult-{}-{}.pick".format(name, currentId)
      res = SampleManager.ESCAPE_CHAR + SampleManager.PICK_CHAR + file_name
      file_path = os.path.join(SampleManager.RESULTDIR, file_name)
      if self.directory :
        file_path = os.path.join(self.directory, file_path)
      with open(file_path, "wb") as f:
        pickle.dump(value, f)
    return res

  def decodeOutput(self, obj, resultdir):
    """
    Decode a value read from the csv file.
    obj: object to decode (string or number).
    resultdir : directory which contains the result files
    return: decoded object.
    """
    res = None
    if isinstance(obj, numbers.Number):
      res = obj
    elif isinstance(obj, str):
      res = obj
      if res[0:1] == SampleManager.ESCAPE_CHAR :
        res = res[1:]
        if res[0:1] == SampleManager.ESCAPE_CHAR :# obj = @@string begins with@
          pass
        elif res[0:1] == SampleManager.PICK_CHAR:# obj = @pidefixresult-x-1.pick
          file_path = os.path.join(resultdir, res[1:])
          with open(file_path, "rb") as f:
            res = pickle.load(f)
        else:
          raise Exception("Unknown escape value:" + obj)
    return res

class InputSampleIterator:
  """
  Iterator used to iterate over the input values of a sample, adding an order
  number.
  """
  def __init__(self, iterable):
    self.it = iter(iterable)
    self.iterNb = -1
  def __next__(self):
    self.iterNb += 1
    return self.iterNb, next(self.it)
  def __iter__(self):
    return self

# Private functions
def _loadOutputNames(filepath):
    outputnames = []
    with open(filepath, "r") as namesfile:
      for line in namesfile:
        line = line.rstrip() # remove whitespaces at the end
        outputnames.append(line)
    return outputnames
