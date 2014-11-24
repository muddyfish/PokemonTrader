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

print("Loading input image")
im = Image.open(sys.argv[1]).convert("RGB")
w, h = [s/SIZE for s in im.size]
print("Seting up tile grid")
tiles = []
tile_hashes = []

tile_ids = [[0 for i in range(h)] for i in range(w)]
print("Converting to tiles")
percent = 0
amount = 10
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
print("Preparing output image")
n_im = Image.new("RGB", (len(tiles)*SIZE,SIZE))

for cw in range(0,len(tiles)):
  n_im.paste(tiles[cw], (cw*SIZE,0))

im_f = StringIO.StringIO()
n_im.save(im_f, format = "tga")

save = zipfile.ZipFile(sys.argv[1].split(".")[0]+".tiles", "a", zipfile.ZIP_DEFLATED)
print("Saving tile arrangement")
save.writestr("position", json.dumps(tile_ids))
print("Saving tiles")
save.writestr("tilesheet", im_f.getvalue())
save.close()
