import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
import requests
from numpy import unique
from numpy import where
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from datetime import date
import src.algorithms.machine_learning_variable_getter as mlVar
import statistics
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
def clusteringAlgorithm(clusterAlgorithm, test=False, testData = None):
    cluster_size = 6

    if test == True:
        X, frequencies = testData[0],testData[1]
    else:
        X, frequencies = createDataSet()
    
    if X.shape[1] != 4:
        return

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    model = algorithms[clusterAlgorithm](n_clusters=cluster_size)

    if clusterAlgorithm == 'minibatchKmean':
        kmeansPredict(model, X, frequencies, scaler, cluster_size)
    else:
        otherPrediction(model, X, frequencies, scaler, cluster_size)

"""
Populate cohorts with other algorithms
"""
def otherPrediction(model, X, frequencies, scaler, cluster_size):
    vals = model.fit_predict(X)
    clusterCycles = []
    yhat = unique(vals)

    #Find indices for patients per cluster
    clusterIndices = []
    for cluster in yhat:
        indices = where(vals == cluster) 
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
        
        """
        find closest test point and use its cluster
        """
        closest = 0
        dist = (cohortExample - X[0])**2
        dist = np.sum(dist)
        dist = np.sqrt(dist)
        for patientIndex in range(1, len(X)):
            newdist = (cohortExample - X[patientIndex])**2
            newdist = np.sum(dist)
            newdist = np.sqrt(dist)

            if newdist < dist:
                dist = newdist
                closest = patientIndex
        
        clusterPred = vals[closest]


        cohort.paper = clusterCycles[clusterPred][0]
        cohort.text = clusterCycles[clusterPred][1]
        cohort.email = clusterCycles[clusterPred][2]

        cohort.cid = int(str(cohort.paper) + str(cohort.text) + str(cohort.email))
        db.session.add(cohort)
    db.session.commit()

    
"""
Populate cohorts from kmeans prediction
"""
def kmeansPredict(model, X, frequencies, scaler, cluster_size):

    clusterCycles = []
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
        cohortExample = scaler.fit_transform(cohortExample)
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
    #Get age
    birthYearList = mlVar.get_all_patients_age()
    currentYear = date.today().year
    ageList = []
    for birth in birthYearList:
        ageList.append(currentYear - birth)
    
    #Get Income
    incomeList = mlVar.get_all_patients_family_income()

    #Get gender
    genderList = mlVar.get_all_patients_gender()
    genderValueList = []
    for gender in genderList:
        if gender == 'M':
            genderValueList.append(1)
        else:
            genderValueList.append(2)

    #Get bill
    billList = mlVar.get_all_patients_bill_amount()

    freqPaper = mlVar.get_all_patients_frequency("PAPER")
    freqText = mlVar.get_all_patients_frequency("TEXT")
    freqEmail = mlVar.get_all_patients_frequency("EMAIL")
    combinedCommFreqs = list(zip(freqPaper, freqText, freqEmail))

    successCases = mlVar.get_all_patients_success()

    patientList = list(zip(ageList, genderValueList, incomeList, billList))

    prunedList = []
    prunedFreqs = []
    for case in range(len(successCases)):
        if case > 0:
            prunedList.append(patientList[case])
            prunedFreqs.append(combinedCommFreqs[case])
        

    arrayList = np.array(prunedList)

    return arrayList,prunedFreqs
