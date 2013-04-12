"""
	penn2json

	converts a file from PENN format to JSON.

	in the JSON format, each line is a JSON array.

	the output is not in Chomsy normal form, i.e. the branches may be more than 2 at each node.
"""

import sys, re

marker = re.compile("^ *\*\*\*.*\*\*\* *$")
quotes = re.compile("\"", re.M)
words = re.compile("([^ \(\)\t\n]+)", re.M)
commas1 = re.compile("\" [\n ]?[\t ]*([\"\(])", re.M)
commas2 = re.compile("\) ?[\n ]?[\t ]*\(", re.M)
unwrap = re.compile("(^ \( )|( \) $)", re.M)
whiteline = re.compile("\n+", re.M)

def convert_block( block ):
	if len(block) == 0:
		return

	res = marker.sub("", block)
	res = quotes.sub("\\\"", res)
	res = words.sub("\"\g<1>\"", res)
	res = commas1.sub("\", \g<1>", res)
	res = commas2.sub("), (", res)
	res = unwrap.sub("", res)
	res = whiteline.sub("", res)
	print res.replace("(", "[").replace(")", "]")

def main(infile):
	with open(infile) as f:
		block = ""
		for line in f:
			if marker.search(line) != None:
				convert_block(block)

				block = ""
			else:
				block += line

		convert_block(block)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "usage: python penn2json.py infile.penn"
	else:
		main(sys.argv[1])

