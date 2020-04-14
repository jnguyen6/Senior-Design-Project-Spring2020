# yList, x1List and x2List should be lists that have the same size
# the elements in each same index form a multi-linear regression funcion
# return the b0, b1 and b2 value of the linear regression function
import math

def multiLinearRegression(yList, x1List, x2List):
    yTotal = 0
    x1Total = 0
    x2Total = 0
    index = 0
    ySize = len(yList)
    x1Size = len(x1List)
    x2Size = len(x2List)
    sumX1Product = 0
    sumX2Product = 0
    sumX1X2 = 0
    sumX1Y = 0
    sumX2Y = 0
    if (ySize != x1Size or x1Size != x2Size):
        raise ValueError('Sizes of three lists must be the same to perform linear regression')
    while (index < ySize):
        yTotal += yList[index]
        x1Total += x1List[index]
        x2Total += x2List[index]
        sumX1Product += math.pow(x1List[index], 2)
        sumX2Product += math.pow(x2List[index], 2)
        sumX1X2 += x1List[index] * x2List[index]
        sumX1Y += x1List[index] * yList[index]
        sumX2Y += x2List[index] * yList[index]
        index += 1
    denominator = sumX1Product * sumX2Product - math.pow(sumX1X2, 2)
    b1 = (sumX2Product * sumX1Y - sumX1X2 * sumX2Y) / denominator
    b2 = (sumX1Product * sumX2Y - sumX1X2 * sumX1Y) / denominator
    b0 = (yTotal / ySize) - b1 * (x1Total / x1Size) - b2 * (x2Total / x2Size)
    return [b0, b1, b2]

# Method of analyzing each specific patient
# 4 patient variables and 3 communication method variables
# 12 functions used to predict the patient in total
# Input:
#       Patient variables: x1:  int age, int income, int gender(0 or 1), int bill_amount
#       Communication method constant numbers: cons
#       Max communication per month: maxCom
#       12 b0's, b1's and b2's representing 12 prediction functions
#       (12 functions need to be in order: Y_age,email  Y_age,mail  Y_age,text  Y_income,email  Y_income,mail  Y_income,text
#       Y_gender,email  Y_gender,mail  Y_gender,text    Y_billamout,email  Y_billamount,mail  Y_billamount,text)
# Output:
#       Number of emails, mails and texts sent to the patient at given time period
def analyzePatient(age, income, gender, bill_amount, cons, maxCom, b0List, b1List, b2List):
    # Step1
    # generate 12 values of predicting the patient with same amount of communication variables
    y_ageEmail = b0List[0] + b1List[0] * age + b2List[0]*cons
    y_ageMail = b0List[1] + b1List[1] * age + b2List[1]*cons
    y_ageText = b0List[2] + b1List[2] * age + b2List[2] * cons
    y_incomeEmail = b0List[3] + b1List[3] * income + b2List[3] * cons
    y_incomeMail = b0List[4] + b1List[4] * income + b2List[4] * cons
    y_incomeText = b0List[5] + b1List[5] * income + b2List[5] * cons
    y_genderEmail = b0List[6] + b1List[6] * gender + b2List[6] * cons
    y_genderMail = b0List[7] + b1List[7] * gender + b2List[7] * cons
    y_genderText = b0List[8] + b1List[8] * gender + b2List[8] * cons
    y_billEmail = b0List[9] + b1List[9] * bill_amount + b2List[9] * cons
    y_billMail = b0List[10] + b1List[10] * bill_amount + b2List[10] * cons
    y_billText = b0List[11] + b1List[11] * bill_amount + b2List[11] * cons
    # Step2
    yEmail = y_ageEmail + y_incomeEmail + y_genderEmail + y_billEmail
    yMail = y_ageMail + y_incomeMail + y_genderMail + y_billMail
    yText = y_ageText + y_incomeText + y_genderText + y_billText
    yTotal = yEmail + yMail + yText
    # Step3
    numEmails = maxCom * (yEmail / yTotal)
    numMails = maxCom * (yMail / yTotal)
    numTexts = maxCom * (yText / yTotal)
    return [numEmails, numMails, numTexts]

# match the optimal cohort for a certain patient
# optOutList contains strings of methods that the patient does not want to receive, may include "email","text" and/or "paper"
def matchOptimalCohort(age, gender, income, billAmount, numEmails, numMails, numTexts, optOutList, cohortList):
    # filter out cohorts containing methods of opt-out
    for c in cohortList:
        if ("email" in optOutList and c.email != 0):
            cohortList.remove(c)
        if ("paper" in optOutList and c.paper != 0):
            cohortList.remove(c)
        if ("text" in optOutList and c.text != 0):
            cohortList.remove(c)
    # with filtered cohort list, return the id of optimal cohort
    cid = 0
    pastDiffValue = 9999
    for cht in cohortList:
        diffValue = abs(numEmails - cht.email) + abs(numMails - cht.paper) + abs(numTexts - cht.text)
        if (diffValue < pastDiffValue and age < cht.ageMax and age > cht.ageMin and gender == cht.gender and income < cht.incomeMax
        and income > cht.incomeMin and billAmount > cht.billAmountMin and billAmount < cht.billAmountMax):
            cid = cht.cid
            pastDiffValue = diffValue
    return cid


def printFunction(list):
    b0 = list[0]
    b1 = list[1]
    b2 = list[2]

    print(b0, b1, b2, sep = ' ')


def main():
    yList = [20,40,60]
    x1List = [2,4,6]
    x2List = [2,4,6]
    printFunction(multiLinearRegression(yList, x1List, x2List))


if __name__ == '__main__':
    main()