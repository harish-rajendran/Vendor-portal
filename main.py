from flask import Flask,request,Response
from flask_api import status
from flask_cors import CORS, cross_origin
import json
import operation


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/vendor/signup/' , methods=['POST'])
@cross_origin()
def signup():
    if request.method == 'POST':
        values = request.get_json()
        result = operation.validate(values)
        if result == True:
            results = operation.check(values)
            if results == True:
                message=operation.insert(values)
                return message
            else:
                message = json.dumps({"status":"NOT OK","message":"A Store is already registered in this name!"})
                return message
        else:
            return result
             

@app.route('/vendor/details/')
@cross_origin()
def info():
    data = request.get_json()
    if len(str(data['storeid']))>0 and len(str(data['vendorid']))>0 :
        if data['storeid'] == "all":
            #final = operation.check(data)
            #if final != True:
            result = operation.fetch(data)
            if result != False:
                return result
        else:
            #final = operation.check(data)
            #if final != True :
            result = operation.fetchone(data)
            if result != False:
                return result
    else:
        data = {"status":"NOT OK","message":"Please enter a valid STORE ID and VENDOR ID"}
        js = json.dumps(data)
        resp = Response(js, status=400, mimetype='application/json')
        return resp  

@app.route('/vendor/details/update/')
@cross_origin()
def edit():
    value = request.get_json()
    result = operation.validate(value)
    if result == True:
        final = operation.check(value)
        if final != True:
            solution = operation.update(value)
            return solution
        else:
            message = json.dumps({"status":"OK","message":"Store does not exist"})
            return message
    else:
        return result

@app.route('/vendor/details/delete/')
@cross_origin()
def dele():
    values = request.get_json()
    vid = values['vendorid'] 
    sid = values['storeid']
    if len(str(vid))>0 and len(str(sid))>0:
        #final = operation.check(values)
        #if final == True:
        result = operation.delete(values)
        if result == True:
            message = json.dumps({"status":"OK","message":"DELETED SUCCESSFULLY"})
            return message
    else:
        data = {"status":"NOT OK","message":"Please enter a valid VENDOR ID and STORE ID"}
        js = json.dumps(data)
        resp = Response(js, status=400, mimetype='application/json')
        return resp

@cross_origin()
@app.route('/vendor/downloadcsv/')
def downloadexcel():
    values = request.get_json()
    vid = values['vendorid'] 
    if len(str(vid))>0 :
        final = operation.verify(values)
        if final == True :
            result = operation.excelsheet(values)
            if result == True:
                message = json.dumps({"status":"OK","message":"CSV FILE CREATED SUCCESSFULLY"})
                return message
        else:
            message = json.dumps({"status":"OK","message":"Store does not exist"})
            return message
    else:
        data = {"status":"NOT OK","message":"Please enter a valid VENDOR ID"}
        js = json.dumps(data)
        resp = Response(js, status=400, mimetype='application/json')
        return resp

@cross_origin()
@app.route('/vendor/downloadpdf/')
def pdf():
    values = request.get_json()
    vid = values['vendorid'] 
    if len(str(vid))>0 :
        final = operation.verify(values)
        if final == True:
            result = operation.pdf(values)
            if result == True:
                message = json.dumps({"status":"OK","message":"PDF FILE CREATED SUCCESSFULLY"})
                return message
        else:
            message = json.dumps({"status":"OK","message":"Store does not exist"})
            return message
    else:
        data = {"status":"NOT OK","message":"Please enter a valid VENDOR ID"}
        js = json.dumps(data)
        resp = Response(js, status=400, mimetype='application/json')
        return resp


if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5002)

