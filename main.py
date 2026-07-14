# Copyright (c) 2026 xuanfeng0316
# SPDX-License-Identifier: MIT
#
# By xuanfeng0316
#
# This is only the first version of the feasibility test.
# You need to prepare a file called "input.jpg". 
# The output needs to be viewed in "CommandOutput.txt".
# Only square pictures have been tested so far.
# The output command is suggested to be executed by a command block,
# because it is too long to type in chat.
# The command format of this process output is limited to Minecraft: Java Edition.
from PIL import Image
import os

# This is the picture pixel against which all characters are compared.
# In Minecraft:Java Edition, the width of these characters is equal.
BRAILLE_MAP = {
    0b000000: '⠀', 0b000001: '⠁', 0b000010: '⠂', 0b000100: '⠄', 0b001000: '⡀',
    0b010000: '⠈', 0b100000: '⠐', 0b000011: '⠃', 0b000101: '⠅',
    0b001001: '⡁', 0b010001: '⠉', 0b100001: '⠑', 0b000110: '⠆',
    0b001010: '⡂', 0b010010: '⠊', 0b100010: '⠒', 0b001100: '⡄',
    0b010100: '⠌', 0b100100: '⠔', 0b011000: '⠨', 0b101000: '⠠',
    0b000111: '⠇', 0b001011: '⡃', 0b010011: '⠋', 0b100011: '⠓',
    0b001101: '⡅', 0b010101: '⠍', 0b100101: '⠕', 0b001110: '⡆',
    0b010110: '⠎', 0b100110: '⠖', 0b011001: '⠩', 0b101001: '⠡',
    0b011010: '⠪', 0b101010: '⠢', 0b011100: '⠬', 0b101100: '⠤',
    0b110000: '⠰', 0b001111: '⡇', 0b010111: '⠏', 0b100111: '⠗',
    0b011011: '⠫', 0b101011: '⠣', 0b011101: '⠭', 0b101101: '⠥',
    0b011110: '⠮', 0b101110: '⠦', 0b110001: '⠱', 0b110010: '⠲',
    0b110100: '⠴', 0b111000: '⠸', 0b011111: '⠯', 0b101111: '⠧',
    0b110011: '⠳', 0b110101: '⠵', 0b110110: '⠶', 0b111001: '⠹',
    0b111010: '⠺', 0b111100: '⠼', 0b111111: '⠿'
}

MAX_CHAR_COLS = 60
MAX_CHAR_ROWS = 20

def img_to_mc_text(image_path):
    try:
        img = Image.open(image_path).convert('L')
    except Exception as e:
        return None, f"The picture failed to open: {e}"

    img = img.resize((MAX_CHAR_COLS * 2, MAX_CHAR_ROWS * 3))

    blocks = []
    for row in range(MAX_CHAR_ROWS):
        for col in range(MAX_CHAR_COLS):
            total = 0
            for dy in range(3):
                for dx in range(2):
                    total += img.getpixel((col * 2 + dx, row * 3 + dy))
            avg = total // 6
            blocks.append(avg)

    min_bright = min(blocks)
    max_bright = max(blocks)
    if max_bright == min_bright:
        max_bright = min_bright + 1

    def map_to_braille(brightness):
        normalized = (brightness - min_bright) / (max_bright - min_bright)
        value = int(normalized * 255)
        return value

    lines = []
    for row in range(MAX_CHAR_ROWS):
        line = ''
        for col in range(MAX_CHAR_COLS):
            idx = row * MAX_CHAR_COLS + col
            brightness = blocks[idx]
            braille_value = map_to_braille(brightness)
            if braille_value > 200:
                line += '⠿'
            elif braille_value > 150:
                line += '⠧'
            elif braille_value > 100:
                line += '⠇'
            elif braille_value > 50:
                line += '⠁'
            else:
                line += '⠀'
        lines.append(line)

    text = '\\n'.join(lines)
    command = f'/tellraw @a {{"text":"{text}"}}'
    return command, None

# You can customize the names and paths of input files and output files here
def main():
    img_path = 'input.jpg'
    out_path = 'CommandOutput.txt'

    print("Working……")
    cmd, err = img_to_mc_text(img_path)
    if err:
        print(f"Generation failed: {err}")
        return

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(cmd)
    print(f"Done! File: {out_path}")

if __name__ == '__main__':
    main()