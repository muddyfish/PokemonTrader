#!/usr/bin/python
# -*- coding: latin-1 -*-
import struct, urllib2
try: import cPickle as pickle
except ImportError: import pickle

opener = urllib2.build_opener()

text_offsets = {0: u'¶', 1: u'\xe3\x81\x82', 2: u'\xe3\x81\x84', 3: u'\xe3\x81\x86', 4: u'\xe3\x81\x88', 5: u'\xe3\x81\x8a', 6: u'\xe3\x81\x8b', 7: u'\xe3\x81\x8d', 8: u'\xe3\x81\x8f', 9: u'\xe3\x81\x91', 10: u'\xe3\x81\x93', 11: u'\xe3\x81\x95', 12: u'\xe3\x81\x97', 13: u'\xe3\x81\x99', 14: u'\xe3\x81\x9b', 15: u'\xe3\x81\x9d', 16: u'\xe3\x81\x9f', 17: u'\xe3\x81\xa1', 18: u'\xe3\x81\xa4', 19: u'\xe3\x81\xa6', 20: u'\xe3\x81\xa8', 21: u'\xe3\x81\xaa', 22: u'\xe3\x81\xab', 23: u'\xe3\x81\xac', 24: u'\xe3\x81\xad', 25: u'\xe3\x81\xae', 26: u'\xe3\x81\xaf', 27: u'\xe3\x81\xb2', 28: u'\xe3\x81\xb5', 29: u'\xe3\x81\xb8', 30: u'\xe3\x81\xbb', 31: u'\xe3\x81\xbe', 32: u'\xe3\x81\xbf', 33: u'\xe3\x82\x80', 34: u'\xe3\x82\x81', 35: u'\xe3\x82\x82', 36: u'\xe3\x82\x84', 37: u'\xe3\x82\x86', 38: u'\xe3\x82\x88', 39: u'\xe3\x82\x89', 40: u'\xe3\x82\x8a', 41: u'\xe3\x82\x8b', 42: u'\xe3\x82\x8c', 43: u'\xe3\x82\x8d', 44: u'\xe3\x82\x8f', 45: u'\xe3\x82\x92', 46: u'\xe3\x82\x93', 47: u'\xe3\x81\x81', 48: u'\xe3\x81\x83', 49: u'\xe3\x81\x85', 50: u'\xe3\x81\x87', 51: u'\xe3\x81\x89', 52: u'\xe3\x82\x83', 53: u'\xe3\x82\x85', 54: u'\xe3\x82\x87', 55: u'\xe3\x81\x8c', 56: u'\xe3\x81\x8e', 57: u'\xe3\x81\x90', 58: u'\xe3\x81\x92', 59: u'\xe3\x81\x94', 60: u'\xe3\x81\x96', 61: u'\xe3\x81\x98', 62: u'\xe3\x81\x9a', 63: u'\xe3\x81\x9c', 64: u'\xe3\x81\x9e', 65: u'\xe3\x81\xa0', 66: u'\xe3\x81\xa2', 67: u'\xe3\x81\xa5', 68: u'\xe3\x81\xa7', 69: u'\xe3\x81\xa9', 70: u'\xe3\x81\xb0', 71: u'\xe3\x81\xb3', 72: u'\xe3\x81\xb6', 73: u'\xe3\x81\xb9', 74: u'\xe3\x81\xbc', 75: u'\xe3\x81\xb1', 76: u'\xe3\x81\xb4', 77: u'\xe3\x81\xb7', 78: u'\xe3\x81\xba', 79: u'\xe3\x81\xbd', 80: u'\x00', 81: u'\xe3\x82\xa2', 82: u'\xe3\x82\xa4', 83: u'\xe3\x82\xa6', 84: u'\xe3\x82\xa8', 85: u'\xe3\x82\xaa', 86: u'\xe3\x82\xab', 87: u'\xe3\x82\xad', 88: u'\xe3\x82\xaf', 89: u'\xe3\x82\xb1', 90: u'\xe3\x82\xb3', 91: u'\xe3\x82\xb5', 92: u'\xe3\x82\xb7', 93: u'\xe3\x82\xb9', 94: u'\xe3\x82\xbb', 95: u'\xe3\x82\xbd', 96: u'\xe3\x82\xbf', 97: u'\xe3\x83\x81', 98: u'\xe3\x83\x84', 99: u'\xe3\x83\x86', 100: u'\xe3\x83\x88', 101: u'\xe3\x83\x8a', 102: u'\xe3\x83\x8b', 103: u'\xe3\x83\x8c', 104: u'\xe3\x83\x8d', 105: u'\xe3\x83\x8e', 106: u'\xe3\x83\x8f', 107: u'\xe3\x83\x92', 108: u'\xe3\x83\x95', 109: u'\xe3\x83\x98', 110: u'\xe3\x83\x9b', 111: u'\xe3\x83\x9e', 112: u'\xe3\x83\x9f', 113: u'\xe3\x83\xa0', 114: u'\xe3\x83\xa1', 115: u'\xe3\x83\xa2', 116: u'\xe3\x83\xa4', 117: u'\xe3\x83\xa6', 118: u'\xe3\x83\xa8', 119: u'\xe3\x83\xa9', 120: u'\xe3\x83\xaa', 121: u'\xe3\x83\xab', 122: u'\xe3\x83\xac', 123: u'\xe3\x83\xad', 124: u'\xe3\x83\xaf', 125: u'\xe3\x83\xb2', 126: u'\xe3\x83\xb3', 127: u'\xe3\x82\xa1', 128: u'\xe3\x82\xa3', 129: u'\xe3\x82\xa5', 130: u'\xe3\x82\xa7', 131: u'\xe3\x82\xa9', 132: u'\xe3\x83\xa3', 133: u'\xe3\x83\xa5', 134: u'\xe3\x83\xa7', 135: u'\xe3\x82\xac', 136: u'\xe3\x82\xae', 137: u'\xe3\x82\xb0', 138: u'\xe3\x82\xb2', 139: u'\xe3\x82\xb4', 140: u'\xe3\x82\xb6', 141: u'\xe3\x82\xb8', 142: u'\xe3\x82\xba', 143: u'\xe3\x82\xbc', 144: u'\xe3\x82\xbe', 145: u'\xe3\x83\x80', 146: u'\xe3\x83\x82', 147: u'\xe3\x83\x85', 148: u'\xe3\x83\x87', 149: u'\xe3\x83\x89', 150: u'\xe3\x83\x90', 151: u'\xe3\x83\x93', 152: u'\xe3\x83\x96', 153: u'\xe3\x83\x99', 154: u'\xe3\x83\x9c', 155: u'\xe3\x83\x91', 156: u'\xe3\x83\x94', 157: u'\xe3\x83\x97', 158: u'\xe3\x83\x9a', 159: u'\xe3\x83\x9d', 160: u'\x00', 161: u'0', 162: u'1', 163: u'2', 164: u'3', 165: u'4', 166: u'5', 167: u'6', 168: u'7', 169: u'8', 170: u'9', 171: u'!', 172: u'?', 173: u'.', 174: u'-', 175: u'\x00', 176: u'\xe2\x80\xa6', 177: u'\xe2\x80\x9c', 178: u'\xe2\x80\x9d', 179: u'\xe2\x80\x98', 180: u'\xe2\x80\x99', 181: u'\xe2\x99\x82', 182: u'\xe2\x99\x80', 183: u'\x00', 184: u', u', 185: u'\x00', 186: u'/', 187: u'A', 188: u'B', 189: u'C', 190: u'D', 191: u'E', 192: u'F', 193: u'G', 194: u'H', 195: u'I', 196: u'J', 197: u'K', 198: u'L', 199: u'M', 200: u'N', 201: u'O', 202: u'P', 203: u'Q', 204: u'R', 205: u'S', 206: u'T', 207: u'U', 208: u'V', 209: u'W', 210: u'X', 211: u'Y', 212: u'Z', 213: u'a', 214: u'b', 215: u'c', 216: u'd', 217: u'e', 218: u'f', 219: u'g', 220: u'h', 221: u'i', 222: u'j', 223: u'k', 224: u'l', 225: u'm', 226: u'n', 227: u'o', 228: u'p', 229: u'q', 230: u'r', 231: u's', 232: u't', 233: u'u', 234: u'v', 235: u'w', 236: u'x', 237: u'y', 238: u'z', 239: u'\x00', 254: "\n", 255:"\0"}

keys = text_offsets.keys()
values = text_offsets.values()

def parse_text(text):
    return "".join([text_offsets[ord(char)] for char in text])

def encode_text(text):
    return "".join([struct.pack("<B", keys[values.index(char)]) for char in text])

def parse_names(game_rom):     
    names_offset = game_rom.read().find(encode_text("BULBASAUR"))
    game_rom.seek(names_offset)
    pokemon_names = parse_text(game_rom.read(11*411))
    ascii = pokemon_names.replace(text_offsets[0], "@").encode("ascii", "ignore").replace("\x00", "")
    long_names = filter(None, ascii.split("@"))
    pokemon_names = []
    for name in long_names:
        if len(name) >= 10:
            pokemon_names.extend([name[i:i+10] for i in range(0, len(name), 10)])
        else:
            pokemon_names.append(name)
    pokemon_names[28] = "NIDORAN-f"
    pokemon_names[31] = "NIDORAN-m"
    pokemon_names[82] = "FARFETCHD"
    pokemon_names[83] = "DODUO"
    pokemon_names[121] = "MR-MIME"
    del pokemon_names[122]
    return pokemon_names

def get_url(url):
    file_obj = opener.open(urllib2.Request(url))
    contents = file_obj.read()
    file_obj.close()
    return contents

def get_images(names):
    images = {}
    save_locations = ["anim/normal", "anim/shiny", "anim/back-normal", "anim/back-shiny", "normal", "shiny", "back-normal", "back-shiny"]
    for index, name in enumerate(names):
        if name != "?" and name != "UNOWN":
            print "Downloading Pokemon %s %s"%(index, name)
            pokemon = []
            for i in save_locations:
                form = "gif"
                if i.find("anim/") == -1: form = "png"
                print "http://img.pokemondb.net/sprites/black-white/%s/%s.%s"%(i, name.lower(), form)
                pokemon.append(get_url("http://img.pokemondb.net/sprites/black-white/%s/%s.%s"%(i, name.lower(), form)))
                party = open("pokemon/party/%03d.png"%(index+1), "rb")
                images[index].append(party.read())
                party.close()
                fprint = open("pokemon/print/%03d.png"%(index+1), "rb")
                images[index].append(fprint.read())
                fprint.close()
            images[index] = (name, pokemon)
    return images

def main():
    print "Opening ROM"
    rom = open("Pokemon Emerald.gba", "rb")
    names = parse_names(rom)
    rom.close()
    print "Parsed Pokemon names"
    images = get_images(names)))
    chunks = []
    print "Got all Images.\nConverting to standard format..."
    for index in images.keys():
        print "Converting table %s (%s)..."%(index, images[index][0])
        sizes = [len(image) for image in images[index][1]]
        fmt = "<%sI%sc"%(len(sizes), sum(sizes))
        size = struct.calcsize(fmt)
        sizes.extend(list("".join(images[index][1])))
        chunks.append(struct.pack(fmt, *sizes))
    print "Adding Main Pointer Table..."
    sizes = [len(chunk) for chunk in chunks]
    fmt = "<%sI%sc"%(len(sizes), sum(sizes))
    size = struct.calcsize(fmt)
    sizes.extend(list("".join(chunks)))
    print "Converting..."
    table = struct.pack(fmt, *sizes)
    print "Writing..."
    poke_table = open("pokemon_im.dat", "wb")
    poke_table.write(table)
    poke_table.close()
    print "Done!"

main()

