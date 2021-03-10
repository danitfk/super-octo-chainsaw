#!/usr/bin/python3
import flask
import os

counter = 0
csv_file = "/tmp/test.csv"
app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.route('/get', methods=['GET'])
def home():
    global counter
    counter = counter + 1
    return chap(counter)
def chap(i):
    with open(csv_file) as file:
        array = file.readlines()
    if len(array) > i:
        return array[i]
    os._exit(0)
@app.route('/ready', methods=['GET'])
def status():
    global csv_file
    if os.path.exists(csv_file):
        return 'Ready'
app.run(host='0.0.0.0', port=80)
