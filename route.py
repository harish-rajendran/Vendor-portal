from flask import Flask,request
import requests
from flask_cors import CORS, cross_origin
import json

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

@application.route('/test/signup')
@cross_origin()
def signup():
    url = 'http://localhost:5002/vendor/signup/'
    d = {'vendorid' :'1' ,'storename' : 'MAD','storeid' : '200','city' : 'Chennai','branch' : 'Race Club','state' : 'TamilNadu'}
    head = {'Content-Type' : 'application/json'}
    r=requests.post(url, data=json.dumps(d), headers=head) 
    return r.text
    

@application.route('/test/details')
@cross_origin()
def info():
    url = 'http://localhost:5002/vendor/details/'
    d = {'vendorid' : 1 ,'storeid' : "all" }
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/update')
@cross_origin()
def update():
    url = 'http://localhost:5002/vendor/details/update/'
    d = {'vendorid' : 1 ,'storename' : 'grey','storeid' : 5200,'city' : 'Chennai','branch' : 'Poes','state' : 'Tamilnadu'}
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/delete')
@cross_origin()
def delete():
    url = 'http://localhost:5002/vendor/details/delete/'
    d = {'vendorid' : 1 ,'storeid' : 2200 }
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/downloadcsv')
@cross_origin()
def downloadcsv():
    url = 'http://localhost:5002/vendor/downloadcsv/'
    d = {'vendorid' : 1 }
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/downloadpdf')
@cross_origin()
def downloadpdf():
    url = 'http://localhost:5002/vendor/downloadpdf/'
    d = {'vendorid' : 1  }
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text


if __name__ == "__main__":
    application.debug = True
    application.run(host = "0.0.0.0", port = 5004)
