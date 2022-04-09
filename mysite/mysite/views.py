from unittest import result
from django.core.files.storage import FileSystemStorage
import EXCELCODE as EXCELCODE
from django.http import HttpResponse
from django.shortcuts import render
import datetime
import os

def index(request):
    date=datetime.datetime.today()
    State=""
    
    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if str(myfile.name).split(".")[-1] == "csv":
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print("Filename :",filename)
            EXCELCODE.main(f"{filename}","equipment.csv","1")
            with open("media/1.xlsx",'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename("media/1.xlsx")
                return response
    
    return render(request, "homepage.html",context={"TODAY": date, "STATE": State})
    #return HttpResponse("ok")

def equipment(request):
    try:
        file=open("equipment.csv","r")
        c=file.read().split("\n")
        file.close()
        result=[]
        for i in c:
            if i != "":
                result.append(i.split(";"))
    except:
        result=[["None"]]
    return render(request, "equipment.html",context={"data":result})


def data_upgrade(request):
    try:
        file=open("equipment.csv","r")
        c=file.read().split("\n")
        file.close()
        result=[]
        for i in c:
            if i != "":
                result.append(i.split(";"))
    except:
        result=[]
    result.append([request.GET["first"],request.GET["second"],request.GET["third"]])
    __write_equipment(result)
    return render(request, "equipment.html",context={"data":result})

def equipment_update(request):
    data = dict(request.GET)
    result=[]
    for key in data:
        t=0
        for el in data[key]:
            if len(result) <= t:
                result.append([el])
            else:
                old = result[t]
                old.append(el)
                result[t] = old
            t += 1
    #Traiter la liste
    #SI 1 VIDE MINIMUM ALORS DELETE
    r=[]
    for line in result:
        find=False
        for i in line:
            if i == "":
                find = True
        if not find:
            r.append(line)
    __write_equipment(r)
    return render(request, "equipment.html",context={"data":r})

def __write_equipment(result):
    line=[]
    for i in result:
        line.append(";".join(i))
    file=open("equipment.csv","w")
    file.write("\n".join(line))
    file.close()

def home_test(request):
    html="Please <a href=../formtest>Introduce Yourself</a>"
    return HttpResponse(html)

def getData(request):
    return render(request, "form_sample.html", context={"name": None})

def showResult(request):
    nm1 = request.GET['fname']
    nm2 = request.GET['lname']
    nm = nm1 + " " + nm2
    return render(request, "form_sample.html", context={"name": nm})