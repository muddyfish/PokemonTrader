import os

class AssetLoader():
  def __init__(self, pygame, debug = False):
    globals()["pygame"] = pygame
    self.debug = False
    self.loaded_assets = {}
  
  def load_asset(self, filename, mode):
    asset_hash = hash((filename, mode))
    if asset_hash in self.loaded_assets:
      asset = self.loaded_assets[asset_hash]
      if self.debug:
	print "Asset %s already loaded as %s" %(filename, asset)
      if asset.closed:
	if self.debug:
	  print "Reloading asset %s as it was closed" %(filename)
	return self.reload_asset(asset)
      return asset

    self.loaded_assets[asset_hash] = open(("Assets/"+filename).replace("/", os.sep), mode)
    return self.loaded_assets[asset_hash]
    
  def load_image(self, filename):
    asset_hash = hash((filename, "rb"))
    if asset_hash in self.loaded_assets:
      asset = self.loaded_assets[asset_hash]
      if self.debug:
	print "Asset %s already loaded as %s" %(filename, asset)
      return asset
    self.loaded_assets[asset_hash] = pygame.image.load(("Assets/Graphics/"+filename).replace("/", os.sep))
    return self.loaded_assets[asset_hash]
  
  def reload_asset(self, *args):
    asset_hash = self.get_hash(args)
    self.loaded_assets[asset_hash] = open(("Assets/"+filename).replace("/", os.sep), mode)
    return self.loaded_assets[asset_hash]
  
  def reload_image(self, filename):
    asset_hash = self.get_hash(filename)
    self.loaded_assets[asset_hash] = pygame.image.load(("Assets/Graphics/"+filename).replace("/", os.sep))
    return self.loaded_assets[asset_hash]
  
  def del_asset(self, *args):
    del self.loaded_assets[self.get_hash(args)]
    
  def get_hash(self, *args):
    assert(len(args) in [1,2])
    if len(args) == 1:
      if type(args[0]) == file:
	return hash((args[0].name, args[0].mode))
      else:
	return hash((args[0], "rb"))
    elif len(args) == 2:
      return hash(args)
    
