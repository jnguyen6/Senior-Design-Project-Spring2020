"""
Move communications from .csv files to DB
"""
import csv
import os
import requests

"""
Pareses data from csv file and collects it into nested object structure
Tied each record to a patient ID
"""
def moveData():
    absolutePath = os.path.abspath(__file__)[:-13]

    rel_path = '\SponsorDataSets\demographics.csv'
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
                r = requests.post("http://127.0.0.1:5000/patients/" + account_id + "," + gender + "," + birth_year + "," + address_zip + "," + family_income + "," + bill_amount, headers=header_content, verify=False)
                print(r.status_code)
                plineCount += 1


    rel_path = '\SponsorDataSets\commuications.csv'
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
                uidStr = str(clineCount)
                r = requests.post("http://127.0.0.1:5000/communications/" + uidStr + "," + account_id + "," + notification_date_time + "," + method + "," + notification_type, headers=header_content, verify=False)
                print(r.status_code)
                clineCount += 1
    #return

    rel_path = '\SponsorDataSets\website activity.csv'
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
                uid = str(wlineCount)
                r = requests.post("http://127.0.0.1:5000/web activities/" + uid + "," + account_id + "," + event_id + "," + bill_status + "," + action_date, headers=header_content, verify=False)
                print(r.status_code)
                wlineCount += 1

        return


"""
Main function of program
"""
if __name__ == "__main__":
    moveData()
