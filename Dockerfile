FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code
RUN apt-get install libffi-dev libssl-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /code/