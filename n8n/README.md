# FinBot - Proof of Concept (POC)

This project demonstrates a Proof of Concept (POC) for using the [n8n](https://n8n.io/) platform to send an email to a user. The POC includes a Python script that collects user information and sends it to an n8n webhook, which processes the data and triggers an email.

## Features

- Collects user name and age via a Python script.
- Sends the collected data to an n8n webhook.
- n8n processes the data and sends an email to the user.

## Prerequisites

- [n8n](https://n8n.io/) installed and running locally or on a server.
- Python 3.8+ installed.
- Required Python dependencies (see `requirements.txt`).
- Docker
- Docker Compose

# n8n with PostgreSQL

Starts n8n with PostgreSQL as database.

## Start

To start n8n with PostgreSQL simply start docker-compose by executing the following
command in the current folder.

**IMPORTANT:** But before you do that change the default users and passwords in the [`.env`](.env) file!

```
docker-compose up -d
```

To stop it execute:

```
docker-compose stop
```

## Configuration

The default name of the database, user and password for PostgreSQL can be changed in the [`.env`](.env) file in the current directory.


## Installation

1. Clone this repository:

        git clone https://github.com/your-repo/finbot.git
        cd finbot
        python3 test.py

        {{ name }}
        {{ age }}
        {{ city }}
        {{ state }}

After that an email is send to annia_sebold@ufms.br informing that register is Approved or Not Approved.