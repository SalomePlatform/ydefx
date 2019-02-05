import SALOMERuntime
import pickle
import json

datafile="input.csv"
resultfile="output.csv"
class myalgosync(SALOMERuntime.OptimizerAlgSync):
  def __init__(self):
    SALOMERuntime.OptimizerAlgSync.__init__(self, None)

  def setPool(self,pool):
    """Must be implemented to set the pool"""
    self.pool=pool

  def getTCForIn(self):
    """return typecode of type expected as Input of the internal node """
    return SALOMERuntime.getSALOMERuntime().getTypeCode("string")

  def getTCForOut(self):
    """return typecode of type expected as Output of the internal node"""
    return SALOMERuntime.getSALOMERuntime().getTypeCode("string")

  def getTCForAlgoInit(self):
    """return typecode of type expected as input for initialize """
    return SALOMERuntime.getSALOMERuntime().getTypeCode("string")

  def getTCForAlgoResult(self):
    """return typecode of type expected as output of the algorithm """
    return SALOMERuntime.getSALOMERuntime().getTypeCode("int")

  def initialize(self,input):
    """Optional method called on initialization.
       The type of "input" is returned by "getTCForAlgoInit"
    """
    with open("idefixconfig.json", "r") as f:
      self.config = json.load(f)

  def start(self):
    """Start to fill the pool with samples to evaluate."""
    self.id=0
    self.datafile=open(datafile, newline='')
    #self.datafile=open(datafile)
    import csv
    self.data = csv.DictReader(self.datafile, quoting=csv.QUOTE_NONNUMERIC)
    values=None
    for i in range(0, self.getNbOfBranches()):
      try:
        values = next(self.data)
        self.pool.pushInSample(self.id,
                               pickle.dumps(values, protocol=0).decode())
        self.id += 1
      except StopIteration:
        pass
    if values is not None:
      with open(resultfile,"w") as f:
        f.write("id,")
        for v in values.keys():
          f.write(v+",")
        f.write("\n")

  def takeDecision(self):
    """ This method is called each time a sample has been evaluated. It can
        either add new samples to evaluate in the pool, do nothing (wait for
        more samples), or empty the pool to finish the evaluation.
    """
    currentId=self.pool.getCurrentId()
    samplebyte=self.pool.getCurrentInSample().getStringValue().encode()
    sample = pickle.loads(samplebyte)
    resultbyte=self.pool.getCurrentOutSample().getStringValue().encode()
    error,result = pickle.loads(resultbyte)
    with open(resultfile,"a") as f:
      f.write(repr(currentId)+",")
      for v in sample.values():
        f.write(repr(v)+",")
      if error is None:
        try:
          for v in result:
            f.write(repr(v)+",")
        except TypeError:
          # result is not iterable, it is just one number
          f.write(repr(result))
      else:
        error="Error:"+error.split('\n')[0]
        f.write(error)
      f.write("\n")
    try:
      values = next(self.data)
      self.pool.pushInSample(self.id, pickle.dumps(values, protocol=0).decode())
      self.id += 1
    except StopIteration:
      pass

  def finish(self):
    """Optional method called when the algorithm has finished, successfully
       or not, to perform any necessary clean up."""
    try:
      self.datafile.close()
    except:
      pass
    self.pool.destroyAll()

  def getAlgoResult(self):
    """return the result of the algorithm.
       The object returned is of type indicated by getTCForAlgoResult.
    """
    return 0
