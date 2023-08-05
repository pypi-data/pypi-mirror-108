from os import error
import click
from fontTools import ttLib
import os
import json
from pathlib import Path
import shutil
from re import sub

OUTPUT_FOLDER_NAME = "xcfont_out"


@click.command()
@click.option("--in", "-i", "in_dir", required=True, help="Path to foler font file.")
@click.option("--out", "-o", "out_dir", required=False, default="", help="Path to generate output")
def process(in_dir, out_dir):

    if not bool(out_dir):
        out_dir = in_dir

    fonts = get_font(in_dir)
    # jsonStr = json.dumps(fonts, default=lambda font: font.__dict__)
    # print(jsonStr)
    generate_plist(fonts, out_dir)
    generate_convenient_code(fonts, out_dir)


class Font:
    def __init__(self, name, family, file_name):
        self.name = name
        self.family = family
        self.file_name = file_name


def get_font(dir):
    res = []

    # find all ttf file in path
    files = read_font_folder(dir)

    if len(files) > 0:
        print("👏 Found {} font file(s)".format(len(files)))
    else:
        print("😢 Found nothing!!!")
        exit(1)

    # extract font name
    for dir, file_name in files:
        font_name, font_family = read_font(dir)
        res.append(Font(font_name, font_family, file_name))

    return res


def read_font_folder(path):
    res = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".ttf"):
                res.append((os.path.join(root, file), file))

    return res


def read_font(font_path):
    font = ttLib.TTFont(font_path)
    return shortName(font)


FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1


def shortName(font):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font['name'].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')
        else:
            name_str = record.string.decode('latin-1')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            family = name_str
        if name and family:
            break
    return name, family


def generate_plist(fonts, out_dir):
    formatStr = """
<key>UIAppFonts</key>
<array>
{}
</array>
    """
    items = []
    for font in fonts:
        items.append("\t<string>{}</string>".format(font.file_name))
    itemsStr = "\n".join(items)
    xmlString = formatStr.format(itemsStr)

    out_path = Path(out_dir).joinpath(OUTPUT_FOLDER_NAME)
    if out_path.is_dir():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)
    xmlFilePath = out_path.joinpath('plist.xml')
    if out_path.is_dir():
        f = open(xmlFilePath, "w")
        f.write(xmlString)
        f.close()
        print("✅ Generated plist file success")
        print("👉 Copy and paste its content to Info.plist file of Xcode project: {}".format(
            xmlFilePath.absolute()))


def camelCase(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return string[0].lower() + string[1:]


def generate_convenient_code(fonts, out_dir):
    formatStr = """import UIKit
    
enum FontName: String {{
{0}
}}

extension FontName {{
    func asUIFont(size: CGFloat) -> UIFont? {{
        UIFont(name: rawValue, size: size)
    }}
}}

#if canImport(SwiftUI)
import SwiftUI

extension FontName {{
    func asFont(size: CGFloat) -> Font {{
        Font.custom(rawValue, size: size)
    }}
    
    func asFont(fixedSize: CGFloat) -> Font {{
        Font.custom(rawValue, fixedSize: fixedSize)
    }}
    
    func asFont(size: CGFloat, relativeTo: Font.TextStyle) -> Font {{
        Font.custom(rawValue, size: size, relativeTo: relativeTo)
    }}
}}
#endif
    """
    formatItem = """\tcase {} = {}"""
    items = []
    for font in fonts:
        items.append(formatItem.format(camelCase(font.name), "\"" + font.name + "\""))
    itemsStr = "\n".join(items)
    contentString = formatStr.format(itemsStr)
    
    out_path = Path(out_dir).joinpath(OUTPUT_FOLDER_NAME)
    out_path.mkdir(parents=True, exist_ok=True)
    xmlFilePath = out_path.joinpath('FontName.swift')
    if out_path.is_dir():
        f = open(xmlFilePath, "w")
        f.write(contentString)
        f.close()
        print("✅ Generated swift file success")
        print("👉 Copy and paste its content to your project file of Xcode project: {}".format(
            xmlFilePath.absolute()))


if __name__ == "__main__":
    process()
