import os   
import string
import csv


rempunc = string.punctuation.replace("@", "") #keep "@" and "#" in the results
removepunctuation = rempunc.replace("#", "")

#removespam = ("excellent", "nearly-new", "ebay") #option to remove spam tweets

count = {}
for filename in os.listdir("."):  #loop through each file in current directory
    if filename.startswith("tweets-"): #only interact with particular files
        textInput = open(filename, "r")
        for line in textInput:
            if line[:2] == "en":  #Only count English texts
                line = line.decode('unicode_escape').encode('ascii','ignore')
                line = line[2:].split()   #remove the lang code and split line
                for word in line:
                    word = word.strip(removepunctuation)
                    word = word.lower()
                    if word == "":
                        pass
                #    elif any(word in s for s in removespam):
                #        pass
                    elif word in count:
                        count[word] += 1  #add 1 to the current count for that word
                    else:
                        count[word] = 1   #add the word to the dictionary with a count of 1


notenough = 0 #count how many words I'm eliminating
with open("output.csv", "wb") as csvfile:
    g = csv.writer(csvfile, delimiter=',')
    for word, times in count.items():
        if times < 5:
            notenough += 1
        else:
            g.writerow([word, times])
    csvfile.close()
print notenough
