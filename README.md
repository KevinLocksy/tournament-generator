# Tournament generator

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Linting , formatting, imports sorting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Django](https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white)](#)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)

First sketch of rebuilding the website https://engarde-service.com/tournament/era/sem_es_24 to have a free version of a tournament generator, and tournament displayer.

## Table of contents
- [Documentation](#documentation)
- [Getting Started](#getting-started)
  - [Requirements](#Requirements)
  - [Installation](#installation)
  - [Demonstration](#demonstration)
  - [Unit Tests](#unit-tests)

## Documentation
The web application is made of 3 django apps:
- authentication: manages authentificated users to the webapp
- tournaments: manages tournaments' creation
- users: manages competitors and referees

A tournament is composed of different stages: optionnal pool phases, and knock-out phase.

It exists three types of users: Competitor, Referee, Fencer (not used yet)

To register a new referee, you will have to connect to an account you've created through the sign up page or to the following superaccount:
|Login|Password|
|--|--|
|admin | Welcome1|

## Getting Started
### Requirements
For manual installation, the web application requires the following:
- Python >=3.8
- Django >=3.2
- Ruff >=0.7.2

### Installation

Clone the project
```sh
git clone https://github.com/KevinLocksy/tournament-generator.git
```
Install the dependencies
```sh
poetry install 
```
If poetry is not installed, run the following command:
```sh
pipx install poetry
```


### Demonstration



```sh
python manage.py runserver
```

Open in a browser the web application. The default one is http://localhost:8000/

### Unit Tests

To run tests, after having install launch the following command line:
```sh
python manage.py test
```
