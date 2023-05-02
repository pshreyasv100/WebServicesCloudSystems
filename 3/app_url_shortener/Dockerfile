FROM python:3.7-alpine
WORKDIR /code

ENV FLASK_APP=urlshortener_service.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
COPY urlshortener_service.py .

#  allow requests from any host
CMD ["flask", "run"]