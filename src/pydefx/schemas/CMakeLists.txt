SET(SCHEMA_FILES
  plugin.py
  idefix_pyschema.xml
  )

INSTALL(FILES ${SCHEMA_FILES} DESTINATION ${SALOME_INSTALL_PYTHON}/pydefx/schemas)
