import math

def mutli_linear_regression(y_list, x1_list, x2_list):
    """
    Runs the Multi-Linear Regression Algorithm from the lists provided
    All Lists should be the same size
    :param y_list: The success variable (or dependent variable)
    :param x1_list: The first independent variable
    :param x2_list: The second independent variable
    :return: The b-values (b0, b1, & b2) from the regression
    """
    yTotal = 0
    x1Total = 0
    x2Total = 0
    index = 0
    ySize = len(y_list)
    x1Size = len(x1_list)
    x2Size = len(x2_list)
    sumX1Product = 0
    sumX2Product = 0
    sumX1X2 = 0
    sumX1Y = 0
    sumX2Y = 0
    if ySize != x1Size or x1Size != x2Size:
        raise ValueError('Sizes of three lists must be the same to perform linear regression')
    while index < ySize:
        yTotal += y_list[index]
        x1Total += x1_list[index]
        x2Total += x2_list[index]
        sumX1Product += math.pow(x1_list[index], 2)
        sumX2Product += math.pow(x2_list[index], 2)
        sumX1X2 += x1_list[index] * x2_list[index]
        sumX1Y += x1_list[index] * y_list[index]
        sumX2Y += x2_list[index] * y_list[index]
        index += 1
    denominator = sumX1Product * sumX2Product - math.pow(sumX1X2, 2)
    # Prevent Divide by 0 errors
    if denominator == 0: denominator = 1
    if ySize == 0: ySize = 1
    if x1Size == 0: x1Size = 1
    if x2Size == 0: x2Size = 1
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
#       Y_gender,email  Y_gender,mail  Y_gender,text    Y_billamount,email  Y_billamount,mail  Y_billamount,text)
# Output:
#       Number of emails, mails and texts sent to the patient at given time period
def analyze_patient(age, income, gender, bill_amount, cons, max_com, b0_list, b1_list, b2_list):
    """
    Method of analyzing each specific patient from the output of the regression
    :param age: The age of the patient
    :param income: The income of the patient
    :param gender: The gender of the patient
    :param bill_amount: The patient's bill that is due
    :param cons: The communication method constant
    :param max_com: The max number of communications per month
    :param b0_list: The b0 list from the linear regression
    :param b1_list: The b1 list from the linear regression
    :param b2_list: The b2 list from the linear regression
    :return: The number of emails, paper messages, and texts to be sent to the patient
    """
    # Step1
    # generate 12 values of predicting the patient with same amount of communication variables
    y_ageEmail = b0_list[0] + b1_list[0] * age + b2_list[0] * cons
    y_ageMail = b0_list[1] + b1_list[1] * age + b2_list[1] * cons
    y_ageText = b0_list[2] + b1_list[2] * age + b2_list[2] * cons
    y_incomeEmail = b0_list[3] + b1_list[3] * income + b2_list[3] * cons
    y_incomeMail = b0_list[4] + b1_list[4] * income + b2_list[4] * cons
    y_incomeText = b0_list[5] + b1_list[5] * income + b2_list[5] * cons
    y_genderEmail = b0_list[6] + b1_list[6] * gender + b2_list[6] * cons
    y_genderMail = b0_list[7] + b1_list[7] * gender + b2_list[7] * cons
    y_genderText = b0_list[8] + b1_list[8] * gender + b2_list[8] * cons
    y_billEmail = b0_list[9] + b1_list[9] * bill_amount + b2_list[9] * cons
    y_billMail = b0_list[10] + b1_list[10] * bill_amount + b2_list[10] * cons
    y_billText = b0_list[11] + b1_list[11] * bill_amount + b2_list[11] * cons
    # Step2
    yEmail = y_ageEmail + y_incomeEmail + y_genderEmail + y_billEmail
    yMail = y_ageMail + y_incomeMail + y_genderMail + y_billMail
    yText = y_ageText + y_incomeText + y_genderText + y_billText
    yTotal = yEmail + yMail + yText
    if yTotal == 0: yTotal = 1
    # Step3
    numEmails = max_com * (yEmail / yTotal)
    numMails = max_com * (yMail / yTotal)
    numTexts = max_com * (yText / yTotal)
    return [numEmails, numMails, numTexts]

# match the optimal cohort for a certain patient
# optOutList contains strings of methods that the patient does not want to receive, may include "email","text" and/or "paper"
def match_optimal_cohort(age, gender, income, bill_amount, num_emails, num_mails, num_texts, opt_out_list, cohort_list):
    """
    Matches the optimal cohort for the given patient
    :param age: The age of the patient
    :param income: The income of the patient
    :param gender: The gender of the patient
    :param bill_amount: The patient's bill that is due
    :param num_emails:
    :param num_mails:
    :param num_texts:
    :param opt_out_list: The list of opt-outs that the patient has chosen
    :param cohort_list: The list of generated cohorts
    :return: The cid (condensed communications) for the chosen cohort
    """
    # filter out cohorts containing methods of opt-out
    for c in cohort_list:
        if "email" in opt_out_list and c.email != 0:
            cohort_list.remove(c)
        if "paper" in opt_out_list and c.paper != 0:
            cohort_list.remove(c)
        if "text" in opt_out_list and c.text != 0:
            cohort_list.remove(c)
    # with filtered cohort list, return the id of optimal cohort
    cid = 0
    pastDiffValue = 9999
    for cht in cohort_list:
        diffValue = abs(num_emails - cht.email) + abs(num_mails - cht.paper) + abs(num_texts - cht.text)
        if diffValue < pastDiffValue and cht.ageMax > age > cht.ageMin and gender == cht.gender and cht.incomeMax > income > cht.incomeMin and cht.billAmountMin < bill_amount < cht.billAmountMax:
            cid = cht.cid
            pastDiffValue = diffValue
    return cid
