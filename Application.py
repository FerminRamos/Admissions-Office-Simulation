import json
import csv
import random
from datetime import datetime, timedelta


def load_config(filepath="config.json"):
    with open(filepath) as jsonFile:
        config = json.load(jsonFile)
    return config


def loadStatesList():
    states = []
    with open("Databases/US_States.csv") as csvFile:
        reader = csv.reader(csvFile)
        csvFile.readline()  # Skip Header
        for line in reader:
            states.append(line)
    return states


def loadMajors():
    majors = []
    with open("Databases/Majors.csv") as csvFile:
        reader = csv.reader(csvFile)
        csvFile.readline()  # Skip Header
        for line in reader:
            majors.append(line[1])
    return majors


def loadCountries():
    countries = []
    with open("Databases/Foreign_Countries.csv") as csvFile:
        reader = csv.reader(csvFile)
        csvFile.readline()  # Skip Header
        for line in reader:
            countries.append(line)
    return countries


# Reads CSV file containing baby names, gender, ethnicity. Generates last
#  name initial for randomness. File is contains 77,000 unique names.
def generatePersons(n):
    names = []
    with open("Databases/Popular_Baby_Names.csv") as csvFile:
        reader = csv.reader(csvFile)
        csvFile.readline()  # Skip headers
        for row in reader:
            names.append([row[1], row[2], row[3], randomInitial()])
    return random.sample(names, n)


# Random initial used for last names
def randomInitial():
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F',
                'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R',
                'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']
    randIndex = random.randint(0, 25)
    return alphabet[randIndex]


# Applications go through this distribution:
#     (percentages vary based on config.json)
#                    APPLIED
#                     100%
#                /            \
#           ADMITTED         REJECTED      PHASE-1
#             64%               36%         100%
#      /       |        \
# ENROLLED  UNDER-REVIEW  LOST             PHASE-2
#  65%          5%        30%               100%
#                          |
#                      WITHDRAWN
#                         14%
def getAppDist():
    # Get Admitted & Rejected
    dist = {
        'admitted': APP_DIST['admitted'],
        'rejected': APP_DIST['rejected']
    }
    phase1 = genMockData(dist, NUM_OF_APP)

    # From Admitted -> get how many enrolled, under-review, lost
    dist = {
        'enrolled': APP_DIST['enrolled'],
        'under-review': APP_DIST['under_review'],
        'lost': APP_DIST['lost']
    }
    phase2 = genMockData(dist, phase1.count('admitted'))
    k = 0
    for i in range(len(phase1)):
        if phase1[i] == 'admitted':  # replace all admitted tags
            phase1[i] = phase2[k]
            k += 1

    # Adds withdrawn % to lost
    dist = {
        'withdrawn':  APP_DIST['withdrawn'],
        'lost': 1-APP_DIST['withdrawn']
    }
    phase3 = genMockData(dist, phase1.count('lost'))
    k = 0
    for i in range(len(phase1)):
        if phase1[i] == 'lost':
            phase1[i] = phase3[k]
    
    return phase1


# Assigns an "in-state" status & state to each person in our dataset,
#  based on nationality.
def assignUSALocationData(dataset):
    data = []
    nationalityIndex = 6
    for row in dataset:
        nationality = row[nationalityIndex]
        data.append(getUSALocationData(nationality))
    return data


# Decides the state_distribution of a person
def getUSALocationData(nationality):
    # Case1: Foreigner -> No state
    if nationality != "usa":
        return ["N/A", "N/A"]

    homeStateStatus = genMockData(STATE_DIST, 1)[0]  # Returns 1 item

    # Case2: In-state
    if homeStateStatus == "in-state":
        return [homeStateStatus, UNI_LOCATION]

    # Case3: Out-of-State
    try:
        STATES.remove(UNI_LOCATION)  # Remove uni_location from options
    except ValueError:
        pass
    randInt = random.randint(0, len(STATES) - 1)
    return [homeStateStatus, STATES[randInt][0]]


# Returns n-number of majors
def getRandMajors():
    majors = []
    for i in range(NUM_OF_APP):
        randInt = random.randint(0, len(MAJORS) - 1)
        majors.append(MAJORS[randInt])
    return majors


# Converts a string to datetime obj
def convertToDatetime(datestr):
    return datetime.strptime(datestr, "%Y-%m-%d").date()


# Assigns n-number of random start dates and days open counters
def getAppDates():
    dates = []
    for i in range(NUM_OF_APP):
        app_started = random_date()
        daysOpen = getDaysAppOpen((APP_END - app_started).days)
        dates.append([str(app_started), daysOpen])
    return dates


def random_date():
    delta = APP_END - APP_START
    random_days = random.randrange(delta.days + 1)
    return APP_START + timedelta(days=random_days)


# Calculates how many days a user spent on the application either by
#  assigning the max number of days (config.json) or subtracting the
#  amount of days left til the application closes. Whichever is less.
def getDaysAppOpen(daysTilClose):
    if daysTilClose <= DAYS_TO_APPLY_DIST['min']:
        return daysTilClose
    randInt = random.randint(DAYS_TO_APPLY_DIST['min'],
                             min(DAYS_TO_APPLY_DIST['max'], daysTilClose))
    return randInt


def getNationalityDist():
    dist = {
        'usa': NATIONALITY_DIST['usa'],
        'foreign': NATIONALITY_DIST['foreign']
    }

    data = genMockData(add_variation(dist), NUM_OF_APP)

    # replace 'foreign' status with an actual country
    nationalities = []
    numOfCountries = len(COUNTRIES)
    for nationality in data:
        if nationality == 'foreign':
            randInt = random.randint(0, numOfCountries-1)
            nationalities.append(COUNTRIES[randInt][0].lower())
        else:
            nationalities.append(nationality)
    return nationalities


# Add random ±10% variation to each probability
def add_variation(distribution, variation=0.10):
    new_dist = {}

    # Add variation
    for k, v in distribution.items():
        varInt = int(variation*100)
        var = random.randint(-1*varInt, varInt)/100
        v = v if v + var <= 0 else round(v + var, 2)
        new_dist[k] = v

    # Normalize back to 1 & return
    return normalize(new_dist)


def normalize(dist):
    # Attempt to normalize back to 1
    total = sum(dist.values())
    for k, v in dist.items():
        dist[k] = round(v / total, 2)

    # Adds 0.00999 to a random prob IF we had rounding errors (not exactly 1)
    total = sum(dist.values())
    if total != 1:
        randIndex = random.randint(0, len(dist.values()) - 1)
        key = list(dist.keys())[randIndex]
        dist[key] += 1 - total
    return dist


# Generates n-number of mock datapoints given a distribution probability
def genMockData(dist, n):
    state = list(dist.keys())
    prob = list(dist.values())

    outcomes = random.choices(state, weights=prob, k=n) # Avoid np bc of wrapper
    return outcomes


# Given arrays "a" & "b", append all items of b onto the end of each row of a
def mergeArrays(a, b):
    isList = True if isinstance(a[0], list) else False
    c = []
    for i in range(len(a)):
        c.append(a[i] + [b[i]]) if isList else c.append([a[i], b[i]])
    return c


# Shift headers around & lower "male" category
    # Original: [Gender, Ethnicity, FirstName, LastInitial, AdmissionStatus,
    #            AgeGroup, Nationality, InStateStatus, State, Program,
    #            UnderScholarship, FirstGen, Major, ApplicationStart,
    #            DaysAppOpen]
    # New Format: [ApplicationStart, DaysAppOpen, FirstName, LastInitial,
    #              AdmissionStatus, AgeGroup, Gender, Ethnicity, Nationality,
    #              InStateStatus, State, Program, Major, UnderScholarship,
    #              FirstGen]
def reformatHeaders(dataset):
    reformatted = [['ApplicationStart', 'DaysAppOpen', 'FirstName',
                   'LastInitial', 'AdmissionStatus', 'AgeGroup', 'Gender',
                   'Ethnicity', 'Nationality', 'InStateStatus', 'State',
                   'Program', 'Major', 'UnderScholarship', 'FirstGen']]
    for row in dataset:
        reformatted.append([row[13], row[14], row[2], row[3], row[4],
                            row[5], row[0].lower(), row[1], row[6], row[7],
                            row[8], row[9], row[12], row[10], row[11]])

    return reformatted


def writeCSV(simulation_name, dataset):
    with open(f"Admission Cycles/{simulation_name}.csv", "w") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(dataset)
    print(f"Wrote to '{simulation_name}.csv'")


def printHead(data, rows=10):
    i = 0
    for row in data:
        print(f"{i}. {row}")
        i += 1
        if i > rows:
            break


# GLOBALS
CONFIG_FILE = load_config()
SIMULATION_NAME = CONFIG_FILE['simulation_name']
APP_START = convertToDatetime(CONFIG_FILE['application_start'])
APP_END = convertToDatetime(CONFIG_FILE['application_end'])
UNI_LOCATION = CONFIG_FILE['uni_location']
APP_DIST = add_variation(CONFIG_FILE['application_distribution'])
AGE_DIST = add_variation(CONFIG_FILE['age_distribution'])
NATIONALITY_DIST = add_variation(CONFIG_FILE['nationality_distribution'])
STATE_DIST = add_variation(CONFIG_FILE['state_distribution'])
PROGRAM_DIST = add_variation(CONFIG_FILE['program_distribution'])
UNDER_SCLSHP_DIST = add_variation(CONFIG_FILE['under_scholarship_distribution'])
FIRST_GEN_DIST = add_variation(CONFIG_FILE['first_gen_distribution'])
DAYS_TO_APPLY_DIST = CONFIG_FILE['days_to_apply_distribution']
NUM_OF_APP = CONFIG_FILE['num_applications']
STATES = loadStatesList()
MAJORS = loadMajors()
COUNTRIES = loadCountries()


if __name__ == "__main__":
    applicants = generatePersons(NUM_OF_APP)

    applicants = mergeArrays(applicants, getAppDist())
    applicants = mergeArrays(applicants, genMockData(AGE_DIST, NUM_OF_APP))
    applicants = mergeArrays(applicants, getNationalityDist())

    # Appends "in-state" status & state to application data
    locations = assignUSALocationData(applicants)
    transposedLocations = list(map(list, zip(*locations)))
    applicants = mergeArrays(applicants, transposedLocations[0])
    applicants = mergeArrays(applicants, transposedLocations[1])

    applicants = mergeArrays(applicants, genMockData(PROGRAM_DIST, NUM_OF_APP))
    applicants = mergeArrays(applicants, genMockData(UNDER_SCLSHP_DIST, NUM_OF_APP))
    applicants = mergeArrays(applicants, genMockData(FIRST_GEN_DIST, NUM_OF_APP))
    applicants = mergeArrays(applicants, getRandMajors())

    # Appends "date app started" and "days open" to applications
    dates = getAppDates()
    transposedDates = list(map(list, zip(*dates)))
    applicants = mergeArrays(applicants, transposedDates[0])
    applicants = mergeArrays(applicants, transposedDates[1])

    # Reformat headers & write to csv
    writeCSV(SIMULATION_NAME, reformatHeaders(applicants))
