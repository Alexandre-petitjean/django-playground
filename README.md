# Django Playground

> This app is not meant to be used in production, it's just a playground to test Django feature or create POC.


[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![python](https://img.shields.io/badge/Python-3.12.5-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Django](https://img.shields.io/badge/5.0.9-green?logo=django&label=Django&labelColor=grey&color=%23092E20)](https://www.python.org)


License: MIT

## Introduction

### Features

// TODO

### Technologies and tools used in this project

* [poetry](https://python-poetry.org/) as package manager.
* [pyenv](https://github.com/pyenv/pyenv) to manage python versions.
* [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage virtual environments.
* [docker](https://www.docker.com/) to run the project in a container.
* [docker-compose](https://docs.docker.com/compose/) to manage multiple containers.
* [pre-commit](https://pre-commit.com/) to run linters and formatters before commiting.

## Installation

### 1. Install OS dependencies


#### Ubuntu
```bash
sudo apt-get install -y build-essential curl graphviz graphviz-dev
```

#### MacOS

// TODO

### 1. Create a virtual environment

> It's recommended to use a virtual environment to avoid conflicts with other projects.




## Add a feature

// TODO

## Contributing

// TODO

```bash
python -m venv venv
```






## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy django_playground

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
