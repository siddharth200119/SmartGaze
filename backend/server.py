from flask import Flask, request
import requests
import threading

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello World</h1>'

if __name__ =='__main__':  
    app.run(port = 8080, host='0.0.0.0')  