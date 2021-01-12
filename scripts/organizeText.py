#! /usr/bin/env python3

import os
import re
import sys

SPEAKERS = {
    "a2b": "2B",
    "a9s": "9S",
    "a2": "A2",
    "op60": "Operator 6O",
    "pod042": "Pod 042",
    "pod153": "Pod 153",
    "a1d": "1D",
    "a4b": "4B",
    "telo": "TODO",
    "eng": "Engels",
}

def parseId(id):
    splitted = id.split("_")
    if len(splitted) != 5:
        print(id)
        # TODO: check
        return None

    mission = splitted[0]
    section = splitted[1]
    scene = splitted[2]
    number = splitted[3]
    speaker = splitted[4]

    return {
        "mission": mission,
        "section": section,
        "scene"  : scene,
        "number" : number,
        "speaker": speaker,
    }

def scenePrefixToNumber(scene):
    s = scene[0]
    assert s in ["S", "G", "H"]
    if s == "S":
        return 0
    elif s == "G":
        return 1
    elif s == "H":
        return 2

def idKeyFunction(id):
    mission = id["mission"]
    assert mission[0] == "M", "{}".format(mission)
    section = id["section"]
    assert section[0] == "S", "{}".format(section)
    scene = id["scene"]
    assert scene[0] in ["G", "H", "S"]
    number = id["number"]

    return (int(mission[1:]), int(section[1:]), scenePrefixToNumber(scene), int(scene[1:]), int(number))

def parseFile(filename, parsedText):
    contents = None
    with open(filename, "r") as f:
        contents = f.readlines()
    if contents is None:
        return

    contents = [ line.strip() for line in contents ]
    i = 0
    data = {}
    while i < len(contents):
        line = contents[i]

        if line.startswith("ID"):
            id = contents[i][4:]
            jp = contents[i+1][4:]
            en = contents[i+2][4:]
            parsedId = parseId(id)
            data[id] = (parsedId, jp, en, filename)
            i += 3
        else:
            i += 1

    # data = dict(sorted(data.items(), key=lambda item: idKeyFunction(item[1][0])))
    # print("\n".join([k for k, v in data.items()]))

    return {**parsedText, **data}

def exportText(text, fname, filter=None):
    with open(fname, "w") as f:
        for id, v in text.items():
            # if (filter is not None) and (filter not in id):
            #     continue
            if (filter is not None) and (re.match(filter, id) is None):
                continue

            idParsed, jp, en, filename = v
            f.write("filename: {}\n".format(filename))
            f.write("ID: {}\n".format(id))
            f.write("JP: {}\nEN: {}\n\n".format(jp, en))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <link rel="stylesheet" href="css/yorha.min.css"/>
        <title>YoRHa</title>
    </head>
    <body>
        <h1>Nier:Automata</h1>

        {}
    </body>
</html>
"""

LINE_TEMPLATE = """
        <figure>
            <figcaption>{caption}</figcaption>
            <div>
                <p>{japanese}</p>
                <p>{english}</p>
            </div>
        </figure>
"""

def exportHtml(text, fname, filter=None):
    contents = ""
    for id, v in text.items():
        # if (filter is not None) and (filter not in id):
        #     continue
        if (filter is not None) and (re.match(filter, id) is None):
            continue

        idParsed, jp, en, filename = v
        contents += LINE_TEMPLATE.format(caption=SPEAKERS[idParsed["speaker"]], japanese=jp, english=en)
    contents = HTML_TEMPLATE.format(contents)

    with open(fname, "w") as f:
        f.write(contents)

if __name__ == "__main__":
    DIRS = ["data/ph1", "data/ph2"]

    parsedText = {}
    for d in DIRS:
        for root, dir, files in os.walk(d):
            for name in files:
                filename = os.path.join(root, name)
                print(filename)
                parsedText = parseFile(filename, parsedText)

    parsedText = dict(sorted(parsedText.items(), key=lambda item: idKeyFunction(item[1][0])))
    print("\n".join([k for k, v in parsedText.items()]))

    # First mission, first route (A)
    # exportText(parsedText, "output/mission0010.txt", filter="M0010")
    exportText(parsedText, "output/mission0010.txt", filter=r"M0010_.+_.+_[01]\d+_.")
    exportHtml(parsedText, "website/test.html", filter=r"M0010_.+_.+_[01]\d+_.")

    # exportText(parsedText, "output/mission1020.txt", filter=r"M1020_S\d+_.+_[01]\d+_.")
