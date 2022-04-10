from django.http import HttpResponseRedirect
from django.shortcuts import render

def login_access(request):
    msg=None

    if request.method == 'POST':
        name=request.POST["name"]
        mp=request.POST["pass"]
        data=__get_database()
        try :
            if data[name] == mp:
                msg="Success"
            else:
                msg="Wrong pass"
        except:
            msg="Wrong Name"
    
    response = render(request, "login.html",{"Success":f"{msg}"})
    
    if msg == "Success":
        response.set_cookie("username",name)
        response.set_cookie("log_statut",True)
    
    if "log_statut" not in request.COOKIES:
        return response
    elif str(request.COOKIES["log_statut"]) == "False":
        return response
    else:
        return HttpResponseRedirect("../")

def __get_database():
    file=open("login1/database.txt","r")
    result={}
    for line in file.read().split('\n'):
        c=line.split(":")
        try:
            result[c[0]] = c[1]
        except:pass
    file.close()
    print(result)
    return result

def home(request):

    if "log_statut" in request.COOKIES:
        if "username" in request.COOKIES:
           context = {
                "log_statut": request.COOKIES["log_statut"],
                "username": request.COOKIES["username"]
            } 
    else :
        context = {
            "log_statut": False,
            "username": None
        }
    print(context)
    return render(request, "home.html", context)

def unlog(request):
    response = render(request, "login.html")
    response.delete_cookie("username")
    response.delete_cookie("log_statut")
    return response