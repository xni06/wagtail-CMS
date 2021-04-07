# Introduction
The purpose of this document is to try an simplify the dev start-up process, in particular:
- introduce a virtual environment, of use when running tests outside of docker
- use a default `docker-compose.yml` file suitable for dev
- use docker `.env` files to store local environment variables (not part of repo)
- easier and quicker to read/digest

This is a work-in-progress and requires some further attention:
- where should the `.env` files be stored so that they can be shared securely?
- refactor pipeline scripts so that `docker-compose.non-dev.yml` is used instead of `docker-compose.yml.example` 

# Virtual environment setup
```bash
## Create a virtual environment using Python 3.6.8 using https://virtualenv.pypa.io
virtualenv venv -p 3.6.8

# Activate the virtual environment 
source venv/bin/activate

# Verify Python version
python -V
```

# How to run tests
## Without Docker
### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Enable mocks for testing
export LOCAL=True

# To unset...
unset LOCAL
```

### Run tests
```bash
python manage.py test
```

<font color="red"><i>Why do these test fail? I wonder whether the actual DB* values make any difference during unit tests?</i></font>

## With Docker
### Run tests
```bash
# Fire it up if not already running
docker-compose --env-file .env.test up 

docker container exec -it wagtail-cms_web_1 python manage.py test   
```

# How configure the server

```bash
# Fire it up 

# dev environment using default `docker-compose.yml` and `.env` files
docker-compose up 

# or using a specific `.env` file for remote Courses/Institutions
docker-compose --env-file .env.pre-prod up
docker-compose --env-file .env.prod up

# or using a specific `docker-compose` file for remote CMS
docker-compose -f docker-compose.non-dev.yml --env-file .env.pre-prod up
docker-compose -f docker-compose.non-dev.yml --env-file .env.prod up
```

# Databases
## Fixtures
Type         | Local DB    | Remote DB   | Name                                     
---          | ---         | ---         | ---
CMS          | PostgresSQL | PostgresSQL | `CMS/fixtures/postgres.json` 
Courses      | MongoDB     | CosmosDB    | `courses/fixtures/courses.json` 
Institutions | MongoDB     | CosmosDB    | `institutions/fixtures/institutions.json` 

## Load local databases with data from fixtures
```bash
# CMS
docker container exec -it wagtail-cms_web_1 python manage.py populate_cms

# Courses
docker container exec -it wagtail-cms_web_1 python manage.py populate_courses

# Institutions
docker container exec -it wagtail-cms_web_1 python manage.py populate_institutions
```

## Optional - update fixture with data from remote database
```bash
# CMS
docker container exec -it wagtail-cms_web_1 python manage.py update_cms_fixture \
      --db_host $REMOTE_DB_HOST \
      --db_name $REMOTE_DB_NAME \
      --db_user $REMOTE_DB_USER \
      --db_password $REMOTE_DB_PASSWORD \
      --db_port $REMOTE_DB_PORT

# Courses
docker container exec -it wagtail-cms_web_1 python manage.py populate_courses --update

# Institutions
docker container exec -it wagtail-cms_web_1 python manage.py populate_institutions --update
```
