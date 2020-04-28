import math
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from app import db
from src.models.Cohort import Cohort


# Truncate decimal values to specific precision
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


# Logistic regression algorithm that will take the patient variables (i.e. demographics, frequency of
# communication methods) as the independent variables and predict the dependent variables (i.e. whether
# the patient has paid their bill or not).
def logisticRegression(x_list, y_list):
    logistic_regression = LogisticRegression(max_iter=1000)
    # Train the model
    logistic_regression.fit(x_list, y_list)

    print("Updating cohorts with new communication cycles and cohort ID...")

    # Retrieve the list of cohorts and iteratively predict and update the cohort
    cohorts = Cohort.query.all()
    for cohort in cohorts:
        gender = 0
        if cohort.gender == "M":
            gender = 1
        else:
            gender = 2

        age = (cohort.ageMax + cohort.ageMin) / 2
        income = (cohort.incomeMax + cohort.incomeMin) / 2
        bill_amount = (cohort.billAmountMax + cohort.billAmountMin) / 2

        # Iterate through a set communication cycle and choose the communication cycle with the
        # best prediction accuracy. The communication cycle is arranged in the following way:
        # comm_cycle = [email, paper, text]
        num_email = 0
        num_paper = 0
        num_text = 0
        max_communication = 8
        # Best prediction probability estimate for a specific communication cycle
        best_pred_prob = 0
        while num_email != max_communication or num_paper != max_communication or num_text != max_communication:
            x_test_list = [age, income, gender, bill_amount, num_email, num_paper, num_text]
            # Using log_proba, y_pred will contain the probability estimate of the class labels, arranged as
            # ([probability estimate of 0], [probability estimate of 1])
            y_pred = logistic_regression.predict_proba([x_test_list])
            y_pred = y_pred[0]
            print("Y val: " + str(y_pred[1]))
            print(truncate(y_pred[1], 2))

            # If we found a better probability estimate of the patient paying their bills based on a specific
            # communication cycle, update the cohort accordingly
            if truncate(y_pred[1], 2) > 0.5:
                cohort.email = num_email
                cohort.paper = num_paper
                cohort.text = num_text
                cohort.cid = int(str(cohort.paper) + str(cohort.text) + str(cohort.email))
                print("Y Pred: " + str(truncate(y_pred[1], 2)))
                print("Cohort ID: " + str(cohort.cid))
                # Add updated cohort to DB
                db.session.add(cohort)
                break

            # Increment communication cycles until it reaches the max communication
            if num_text < max_communication:
                num_text += 1
            elif num_paper < max_communication:
                num_paper += 1
            elif num_email < max_communication:
                num_email += 1

    db.session.commit()
    print("Cohorts are now updated.")