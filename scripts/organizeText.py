#! /usr/bin/env python3

import os
import re

SPEAKERS = {
    "a2b"        : "2B",
    "a7b"        : "7B",
    "a8b"        : "8B",
    "a9s"        : "9S",
    "a11s"       : "11S",
    "a2"         : "A2",
    "a1d"        : "1D",
    "a4b"        : "4B",
    "op60"       : "Operator 6O",
    "op210"      : "Operator 21O",
    "pod042"     : "Pod 042",
    "pod153"     : "Pod 153",
    "ane"        : "Anemone",
    "resi"       : "Resistance Member",
    "resiman"    : "Resistance Member (man)",
    "resiwoman"  : "Resistance Member (woman)",
    "resiwoman2" : "Resistance Member (woman)",
    "hennnawresi": "Strange Resistance Member",
    "pascal"     : "Pascal",
    "robo"       : "Robot",
    "eng"        : "Engels",
    "adam"       : "Adam",
    "eve"        : "Eve",
    "sele"       : "Selection (in a textbox)",
}

ALL_MISSIONS_FILE = "scripts/data/ALL_MISSIONS.txt"
assert os.path.isfile(ALL_MISSIONS_FILE)

class LineID(object):
    def __init__(self, s):
        self._parse(s)

    def isValid(self):
        if self.mission[0] != "M":
            return False
        if self.section[0] != "S":
            return False
        if self.scene[0] not in ["G", "H", "S"]:
            return False

        return True

    def comparator(self):
        assert self.isValid()

        return (int(self.mission[1:]), int(self.section[1:]), self._scenePrefixToNumber(), int(self.scene[1:]), int(self.number))

    def getSpeaker(self):
        if self.speaker not in SPEAKERS.keys():
            return "UNKNOWN ({})".format(self.speaker)
        return SPEAKERS[self.speaker]

    def __str__(self):
        s = ""
        s += "mission={},".format(self.mission)
        s += "section={},".format(self.section)
        s += "scene={},".format(self.scene)
        s += "number={},".format(self.number)
        s += "speaker{}".format(self.speaker)

        return s

    def _parse(self, s):
        self.raw_id = s

        splitted = s.split("_")
        if len(splitted) != 5:
            raise ValueError("{} is not a valid Id".format(s))

        self.mission = splitted[0]
        self.section = splitted[1]
        self.scene = splitted[2]
        self.number = splitted[3]
        self.speaker = splitted[4]

    def _scenePrefixToNumber(self):
        assert self.isValid()

        s = self.scene[0]
        if s == "S":
            return 0
        elif s == "G":
            return 1
        elif s == "H":
            return 2

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <link rel="stylesheet" href="../css/yorha.min.css"/>
        <link rel="stylesheet" href="../css/style.css"/>
        <title>Nier:Automata - {title}</title>
    </head>
    <body>
        <h1>Nier:Automata</h1>
        <h2>{title}</h2>

        <ul>
            <li><a href="../index.html">Home</a></li>
            <li><a href="#" id="show-jp">Show Japanese</a></li>
            <li><a href="#" id="show-en">Show English</a></li>
        </ul>

        {text}

        <script src="../js/main.js"></script>
    </body>
</html>
"""

LINE_TEMPLATE = """
        <figure>
            <figcaption>{caption}</figcaption>
            <div class="container">
                <div>
                    <p class="jp-{idx}">{japanese}</p>
                    <p class="en-{idx}">{english}</p>
                </div>
                <div>
                    <button class="switch-lang-{idx}">Switch</button>
                </div>
            </div>
        </figure>
"""

class TextDump(object):
    def __init__(self):
        self.data = {}

    def __str__(self):
        return "\n".join([k for k, v in self.data.items()])

    def sort(self):
        self.data = dict(sorted(self.data.items(), key=lambda item: item[1][0].comparator()))

    def parseFile(self, filename):
        assert os.path.isfile(filename)

        with open(filename, "r") as f:
            contents = f.readlines()

        contents = [ line.strip() for line in contents ]
        i = 0
        data = {}
        while i < len(contents):
            line = contents[i]

            if line.startswith("ID"):
                id = contents[i][4:]
                jp = contents[i+1][4:]
                en = contents[i+2][4:]

                self.data[id] = (LineID(id), jp, en, filename)
                i += 3
            else:
                i += 1

    def exportText(self, fname, filter=None, verbose=False):
        if verbose:
            print("Exporting to {}...".format(fname))

        with open(fname, "w") as f:
            for id, v in self.data.items():
                if (filter is not None) and (re.match(filter, id) is None):
                    continue

                idParsed, jp, en, filename = v
                f.write("filename: {}\n".format(filename))
                f.write("ID: {}\n".format(id))
                f.write("JP: {}\nEN: {}\n\n".format(jp, en))

    def exportHtml(self, fname, title, filter=None, verbose=False):
        if verbose:
            print("Exporting to {}...".format(fname))

        contents = ""
        for idx, (id, v) in enumerate(self.data.items()):
            if (filter is not None) and (re.match(filter, id) is None):
                continue

            idParsed, jp, en, filename = v
            contents += LINE_TEMPLATE.format(caption=idParsed.getSpeaker(),
                                             idx=idx,
                                             japanese=jp, english=en)
        contents = HTML_TEMPLATE.format(title=title, text=contents)

        with open(fname, "w") as f:
            f.write(contents)

if __name__ == "__main__":
    # Parse missions file
    with open(ALL_MISSIONS_FILE, "r") as f:
        ALL_MISSIONS = f.readlines()
        ALL_MISSIONS = [ mission.strip() for mission in ALL_MISSIONS ]

    # Parse all text
    DIRS = ["data/core",
            "data/ph1", "data/ph2", "data/ph3", "data/ph4", "data/phf",
            ]

    textDump = TextDump()
    for d in DIRS:
        print("Reading from directory {}:".format(d))
        assert os.path.isdir(d)
        for root, dir, files in os.walk(d):
            for name in files:
                filename = os.path.join(root, name)
                print("\t- parsing {}...".format(filename))
                textDump.parseFile(filename)

    textDump.sort()

    # Export
    # First route, first mission
    # textDump.exportText("output/mission0010.txt",
    #                     filter=r"M0010_.+_.+_[01]\d+_.", verbose=True)
    # textDump.exportHtml("website/missions/0010.html", title="Misssion 0010",
    #                     filter=r"M0010_.+_.+_[01]\d+_.", verbose=True)

    # All missions for the first route
    # TODO: check if it is really only the first route
    for mission in ALL_MISSIONS:
        textDump.exportHtml("website/missions/{}.html".format(mission[1:]),
                            title="Mission {}".format(mission[1:]),
                            filter=r"{}_S\d+_.+_[01]\d+_.".format(mission), verbose=True)
