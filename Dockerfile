FROM python:3.11.0

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN apt-get update -y
RUN apt-get install -y libcap-dev

RUN /app/isolate/isolate-check-environment --execute

CMD ["python", "/app/sandbox.py"]
