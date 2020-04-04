# This class is to analyze datasets from DB, get all parameters needed to put into
# machine learning algorithm by analyzing those instances of patients, communications
# and web activities
# The goal is to generate three types of lists: x1, x2, y
# The element in the same index of those lists should represent data from one same patient

import math
import requests
from datetime import date

# Generate a list containing ages of all patients, in order of account ID
def getAllPatientsAgeInOrder():
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/birth_year", headers=header_content, verify=False)
    birthYearList = r.json()
    currentYear = date.today().year
    # print(birthYearList[1])
    # print(currentYear)
    ageList = []
    for birthYear in birthYearList:
        ageList.append(currentYear - birthYear)
    # print(ageList[1])
    return ageList

# Generate a list containing genders of all patients, in order
def getAllPatientsGenderInOrder():
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/gender", headers=header_content, verify=False)
    genderList = r.json()
    print(genderList[0])
    #return genderList

# Main Method only for Testing
if __name__ == "__main__":
    getAllPatientsAgeInOrder()
    getAllPatientsGenderInOrder()