"""
File that contains methods for categorizing patients
"""
from app import db
from src.models.Cohort import Cohort


"""
Example bucket size maxes, need to be matched later to real brackets
-1 will be the max bracket that extends from the largest value to infinity
"""
ages = [25,40,60,80]
incomes = [50000, 100000, 150000, 250000]
bills = [1500, 5000, 10000, 25000, 100000]

"""
Categorizes patient based on existing buckets
Doesn't run algorithm
"""
def categorizeFromBuckets(patient):
    age = 2020 - patient['dateOfBirth']
    gender = patient['gender']
    income = patient['income']
    bill = patient['billAmount']
    #TODO clarify whether add more buckets for opt out or try and do distance algorithm
    optOut = patient['OptOut']


    ageParameter = 0
    incomeParameter = 0
    billParameter = 0

    for a in ages:
        if age <= a:
            ageParameter = a
            break
    if ageParameter == 0: ageParameter = -1

    for i in incomes:
        if income <= i:
            incomeParameter = i
            break
    if incomeParameter == 0: incomeParameter = -1

    for b in bills:
        if bill <= b:
            billParameter = b
            break
    if billParameter == 0: billParameter = -1

    cohort = Cohort.query.filter_by(gender=gender, ageMax=ageParameter, incomeMax=incomeParameter, billAmountMax=billParameter).all()

    if len(cohort) > 1:
        #Something has gone wrong
        return "Error"
    elif len(cohort) == 0:
        return 0
    
    return cohort[0].cid
    
