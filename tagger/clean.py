
import sys

def reformat(inp):
	return inp.split("-")[1].replace("S","+").replace("U","-")

def reformatline(line):
	return [reformat(scansion) for word,scansion in line]

def divide_wan(line):
	return [word.split("__") for word in line.strip().split(" ")]

if __name__ == '__main__':

	f=open(sys.argv[1])
	lines = [divide_wan(line) for line in f]
	f.close()


	words = [[word for word,scansion in line] for line in lines]
	analyses = [reformatline(line) for line in lines]

	longest_line = max([sum([len(w) for w in line]) for line in words]) + 10

	sep = "_"

	toprint = ""
	for linewords, linescans in zip(words,analyses):
		for word in linewords:
			toprint += word+" "
		toprint += " " 
		lenline = sum([len(w) for w in linewords]) + len(linewords)
		for k in range(longest_line - lenline):
			toprint += sep
		toprint += " " 
		for scan in linescans:
			toprint += scan+" "
		toprint += "\n"

	fw = open(sys.argv[1]+".scansion","w")
	fw.write(toprint)
	fw.close()