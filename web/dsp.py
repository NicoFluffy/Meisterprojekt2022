import requests

address = "http://192.168.1.190?cmd="

cmds = {
        "film": "1.",
        "sprache": "2.",
        "mutem1": "WD03%2A1GRPM|",
        "unmutem1": "WD03%2A0GRPM|",
        "vol0":  "WD1%2A-300GRPM|",
        "vol1": "WD1%2A-270GRPM|",
        "vol2": "WD1%2A-240GRPM|",
        "vol3": "WD1%2A-210GRPM|",
        "vol4": "WD1%2A-180GRPM|",
        "vol5": "WD1%2A-150GRPM|",
        "vol6": "WD1%2A-120GRPM|",
        "vol7": "WD1%2A-90GRPM|",
        "vol8": "WD1%2A-60GRPM|",
        "vol9": "WD1%2A-30GRPM|",
        "vol10": "WD1%2A0GRPM|"
}
def sendCMD(cmd):
        print(cmd, cmd in cmds)
        if cmd in cmds:
                print("schalte dsp:", cmd, address+cmds[cmd])
                requests.get(address+cmds[cmd])
       