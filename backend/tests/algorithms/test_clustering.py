import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from conftest import *
from app import db
from app import populateCohorts
from src.algorithms.clustering import clusteringAlgorithm
import pytest
from datetime import date
import numpy as np
from src.models.Cohort import Cohort



def runAllTests(clustertype):
    ageTest(clustertype)
    genderTest(clustertype)
    incomeTest(clustertype)

"""
Tests the cluster algorithm based on biased age groups
"""
def ageTest(clustertype):
    youngPat = patient_gen(number_of_patients=20, age_range=(20,40))
    middlePat = patient_gen(number_of_patients=20, age_range=(41,60), offset=20)
    oldPat = patient_gen(number_of_patients=20, age_range=(61,80), offset=20)

    combined = {**youngPat, **middlePat}
    combined = {**combined, **oldPat}
    
    patientList = []
    freqList = []
    
    for pat in combined:
        patient = combined[pat]
        gender = 1 if patient.gender == 'M' else 0
        patientList.append([gender, date.today().year - patient.birth_year, patient.family_income, patient.bill_amount])

    for i in range(60):
        a = random.randint(0, 5)
        if i < 20:
            freqList.append([6,0,0])
        elif i < 40:
            freqList.append([0,6,0])
        else:
            freqList.append([0,0,6])
    arraylist = np.array(patientList)
    clusteringAlgorithm(clustertype, test=True, testData=[arraylist, freqList])
    
    correct = 0
    semiCorrect = 0
    total = 0

    cohorts = Cohort.query.all()
    for cohort in cohorts:
        if cohort.ageMax <= 20:
            if cohort.cid == 200:
                correct += 1
            elif (cohort.cid // 100) == 2:
                semiCorrect += 1
        elif cohort.ageMax <= 40:
            if cohort.cid == 20:
                correct += 1
            else:
                c = cohort.cid % 100
                c = c - (c % 10)
                if c == 20:
                    semiCorrect += 1 
        else:
            if cohort.cid == 2:
                correct += 1
            elif cohort.cid % 10 == 2:
                semiCorrect += 1

        total += 1
    
    accuracy = correct/total
    partialAccuracy = (correct + semiCorrect) / total
    if accuracy < .7:
        print(f"Test Failed: {accuracy} accuracy | {partialAccuracy} Partial Accuracy")
    else:
        print(f"Test Passed: {accuracy} accuracy | {partialAccuracy} Partial Accuracy")



"""
Tests the cluster algorithm based on biased gender groups
"""
def genderTest(clustertype):
    malePat = patient_gen(number_of_patients=20, preferred_sex='M')
    femalPat = patient_gen(number_of_patients=20, preferred_sex='F', offset=20)

    combined = {**malePat, **femalPat}
    
    patientList = []
    freqList = []
    
    for pat in combined:
        patient = combined[pat]
        gender = 1 if patient.gender == 'M' else 0
        patientList.append([gender, date.today().year - patient.birth_year, patient.family_income, patient.bill_amount])

    for i in range(40):
        if i < 20:
            freqList.append([6,0,0])
        else:
            freqList.append([0,0,6])
    arraylist = np.array(patientList)
    clusteringAlgorithm(clustertype, test=True, testData=[arraylist, freqList])

    correct = 0
    semiCorrect = 0
    total = 0
    

    cohorts = Cohort.query.all()
    for cohort in cohorts:
        if cohort.ageMax == 'M':
            if cohort.cid == 200:
                correct += 1
            elif (cohort.cid // 100) == 2:
                semiCorrect += 1
        else:
            if cohort.cid == 2:
                correct += 1
            elif (cohort.cid % 10) == 2:
                semiCorrect += 1

        total += 1
    
    accuracy = correct/total
    partialAccuracy = (correct + semiCorrect) / total
    if accuracy < .7:
        print(f"Test Failed: {accuracy} accuracy | {partialAccuracy} Partial Accuracy")
    else:
        print(f"Test Passed: {accuracy} accuracy | {partialAccuracy} Partial Accuracy")


"""
Tests the cluster algorithm based on biased income groups
"""
def incomeTest(clustertype):
    lowPat = patient_gen(number_of_patients=20, income_range=(10000,40000))
    middlePat = patient_gen(number_of_patients=20, income_range=(60000,100000), offset=20)
    upperPat = patient_gen(number_of_patients=20, income_range=(120000,140000), offset=20)

    combined = {**lowPat, **middlePat}
    combined = {**combined, **upperPat}
    
    patientList = []
    freqList = []
    
    for pat in combined:
        patient = combined[pat]
        gender = 1 if patient.gender == 'M' else 0
        patientList.append([gender, date.today().year - patient.birth_year, patient.family_income, patient.bill_amount])

    for i in range(60):
        if i < 20:
            freqList.append([6,0,0])
        elif i < 40:
            freqList.append([0,6,0])
        else:
            freqList.append([0,0,6])
    arraylist = np.array(patientList)
    clusteringAlgorithm(clustertype, test=True, testData=[arraylist, freqList])


    correct = 0
    semiCorrect = 0
    total = 0

    cohorts = Cohort.query.all()
    for cohort in cohorts:
        if cohort.incomeMax <= 40000:
            if cohort.cid == 200:
                correct += 1
            elif (cohort.cid // 100) == 2 :
                semiCorrect += 1
        elif cohort.incomeMax <= 100000:
            if cohort.cid == 20:
                correct += 1
            else:
                c = cohort.cid % 100
                c = c - (c % 10)
                if c == 20:
                    semiCorrect += 1
        else:
            if cohort.cid == 2:
                correct += 1
            if (cohort.cid % 10) == 2:
                semiCorrect += 1
        total += 1
    
    accuracy = correct/total
    partialAccuracy = (correct + semiCorrect) / total
    if accuracy < .7:
        print(f"Test Failed: {accuracy} accuracy | {partialAccuracy} Partial Accuracy")
    else:
        print(f"Test Passed: {accuracy} accuracy | {partialAccuracy} Partial Accuracy")

runAllTests('spectral')