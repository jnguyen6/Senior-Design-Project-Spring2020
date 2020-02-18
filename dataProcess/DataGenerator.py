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
        #Dictionary of notifications by day
        self.notByDay = {}
        self.activities = []

"""
Class for communication logs
"""
class notification:
    def __init__(self, noteTime, meth, notification=[0,1]):
        #Time of notification
        self.time = noteTime
        #Enum of methods of communication
        self.method = meth
        #List with values: 0-1 if pre or post due,
        #                  # of cycles this communication has had
        self.notType = notification
        
"""
Class for activity logs
"""
class activity:
    def __init__(self, actionDate):
        self.date = actionDate

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

"""
Generate Test data sets
"""
def dataGenAgeDemo():
    absolutePath = os.path.abspath(__file__)[:-16]
    relpath = absolutePath + r'\GeneratedDataSets\ageToDelivery.csv'

    patients = list(patientDict.values())
    patients.sort(key=operator.attrgetter('age'))


    basetime = np.datetime64('2019-01-01')

    youngMean = 700
    youngStDev = 200
    YoungSamples = np.random.normal(youngMean, youngStDev, 700)
    indices = set([int(i) for i in YoungSamples])
    with open(relpath, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for pat in indices:
            if pat < 3000 and pat >= 0:
                time = basetime + int(np.random.normal(90,8))
                newActTime = time + np.random.randint(1,10)
                idnum = patients[pat].id
                
                filewriter.writerow([idnum, time, 'Text', '7', newActTime])

    middleMean = 1400
    middleStDev = 200
    middleSamples = np.random.normal(middleMean, middleStDev, 700)
    indices = set([int(i) for i in middleSamples])
    with open(relpath, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for pat in indices:
            if pat < 3000 and pat >= 0:
                time = basetime + int(np.random.normal(90,8))
                newActTime = time + np.random.randint(1,10)
                idnum = patients[pat].id
                
                filewriter.writerow([idnum, time, 'Email', '7', newActTime])



    oldMean = 2400
    oldStDev = 200
    oldSamples = np.random.normal(oldMean, oldStDev, 700)
    indices = set([int(i) for i in oldSamples])
    with open(relpath, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for pat in indices:
            if pat < 3000 and pat >= 0:
                time = basetime + int(np.random.normal(90,8))
                newActTime = time + np.random.randint(1,10)
                idnum = patients[pat].id
                
                filewriter.writerow([idnum, time, 'Paper', '7', newActTime])

"""
Main function of program
"""
if __name__ == "__main__":
    generateNormalizedPatients(3000)
    #patientChart()
    dataGenAgeDemo()
