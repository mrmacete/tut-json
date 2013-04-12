"""
	pick_sets

	simple script to split a JSON file, randomly, in train/test/dev sets.

	the input parameters are the file name and the (integer) percentage of input lines to use in training set.
	the remaining percentage is equally divided in test/dev.

	although this script has been made to handle JSON format, it does not make assumptions in the input format
	except that there should be one sample per line.


"""


import sys, os, random

def main(infile, ptrain):
	splt = os.path.splitext(infile)
	bname = splt[0]
	ext = ""

	if len(splt) == 2:
		ext = splt[1]

	outtrain = bname + ".train" + ext
	outdev = bname + ".dev" + ext
	outtest = bname + ".test" + ext

	pt = float(ptrain) / 100.0
	pdt = float(100 - ptrain) / 100.0
	pdev = float( pdt / 2 )

	print outtrain + " %f" % pt
	print outdev + " %f" % pdev
	print outtest + " %f" % pdev

	with open(infile) as f:
		with open(outtrain, "w") as tra:
			with open(outtest, "w") as tes:
				with open(outdev, "w") as dev:
					for line in f:
						x = random.random()
						if x <= pt:
							tra.write(line)
						elif x > pt and x <= (pt+pdev):
							dev.write(line)
						elif x > (pt+pdev):
							tes.write(line)

if __name__ == "__main__":
	main(sys.argv[1], int(sys.argv[2]))