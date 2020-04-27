import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from app import db
import csv
import os
from src.models.Patient import Patient
from src.models.Communication import Communication
from src.models.WebActivity import WebActivity


def moveData():
    """
    Pareses data from csv file and collects it into nested object structure
    Tied each record to a patient ID
    """
    absolutePath = os.path.abspath(__file__)[:-13]

    rel_path = '/SponsorDataSets/demographics.csv'
    demPath = absolutePath + rel_path
    with open(demPath, newline='') as csvfile:
        patientReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        plineCount = 0

        for row in patientReader:
            if plineCount == 0:
                plineCount += 1
            else:
                header_content = {'Content-type': 'application/json'}
                account_id = row[0]
                gender = row[1]
                birth_year = row[2]
                address_zip = row[3]
                family_income = row[4]
                bill_amount = row[5]
                patient = Patient()
                patient.accountId = int(account_id)
                patient.gender = gender
                patient.birth_year = int(birth_year)
                patient.address_zip = address_zip
                patient.family_income = int(family_income)
                patient.bill_amount = int(bill_amount)
                db.session.add(patient)

                plineCount += 1
        db.session.commit()


    rel_path = '/SponsorDataSets/commuications.csv'
    commPath = absolutePath + rel_path
    with open(commPath, newline='') as csvfile:
        comReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        clineCount = 0

        for row in comReader:
            if clineCount == 0:
                clineCount += 1
            else:
                header_content = {'Content-type': 'application/json'}
                account_id = row[0]
                notification_date_time = row[1]
                method = row[2]
                notification_type = row[3]
                uid = clineCount
                comm = Communication()
                comm.accountId = int(account_id)
                comm.notification_date_time = notification_date_time
                comm.method = method
                comm.notification_type = notification_type
                comm.uid = int(uid)
                db.session.add(comm)
                clineCount += 1
        db.session.commit()
    #return

    rel_path = '/SponsorDataSets/website activity.csv'
    webPath = absolutePath + rel_path
    with open(webPath, newline='') as csvfile:
        webReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        wlineCount = 0

        for row in webReader:
            if wlineCount == 0:
                wlineCount += 1
            else:
                header_content = {'Content-type': 'application/json'}
                account_id = row[0]
                event_id = row[1]
                bill_status = row[2]
                action_date = row[3]
                uid = wlineCount
                web_act = WebActivity()
                web_act.uid = uid
                web_act.accountId = int(account_id)
                web_act.eventId = int(event_id)
                web_act.billStatus = bill_status
                web_act.actionDate = action_date
                db.session.add(web_act)
                wlineCount += 1
        db.session.commit()

if __name__ == "__main__":
    moveData()
