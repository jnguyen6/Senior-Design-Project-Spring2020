from datetime import datetime
import random
import pytest
import numpy as np
from app import app, db
from src.models.Communication import Communication
from src.models.Patient import Patient
from src.models.WebActivity import WebActivity


@pytest.fixture
def client():
    app.config['TESTING'] = True
    db.drop_all()
    db.create_all()
    with app.test_client() as client:
        yield client

def patient_gen(
        number_of_patients: int,
        age_range: (int, int) = None,
        income_range: (int, int) = None,
        bill_range: (int, int) = None,
        preferred_sex: str = None,
        offset: int = 0
):
    """
    Pytest Fixture to generate patients
    :param number_of_patients: Mandatory argument stating the number of patients to generate
    :param age_range: Optional Tuple specifying the start and end of the age range
    :param income_range: Optional Tuple specifying the start and end of the income range. In increments of 1000
    :param bill_range: Optional Tuple specifying the start and end of of the bill range. Increments of 10
    :param preferred_sex: Optional value ('M' or 'F') specifying if all patients should be this sex
    :return: The generated patient dictionary
    """
    patient_dict = {}
    for index in range(0 + offset, number_of_patients + offset):
        patient_id = index

        if age_range is not None:
            age = random.randrange(age_range[0], age_range[1])
        else:
            age = random.randrange(18, 100, 1)

        if preferred_sex is not None and (preferred_sex == 'F' or preferred_sex == 'M'):
            sex = preferred_sex
        else:
            if index < (number_of_patients / 2):
                sex = 'F'
            else:
                sex = 'M'

        if income_range is not None:
            income = random.randrange(income_range[0], income_range[1], 1000)
        else:
            income = random.randrange(10000, 200000, 1000)

        if bill_range is not None:
            bill = random.randrange(bill_range[0], bill_range[1], 10)
        else:
            bill = random.randrange(200, 5000, 10)

        patient = Patient()
        patient.accountId = patient_id
        patient.birth_year = datetime.now().year - age
        patient.gender = sex
        patient.family_income = income
        patient.bill_amount = bill
        patient_dict[patient_id] = patient

    return patient_dict

@pytest.fixture
def patient_generator():
    return patient_gen

def activity_gen(patients, start_time, sampling_percent = 1):
    """
    Generator for the activities
    :param patients: The patients to generate activities for
    :param start_time: The time that the baseline for all activities should be
    :param sampling_percent: The threshold for the randomness of to add an activity
    :return: The generated activities
    """
    activities = []
    for patient in patients.values():
        chance = random.random()
        if chance < sampling_percent:
            new_time = start_time + (np.random.randint(1,17) * 7)
            activity = WebActivity()
            activity.accountId = patient.accountId
            activity.actionDate = new_time
            activity.billStatus = 'DUE'
            activity.eventId = 7
            activities.append(activity)

    return activities

@pytest.fixture
def activity_generator():
    return activity_gen

def communication_gen(patients, start_time, paper = 2, text = 2, email = 2, num_weeks = 17):
    """
    Generator for communications
    :param patients: The patients to generate communications for
    :param start_time: The base start time of the communications
    :param paper: Integer for paper cycle length in weeks (0 is opt out)
    :param text: Integer for text cycle length in weeks (0 is opt out)
    :param email:Integer for email cycle length in weeks (0 is opt out)
    :param num_weeks: The number of weeks to generate for
    :return: The communications array
    """
    communications = []
    for num in range(1, num_weeks):
        new_time = start_time + num * 7
        for patient in patients.values():
            if num % paper == 0:
                communication = Communication()
                communication.accountId = patient.accountId
                communication.method = "PAPER"
                communication.notification_type = f"PAPER_CYCLE_{num}(0002)"
                communication.notification_date_time = new_time
                communications.append(communication)
            if num % text == 0:
                communication = Communication()
                communication.accountId = patient.accountId
                communication.method = "TEXT"
                communication.notification_type = "BILL_REMINDER"
                communication.notification_date_time = new_time
                communications.append(communication)
            if num % email == 0:
                communication = Communication()
                communication.accountId = patient.accountId
                communication.method = "EMAIL"
                communication.notification_type = "PAST_DUE_BILL_REMINDER"
                communication.notification_date_time = new_time
                communications.append(communication)
    return communications

@pytest.fixture
def communication_generator():
    return communication_gen
