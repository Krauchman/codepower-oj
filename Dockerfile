FROM python:3.11.0

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN apt-get update -y
# RUN sudo apt-get install -y libcap-dev
CMD apt-get install -y libcap-dev

# RUN make /app/isolate/isolate
# # RUN /app/isolate/isolate-check-environment --execute

# # CMD ["python", "/app/sandbox.py"]
# CMD ls /app/isolate/
