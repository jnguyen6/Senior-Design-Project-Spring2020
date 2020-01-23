#Patient Pay Backend
##Local Development
###Installation
1. Install Python and Pip (package manager)
2. Run in shell: `pip install --user pipenv`
3. Run in shell: `pipenv install`
###Run Locally
1. Complete installation steps
2. Run in shell `flask run`
3. Endpoints are accessed through `localhost:5000`
4. End process with `Ctrl+C`
##Build and Run with Docker
1. Ensure that Docker is installed by running `docker -v`
2. Run in shell `docker build -t patient_pay_backend .`
3. Run in shell `docker run -d -p 5000:5000 patient_pay_backend`
4. Ensure that process is running by `docker ps`
5. To kill, run `docker kill <CONTAINER_ID>` (found by `docker ps`)
