from flask import Flask,jsonify,Response
import yaml
import MySQLdb
import MySQLdb.cursors
import json
import sys
import csv
from config import Config
from DBsingleTon import DBsingleTon 
from pyPdf import PdfFileReader,PdfFileWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

dbaccess = DBsingleTon()

def validate(values):
    vid = values['vendorid'] 
    sname = values['storename']
    sid = values['storeid']
    city = values['city']
    branch = values['branch']
    state = values['state']
    if len(str(vid))>0 :
        if len(sname)>0:
            if len(str(sid))>0:
                if len(city)>0:
                    if len(branch)>0:
                        if len(state)>0:
                            return True
                        else:
                            data = {"status":"NOT OK","message":"Please enter a valid STATE name"}
                            js = json.dumps(data)
                            resp = Response(js, status=400, mimetype='application/json')
                            return resp
                    else:
                        data = {"status":"NOT OK","message":"Please enter a valid BRANCH name"}
                        js = json.dumps(data)
                        resp = Response(js, status=400, mimetype='application/json')
                        return resp
                else:
                    data = {"status":"NOT OK","message":"Please enter a valid CITY name"}
                    js = json.dumps(data)
                    resp = Response(js, status=400, mimetype='application/json')
                    return resp
            else:
                data = {"status":"NOT OK","message":"Please enter a valid STORE ID "}
                js = json.dumps(data)
                resp = Response(js, status=400, mimetype='application/json')
                return resp    
        else:
            data = {"status":"NOT OK","message":"Please enter a valid STORE name"}
            js = json.dumps(data)
            resp = Response(js, status=400, mimetype='application/json')
            return resp
    else:
        data = {"status":"NOT OK","message":"Please enter a valid VENDOR ID"}
        js = json.dumps(data)
        resp = Response(js, status=400, mimetype='application/json')
        return resp


def check(values):
    vid = values['vendorid']
    sid = values['storeid']
    if sid == "all" or type(sid) == list:
        for store in sid :
            db = dbaccess.db_conn()
            cursor = db.cursor(buffered=True)
            cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid =%s AND storeid = %s " ,(vid,store,))
            count = cursor.rowcount
            if count == 0:
                return True
            else:
                message = json.dumps({"status":"OK","message":"This STORE ID is already registered"})
                return message
    else:
        db = dbaccess.db_conn()
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid =%s AND storeid = %s" ,(vid,sid,))
        count = cursor.rowcount       
        if count == 0:
            return True
        else:
            message = json.dumps({"status":"OK","message":"This STORE ID is already registered"})
            return message

def verify(values):
    vid = values['vendorid']
    if len(str(vid))>0:
        db = dbaccess.db_conn()
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid =%s" ,(vid,))
        count = cursor.rowcount       
        if count == 0:
            message = json.dumps({"status":"OK","message":"This ID does not exist"})
            return message
        else:
            return True


def insert(values):
    vid = values['vendorid'] 
    sname = values['storename']
    sid = values['storeid']
    city = values['city']
    branch = values['branch']
    state = values['state']
    db = dbaccess.db_conn()
    cursor = db.cursor(buffered=True)
    cursor.execute("INSERT INTO vendor(vendorid,storename,storeid,city,branch,state)VALUES(%s,%s,%s,%s,%s,%s)",(vid,sname,sid,city,branch,state))
    db.commit()
    message = json.dumps({"status":"OK","message":"SIGN IN SUCCESS"})
    return message


def fetch(data):
    vid = data['vendorid']
    if len(str(vid))>0:
        db = dbaccess.db_conn()
        cursor = db.cursor(buffered=True,dictionary=True)
        cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s  ",(vid,)) 
        rows = cursor.fetchall()
        s={}
        d={}
        cnt=0
        for row in rows:
            d = {key: value for (key, value) in row.items()}
            s[row['storeid']]=d
            cnt=cnt+1
        #print json.dumps(s)
        return json.dumps(s)
    else:
        data = {"status":"NOT OK","message":"Please enter a valid VendorID"}
        js = json.dumps(data)
        resp = Response(js, status=400, mimetype='application/json')
        return resp



def fetchone(datas):
    vid=datas['vendorid']
    sid=datas['storeid']
    if len(str(vid))>0 and len(str(sid))>0:
        if type(datas['storeid'])==list:
            value = datas['storeid']
            count=0
            s={}
            d={}
            for sid in value:
                if len(str(sid))>0:
                    print vid,sid
                    db = dbaccess.db_conn()
                    cursor=db.cursor(buffered=True,dictionary=True)
                    cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s AND storeid =%s",(vid,sid,))
                    row = cursor.fetchone()
                    #print count
                    if row == None:
                        pass
                    else:
                        d = {key: value for (key, value) in row.items()}
                        s[row['storeid']]=d
                        print s
                        count+=1
                else:
                    data = {"status":"NOT OK","message":"Please enter a valid Store ID"}
                    js = json.dumps(data)
                    resp = Response(js, status=400, mimetype='application/json')
                    return resp

            return json.dumps(s)

        else:
            sid = datas['storeid']
            #print vid,type(sid)
            db = dbaccess.db_conn()
            cursor=db.cursor(buffered=True,dictionary=True)
            cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s AND storeid =%s",(vid,sid))
            row = cursor.fetchone()
            #print row
            name = json.dumps(row)
            return name
    else:
        data = {"status":"NOT OK","message":"Please enter a valid VendorID"}
        js = json.dumps(data)
        resp = Response(js, status=400, mimetype='application/json')
        return resp


        
def update(values):
    vid = values['vendorid']
    sname = values['storename']
    sid = values['storeid']
    city = values['city']
    branch = values['branch']
    state = values['state']
    db = dbaccess.db_conn()
    cursor = db.cursor(buffered=True)
    cursor.execute("UPDATE vendor SET storename=%s,city=%s,branch=%s,state=%s WHERE vendorid=%s AND storeid=%s",(sname,city,branch,state,vid,sid)) 
    db.commit()
    message = json.dumps({"status":"OK","message":"UPDATED SUCCESSFULLY"})
    return message


def delete(value):
    vid = value['vendorid']
    if type(value['storeid'])==list:
        c=len((value['storeid']))
        print c
        count=0
        while count <c : 
            print count ,c
            sid = value['storeid'][count]
            #print sid
            db = dbaccess.db_conn()
            cursor=db.cursor(buffered=True)
            cursor.execute("DELETE FROM vendor WHERE vendorid=%s AND storeid=%s",(vid,sid,))
            db.commit()
            count+=1
        return True

    else:
        sid = value['storeid']
        db = dbaccess.db_conn()
        cursor=db.cursor(buffered=True)
        cursor.execute("DELETE FROM vendor WHERE vendorid=%s AND storeid = %s " ,(vid,sid,))
        db.commit()
        return True

def excelsheet(value):
    vid = value['vendorid']
    db = dbaccess.db_conn()
    cursor=db.cursor(buffered=True,dictionary=True)
    cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s", (vid,))
    result=cursor.fetchall()
    if result != None: 
        fp = open('sheet.csv', 'w')
        myFile = csv.writer(fp, lineterminator='\n')
        myFile.writerows([result[0].keys()])
        for row in result:
            myFile.writerows([row.values()])
        fp.close()
        return True

def pdf(value):
    vid = value['vendorid']
    doc = SimpleDocTemplate("details.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    doc.pagesize = landscape(A4)
    magName = "Store Details "
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.black),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.black),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])
    db = dbaccess.db_conn()
    cursor=db.cursor(buffered=True,dictionary=True)
    cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s ", (vid,))
    result=cursor.fetchall()
    #content = file("list.pdf","wb")
    elements=[]
    elements.append(Paragraph(magName, styles["Justify"]))
    values=[]
    values.append(result[0].keys())
    for row in result:
        values.append(row.values())
    #print type(values)
    sheet = getSampleStyleSheet()
    sheet = sheet["BodyText"]
    sheet.wordWrap = 'CJK'
    table=Table(values, hAlign='CENTER')
    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    output = PdfFileWriter() 
    input1 = PdfFileReader(file("details.pdf", "rb")) 
    print "title = %s" % (input1.getDocumentInfo().title)
    page1 = input1.getPage(0)
    watermark = PdfFileReader(file("sample.pdf", "rb"))
    page1.mergePage(watermark.getPage(0))
    output.addPage(page1)
    print "watermarked_pdf.pdf has %s pages." % input1.getNumPages()
    outputStream = file("details.pdf", "wb") 
    output.write(outputStream) 
    outputStream.close()
    return True

