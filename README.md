# scq
Our main repo for the SCQ senior project.

## Installing:

Make sure you have python3 and [gulp](https://github.com/gulpjs/gulp/blob/master/docs/getting-started.md) installed on your computer. Then run:

```
make build
```

This will install all of the pip modules as well as the

## Running:

To run the server, make sure you have rethinkDB is up.

```
make serve
```

## Installing (Hard Way):
We are using virtual environments to manage our dependencies and make sure they are the same between dev environments. If you don't have a virtualenv setup for this project, this is how to do it.

To setup virtualenvs in general on your computer, do the following:
```
brew install nodejs
sudo easy_install pip
sudo pip install virtualenvwrapper
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
```

To setup our specific environment:
```
mkvirtualenv scq
```

Whenever you are going to work on the project to ensure that we are all using the same dependencies:
```
workon scq
```

Add the following to ~/.bashrc (or zshrc if you use one):

```
export WORKON_HOME=$HOME/Envs
source /usr/local/bin/virtualenvwrapper.sh
```

Then source it (bashrc example below):
```
source ~/.bashrc
```

Then go to the project and run this command in your project directory to install the dependencies.
```
make build
```
you will likely be asked for sudo privileges to install all needed packages

## Install [rethinkdb]( https://rethinkdb.com/docs/install/):

On Mac:

```
brew update && brew install rethinkdb
```

[On Linux](https://www.rethinkdb.com/docs/install/ubuntu/):

Copy and past the entire codeblock:

```
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```

## API

### List user information
*Test: PASS*
```
GET /api/me
```
**Response:**

| Status: 200 OK                                                      |
|---------------------------------------------------------------------|
| {                                                                   |
|    "answers": [],                                                   |
|    "last_sign_in": 1456035511.3893418,                              |
|    "id": "7423c6be-2ce7-4f9a-882e-1130d21cf52b",                    |
|    "major3": "",                                                    |
|    "date_registered": 1455754947.062986,                            |
|    "gender": "Female",                                              |
|    "created_surveys": ["d8e70e63-12bd-46b7-bd0e-a9758bc632fd"],     |
|    "native_language": "English",                                    |
|    "unanswered_surveys": ["d8e70e63-12bd-46b7-bd0e-a9758bc632fd"],  |
|    "email": "sung.bae@colorado.edu",                                |
|    "survey_responses": [],                                          |
|    "dob": "2016-02-03",                                             |
|    "status": "Senior",                                              |
|    "answered_surveys": [],                                          |
|    "courses": ["1c406ea0-6b4a-437f-acc6-372e4a37ac6f"],             |
|    "courses_taught": [],                                            |
|    "ethnicity": "American Indian or Alaska Native",                 |
|    "major2": "Mathematics",                                         |
|    "accepted_tos": true,                                            |
|    "minor1": "",                                                    |
|    "departments": ["Computer Science"],                             |
|    "major4": "",                                                    |
|    "major1": "",                                                    |
|    "username": "suba8204",                                          |
|    "primary_affiliation": ["Student"],                              |
|    "minor2": "",                                                    |
|    "registration": "registration_culdap"                            |
| }                                                                   |

### Change user information
*Test: PASS*
```
POST /api/me
```
**Parameter:**

| Field               | Type          | Description                                                       |
| ------------------- |:-------------:| -----------------------------------------------------------------:|
| email               | String        | User's email must be Colorado domain (i.e. user@colorado.edu).    |
| status              | String        | User's academic year (i.e. Freshman, Sophomore, Junior, Senior).  |
| dob                 | String        | User's date of birth.                                             |
| native_language     | String        | User's native language.                                           |
| gender              | String        | User's gender.                                                    |
| ethnicity           | String        | User's, ethnicity.                                                |
| major1              | String        | User's first major.                                               |
| major2              | String        | User's second major.                                              |
| major3              | String        | User's third major.                                               |
| major4              | String        | User's fourth major.                                              |
| minor1              | String        | User's first minor.                                               |
| minor2              | String        | User's second minor.                                              |
| departments         | String[]      | User's departments.                                               |
| courses             | String[]      | Courses taken by user.                                            |
| courses_taught      | String[]      | Courses taught by user.                                           |
| primary_affiliation | String[]      | User's affiliation to CU (i.e. Student, Faculty, Student/Faulty). |

**Response:**

### Display surveys taken by user
*Test: FAIL*
```
GET /api/surveys
```
**Response:**

### Create/update user's survey questions.
*Test: IDK*
```
POST /api/surveys
```
**Parameter:**
######Take a look at schema/sampleSurvey.json for reference.

**Response:**

### Create/update user's response to a survey
*Test: IDK*
```
POST /api/response
```
**Parameter:**

**Response:**

### Refresh user's cookie
*Test: PASS*
```
GET /api/refresh
```
**Response:**

| Status: 200 OK |
| -------------- |
