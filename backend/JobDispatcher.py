import time
import sys
from app import db
from src.models.Cohort import Cohort
import src.algorithms.linear_regression as linear_regression
import src.algorithms.MachineLearningVariableGetter as mlVariableGetter
import src.algorithms.clustering as clustering


# Pull data from the database and starts the learning algorithm
def start_learning_algorithm():
    # Lists of b0, b1, and b2 variables
    b0_list = []
    b1_list = []
    b2_list = []

    # X1 variables (patient demographics)
    patient_age_list = mlVariableGetter.getAllPatientsAgeInOrder()
    patient_income_list = mlVariableGetter.getAllPatientsFamilyIncome()
    patient_gender_list = mlVariableGetter.getAllPatientsGenderInOrder()
    patient_bill_list = mlVariableGetter.getAllPatientsBillAmount()
    # Convert patient gender list to numeric representation of gender (ex.: M = 1, F = 2)
    patient_gender_numeric_list = []
    for gender in  patient_gender_list:
        if gender == "M":
            patient_gender_numeric_list.append(1)
        elif gender == "F":
            patient_gender_numeric_list.append(2)

    # X2 variables (freq. of communication methods)
    freq_paper_list = mlVariableGetter.getAllPatientsFreq("PAPER")
    freq_text_list = mlVariableGetter.getAllPatientsFreq("TEXT")
    freq_email_list = mlVariableGetter.getAllPatientsFreq("EMAIL")

    # Y variables (successes and failures of patients paying their bills)
    succ_list = mlVariableGetter.getAllPatientsSuccess()

    # Start running the learning algorithm (linear regression) and append b0, b1, and b2 values to appropriate list

    # Patient age and email
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_age_list, freq_email_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
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

    # Patient income and email
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_income_list, freq_email_list)
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

    # Patient gender and email
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_gender_numeric_list, freq_email_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient gender and paper
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_gender_numeric_list, freq_paper_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])
    # Patient gender and text
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_gender_numeric_list, freq_text_list)
    b0_list.append(prediction_variable_list[0])
    b1_list.append(prediction_variable_list[1])
    b2_list.append(prediction_variable_list[2])

    # Patient bill amount and email
    prediction_variable_list = linear_regression.multiLinearRegression(succ_list, patient_bill_list, freq_email_list)
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

    # Print out the b0, b1, and b2 lists
    print("b0 list: ")
    print(b0_list)
    print("b1 list: ")
    print(b1_list)
    print("b2 list: ")
    print(b2_list)

    # TODO Assign communication cycles to each cohort using b0, b1, and b2
    # TODO Come up with max communication frequency (ex.: the max # of mails this patient should get is 10)
    # In analyzePatient(), it would probably be better to store the communication cycles in the cohort.
    # To do that, we'll need to pass the uid of the cohort and generate a cid
    cohorts = Cohort.query.all()
    for cohort in cohorts:
        gender = 0
        if cohort.gender == "M":
            gender = 1
        else:
            gender = 2
        age = cohort.ageMin
        income = cohort.incomeMin
        bill_amount = cohort.billAmountMin
        # Choosing a constant #
        cons = 2
        # The max communication frequency (ex.: the max # of mails, emails, and text this patient should get)
        max_com_freq = 10

        # Use b0, b1, and b2 to create linear regression functions and predict best cycle
        # of communication methods for each cohort of patients
        comm_cycle = linear_regression.analyzePatient(age, income, gender, bill_amount, cons, max_com_freq, b0_list, b1_list, b2_list)
        cohort.email = int(comm_cycle[0])
        cohort.paper = int(comm_cycle[1])
        cohort.text = int(comm_cycle[2])

        # After receiving communication cycles, create the cohort ID (cid) based on cycles
        # Ex.: If paper = 1, text = 2, email = 1, then cid = 121
        #      If paper = 0, text = 2, email = 2, then cid = 22
        #      If paper = 2, text = 1, email = 0, then cid = 210
        cohort.cid = int(str(cohort.paper) + str(cohort.text) + str(cohort.email))

        print("Cohort: ")
        print(cohort)
        db.session.add(cohort)
    db.session.commit()


# Runs the background task of continuously checking the database and updating
# the job statuses.
def run_background_task():
    print("Background task started.")
    try:
        while True:
            time.sleep(3)
            from src.models.QueueJob import QueueJob
            jobs = QueueJob.query.all()

            # Before dispatching the learning job, check the list of jobs and set any jobs with status
            # IN_PROGRESS to status NOT_STARTED. This is to ensure that the jobs are restarted in
            # case the user terminates the job dispatcher while the job is in progress
            for job in jobs:
                if job.status is 1:
                    job.status = 0
                    db.session.commit()

            # Dispatch learning jobs that have not started yet in a first come, first serve basis
            for job in jobs:
                # From the list of jobs, check if the first job with a status of 0 (NOT_STARTED)
                if job.status is 0:
                    print("Job " + str(job.id) + " is now in progress.")
                    # If the job has not started yet, set the status to 1 (IN_PROGRESS)
                    job.status = 1
                    db.session.commit()
                    # And wait for a certain amount of time (Testing purposes)
                    time.sleep(3)

                    
                    if job.algorithm == 'LinearRegression':
                        # Start the learning algorithm
                        start_learning_algorithm()
                    else:
                        clustering.clusteringAlgorithm(job.clusterAlgorithm)

                    print("Job " + str(job.id) + " is now done.")
                    # Set job status to 2 (DONE)
                    job.status = 2
                    db.session.commit()
                    break
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    run_background_task()