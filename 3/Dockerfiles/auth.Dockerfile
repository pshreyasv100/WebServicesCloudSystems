FROM python:3.7-alpine

WORKDIR /code

ENV FLASK_APP=authentication_service.py

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5001

COPY authentication_service.py .
COPY authentication.py .

# allow requests from any host
CMD ["flask", "run", "--host=0.0.0.0"]