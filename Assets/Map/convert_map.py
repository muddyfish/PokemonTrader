import sys, os
x = os.getcwd()
os.chdir(x+"/Tiles/")
os.system("python to_tilesheet.py %s"%("../"+sys.argv[1]))
os.chdir("../map_text/")
os.system("python extract_text.py")
os.chdir(x)