#!/usr/bin/python
# -*- coding: latin-1 -*-

import struct, sys
from itertools import permutations

text_offsets = {0: u'¶', 1: u'\xe3\x81\x82', 2: u'\xe3\x81\x84', 3: u'\xe3\x81\x86', 4: u'\xe3\x81\x88', 5: u'\xe3\x81\x8a', 6: u'\xe3\x81\x8b', 7: u'\xe3\x81\x8d', 8: u'\xe3\x81\x8f', 9: u'\xe3\x81\x91', 10: u'\xe3\x81\x93', 11: u'\xe3\x81\x95', 12: u'\xe3\x81\x97', 13: u'\xe3\x81\x99', 14: u'\xe3\x81\x9b', 15: u'\xe3\x81\x9d', 16: u'\xe3\x81\x9f', 17: u'\xe3\x81\xa1', 18: u'\xe3\x81\xa4', 19: u'\xe3\x81\xa6', 20: u'\xe3\x81\xa8', 21: u'\xe3\x81\xaa', 22: u'\xe3\x81\xab', 23: u'\xe3\x81\xac', 24: u'\xe3\x81\xad', 25: u'\xe3\x81\xae', 26: u'\xe3\x81\xaf', 27: u'\xe3\x81\xb2', 28: u'\xe3\x81\xb5', 29: u'\xe3\x81\xb8', 30: u'\xe3\x81\xbb', 31: u'\xe3\x81\xbe', 32: u'\xe3\x81\xbf', 33: u'\xe3\x82\x80', 34: u'\xe3\x82\x81', 35: u'\xe3\x82\x82', 36: u'\xe3\x82\x84', 37: u'\xe3\x82\x86', 38: u'\xe3\x82\x88', 39: u'\xe3\x82\x89', 40: u'\xe3\x82\x8a', 41: u'\xe3\x82\x8b', 42: u'\xe3\x82\x8c', 43: u'\xe3\x82\x8d', 44: u'\xe3\x82\x8f', 45: u'\xe3\x82\x92', 46: u'\xe3\x82\x93', 47: u'\xe3\x81\x81', 48: u'\xe3\x81\x83', 49: u'\xe3\x81\x85', 50: u'\xe3\x81\x87', 51: u'\xe3\x81\x89', 52: u'\xe3\x82\x83', 53: u'\xe3\x82\x85', 54: u'\xe3\x82\x87', 55: u'\xe3\x81\x8c', 56: u'\xe3\x81\x8e', 57: u'\xe3\x81\x90', 58: u'\xe3\x81\x92', 59: u'\xe3\x81\x94', 60: u'\xe3\x81\x96', 61: u'\xe3\x81\x98', 62: u'\xe3\x81\x9a', 63: u'\xe3\x81\x9c', 64: u'\xe3\x81\x9e', 65: u'\xe3\x81\xa0', 66: u'\xe3\x81\xa2', 67: u'\xe3\x81\xa5', 68: u'\xe3\x81\xa7', 69: u'\xe3\x81\xa9', 70: u'\xe3\x81\xb0', 71: u'\xe3\x81\xb3', 72: u'\xe3\x81\xb6', 73: u'\xe3\x81\xb9', 74: u'\xe3\x81\xbc', 75: u'\xe3\x81\xb1', 76: u'\xe3\x81\xb4', 77: u'\xe3\x81\xb7', 78: u'\xe3\x81\xba', 79: u'\xe3\x81\xbd', 80: u'\x00', 81: u'\xe3\x82\xa2', 82: u'\xe3\x82\xa4', 83: u'\xe3\x82\xa6', 84: u'\xe3\x82\xa8', 85: u'\xe3\x82\xaa', 86: u'\xe3\x82\xab', 87: u'\xe3\x82\xad', 88: u'\xe3\x82\xaf', 89: u'\xe3\x82\xb1', 90: u'\xe3\x82\xb3', 91: u'\xe3\x82\xb5', 92: u'\xe3\x82\xb7', 93: u'\xe3\x82\xb9', 94: u'\xe3\x82\xbb', 95: u'\xe3\x82\xbd', 96: u'\xe3\x82\xbf', 97: u'\xe3\x83\x81', 98: u'\xe3\x83\x84', 99: u'\xe3\x83\x86', 100: u'\xe3\x83\x88', 101: u'\xe3\x83\x8a', 102: u'\xe3\x83\x8b', 103: u'\xe3\x83\x8c', 104: u'\xe3\x83\x8d', 105: u'\xe3\x83\x8e', 106: u'\xe3\x83\x8f', 107: u'\xe3\x83\x92', 108: u'\xe3\x83\x95', 109: u'\xe3\x83\x98', 110: u'\xe3\x83\x9b', 111: u'\xe3\x83\x9e', 112: u'\xe3\x83\x9f', 113: u'\xe3\x83\xa0', 114: u'\xe3\x83\xa1', 115: u'\xe3\x83\xa2', 116: u'\xe3\x83\xa4', 117: u'\xe3\x83\xa6', 118: u'\xe3\x83\xa8', 119: u'\xe3\x83\xa9', 120: u'\xe3\x83\xaa', 121: u'\xe3\x83\xab', 122: u'\xe3\x83\xac', 123: u'\xe3\x83\xad', 124: u'\xe3\x83\xaf', 125: u'\xe3\x83\xb2', 126: u'\xe3\x83\xb3', 127: u'\xe3\x82\xa1', 128: u'\xe3\x82\xa3', 129: u'\xe3\x82\xa5', 130: u'\xe3\x82\xa7', 131: u'\xe3\x82\xa9', 132: u'\xe3\x83\xa3', 133: u'\xe3\x83\xa5', 134: u'\xe3\x83\xa7', 135: u'\xe3\x82\xac', 136: u'\xe3\x82\xae', 137: u'\xe3\x82\xb0', 138: u'\xe3\x82\xb2', 139: u'\xe3\x82\xb4', 140: u'\xe3\x82\xb6', 141: u'\xe3\x82\xb8', 142: u'\xe3\x82\xba', 143: u'\xe3\x82\xbc', 144: u'\xe3\x82\xbe', 145: u'\xe3\x83\x80', 146: u'\xe3\x83\x82', 147: u'\xe3\x83\x85', 148: u'\xe3\x83\x87', 149: u'\xe3\x83\x89', 150: u'\xe3\x83\x90', 151: u'\xe3\x83\x93', 152: u'\xe3\x83\x96', 153: u'\xe3\x83\x99', 154: u'\xe3\x83\x9c', 155: u'\xe3\x83\x91', 156: u'\xe3\x83\x94', 157: u'\xe3\x83\x97', 158: u'\xe3\x83\x9a', 159: u'\xe3\x83\x9d', 160: u'\x00', 161: u'0', 162: u'1', 163: u'2', 164: u'3', 165: u'4', 166: u'5', 167: u'6', 168: u'7', 169: u'8', 170: u'9', 171: u'!', 172: u'?', 173: u'.', 174: u'-', 175: u'\x00', 176: u'\xe2\x80\xa6', 177: u'\xe2\x80\x9c', 178: u'\xe2\x80\x9d', 179: u'\xe2\x80\x98', 180: u'\xe2\x80\x99', 181: u'\xe2\x99\x82', 182: u'\xe2\x99\x80', 183: u'\x00', 184: u', u', 185: u'\x00', 186: u'/', 187: u'A', 188: u'B', 189: u'C', 190: u'D', 191: u'E', 192: u'F', 193: u'G', 194: u'H', 195: u'I', 196: u'J', 197: u'K', 198: u'L', 199: u'M', 200: u'N', 201: u'O', 202: u'P', 203: u'Q', 204: u'R', 205: u'S', 206: u'T', 207: u'U', 208: u'V', 209: u'W', 210: u'X', 211: u'Y', 212: u'Z', 213: u'a', 214: u'b', 215: u'c', 216: u'd', 217: u'e', 218: u'f', 219: u'g', 220: u'h', 221: u'i', 222: u'j', 223: u'k', 224: u'l', 225: u'm', 226: u'n', 227: u'o', 228: u'p', 229: u'q', 230: u'r', 231: u's', 232: u't', 233: u'u', 234: u'v', 235: u'w', 236: u'x', 237: u'y', 238: u'z', 239: u'\x00', 254: "\n", 255:"\0"}

keys = text_offsets.keys()
values = text_offsets.values()

def parse_text(text):
    return "".join([text_offsets[ord(char)] for char in text])

def encode_text(text):
    return "".join([struct.pack("<B", keys[values.index(char)]) for char in text])

def NoTracebackError(error, text):
    sys.tracebacklimit = 0
    raise error(text)

class Pokemon(object):
    def __init__(self, data, constant_data):
        self.pokemon_names = constant_data[0]
        self.move_names = constant_data[1]
        self.move_effects = constant_data[2]
        set_data = list(set(data))
        self.dummy = set_data == ['\x00'] or sorted(set_data) == ['\x00', '\xff']
        if not self.dummy:
            self.substructures = [self.parse_growth, self.parse_attacks, self.parse_evs, self.parse_misc]
            self.offsets = [(0, 4), \
                            (4, 4), \
                            (8, 10), \
                            (18, 2), \
                            (20, 7), \
                            (27, 1), \
                            (28, 2), \
                            (32, 48)]
            self.parse_data(data[:80])
            if len(data) == 100:
                self.offsets.extend([
                            (0, 4), \
                            (4, 1), \
                            (5, 1), \
                            (6, 2), \
                            (8, 2), \
                            (10, 2), \
                            (12, 2), \
                            (14, 2), \
                            (16, 2), \
                            (18, 2)])
                self.parse_additional(data[80:])
                                    
    def parse_data(self, data):
        self.personality, self.ot_id, self.name, self.lang, self.ot_name, self.markings, self.checksum, self.data_encrypted = struct.unpack("<II10sH7sBH2x48s", data)
        self.name = parse_text(self.name)
        self.ot_name = parse_text(self.ot_name)
        self.decryption_key = self.ot_id^self.personality
        self.decrypt_data()

    def decrypt_data(self):
        decrypted_ints = [i^self.decryption_key for i in struct.unpack("<%sI"%(len(self.data_encrypted)/4), self.data_encrypted)]
#        assert(sum(decrypted_ints)%65535 == self.checksum)
        order = self.personality%24
        self.decrypted = [struct.pack("<3I", *decrypted_ints[i*3:(i+1)*3]) for i in range(4)]
        order = list(permutations(range(4)))[order]
        for index, value in enumerate(order):
            self.substructures[index](self.decrypted[value])

    def parse_additional(self, data):
        pass

    def parse_growth(self, data):
        self.species_id, self.item_id, self.xp, pp_bonus, self.friendship = struct.unpack("<HHIBB2x", data)
        self.species_name = self.pokemon_names[self.species_id]
        self.item = Item(self.item_id, 1)
        self.pp_bonus = [pp_bonus&2, pp_bonus>>2&2, pp_bonus>>4&2, pp_bonus>>6&2]
    def parse_attacks(self, data):
        moves = struct.unpack("<4H4B", data)
        self.moves = zip(moves[:4], moves[4:], [self.move_names[i-1] for i in moves[:4] if i != 0])
        print self.moves

    def parse_evs(self, data):
        evs = struct.unpack("<12B", data)
        self.evs = evs[:6]
        self.contest = evs[6:]

    def parse_misc(self, data):
        pokerus, self.met, origins, ivs, ribbons = struct.unpack("<2BH2I", data)
        self.pokerus = [pokerus & 7, pokerus >> 3 & 31]
        self.origins = [bool(origins >> 15), origins>>11&0xF, origins>>7&0xF, origins&0x3F]
        self.ivs = [ivs&0xF, ivs>>5&0xF, ivs>>10&0xF, ivs>>15&0xF, ivs>>20&0xF, ivs>>25&0xF]
        self.egg = bool(ivs>>30&1)
        self.ability_no = ivs>>31&1
        self.ribbons = [bool(int(i)) for i in list(format(ribbons, '#028b')[2:])]
        self.obedience = ribbons>>31

class Item(object):
    def __init__(self, index, quantity):
        self.index = index
        self.quantity = quantity
        self.dummy = self.index == 0

class Save(object):
    def __init__(self, inputs):
        self.save_game = open(inputs[0], "rb")
        self.save_name = inputs[0]
        self.game_rom = open(inputs[1], "rb")
        self.rom_name = inputs[1]     
        self.rom = self.game_rom.read()
        self.names_offset = self.rom.find(encode_text("BULBASAUR")) # Offset for names of all the pokemon
        self.move_names_offset = self.rom.find(encode_text("POUND"))
        self.move_effects_offset = self.rom.find("\x00(\x00d#\x00\x00\x003\x00\x00\x00")
        self.game_rom.seek(0)
        self.parse_names() # Extract the pokemon names from the rom
        self.parse_move_names() # Extract the move names from the rom
        self.parse_move_effects() # Extract the move abilities from the rom
        self.pokemon_data = [self.pokemon_names, self.move_names, self.move_effects]
        self.save_offsets = [0x000000,0x00E000]
        self.save_size = 57344
        self.section_size = 4096
        self.no_sections = 14
        self.sections = [(3884, self.section_trainer), \
                         (3968, self.section_team), \
                         (3968, self.section_unknown), \
                         (3968, self.section_unknown), \
                         (3848, self.section_rival), \
                         (3968, self.section_pc), \
                         (3968, self.section_pc), \
                         (3968, self.section_pc), \
                         (3968, self.section_pc), \
                         (3968, self.section_pc), \
                         (3968, self.section_pc), \
                         (3968, self.section_pc), \
                         (3968, self.section_pc), \
                         (2000, self.section_pc)]
        self.section_offsets = [(0x0000, 4080), \
                                (0x0FF4, 2), \
                                (0x0FF6, 2), \
                                (0x0FFC, 4)]
        self.trainer_offsets = [0x0000, 0x0008, 0x000A, 0x000E, 0x00AC, 0x0AF8]
        self.pc_offsets = [0x0000, 0x0004, 0x8344, 0x83C2]

        self.pc_sections = ["" for i in range(9)]

        for offset in self.save_offsets:
            self.save_game.seek(offset)
            self.read_save(self.save_game.read(self.save_size))
    
    def parse_names(self):        
        self.game_rom.seek(self.names_offset) # Goto the section
        pokemon_names = parse_text(self.game_rom.read(11*411)) # 11 as that is the space allocated per pokemon and 411 as that is how many pokemon there are
        ascii = pokemon_names.replace(text_offsets[0], "@").encode("ascii", "ignore").replace("\x00", "")
        long_names = filter(None, ascii.split("@"))
        self.pokemon_names = []
        for name in long_names:
            if len(name) >= 10:
                self.pokemon_names.extend([name[i:i+10] for i in range(0, len(name), 10)])
            else:
                self.pokemon_names.append(name)        

    def parse_move_names(self):        
        self.game_rom.seek(self.move_names_offset) # Goto the section
        move_names = parse_text(self.game_rom.read(4602))
        self.move_names = [str(move_names[i:i+13].split("\x00")[0].replace(u"\xb6", " ")) for i in range(0, len(move_names), 13)]

    def parse_move_effects(self):
        self.game_rom.seek(self.move_effects_offset)
        move_effects_raw = self.game_rom.read(12*len(self.move_names))
        self.move_effects = [struct.unpack("<9B3x", move_effects_raw[i:i+12]) for i in range(0, len(move_effects_raw), 12)]

    def read_save(self, game):
        for i in range(0, self.no_sections*self.section_size, self.section_size):
            self.read_section(game[i:i+self.section_size])            
        self.pc_section = "".join(self.pc_sections)
        self.parse_pc_section()
        
    def read_section(self, section):
        section_id = struct.unpack("<H", self.get_data(section, 1))[0]
        checksum =   struct.unpack("<H", self.get_data(section, 2))[0]
        save_index = struct.unpack("<I", self.get_data(section, 3))[0]
        data = self.get_data(section, 0)
        assert(self.get_checksum(data) == checksum)
        self.sections[section_id][1](data[:self.sections[section_id][0]], section_id, data)

    def section_trainer(self, data, section_id, data_orig):
        self.player_name = parse_text(self.get_splice(data, self.trainer_offsets[0], 7))
        self.player_gender = bool(ord(data[self.trainer_offsets[1]]))
        self.trainer_id = struct.unpack("<I", self.get_splice(data,self.trainer_offsets[2],4))[0]
        self.time_played = struct.unpack("<HBBB", self.get_splice(data,self.trainer_offsets[3],5))
        self.game_code = struct.unpack("<I", self.get_splice(data,self.trainer_offsets[4],4))[0]
        if self.game_code == 1: # Red/Green
            self.security_code = struct.unpack("<I", self.get_splice(data,self.trainer_offsets[5],4))[0]
        elif self.game_code != 0: # Emerald
            self.security_code = self.game_code
            self.game_code = 2
        else:
            self.security_code = 0

    def section_team(self, data, section_id, data_orig):
        if self.game_code == 0:
            team_offsets = [(0x0234, 4), \
                            (0x0238, 600), \
                            (0x0490, 4), \
                            (0x0498, 200), \
                            (0x0560, 120), \
                            (0x05B0, 80), \
                            (0x0600, 64), \
                            (0x0640, 256), \
                            (0x0740, 184)]
        elif self.game_code == 2:
            team_offsets = [(0x0234, 4), \
                            (0x0238, 600), \
                            (0x0490, 4), \
                            (0x0498, 200), \
                            (0x0560, 120), \
                            (0x05D8, 120), \
                            (0x0650, 64), \
                            (0x0690, 256), \
                            (0x0790, 184)]
        elif self.game_code == 1:
            team_offsets = [(0x0234, 4), \
                            (0x0038, 600), \
                            (0x0290, 4), \
                            (0x0298, 168), \
                            (0x0310, 120), \
                            (0x03B8, 120), \
                            (0x0430, 52), \
                            (0x0464, 232), \
                            (0x054C, 172)]
        self.team_size = struct.unpack("<I", self.get_splice(data, *team_offsets[0]))[0]
        self.team_pokemon = self.get_splice(data, *team_offsets[1])
        self.team_pokemon = [Pokemon(self.get_splice(self.team_pokemon, i, 100), self.pokemon_data) for i in range(0, len(self.team_pokemon), 100)]
        self.money = struct.unpack("<I", self.get_splice(data, *team_offsets[2]))[0]^self.security_code
        self.item_pockets = []
        for pocket in range(6):
            security_code = self.security_code
            if pocket == 0: security_code = 0
            pocket_size = team_offsets[pocket+3][1]/4
            items = self.get_splice(data, *team_offsets[pocket+3])
            items = [Item( \
                struct.unpack("<H", self.get_splice(items, i, 2))[0], \
                struct.unpack("<H", self.get_splice(items, i+2, 2))[0] ^ security_code\
                    ) for i in range(0, len(items), 4)]
            self.item_pockets.append((pocket_size, items))

    def section_unknown(self, data, section_id, data_orig): pass

    def section_rival(self, data, section_id, data_orig):
        if self.game_code == 1:
            self.rival_name = self.parse_text(self.get_splice(data, 0x0BCC, 8))
        else:
            self.rival_name = ""

    def section_pc(self, data, section_id, data_orig):
        self.pc_sections[section_id-5] = data

    def parse_pc_section(self):
        self.current_pc = struct.unpack("<I", self.get_splice(self.pc_section, self.pc_offsets[0], 4))[0]
        self.pc_pokemon = self.get_splice(self.pc_section, self.pc_offsets[1], 33600)
        self.pc_pokemon = [Pokemon(self.get_splice(self.pc_pokemon, i, 80), self.pokemon_data) for i in range(0, len(self.pc_pokemon), 80)]
        self.box_names = parse_text(self.get_splice(self.pc_section, self.pc_offsets[2], 126)).replace(text_offsets[0], "").split(text_offsets[255])[:-1]
        self.box_wallpapers = [ord(i) for i in self.get_splice(self.pc_section, self.pc_offsets[3], 14)]

    def get_checksum(self, data):
        value = sum(struct.unpack("<%sI"%(len(data)/4), data))
        return ((value>>16) + value)&0xFFFF                          

    def get_splice(self, var, start, length):
        return var[start:start+length]

    def get_data(self, section, section_offset):
        return section[self.section_offsets[section_offset][0]:self.section_offsets[section_offset][0]+self.section_offsets[section_offset][1]]

if __name__ == "__main__":
    try: sys.argv[2]
    except IndexError: NoTracebackError(IOError, "Save file doesn't exist!")
    save = Save(sys.argv[1:])
