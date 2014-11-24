#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
from text_offsets import *

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
    pokemon_names[82] = "FARFETCH'D"
    pokemon_names[83] = "DODUO"
    pokemon_names[121] = "MR-MIME"
    del pokemon_names[122]
    return pokemon_names

rom = open("Pokemon Emerald.gba", "rb")
names = parse_names(rom)
rom.close()
save_locations = ["normal", "shiny", "back-normal", "back-shiny"]
for index, name in enumerate(names):
    if index in [28, 31, 82, 83, 121, 122]:
        print index, name
    if name != "?" and name != "UNOWN":
        for i in save_locations:
            form = "png"
            save_dir = i
            if i.find("back-") == -1:
                save_dir = "front-"+save_dir
            os.system("wget -O Assets/Textures/Pokemon/%s/%s.%s http://img.pokemondb.net/sprites/emerald/%s/%s.%s"%(save_dir, index, form, i, name.lower(), form))
