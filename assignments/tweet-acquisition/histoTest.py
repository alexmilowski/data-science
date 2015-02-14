import numpy as np
import pylab as pl

dic = {}

with open ("histoTest.txt") as sourceFile:
	for line in sourceFile:
		print(line)
		(key,val) = line.split(" ")
		dic[int(key)] = val

X=np.arange(len(dic))
pl.bar(X,dic.keys(),width=0.2)
pl.xticks(X,dic.values())

ymax= max(dic.keys())+1
pl.ylim(0,ymax)

pl.show()

