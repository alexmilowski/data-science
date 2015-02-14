import numpy as np
import matplotlib.pyplot as plt

dic = {}

#Load the text file as a key, value dictionary
with open("word_count.out") as sourceFile:
    for line in sourceFile:
       (val, key) = line.split('\t')
       dic[int(key)] = val
        
#Setting the number of bins, Axes values        
X = np.arange(len(dic))
plt.bar(X, dic.keys(), width=0.2)
plt.xticks(X, dic.values(), rotation=90)
plt.xlabel("Terms", fontsize=18)
plt.ylabel("Frequency", fontsize=16, rotation=90)
plt.suptitle("Histogram (all terms)")

#Setting the axis range
ymax = max(dic.keys()) + 1
plt.ylim(0, ymax)

#plotting the histogram
plt.savefig("histogram_all_terms.png")