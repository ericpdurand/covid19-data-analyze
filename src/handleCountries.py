import sys

outputFile = "../data/countries.txt"
countries = sys.argv[1]

countriesList = countries.split(',')
countriesList = [s.strip() for s in countriesList]
print("New Countries: ",countriesList)

with open(outputFile,"w") as file: 
    for c in countriesList:
        line = [c,"\n"]
        file.writelines(line)