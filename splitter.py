import string
import re 
from nltk import sent_tokenize
import io
import sys

def score(c,n,l):
    if l > 139:
        return -1
    elif c == "\n" and n == "\n":
        return sys.maxint
    elif c == ",":
        return l * 1.59
    elif c == "'":
        return min(139,l)
    elif c in string.punctuation:
        return l * 1.18
    elif c in string.whitespace:
        return l * 1.03
    else:
        return min(139,l)

def div_text(text):
    if len(text) < 140 and text.find("\n\n") == -1:
        return (text, "")
    zpd = zip(text, "a" +text, xrange(len(text)))
    cmap = map(lambda x: score(x[0],x[1],x[2]) ,zpd)
    index = cmap.index(max(cmap))
    return (text[:index+1] + "<cont/>", text[index+1:])

def split(t):
    if len(t) < 140 and t.find("\n\n") == -1:
        return [t.strip().replace("\n"," ")]
    text = t
    result = []
    while len(text) > 0:
        (extracted, text) = div_text(text)
        clean = extracted.strip().replace("\n"," ")
        assert(len(clean.replace("<cont/>", "")) <= 140)
        result.append(clean)
    return result

def tokenized_file(fn, encoding):
    f = io.open(fn, encoding=encoding)
    text = f.read()
    f.close()
    return sent_tokenize(text)

def working_file(fn, tokenized_text):
    f = io.open(fn, "w+", encoding="utf-8")
    for line in tokenized_text:
        for l in split(line):
            if len(l.strip()) == 0:
                continue
            f.write(l)
            f.write(u"\n")

    f.close()
