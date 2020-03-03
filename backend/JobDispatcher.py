import time
import sys
from app import db

# Runs the background task of continuously checking the database and updating
# the job statuses.
def run_background_task():
    print("Background task started.")
    try:
        while True:
            time.sleep(5)
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
                    time.sleep(5)

                    # TODO: Send job to learning algorithm component.
                    # TODO: Wait for response before setting job status to DONE

                    print("Job " + str(job.id) + " is now done.")
                    # Set job status to 2 (DONE)
                    job.status = 2
                    db.session.commit()
                    break
    except KeyboardInterrupt:
        sys.exit()

run_background_task()