import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from conftest import *
from app import db
from app import populateCohorts
from src.algorithms.logistic_regression import logisticRegression
import pytest
from datetime import date
import numpy as np
from src.models.Cohort import Cohort

def runAllTests():
    ageTest()
    genderTest()
    incomeTest()

"""
Tests the logistic regression algorithm based on biased age groups
"""
def ageTest():
    youngPat = patient_gen(number_of_patients=20, age_range=(20, 40))
    middlePat = patient_gen(number_of_patients=20, age_range=(41, 60), offset=20)
    oldPat = patient_gen(number_of_patients=20, age_range=(61, 80), offset=20)

    combined = {**youngPat, **middlePat}
    combined = {**combined, **oldPat}

    freqList = []
    # Frequency of communication methods is arranged as [# email, # mails, # text]
    for i in range(60):
        if i < 20:
            freqList.append([6, 0, 0])
        elif i < 40:
            freqList.append([0, 6, 0])
        else:
            freqList.append([0, 0, 6])

    # Combine the X1 and X2 variables into one list of independent variables.
    x_list = []
    curr_idx = 0
    x_list_len = len(freqList)
    while curr_idx < x_list_len:
        patient = combined[curr_idx]
        gender = 1 if patient.gender == 'M' else 0
        freq_email = freqList[curr_idx][0]
        freq_paper = freqList[curr_idx][1]
        freq_text = freqList[curr_idx][2]

        x_variables = [patient.age, patient.income, gender, patient.bill_amount, freq_email, freq_paper, freq_text]
        x_list.append(x_variables)
        curr_idx += 1

    # Create a list of all the successes, where email is most successful for young patients, mail
    # is most successful for middle-aged patients, etc.
    y_list = []
    for i in range(60):
        y_list.append(1)

    logisticRegression(x_list, y_list)

    correct = 0
    total = 0

    cohorts = Cohort.query.all()
    for cohort in cohorts:
        if cohort.ageMax <= 20:
            if cohort.cid == 200:
                correct += 1
        elif cohort.ageMax <= 40:
            if cohort.cid == 20:
                correct += 1
        else:
            if cohort.cid == 2:
                correct += 1
        total += 1

    accuracy = correct / total
    if accuracy < .7:
        print(f"Test Failed: {accuracy} accuracy")
    else:
        print(f"Test Passed: {accuracy} accuracy")


"""
Tests the logistic regression algorithm based on biased gender groups
"""
def genderTest():
    malePat = patient_gen(number_of_patients=20, preferred_sex='M')
    femalPat = patient_gen(number_of_patients=20, preferred_sex='F', offset=20)

    combined = {**malePat, **femalPat}

    # Frequency of communication methods is arranged as [# email, # mails, # text]
    freqList = []
    for i in range(40):
        if i < 20:
            freqList.append([6, 0, 0])
        else:
            freqList.append([0, 0, 6])

    # Combine the X1 and X2 variables into one list of independent variables.
    x_list = []
    curr_idx = 0
    x_list_len = len(freqList)
    while curr_idx < x_list_len:
        patient = combined[curr_idx]
        gender = 1 if patient.gender == 'M' else 0
        freq_email = freqList[curr_idx][0]
        freq_paper = freqList[curr_idx][1]
        freq_text = freqList[curr_idx][2]

        x_variables = [patient.age, patient.income, gender, patient.bill_amount, freq_email, freq_paper, freq_text]
        x_list.append(x_variables)
        curr_idx += 1

    # Create a list of all the successes, where email is most successful for male patients and
    # text is most successful for female patients
    y_list = []
    for i in range(40):
        y_list.append(1)

    logisticRegression(x_list, y_list)

    correct = 0
    total = 0

    cohorts = Cohort.query.all()
    for cohort in cohorts:
        if cohort.ageMax == 'M':
            if cohort.cid == 200:
                correct += 1
        else:
            if cohort.cid == 2:
                correct += 1
        total += 1

    accuracy = correct / total
    if accuracy < .7:
        print(f"Test Failed: {accuracy} accuracy")
    else:
        print(f"Test Passed: {accuracy} accuracy")


"""
Tests the logistic regression algorithm based on biased income groups
"""
def incomeTest():
    lowPat = patient_gen(number_of_patients=20, income_range=(10000, 40000))
    middlePat = patient_gen(number_of_patients=20, income_range=(60000, 100000), offset=20)
    upperPat = patient_gen(number_of_patients=20, income_range=(120000, 140000), offset=20)

    combined = {**lowPat, **middlePat}
    combined = {**combined, **upperPat}

    freqList = []
    # Frequency of communication methods is arranged as [# email, # mails, # text]

    for i in range(60):
        if i < 20:
            freqList.append([6, 0, 0])
        elif i < 40:
            freqList.append([0, 6, 0])
        else:
            freqList.append([0, 0, 6])

    # Combine the X1 and X2 variables into one list of independent variables.
    x_list = []
    curr_idx = 0
    x_list_len = len(freqList)
    while curr_idx < x_list_len:
        patient = combined[curr_idx]
        gender = 1 if patient.gender == 'M' else 0
        freq_email = freqList[curr_idx][0]
        freq_paper = freqList[curr_idx][1]
        freq_text = freqList[curr_idx][2]

        x_variables = [patient.age, patient.income, gender, patient.bill_amount, freq_email, freq_paper, freq_text]
        x_list.append(x_variables)
        curr_idx += 1

    # Create a list of all the successes, where email is most successful for young patients, mail
    # is most successful for middle-aged patients, etc.
    y_list = []
    for i in range(60):
        y_list.append(1)

    logisticRegression(x_list, y_list)

    correct = 0
    total = 0

    cohorts = Cohort.query.all()
    for cohort in cohorts:
        if cohort.incomeMax <= 40000:
            if cohort.cid == 200:
                correct += 1
        elif cohort.incomeMax <= 100000:
            if cohort.cid == 20:
                correct += 1
        else:
            if cohort.cid == 2:
                correct += 1
        total += 1

    accuracy = correct / total
    if accuracy < .7:
        print(f"Test Failed: {accuracy} accuracy")
    else:
        print(f"Test Passed: {accuracy} accuracy")