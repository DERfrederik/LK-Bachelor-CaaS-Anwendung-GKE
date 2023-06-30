#Basis Image
FROM python:3.11

#Working directory festlegen vom container  (Man kann WORKDIR mehrmals verwenden)
WORKDIR /backend/src  

# kopiert das Pipfile im backend ordner
COPY ./Pipfile ./Pipfile.lock /backend/

# pipenv installieren
RUN pip install pipenv

# Pipfile installieren
RUN /bin/bash -c "pipenv install --deploy --ignore-pipfile"

# Überschreiben der Enviroment Variablen machen wir jetzt in docker-compose
RUN echo 'AQIN_KEY = "e6e52e8fc683d9fcc03235abe9db9d8bc101230b"\nUmweltstationID = "6143"' > '.env'

# pipenv run, da pipenv shell nicht geht + Starten des Servers "--host", "0.0.0.0" lässt alle IPS zu
# ENTRYPOINT ["pipenv", "run", "uvicorn", "rest_api:app"]

# Default Parameter, könnten beim Aufruf überschrieben werden. z.B: docker run backend:latest --host '127.0.0.1' --port '5000' --host 0.0.0.0 heißt dass auf allen IPs gelauscht wird
# CMD ["pipenv", "run", "uvicorn", "rest_api:app", "--host", "0.0.0.0", "--port", "20000"]

# Container am laufen halten
# CMD [ "sleep", "infinity" ]

# Debuggen
# CMD ["pipenv", "run", "python3", "logik.py"]

# Prod
CMD ["../start.sh" ]
