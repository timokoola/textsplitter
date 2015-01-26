from twython import Twython
import json
import argparse

class TwythonHelper:

    def __init__(self, keyfile):
        f = open(keyfile)
        lines = f.readlines()
        f.close()
        consumerkey = lines[0].split("#")[0]
        consumersecret = lines[1].split("#")[0]
        accesstoken = lines[2].split("#")[0]
        accesssec = lines[3].split("#")[0]

        self.api = Twython(consumerkey, consumersecret, accesstoken, accesssec)


def handle_command_line():
    parser = argparse.ArgumentParser(
        description="Tweets a book split into working file or creates a working file")
    parser.add_argument("-b", "--bookfile",
                        help="contents of the game", default="gamefile.txt")
    args = parser.parse_args()
    return args
