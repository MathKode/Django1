from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import hashlib
import random
import time

def login_page(request):
    __token_time()
    if request.method == "GET":
        return render(request, "login.html")
    else:
        name=request.POST["name"]
        password=request.POST["password"]
        if __check_login(name,password):
            print("Good Login")
            #response=render(request, "home.html")
            response = HttpResponseRedirect("../home")
            response.set_cookie("username",name)
            response.set_cookie("token", __get_token(name))
            return response
        else:
            return render(request, "login.html", {"msg":"Mauvais Log-in"})

def home_page(request):
    __token_time()
    try:
        name=request.COOKIES['username']
        token=request.COOKIES['token']
        if __check_token(name,token):
            print("ALLOW")
            if request.method == "GET":
                try:
                    name_del = request.GET["delete"]
                    __delete_contact(name,name_del)
                except: pass
                try:
                    nb_select=int(request.GET["contact_nb"])
                except:
                    nb_select=0
                #print("nb select", nb_select)
                #people=[["Math","C'est moi"],["Jean","Mon père"]]
                people=__get_contact(str(name))
                people.append(["New","","","",""])
                #print(people)
                select=people[nb_select]
                context={"people": people,
                        "name":select[0],
                        "lname":select[1],
                        "phone":select[2],
                        "mail":select[3],
                        "des":select[4]
                }
                #print(context)
                try:
                    return render(request, "home.html",context)
                except Exception as e:
                    print(e)
            elif request.method == "POST":
                re_name=request.POST["name"]
                re_lname=request.POST["lastname"]
                re_phone=request.POST["phone"]
                re_mail=request.POST["email"]
                re_des=request.POST["des"]
                l=[re_name, re_lname, re_phone, re_mail, re_des]
                print(l)
                result=[]
                find=False
                for contact in __get_contact(name):
                    if contact[0] == re_name:
                        result.append(l)
                        find=True
                    else:
                        result.append(contact)
                if not find:
                    result.append(l)
                print(result)
                __update_contact(name,result)
                return HttpResponseRedirect("../home")

    except: pass
    return HttpResponseRedirect("../login")

def register_page(request):
    if request.method == "GET":
        return render(request,"register.html")
    else:
        name=request.POST["name"]
        mp1=request.POST["password"]
        mp2=request.POST["password2"]
        if mp1 != mp2:
            return render(request, "register.html", {"msg":"Enter the same pass"})
        elif __user_exist(name):
            return render(request, "register.html", {"msg":"Username is already used"})
        elif len(name.split(":%:")) != 1:
            return render(request, "register.html", {"msg":":%: isn't accept"})
        else:
            state = __create_user(name,mp1)
            if state:
                return HttpResponseRedirect("../login")
            else:
                return render(request, "register.html", {"msg":"Erreur Create User"})

def logout_page(request):
    reponse = render(request, "logout.html")
    reponse.delete_cookie("token")
    reponse.delete_cookie("username")
    return reponse

def __create_user(username,password):
    try:
        file=open("database.txt","r")
        data=[]
        for i in file.read().split("\n"):
            data.append(i)
        file.close()
        data.append(f"{username}:%:{password}")
        file=open("database.txt","w")
        file.write("\n".join(data))
        file.close()
        __generate_token(username)
        return True
    except:
        return False

def __user_exist(username):
    file=open("database.txt","r")
    find=False
    for i in file.read().split("\n"):
        c=i.split(":%:")
        try :
            if str(c[0]) == username:
                find=True
        except:pass
    return find

def __check_login(username,password):
    file=open("database.txt","r")
    for i in file.read().split('\n'):
        c=i.split(":%:")
        print(c)
        if c[0]==username:
            if c[1]==password:
                return True
            else:
                return False
    return False

def __check_token(username,token):
    #database
    #<USER>:%:<MP>:%:<TOKEN>:%:<TOKEN-END>
    file=open("database.txt","r")
    for i in file.read().split('\n'):
        c=i.split(":%:")
        if c[0]==username:
            if c[2]==token:
                return True
            else:
                return False
    return False

def __token_time():
    file=open("database.txt","r")
    for i in file.read().split('\n'):
        c=i.split(":%:")
        try:
            if int(c[3]) < int(time.time()):
                tk = __generate_token(c[0]) 
        except:pass

def __get_token(username):
    file=open("database.txt","r")
    tk=""
    for i in file.read().split('\n'):
        c=i.split(":%:")
        if c[0]==username:
            try:
                tk=c[2]
            except:pass
    if tk != "":
        print("TK:",tk)
        return tk
    else:
        return __generate_token(username)

def __generate_token(username):
    tk = hashlib.md5((str(username) + str(random.randint(0,100000))).encode()).hexdigest()
    content={}
    file=open("database.txt","r")
    for i in file.read().split('\n'):
        c=i.split(":%:")
        if len(c) != 0:
            content[c[0]] = c[1:]
    file.close()
    ls = content[username]
    try :
        del ls[1]
        del ls[1]
    except: pass
    ls.insert(1, str(tk))
    ls.insert(2, str(int(time.time())+90))
    content[username] = ls
    #print(content)
    file=open("database.txt","w")
    r=[]
    for key in content:
        y=content[key]
        #print(y)
        y.insert(0,key)
        #print(y)
        line= ":%:".join(y)
        r.append(line)
    file.write("\n".join(r))
    return tk

def __get_contact(username):
    file=open("database.txt") # <USER> <PASS> <TOKEN> <END> <CONTACT>
                              #                             name%)%lname%)%phone%)%mail%)%description                         
    for p in file.read().split("\n"):
        c=p.split(":%:")
        if c[0] == username:
            result=[]
            try:
                for j in c[4:]:
                    result.append(j.split("%)%"))
                return result
            except:pass
    return None

def __update_contact(username, contact_ls):
    #contact_ls = [ [name, lname, phone, mail, des], [...] ...]
    if True:
        file=open("database.txt","r")
        data=[]
        for i in file.read().split("\n"):
            c=i.split(":%:")
            if str(c[0]) == str(username):
                l=[]
                for i in range(4): l.append(c[i])
                for i in contact_ls:
                    l.append("%)%".join(i))
                data.append(":%:".join(l))
            else:
                data.append(":%:".join(c))
        file.close()
        print(data)
        file=open("database.txt","w")
        file.write("\n".join(data))
        file.close()
        return True

def __delete_contact(username, user_del):
    contact_ls = __get_contact(username)
    r=[]
    for i in contact_ls:
        if i[0] != user_del:
            r.append(i)
    __update_contact(username,r)

if __name__=="__main__":
    s=__update_contact("mathis",[["mathis","kremer","","bimathax.STUDIO@gmail.com","C'est moi"], ["James","Bond","007","james@gmx.fr","Urgence only"]])
    print(__get_contact("mathis"))