import csv
import logging
import sys

# We use here the new_cases.csv file from https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv
# This file contains one line per day, each column after the date being a country's new cases for that date. 
# This file is orderd by date, last date last.
newCasesFile = "../data/new_cases.csv"
resultFile = "../report/CountriesMissingData.txt"
nbCountries = 10

# readData reads a new cases file into a list of dicts, one per line
def readData(data, filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

# getCountriesWithMissingData returns a list of countries with no data at the provided index
def getCountriesWithMissingData(data, index):
    countries = []
    currentDay = data[index]
    for country in currentDay:
        if currentDay[country] == '':
            countries.append(country)
    return countries

# writeResult writes the result to a provided file name
def writeResult(filename,data):
    with open(filename,"w") as file:
        for key in reversed(data): # reverse the order to have the oldest first
            line = [key,": ",data[key],"\n"]
            file.writelines(line)

# configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# this will store a list of dicts from the input file, one per date
data = []
# this will store the results, with the country name and last date
result = dict()

readData(data,newCasesFile)
# we exit early if we did not read any data
if len(data) == 0:
    logging.error("No data read from %s",newCasesFile)
    sys.exit(1)

logging.info("Read %s lines from %s",len(data),newCasesFile)

index = len(data) -1

# get countries with missing data for the last date
countriesWithNoData = getCountriesWithMissingData(data,index)

while len(result) < nbCountries:
    index = index - 1
    countriesWithNoDataPreviousDay = getCountriesWithMissingData(data,index)
    for country in countriesWithNoData: 
        if country not in countriesWithNoDataPreviousDay: # we found the last date that country had data
            result[country] = data[index]['date']
            logging.info("Last date with data for %s: %s", country, result[country])
            if len(result) == nbCountries:  # we found all countries, exit the loop
                break
    countriesWithNoData = countriesWithNoDataPreviousDay
    if index == 0: # we are at the beginning of the file
        break

logging.info("Writing results to %s",resultFile)
writeResult(resultFile, result)