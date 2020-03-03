# Patient Pay Backend
## Local Database
### macOS / Unix Instructions
1. Install PostgreSQL and make sure it is currently running (confirm by running `postgres -v`)
2. On the shell, run `psql postgres`
3. Within psql, run `CREATE ROLE admin WITH LOGIN PASSWORD 'Password1!';`
4. Within psql, run `ALTER ROLE admin CREATEDB;`
5. Within psql, run `\q` to exit psql
6. On the shell, run `psql postgres -U admin`
7. Within psql, run `CREATE DATABASE backend;`
8. Within psql, run `GRANT ALL PRIVILEGES ON DATABASE backend TO admin;`
### Windows Instructions
1. Install PostgreSQL and add it to your PATH (confirm by running `postgres -v`)
2. On the shell, run `psql -U postgres`
3. Within psql, run `CREATE ROLE admin WITH LOGIN PASSWORD 'Password1!';`
4. Within psql, run `ALTER ROLE admin CREATEDB;`
5. Within psql, run `CREATE DATABASE backend;`
6. Within psql, run `GRANT ALL PRIVILEGES ON DATABASE backend TO admin;`
## Local Development
### Installation
1. Install Python and Pip (package manager)
2. Run in shell: `pip install --user pipenv`
3. Run in shell: `pipenv install`
### Run Locally
1. Complete installation steps
2. Run in shell `flask run`
3. Endpoints are accessed through `localhost:5000`
4. End process with `Ctrl+C`
## Build and Run with Docker
1. Ensure that Docker is installed by running `docker -v`
2. Ensure that you are in the rood directory of the Git Repo (not the backend directory)
3. Run in shell `docker-compose build`
4. Run in shell `docker-compose up -d`
5. Ensure that process is running by `docker ps`. There should be 2 running containers
6. To kill, run `docker-compose down`
## Testing
### Run Unit Tests
1. Run in shell `pytest`
2. For coverage, Run in shell `coverage run -m pytest && coverage report`

# Flask Information
https://opensource.com/article/18/4/flask
