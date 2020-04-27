# This class is to analyze datasets from DB, get all parameters needed to put into
# machine learning algorithm by analyzing those instances of patients, communications
# and web activities
# The goal is to generate three types of lists: x1, x2, y
# The element in the same index of those lists should represent data from one same patient
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from app import db
from datetime import datetime
from src.models.Patient import Patient
from src.models.Communication import Communication
from src.models.WebActivity import WebActivity

def get_all_patients_age():
    """
    Gets a list of all patient's ages
    :return: List of all patient's ages
    """
    return [p.birth_year for p in Patient.query.all()]

def get_all_patients_family_income():
    """
    Gets a list of all patient's family incomes
    :return: List of all patient's family incomes
    """
    return [p.family_income for p in Patient.query.all()]

def get_all_patients_gender():
    """
    Gets a list of all patient's genders
    :return: List of all patient's genders
    """
    return [p.gender for p in Patient.query.all()]

def get_all_patients_bill_amount():
    """
    Gets a list of all patient's bill amounts
    :return: List of all patient's bill amounts
    """
    return [p.bill_amount for p in Patient.query.all()]

def get_all_patients_frequency(communication_type):
    """
    Gets a list containing the frequency of sending a communication type to all patients
    :param communication_type: The type of communication, either "PAPER", "TEXT", or "EMAIL"
    :return: The list of communication frequencies
    """
    idList = [p.accountId for p in Patient.query.all()]
    comms = Communication.query.all()
    communicationList = []
    for com in comms:
        comDict = dict()
        comDict['uid'] = com.uid
        comDict['account_id'] = com.accountId
        comDict['notification_date_time'] = com.notification_date_time
        comDict['method'] = com.method
        comDict['notification_type'] = com.notification_type
        communicationList.append(comDict)
    freqList = []
    for patient_id in idList:
        numMail = 0
        earliestTime = datetime.now()
        latestTime = datetime(1970, 1, 1)
        for com in communicationList:
            com_account_id = com.get('account_id')
            com_method = com.get('method')
            com_time = com.get('notification_date_time')
            deliveryTime = datetime.strptime(com_time, '%Y-%m-%d %H:%M:%S')
            if deliveryTime < earliestTime:
                earliestTime = deliveryTime
            if deliveryTime > latestTime:
                latestTime = deliveryTime
            if com_account_id == patient_id and com_method == communication_type:
                numMail += 1
        if earliestTime == latestTime:
            timeDiffInThreeMonths = 1
        else:
            timeDiff = latestTime - earliestTime
            timeDiffInSec = timeDiff.total_seconds()
            timeDiffInThreeMonths = timeDiffInSec / 3600 / 24 / 30 / 3
        freqList.append(numMail/timeDiffInThreeMonths)
    return freqList

def get_all_patients_success():
    """
    Gets a list containing the success values for all patients
    :return: The success list
    """
    idList = [p.accountId for p in Patient.query.all()]

    webActs = WebActivity.query.all()
    webActList = []
    for webAct in webActs:
        webActDict = dict()
        webActDict['uid'] = webAct.uid
        webActDict['account_id'] = webAct.accountId
        webActDict['eventId'] = webAct.eventId
        webActDict['billStatus'] = webAct.billStatus
        webActDict['actionDate'] = webAct.actionDate
        webActList.append(webActDict)

    comms = Communication.query.all()
    comList = []
    for com in comms:
        comDict = dict()
        comDict['uid'] = com.uid
        comDict['account_id'] = com.accountId
        comDict['notification_date_time'] = com.notification_date_time
        comDict['method'] = com.method
        comDict['notification_type'] = com.notification_type
        comList.append(comDict)
    successScoreList = []

    for patient_id in idList:
        paid = 0
        firstTimeGet = 0
        firstComTime = datetime(1970, 1, 1)
        timePaid = datetime(1970, 1, 1)
        successScore = 0
        for com in comList:
            if com.get('account_id') == patient_id and firstTimeGet == 0:
                firstComTime = datetime.strptime(com.get('notification_date_time'), '%Y-%m-%d %H:%M:%S')
                firstTimeGet = 1
        for webAct in webActList:
            if webAct.get('account_id') == patient_id and webAct.get('billStatus') == "PAID":
                paid = 1
                actionDate = webAct.get('actionDate')
                timePaid = datetime.strptime(actionDate, '%Y-%m-%d %H:%M:%S')
        if paid == 1:
            timeDiff = timePaid - firstComTime
            timeDiffInSec = timeDiff.total_seconds()
            timeDiffInWeek = timeDiffInSec / 3600 / 24 / 7;
            successScore = 1 / timeDiffInWeek
        if paid == 0:
            successScore = 0
        successScoreList.append(successScore)
    return successScoreList
