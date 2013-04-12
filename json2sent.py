"""
	json2sent

	converts a JSON tree back to a plain text sentence
"""

import sys, json


def get_sentence(tree, sent):
	if isinstance(tree, basestring):
		if len(sent[0]) > 0:
			sent[0] += " "
		sent[0] += tree
		
		return

	for i in range(1, len(tree)):
		get_sentence(tree[i], sent)

def main(infile):
	with open(infile) as f:
		for line in f:
			tree = json.loads(line.rstrip('\n'))
			sent = [""]
			get_sentence(tree, sent)
			print sent[0].encode('utf-8', 'ignore')

if __name__ == "__main__":
	main(sys.argv[1])