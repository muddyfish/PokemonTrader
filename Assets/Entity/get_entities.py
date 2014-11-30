import os, itertools
ENTITY_PATH = "Assets%sEntity"%os.sep
def get_entities():
  entities = {}
  for root, dirs, files in os.walk(ENTITY_PATH):
    for file in files:
      if file.endswith(".py") and \
         file != "__init__.py" and \
	 root != ENTITY_PATH:
	entities[file[:-3]]=__import__(root.replace(os.sep, '.')+"."+file[:-3], globals(), locals(), ['object'], -1).__dict__[file[:-3].capitalize()]
  return entities