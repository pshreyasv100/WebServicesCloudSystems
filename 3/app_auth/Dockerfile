FROM python:3.7-alpine

WORKDIR /code


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5001

ENV FLASK_APP=authentication_service.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

COPY authentication_service.py .
COPY authentication.py .


CMD ["python3", "-m", "flask", "run"]

# References
# https://stackoverflow.com/questions/67506827/error-connect-econnrefused-127-0-0-15000-or-error-socket-hang-up-after-get-re
# https://docs.docker.com/language/python/build-images/