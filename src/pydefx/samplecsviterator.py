import csv
import os

def tofile(t):
  result = {}
  for k,v in t:
    if isinstance(v, (int, float)):
      result[k]=v
    else:
      result[k] = repr(e)
  return result

def fromfile(t):
  result = {}
  for k,v in t:
    if isinstance(v, str):
      result[k] = eval(e)
    else:
      result[k] = e
  return result

class SampleIterator:
  DATAFILE = "idefixdata.csv"
  OUTPUTNAMESFILE = "idefixoutputnames.csv"
  RESULTFILE = "idefixresult.csv"
  ERRORCOLUMN = "idefix_error"
  IDCOLUMN ="idefix_id"
  def __init__(self, directory=None):
    if directory:
      datapath = os.path.join(directory, SampleIterator.DATAFILE)
      outputnamespath = os.path.join(directory, SampleIterator.OUTPUTNAMESFILE)
      resultpath = os.path.join(directory, SampleIterator.RESULTFILE)
    else:
      datapath = SampleIterator.DATAFILE
      outputnamespath = SampleIterator.OUTPUTNAMESFILE
      resultpath = SampleIterator.RESULTFILE
      
    self.iterNb   = -1
    self.datafile = open(datapath, newline='')
    self.data     = csv.DictReader(self.datafile, quoting=csv.QUOTE_NONNUMERIC)
    result_columns = [SampleIterator.IDCOLUMN]
    result_columns.extend(self.data.fieldnames)
    self.outputnames = _loadOutputNames(outputnamespath)
    result_columns.extend(self.outputnames)
    result_columns.append(SampleIterator.ERRORCOLUMN)
    self.result_file = open(resultpath, 'w', newline='')
    self.result_csv = csv.DictWriter( self.result_file,
                                      fieldnames=result_columns,
                                      quoting=csv.QUOTE_NONNUMERIC )
    self.result_csv.writeheader()
    self.result_file.flush()

  def addResult(self, currentId, currentInput, currentOutput, currentError):
    """
    currentId : int value
    currentInput : dictionary {"input name":value}
    currentOutput : result returned by _exec.  Can be a tuple, a simple value or
    None in case of error.
    currentError : string or None if no error
    """
    currentRecord = {}
    currentRecord[SampleIterator.IDCOLUMN] = currentId
    for name in self.data.fieldnames:
      currentRecord[name] = currentInput[name]
    if currentError is None:
      if len(self.outputnames) == 1 :
        outputname = self.outputnames[0]
        currentRecord[outputname] = currentOutput
      elif len(self.outputnames) > 1 :
        outputIter = iter(currentOutput)
        for name in self.outputnames:
          currentRecord[name] = next(outputIter)
    else:
      for name in self.outputnames:
        currentRecord[name] = None
    currentRecord[SampleIterator.ERRORCOLUMN] = currentError
    self.result_csv.writerow(currentRecord)
    self.result_file.flush()

  def __next__(self):
    self.iterNb += 1
    return self.iterNb, next(self.data)
    #TODO: we need to close the files somewhere, but we cannot do it here

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
