SET(SCHEMA_FILES
  executor.py
  mainjob.py
  pointeval.py
  )

INSTALL(FILES ${SCHEMA_FILES} DESTINATION ${SALOME_INSTALL_PYTHON}/pydefx/slurm)
