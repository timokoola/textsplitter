from __future__ import print_function
from twython import Twython
import json
import argparse
import io
import sys
import os.path 
from datetime import datetime, timedelta
from email.utils import parsedate_tz


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
        description="Tweets a book split into working file. Run init.py to create the workingfile.")
    parser.add_argument("-w", "--workingfile",
                        help="workingfile to be tweeted", default="book.working")
    parser.add_argument("-k", "--keyfile",
                        help="credentials of the twitter accounts", default="test.keys")
    parser.add_argument("-p", "--progressfile",
                        help="which line are we at?", default="line.txt")
    parser.add_argument("-l", "--line",
                        help="tweet line number", type=int, default=-1)

    args = parser.parse_args()
    return args

def update_bio(bio, api):
    if bio != "":
        api.update_profile(description=bio_text % bio)

def open_working_file(wf):
    if not os.path.exists(wf):
        print("No such file %s. Run init.py on book" % wf, file=sys.stderr)
        sys.exit(1)
    else:
        f = io.open(args.workingfile, encoding="utf-8")
        lines = f.readlines()
        f.close()
        return (lines, len(lines))

def current_line(lineno, progressfile, maxlines):
    if lineno >= 0:
        return (lineno, lineno >= maxlines)
    elif os.path.exists(progressfile):
        f = io.open(progressfile)
        prlines = f.readlines()
        f.close()
        if(len(prlines)) < 1:
            line = 0
        else:
            line = int(prlines[-1].strip(),10) + 1
        f = io.open(progressfile, "w")
        for i in prlines[-10:]:
            f.write(i)
        f.write(u"%d\n" % line)
        f.close()
        return (line, line >= maxlines)
    else:
        f = io.open(progressfile, "w")
        f.write(u"0\n")
        f.close()
        return (0, False)

def last_seen_ages_ago(api):
    tl = api.get_user_timeline()
    if len(tl) == 0:
        # Just starting (or API acting up), no need to inform about that
        return False
    else:
        td = tl[0]["created_at"]
        timestamp = datetime(*(parsedate_tz(td)[:6]))
        utcnow = datetime.utcnow()
        diff = (timestamp - utcnow).total_seconds()
        if diff > 3600:
            return True
        else:
            return False


def check_for_problems(api, finished=False, args=None):
    if finished:
        perform_tweet("@tkoola I am done reading. See you soon!", api)
        os.remove(api.progressfile)
        sys.exit(1)
    if last_seen_ages_ago(api):
        perform_tweet("@tkoola I am not feeling alright. %f" % time.time(), api)

def prepare_tweet(lines, curr_line):
    line = lines[curr_line].strip()
    line = line.replace("<br/>", "\n")
    bio = ""
    if line.startswith("* "):
        bio = line[2:]
    return (bio, line)

def perform_tweet(tweet,api):
    api.update_status(status=tweet)

if __name__ == "__main__":
    args = handle_command_line()
    api = (TwythonHelper(args.keyfile)).api
    check_for_problems(api, False, api)
    args = handle_command_line()
    (lines, linecount) = open_working_file(args.workingfile)
    (curr_line, finished)  = current_line(args.line, args.progressfile, linecount)
    check_for_problems(api, finished, args)
    (bio, tweet) = prepare_tweet(lines,curr_line)
    update_bio(bio, api)
    perform_tweet(tweet, api)