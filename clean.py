
import sys

def reformat(inp):
	return inp.split("-")[1].replace("S","+").replace("U","-")

f=open(sys.argv[1])
lines = [[word.split("__") for word in line.strip().split(" ")] for line in f]
f.close()


words = [[word for word,scansion in line] for line in lines]
analyses = [[reformat(scansion) for word,scansion in line] for line in lines]

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