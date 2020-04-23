import requests
from numpy import unique
from numpy import where
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from datetime import date
from MachineLearningVariableGetter import getAllPatientsFreq
import statistics
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from app import db
from src.models.Cohort import Cohort
from math import floor

"""
Dictionary of different clustering algorithms
"""
algorithms = {'minibatchKmean':MiniBatchKMeans, 'agglomeration':AgglomerativeClustering, 'spectral':SpectralClustering}

"""
Main function, called by dispatcher and runs clustering algorithm
populates cohort database
"""
def clusteringAlgorithm(clusterAlgorithm):
    cluster_size = 6
    clusterCycles = []
    X, frequencies  = createDataSet()

    model = algorithms[clusterAlgorithm](n_clusters=cluster_size)
    model.fit(X)
    yhat = model.predict(X)
    clusters = unique(yhat)

    #Find indices for patients per cluster
    clusterIndices = []
    for cluster in clusters:
        indices = where(yhat == cluster)
        clusterIndices.append(indices)

    #Find shared cycle lengths
    for i in range(len(clusterIndices)):
        cluster = clusterIndices[i]
        paperTotal = []
        textTotal = []
        emailTotal = []
        for i in np.nditer(cluster[0]):
            paperTotal.append(frequencies[i][0] / 3)
            textTotal.append(frequencies[i][1] / 3)
            emailTotal.append(frequencies[i][2] / 3)
        paperMedian = statistics.median(paperTotal)
        textMedian = statistics.median(textTotal)
        emailMedian = statistics.median(emailTotal)
        
        clusterCycles.append([floor(paperMedian), floor(textMedian), floor(emailMedian)])


    cohorts = Cohort.query.all()
    for cohort in cohorts:
        gender = 0
        if cohort.gender == "M":
            gender = 1
        else:
            gender = 2
        age = cohort.ageMin
        income = cohort.incomeMin
        bill_amount = cohort.billAmountMin

        cohortExample = np.array([gender,age,income,bill_amount]).reshape(1,4)
        clusterPred = model.predict(cohortExample)

        cohort.paper = clusterCycles[clusterPred[0]][0]
        cohort.text = clusterCycles[clusterPred[0]][1]
        cohort.email = clusterCycles[clusterPred[0]][2]

        cohort.cid = int(str(cohort.paper) + str(cohort.text) + str(cohort.email))
        db.session.add(cohort)
    db.session.commit()


"""
Polls database for patients to cluster
"""
def createDataSet():
    header_content = {'Content-type': 'application/json'}
    r = requests.get("http://127.0.0.1:5000/patients/birth_year", headers=header_content, verify=False)
    birthYearList = r.json()
    currentYear = date.today().year
    ageList = []
    for birthYear in birthYearList:
        ageList.append(currentYear - birthYear)
    r = requests.get("http://127.0.0.1:5000/patients/family_income", headers=header_content, verify=False)
    incomeList = r.json()
    r = requests.get("http://127.0.0.1:5000/patients/gender", headers=header_content, verify=False)
    genderList = r.json()
    genderValueList = []
    for gender in genderList:
        if gender == 'M':
            genderValueList.append(1)
        else:
            genderValueList.append(2)
    r = requests.get("http://127.0.0.1:5000/patients/bill_amount", headers=header_content, verify=False)
    billList = r.json()
    r = requests.get("http://127.0.0.1:5000/patients/account_id", headers=header_content, verify=False)
    idList = r.json()
    r1 = requests.get("http://127.0.0.1:5000/web activities", headers=header_content, verify=False)
    webActList = r1.json()
    
    freqPaper = getAllPatientsFreq("PAPER")
    freqText = getAllPatientsFreq("TEXT")
    freqEmail = getAllPatientsFreq("EMAIL")
    combinedCommFreqs = list(zip(freqPaper, freqText, freqEmail))

    #Separating for success cases
    successCases = set()
    for act in webActList:
        if act['eventId'] == 7:
            successCases.add(act['account_id'])

    patientList = list(zip(ageList, genderValueList, incomeList, billList))

    prunedList = []
    prunedFreqs = []
    for patient in range(len(idList)):
        if idList[patient] in successCases:
            prunedList.append(patientList[patient])
            prunedFreqs.append(combinedCommFreqs[patient])
        

    arrayList = np.array(prunedList)

    return arrayList,prunedFreqs


clusteringAlgorithm('minibatchKmean')