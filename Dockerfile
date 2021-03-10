FROM python:3.9

CMD ["python","octo.py"]

WORKDIR /opt/app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY octo.py .
EXPOSE 80
