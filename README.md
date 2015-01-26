# textsplitter
Splits long texts to tweet sized chunks Python version

## Algorithm

Splits a long text to 140 or less long chunks. Following rules apply:

Prerun:
* Replace single line break with space unless it is followed by a capitalized character


* Split when two or more consecutive line breaks
* Split at last punctuation before 140 characters is full as long as punctuation is preceded by at least five non-punctuation characters. (e.g. when we have "...John Smith was late. P. G. Wodehouse was getting angry." we prefer to break after "late.") 
* If that fails, split at last whitespace before 140 characters is full, favour linebreaks over other white space
* And if even that fails, split at 140 characters.
