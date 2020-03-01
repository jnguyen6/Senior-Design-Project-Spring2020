"""
File for generating biased data sets
@Author Mark Snedecor
"""

import random
from enum import Enum
import matplotlib.pyplot as plt
import operator
import numpy as np
import csv
import os
from random import random

#Dictionary of patients
patientDict = {}

"""
Class that represents a patient and holds all relevant data
"""
class Patient:
    def __init__(self, s, i, inc, bill, a):
        self.sex = s
        self.id = i
        self.income = inc
        self.billAmount = bill
        self.age = a
        self.opt = OptOut.NEITHER


        self.notifications = []
        self.activities = []

"""
Class for communication logs
"""
class notification:
    def __init__(self, noteTime, meth):
        #Time of notification
        self.time = noteTime
        #Enum of methods of communication
        self.method = meth
        
"""
Class for activity logs
"""
class activity:
    def __init__(self, idn, actionDate):
        self.idNum = idn
        self.date = actionDate
        self.status = 'DUE'
        self.actId = '7'

"""
Enums for the different opt out options
"""
class OptOut(Enum):
    BOTH = 1
    EMAIL = 2
    TEXT = 3
    NEITHER = 4

"""
Enums for delivery methods
"""
class DeliveryMethod(Enum):
    PAPER = 1
    EMAIL = 2
    TEXT = 3

"""
Visualize patient distribution
"""
def patientChart():
    ages = []
    incomes = []
    bill = []
    sex = [0,0]

    for key in patientDict:
        ages.append(patientDict[key].age)
        incomes.append(patientDict[key].income)
        bill.append(patientDict[key].billAmount)
        if patientDict[key].sex == 'F':
            sex[0] += 1
        else:
            sex[1] += 1
    print(sex)
    plt.hist(ages)
    plt.show()
    plt.hist(incomes)
    plt.show()
    plt.hist(bill)
    plt.show()
    labels = 'Female', 'Male'
    plt.pie([sex[0], sex[1]], labels=labels)
    plt.show()


"""
Generates a dictionary of patients that have random values
equally distributed across demographics
@param n the number of patients to generate
"""
def generateNormalizedPatients(n):
    global patientDict
    for patid in range(n):
        idnumber = patid
        age = random.randrange(18, 100, 1)
        if patid < (n/2):
            sex = 'F'
        else:
            sex = 'M'

        income = random.randrange(10000, 200000, 1000)
        bill = random.randrange(200, 5000, 10)
        newPat = Patient(sex, idnumber, income, bill, age)
        patientDict[patid] = newPat

        absolutePath = os.path.abspath(__file__)[:-16]
        relpath = absolutePath + r'\GeneratedDataSets\generatedPatients.csv'
    
    with open(relpath, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for idnum in patientDict:
                pat = patientDict[idnum]
                filewriter.writerow([pat.id, pat.sex, 2020-(pat.age), '*', pat.income, pat.billAmount])


"""
Generate Test data sets
"""
def dataGenAgeDemo():
    absolutePath = os.path.abspath(__file__)[:-16]
    relpathComm = absolutePath + r'\GeneratedDataSets\ageCommCommunications.csv'
    relpathAct = absolutePath + r'\GeneratedDataSets\ageCommActivity.csv'


    patients = list(patientDict.values())
    patients.sort(key=operator.attrgetter('age'))

    activities = []

    basetime = np.datetime64('2019-01-01')

    youngMean = 700
    youngStDev = 200
    YoungSamples = np.random.normal(youngMean, youngStDev, 700)
    youngIndices = set([int(i) for i in YoungSamples])

    middleMean = 1400
    middleStDev = 200
    middleSamples = np.random.normal(middleMean, middleStDev, 700)
    middleIndices = set([int(i) for i in middleSamples])

    oldMean = 2400
    oldStDev = 200
    oldSamples = np.random.normal(oldMean, oldStDev, 700)
    oldIndices = set([int(i) for i in oldSamples])

    with open(relpathComm, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for pat in youngIndices:
            if pat < 3000 and pat >= 0:
                time = basetime + int(np.random.normal(90,8))
                newActTime = time + np.random.randint(1,10)
                idnum = patients[pat].id

                activities.append(activity(idnum, newActTime))
                
                filewriter.writerow([idnum, time, 'Text', '*'])
        
        for pat in middleIndices:
            if pat < 3000 and pat >= 0:
                time = basetime + int(np.random.normal(90,8))
                newActTime = time + np.random.randint(1,10)
                idnum = patients[pat].id

                activities.append(activity(idnum, newActTime))
                
                filewriter.writerow([idnum, time, 'Email', '*'])

        for pat in oldIndices:
            if pat < 3000 and pat >= 0:
                time = basetime + int(np.random.normal(90,8))
                newActTime = time + np.random.randint(1,10)
                idnum = patients[pat].id

                activities.append(activity(idnum, newActTime))
                
                filewriter.writerow([idnum, time, 'Paper', '*'])

    with open(relpathAct, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for act in activities:
            filewriter.writerow([act.idNum, act.actId, act.status, act.date])

"""
Generate notifications for patients
@param patients: list of patient ids
@params paper, text, email: integer for cycle length in weeks (0 is opt out)
"""
def patientNotificationGenerator(patients, starttime, paper=2, text=2, email=2, numWeeks=17):
    for num in range(1, numWeeks):
        deliveryType = DeliveryMethod.PAPER
        newTime = starttime + (num*7)
        for patient in patients:
            if(num % paper == 0):
                patientDict[patient].notifications.append(notification(newTime, deliveryType))
            if(num % text == 0):
                deliveryType = DeliveryMethod.TEXT
                patientDict[patient].notifications.append(notification(newTime, deliveryType))
            if(num % email == 0):
                deliveryType = DeliveryMethod.EMAIL
                patientDict[patient].notifications.append(notification(newTime, deliveryType))

"""
Generates success cases for given list of patients
@param samplingPercent: percentage of given patient range that actually succeed
"""
def patientActivityGenerator(patients, starttime, samplingPercent = 1):
    for patient in patients:
        chance = random()
        if chance < samplingPercent:
            newtime = starttime + (np.random.randint(1,17) * 7)
            patientDict[patient].activities.append(activity(patient, newtime))

"""
Main function of program
"""
if __name__ == "__main__":
    generateNormalizedPatients(3000)
    #patientChart()
    dataGenAgeDemo()

