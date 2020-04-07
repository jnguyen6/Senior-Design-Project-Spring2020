"""
Data scraping tool for senior design
Author: Mark Snedecor
"""
import csv 
import matplotlib.pyplot as plt
import os 

#Dictionary of all patients, keys are patient IDs
patientDict = {}

#Dictionary for patients who logged in
successDict = {}

"""
Class that represents a patient and holds all relevant data
"""
class Patient:
    def __init__(self, s, i, inc, bill, date):
        self.sex = s
        self.id = i
        self.income = inc
        self.billAmount = bill
        self.birthDate = date
        self.age = 2020 - int(date)
        self.notifications = []
        #Dictionary of notifications by day
        self.notByDay = {}
        self.activities = []
        #Dictionary of website activity that only keeps the first login in the day
        self.firstActInDay = {}
        self.login = False            
    
    def printer(self):
        print("User Id: {}\nSex: {}\nIncome: {}\nBill amount: {}\nBirth Year: {}\nAge: {}\n".format(self.id, self.sex, self.income, self.billAmount, self.birthDate, self.age))

        print("         Communications\n======================================\n")
        counter = 1
        for n in self.notifications:
            print(n.printer(counter))
            counter += 1

        counter = 1
        print("         Activity\n======================================\n")
        if(len(self.activities) == 0):
            print("None\n")
        else:
            for a in self.activities:
                print(a.printer(counter))
                counter += 1
        return

"""
Class for communication logs
"""
class notfication:
    def __init__(self, noteTime, meth, notification):
        self.time = noteTime
        self.method = meth
        self.notType = notification
        self.numericalDate = noteTime[:10].split('-')

    def printer(self, counter):
        return("{}\n  Date: {}\n  Method: {}\n  Communication Type: {}\n  Day of Message: {}\n".format(counter, self.time, self.method, self.notType, self.numericalDate))

"""
Class for activity logs
"""
class activity:
    def __init__(self, idnum, billStatus, actionDate):
        self.eventID = idnum
        self.status = billStatus
        self.date = actionDate
        self.numericalDate = actionDate.split('-')


    def printer(self, counter):
        return("{}\n  Event ID: {}\n  Status: {}\n  Date: {}\n".format(counter,self.eventID, self.status, self.date))


"""
Pareses data from csv file and collects it into nested object structure
Tied each record to a patient ID
"""
def readFiles():
    absolutePath = os.path.abspath(__file__)[:-14]

    rel_path = r'\SponsorDataSets\demographics.csv'
    demPath = absolutePath + rel_path
    with open(demPath, newline='') as csvfile:
        patientReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(patientReader)
        for row in patientReader:
            newPat = Patient(row[1], row[0], row[4], row[5], row[2])
            patientDict[newPat.id] = newPat
    
    
    rel_path = r'\SponsorDataSets\commuications.csv'
    commPath = absolutePath + rel_path
    with open(commPath, newline='') as csvfile:
        patientReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(patientReader)

        s = set()

        for row in patientReader:
            
            size = len(s)
            r = ' '.join(row)
            s.add(r)

            if(len(s) != size):
                newComm = notfication(row[1], row[2], row[3])
                patientDict[row[0]].notifications.append(newComm)
                date = ''
                if date.join(newComm.numericalDate) not in patientDict[row[0]].notByDay.keys():
                    patientDict[row[0]].notByDay[date.join(newComm.numericalDate)] = newComm

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
Returns a pie chart of the success rate for patients logging in
"""
def pieChart():
    success = 0
    for keys in patientDict:
        if patientDict[keys].login == True:
            success += 1
    
    labels = 'Success', 'No login'
    plt.pie([(success/len(patientDict) * 100), (len(patientDict)-success / len(patientDict) * 100)], labels=labels)
    plt.show()

"""
Creates histogram for age distribution in success cases
"""
def ageHistogram():
    ages = []
    for key in successDict:
        ages.append(successDict[key].age)
    plt.hist(ages)
    plt.show()


"""
Scatter plot showing relationship between last notification and logging in
And the type of communication
"""
def scatterCommtypeResponseTime():
    successCases = []
    for key in successDict:
        pat = successDict[key]
        for day in pat.firstActInDay:
            login = pat.firstActInDay[day]



"""
Main function of program
"""
if __name__ == "__main__":
    readFiles()
    pieChart()
    ageHistogram()
    patientDict['123262'].printer()
