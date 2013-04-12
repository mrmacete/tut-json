"""
	normalize_tree

	convert a JSON tree to chomsky normal form,
	performs a simplification of the grammar, to be handled by poor-performing scripts
"""

import sys, json, re

punctuation = re.compile("^[^\w\s\d\(\)\"]$")
simple_articles = set(["il", "lo", "la", "i", "gli", "le", "l'"])
simplifier = re.compile("^([A-Za-z0-9\*]+)[\-~].*$")

def split_nary(tree):
	if isinstance(tree, basestring):
		return

	if len(tree) > 3:
		tree[2] = [tree[0]] + tree[2:]
		del tree[3:]

	for i in range(1, len(tree)):
		split_nary(tree[i])

def split_nary_old(tree):
	if isinstance(tree, basestring):
		return

	if len(tree) > 3:
		split = [tree[0]]
		for i in range(2,len(tree)):
			split.append(tree[i])
		tree[2] = split
		del tree[3:]
		split_nary(tree[2])
	else:
		for i in range(1,len(tree)):
			split_nary(tree[i])

def remove_next_art_de(tree):
	if isinstance(tree, basestring):
		return False

	if tree[0].find("NP") == 0 and len(tree) > 1 and not isinstance(tree[1], basestring):
		if tree[1][0] == "ART~DE" and tree[1][1].lower() not in simple_articles:
			del tree[1]
			return True;
		return remove_next_art_de(tree[1])



def collapse_prepart(tree):
	if isinstance(tree, basestring):
		return

	if tree[0].find("PP") == 0:
		for i in range(1,len(tree)):
			if not isinstance(tree[i], basestring) and tree[i][0] == "PREP":
				if (i+1) < len(tree):
					if remove_next_art_de(tree[i+1]):
						tree[i][0] = "PREP~ART"

	for i in range(1,len(tree)):
		collapse_prepart(tree[i])


def collapse_unary(tree):
	if isinstance(tree, basestring):
		return

	if len(tree) == 2:
		if len(tree[0]) == 1:
			tree[0] = punctuation.sub(".", tree[0])

		if not isinstance(tree[1], basestring) and len(tree[1]) > 1:
			
			tree[0] += "+" + tree[1][0]
			tree[1] = tree[1][1]
			collapse_unary(tree)
	else:
		for i in range(1, len(tree)):
			collapse_unary(tree[i])

def reduce_rules(tree):
	if isinstance(tree, basestring):
		return

	tree[0] = simplifier.sub("\g<1>", tree[0])
	for i in range(1,len(tree)):
		reduce_rules(tree[i])


def normalize_tree(tree):
	collapse_prepart(tree)
	reduce_rules(tree)
	collapse_unary(tree)
	split_nary(tree)
	print json.dumps(tree)
	

def main(infile):
	with open(infile) as f:
		for line in f:
			lstring = line.rstrip('\n')
			tree = json.loads(lstring)
			normalize_tree(tree)
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "usage: python normalize_tree.py unnormalized.json"
	else:
		main(sys.argv[1])
