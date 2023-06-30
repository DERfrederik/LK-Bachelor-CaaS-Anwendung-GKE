#!/bin/bash

pipenv run python3 logik.py &
pipenv run uvicorn rest_api:app --host 0.0.0.0 --port 20000 --reload

