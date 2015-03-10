#!/usr/bin/python
import sys 
import re 

def main(argv): 
    pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*") 
    for line in sys.stdin: 
        line = line.replace("..."," ")
        line.replace("("," ")
        line.replace(")"," ")
        for word in line.split(): 
            if len(word)<3 or word[0:5] == "http:" or word[0:6] == "https:" or word == "-":
               continue
            if word[0] == "." or word[0] == "\"" or word[0] == "(":
               word = word[1:]
            if word[-1] == "." or word[-1] == "," or word[-1] == "!" or word[-1] == ":" or word[-1] == "\"" or word[-1] == ")":
               word = word[0:-1]
            if len(word)<3:
               continue
            print "LongValueSum:" + word.lower() + "\t" + "1" 


if __name__ == "__main__": 
    main(sys.argv) 
