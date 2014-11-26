import Image
import sys
import json
import zipfile
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO

SIZE = 16

def dhash(image, hash_size = 8):
  # Grayscale and shrink the image in one step.
  image = image.convert('L').resize((hash_size + 1, hash_size), Image.ANTIALIAS).load()
  # Compare adjacent pixels.
  difference = []
  for row in xrange(hash_size):
    for col in xrange(hash_size):
      pixel_left = image[col, row]
      pixel_right = image[col + 1, row]
      difference.append(pixel_left > pixel_right)
  # Convert the binary array to a hexadecimal string.
  return hash(tuple(difference))

def convert(im, amount=20):
  tiles = []
  tile_hashes = []
  w, h = [s/SIZE for s in im.size]
  tile_ids = [[0 for i in range(h)] for i in range(w)]
  print("Converting to tiles")
  percent = 0
  print(0)
  for cw in range(0,w):
    for ch in range(0,h):
      cropped = im.crop((cw*SIZE,ch*SIZE,cw*SIZE+SIZE,ch*SIZE+SIZE))
      cols = cropped.getcolors()
      if len(cols) == 1:
	hash_cropped = hash(cols[0][1])
      else:
	hash_cropped = hash((dhash(cropped), tuple([i[1] for i in cols])))
      if hash_cropped not in tile_hashes:
	tile_hashes.append(hash_cropped)
	tiles.append(cropped)
      tile_ids[cw][ch] = tile_hashes.index(hash_cropped)
      if ch==cw!=0:
	if percent+amount<=100*(ch+(cw*w))/float(w*h):
	  percent+=amount
	  print(percent)
  print("%s%% of tiles kept"%(100*float(len(tile_hashes))/(w*h)))
  n_im = Image.new("RGB", (len(tiles)*SIZE,SIZE))

  for cw in range(0,len(tiles)):
    n_im.paste(tiles[cw], (cw*SIZE,0))

  im_f = StringIO.StringIO()	
  n_im.save(im_f, format = "tga")
  return im_f, tile_ids

print("Loading input image")
im = Image.open(sys.argv[1])
print("Creating save file")
save = zipfile.ZipFile(sys.argv[1].split("/")[-1][:-4]+".tiles")
files = {i:save.open(i).read() for i in save.namelist() if not ('position' in i or 'tilesheet' in i)}
save = zipfile.ZipFile(sys.argv[1].split("/")[-1][:-4]+".tiles", "w", zipfile.ZIP_DEFLATED)
for f in files:
  save.writestr(f, files[f])
image_id = 0
while 1:
  try:
    im.seek(image_id)
    rgb_im = im.convert("RGB")
  except EOFError: break
  layer, tile_ids = convert(rgb_im)
  print("Saving tile arrangement %i"%(image_id+1))
  pos = "_%i"%image_id
  if image_id == 0: 
    pos = ""
  save.writestr("position"+pos, json.dumps(tile_ids))
  print("Saving tilesheet %i"%(image_id+1))
  save.writestr("tilesheet"+pos, layer.getvalue())
  image_id+=1
  
save.close()
