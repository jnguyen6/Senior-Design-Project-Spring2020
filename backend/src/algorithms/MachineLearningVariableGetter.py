# This class is to analyze datasets from DB, get all parameters needed to put into
# machine learning algorithm by analyzing those instances of patients, communications
# and web activities
# The goal is to generate three types of lists: x1, x2, y
# The element in the same index of those lists should represent data from one same patient

import math
import requests
from datetime import date
from datetime import datetime

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
    print(ageList[0])
    return ageList

# Generate a list containing family income of all patients, in order
def getAllPatientsFamilyIncome():
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/family_income", headers=header_content, verify=False)
    incomeList = r.json()
    print(incomeList[0])
    return incomeList

# Generate a list containing genders of all patients, in order
def getAllPatientsGenderInOrder():
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/gender", headers=header_content, verify=False)
    genderList = r.json()
    print(genderList[0])
    return genderList

# Generate a list containing bill amounts of all patients, in order
def getAllPatientsBillAmount():
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/bill_amount", headers=header_content, verify=False)
    billList = r.json()
    print(billList[0])
    return billList

# Generate a list containing frequency of sending certain communications to all patients, in order
# the parameter "communication_type" may be "PAPER", "TEXT" and "EMAIL"
def getAllPatientsFreq(communication_type):
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/account_id", headers=header_content, verify=False)
    idList = r.json()
    #print(len(idList))
    r1 = requests.get("http://127.0.0.1:5000/communications", headers=header_content, verify=False)
    communicationList = r1.json()
    #print(len(communicationList))
    #print(communicationList[0].get('uid'))
    #print(communicationList[0].get('account_id'))
    #print(communicationList[0].get('notification_type'))
    #print(communicationList[1].get('notification_type'))
    freqList = []
    for id in idList:
        numMail = 0
        earliestTime = datetime.now()
        latestTime = datetime(1970, 1, 1)
        for com in communicationList:
            com_account_id = com.get('account_id')
            com_method = com.get('method')
            com_time = com.get('notification_date_time')
            deliveryTime = datetime.strptime(com_time, '%Y-%m-%d %H:%M:%S')
            if (deliveryTime < earliestTime):
                earliestTime = deliveryTime
            if (deliveryTime > latestTime):
                latestTime = deliveryTime
            if (com_account_id == id and com_method == communication_type):
                numMail += 1
        if (earliestTime == latestTime):
            timeDiffInThreeMonths = 1
        else:
            timeDiff = latestTime - earliestTime
            timeDiffInSec = timeDiff.total_seconds()
            timeDiffInThreeMonths = timeDiffInSec / 3600 / 24 / 30 / 3;
        freqList.append(numMail/timeDiffInThreeMonths)
    """
    print(freqList[0])
    print(freqList[1])
    print(freqList[2])
    print(freqList[3])
    print(freqList[4])
    """
    return freqList

# Generate a list containing all successes or not for patients, in order
def getAllPatientsSuccess():
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/account_id", headers=header_content, verify=False)
    idList = r.json()
    r1 = requests.get("http://127.0.0.1:5000/web activities", headers=header_content, verify=False)
    webActList = r1.json()
    r2 = requests.get("http://127.0.0.1:5000/communications", headers=header_content, verify=False)
    comList = r2.json()
    successScoreList = []

    for id in idList:
        paid = 0
        firstTimeGet = 0
        firstComTime = datetime(1970, 1, 1)
        timePaid = datetime(1970, 1, 1)
        successScore = 0
        for com in comList:
            if com.get('account_id') == id and firstTimeGet == 0:
                firstComTime = datetime.strptime(com.get('notification_date_time'), '%Y-%m-%d %H:%M:%S')
                firstTimeGet = 1
        for webAct in webActList:
            if webAct.get('account_id') == id and webAct.get('billStatus') == "PAID":
                paid = 1
                actionDate = webAct.get('actionDate')
                timePaid = datetime.strptime(actionDate, '%Y-%m-%d %H:%M:%S')
        if (paid == 1):
            timeDiff = timePaid - firstComTime
            timeDiffInSec = timeDiff.total_seconds()
            timeDiffInWeek = timeDiffInSec / 3600 / 24 / 7;
            successScore = 1 / timeDiffInWeek
        if (paid == 0):
            successScore = 0
        successScoreList.append(successScore)
        print(successScore)
    return successScoreList


# Main Method only for Testing
if __name__ == "__main__":
    getAllPatientsAgeInOrder()
    getAllPatientsFamilyIncome()
    getAllPatientsGenderInOrder()
    getAllPatientsBillAmount()
    #getAllPatientsFreq("PAPER")
    print("-------")
    #getAllPatientsFreq("TEXT")
    print("-------")
    #getAllPatientsFreq("EMAIL")
    print("-------")
    getAllPatientsSuccess()