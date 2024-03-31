FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

RUN chmod 755 .

COPY . .
