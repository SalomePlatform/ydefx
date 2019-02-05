SET(SCRIPTS
  __init__.py
  configuration.py
  parameters.py
  pyscript.py
  pystudy.py
  sample.py
  samplecsviterator.py
  samplecsvmanager.py
  )

INSTALL(FILES ${SCRIPTS} DESTINATION ${SALOME_INSTALL_PYTHON}/pydefx)
ADD_SUBDIRECTORY(schemas)
