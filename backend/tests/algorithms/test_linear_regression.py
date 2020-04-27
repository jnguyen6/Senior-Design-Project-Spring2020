import pytest

def test_generate_patients(patient_generator, activity_generator, communication_generator):
    patients = patient_generator(10)
    activities = activity_generator(patients, 1)
    communications = communication_generator(patients, 1)
    print(communications)
