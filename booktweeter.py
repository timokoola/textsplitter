from twython import Twython
import json
import argparse
import io

bio_text = """The One From Sun Race. Tweets collected works of H.P.Lovecraft. Run by @tkoola\n\nReading: %s"""

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
                        help="bookfile to be converted", default="book.txt")
    parser.add_argument("-w", "--workingfile",
                        help="workingfile to be tweeted", default="book.working")
    parser.add_argument("-k", "--keyfile",
                        help="credentials of the twitter accounts", default="test.keys")
    parser.add_argument("-p", "--progressfile",
                        help="which line are we at?", default="line.txt")
    parser.add_argument("-l", "--line",
                        help="tweet line number", type=int, default=0)

    args = parser.parse_args()
    return args

def update_bio(tweet, api):
    if tweet.startswith("* "):
        bio = tweet[2:]
        api.update_profile(description=bio_text % bio)



if __name__ == "__main__":
    args = handle_command_line()
    api = (TwythonHelper(args.keyfile)).api
    f = io.open(args.workingfile, encoding="utf-8")
    lines = f.readlines()
    tweet = lines[args.line]
    update_bio(tweet, api)
    api.update_status(status=tweet.replace("<br/>","\n"))