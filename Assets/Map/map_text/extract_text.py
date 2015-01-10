import glob, json, zipfile


def convert_file(filename):
  asm_file = open(filename)
  asm = asm_file.read()
  asm_file.close()
  asm_funcs = {}
  current_function = ""
  for asm_line in asm.split('\n'):
    if len(asm_line) == 0: continue
    if asm_line[0]!='\t':
      current_function = asm_line[1:].split(":: ")[0]
      if current_function[-2:]=="::":
	current_function = current_function[:-2]
      asm_funcs[current_function] = []
    else:
      if asm_line == '\tdone': continue
      msg_type = asm_line[1:].split(" ")[0]
      msg = ' '.join(asm_line.split(" ")[1:])[1:-1]
      asm_funcs[current_function].append((msg_type, msg))
  return asm_funcs

def add_tiles_file(filename, contents):
  filename = '../Tiles/'+filename.replace('_', '-')+".tiles"
  try:
    save = zipfile.ZipFile(filename)
  except IOError:
    return
  else:
    print "Overwriting:", filename
    files = {i:save.open(i).read() for i in save.namelist()}
    save.close()
  script = {"text": contents}
  if "script" in files:
      script = json.loads(files["script"])
      script["text"] = contents
  files["script"] = json.dumps(script)
  save = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
  for f in files:
    save.writestr(f, files[f])
  save.close()

[add_tiles_file(i[:-4], convert_file(i)) for i in glob.glob("*.asm")]