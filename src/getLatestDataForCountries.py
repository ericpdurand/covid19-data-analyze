import csv
import logging

# we get the vaccinations from https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv
# this file contains lines per country and per date. Some days the total vaccinations fields are not valued, so we need to read back to get that value
vaccinationsFile = "../data/vaccinations.csv"
# we get the total cases from https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/total_cases.csv
# this file contains 1 line per date with country data in columns
totalCasesFile = "../data/total_cases.csv"
# we get the new cases from https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv
# this file contains 1 line per date with country data in columns
newCasesFile = "../data/new_cases.csv"
countriesFile = "../data/countries.txt"
resultFile = "../docs/CasesAndVaccinationsPerCountry.txt"

# Result is meant to store the data we want to capture, for each country
class Result:
    def __init__(self):
        self.totalcases = 0
        self.newcases = 0
        self.totalvaccinations = 0
        self.newvaccinations = 0
    
    def __str__(self):
        return "totalcases:% s, newcases:% s, totalvaccinations:% s, newvaccinations:% s" \
            % (self.totalcases, self.newcases, self.totalvaccinations, self.newvaccinations)

# readCountries reads the countries into a list from the countries file. We expect countries here as valid locations.
def readCountries():
    with open(countriesFile) as f:
        countries = f.read().splitlines()
    return countries

# getLastTotalCases gets the last Total Cases for each country and fills them in the results dict
def getLastTotalCases(countries, results):
    with open(totalCasesFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = row
    for country in countries:
        results[country].totalcases = data[country]

# getLastnewCases gets the last New Cases for each country and fills them in the results dict
def getLastNewCases(countries, results):
    with open(newCasesFile,  newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = row
    for country in countries:
        if data[country] == '':
            results[country].newcases = 0 # we put 0 if there was no data reported for the last date
        else:
            results[country].newcases = data[country]

# getVaccinations get the total vaccinations and last vaccinations and puts them in the results dict
def getVaccinations(countries, results):
    # data is going to store the vaccination data, only for the countries of the list
    data = dict()
    for country in countries:
        data[country] = []
    # Read data into a Dict per country
    with open(vaccinationsFile, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            location = row['location']
            if location in countries:
                data[location].append(row)
    # Now for each country find the data
    for country in countries:
        index = len(data[country]) -1
        # First the new vaccinations
        results[country].newvaccinations = data[country][index]['daily_vaccinations'] # we take daily_vaccinations and not daily_vaccinations_raw as per the github doc
        # Then the total vaccinations
        while data[country][index]['total_vaccinations'] == '':
            if data[country][index]['daily_vaccinations']!= '':
                results[country].totalvaccinations += int(data[country][index]['daily_vaccinations'])
            index -= 1
            print(data[country][index]['total_vaccinations'])
        results[country].totalvaccinations += int(data[country][index]['total_vaccinations'])
        
# writeResults dumps the results to the results file
def writeResults(results, file):
     with open(resultFile,"w") as file:
        for country in results:
            line = [country,": ",results[country].__str__(),"\n"]
            file.writelines(line)
            logging.info("%s: %s",country, results[country].__str__())

# configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

countries = readCountries()
logging.info("Countries read: %s", countries)

# results is a dict of results, for each country
results = dict()
for country in countries:
    results[country] = Result()

# get all the data
getLastTotalCases(countries,results)
getLastNewCases(countries,results)
getVaccinations(countries,results)

# write results to result file
writeResults(results, resultFile)
logging.info("Results written to %s",resultFile)