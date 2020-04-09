import time
import sys
from app import db
import src.algorithms.linear_regression as linear_regression
import src.algorithms.MachineLearningVariableGetter as mlVariableGetter


# Pull data from the database and starts the learning algorithm
def start_learning_algorithm():
    # Lists of b0, b1, and b2 variables
    b0_list = []
    b1_list = []
    b2_list = []

    # X1 variables (patient demographics)
    patient_age_list = mlVariableGetter.getAllPatientsAgeInOrder()
    patient_income_list = mlVariableGetter.getAllPatientsFamilyIncome()
    patient_bill_list = mlVariableGetter.getAllPatientsBillAmount()

    # X2 variables (freq. of communication methods)
    freq_paper_list = mlVariableGetter.getAllPatientsFreq("PAPER")
    freq_text_list = mlVariableGetter.getAllPatientsFreq("TEXT")
    freq_email_list = mlVariableGetter.getAllPatientsFreq("EMAIL")

    # Y variables (successes and failures of patients paying their bills)
    succ_list = mlVariableGetter.getAllPatientsSuccess()

    # Start running the learning algorithm (linear regression) and append b0, b1, and b2 values to appropriate list

    # Patient age and paper
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_age_list, freq_paper_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient age and text
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_age_list, freq_text_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient age and email
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_age_list, freq_email_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])

    # Patient income and paper
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_income_list, freq_paper_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient income and text
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_income_list, freq_text_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient income and email
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_income_list, freq_email_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])

    # Patient bill amount and paper
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_bill_list, freq_paper_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient bill amount and text
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_bill_list, freq_text_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient bill amount and email
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_bill_list, freq_email_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])

    # Print out the b0, b1, and b2 lists
    print("b0 list: ")
    print(b0_list)
    print("b1 list: ")
    print(b1_list)
    print("b2 list: ")
    print(b2_list)

# Runs the background task of continuously checking the database and updating
# the job statuses.
def run_background_task():
    print("Background task started.")
    try:
        while True:
            time.sleep(3)
            from src.models.QueueJob import QueueJob
            jobs = QueueJob.query.all()

            for job in jobs:
                # From the list of jobs, check if the first job with a status of 0 (NOT_STARTED)
                if job.status is 0:
                    print("Job " + str(job.id) + " is now in progress.")
                    # If the job has not started yet, set the status to 1 (IN_PROGRESS)
                    job.status = 1
                    db.session.commit()
                    # And wait for a certain amount of time (Testing purposes)
                    time.sleep(3)

                    # Start the learning algorithm
                    start_learning_algorithm()

                    print("Job " + str(job.id) + " is now done.")
                    # Set job status to 2 (DONE)
                    job.status = 2
                    db.session.commit()
                    break
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    run_background_task()