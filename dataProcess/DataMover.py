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

    """"
    rel_path = r'\SponsorDataSets\demographics.csv'
    demPath = absolutePath + rel_path
    with open(demPath, newline='') as csvfile:
        patientReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(patientReader)
        for row in patientReader:
            newPat = Patient(row[1], row[0], row[4], row[5], row[2])
            patientDict[newPat.id] = newPat
    """

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
                r = requests.post("http://127.0.0.1:5000/communications/" + account_id + "," + notification_date_time + "," + method + "," + notification_type, headers=header_content, verify=False)
                print(r.status_code)
                clineCount += 1
    return

"""
    rel_path = r'\SponsorDataSets\website activity.csv'
    webPath = absolutePath + rel_path
    with open(webPath, newline='') as csvfile:
        patientReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(patientReader)
        for row in patientReader:
            newAct = activity(row[1], row[2], row[3])
            if newAct.eventID == '7':
                patientDict[row[0]].activities.append(newAct)
                day = newAct.date[:10]

                if day not in patientDict[row[0]].firstActInDay.keys():
                    patientDict[row[0]].firstActInDay[day] = newAct

                if patientDict[row[0]].login == False:
                    patientDict[row[0]].login = True
                    successDict[patientDict[row[0]]] = patientDict[row[0]]

        return
        """

"""
Main function of program
"""
if __name__ == "__main__":
    moveData()
