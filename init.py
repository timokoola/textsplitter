import argparse
from splitter import tokenized_file, working_file


def handle_command_line():
    parser = argparse.ArgumentParser(
        description="Splits a text into working file. ")
    parser.add_argument("-t", "--textfile",
                        help="Text file to be converted", default="book.txt")
    parser.add_argument("-w", "--workingfile",
                        help=" Name of workingfile to be created", default="book.working")
    parser.add_argument("-e", "--encoding",
    					help="Encoding of the input file", default="utf-8")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
	args = handle_command_line()
	working_file(args.workingfile,tokenized_file(args.textfile,args.encoding))


