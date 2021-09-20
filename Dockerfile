FROM python:3.6

WORKDIR /instNir/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000