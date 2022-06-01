from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
import random
import time
import os

def home_page(request):
    check_time()
    if request.method == "GET" :
        return render(request, "homepage.html", {})

def picture(resquest, picture_name):
    with open(f"./urbex_share/picture/{picture_name}.png", "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")

def trade(request, trade_id):
    check_time()
    print("trade id :",trade_id)

    #Get the user
    try:
        user=int(request.COOKIES[f"{trade_id}"])
    except:
        user=2
    
    #Get the id list
    try:
        file = open("trade.txt","r")
        c = file.read().split("\n") # c = ["<ID>:::<GEO1>:::<GEO2>:::<TIME>"]
        c = delete_empty(c)
        file.close()
        id_exist = []
        ls = []
        for i in c:
            id_exist.append(i.split(':::')[0])
            ls.append(i.split(":::"))
    except:
        c = []
        id_exist = []
        ls = []
    
    #Not found
    if str(trade_id) not in str(id_exist):
        return render(request,"trade_notfound.html", {})

    #Check que c'est un post
    if request.method == "POST":
        rep = trade_post(request, trade_id,ls,user)
        return rep
    
    #Check que c'est pas un ok
    if request.method == "GET":
        work = False
        try:
            trade_state = request.GET["trade"]
            user_uid = request.GET["user_uid"]
            work = True
        except:pass

        if work:
            current_uid = get_uid(trade_id)[user-1]
            if str(current_uid) == str(user_uid):
                if str(trade_state) == "yes":
                    allow_add(trade_id,user)
                    trade_is_ok = allow_check(trade_id)
                    if trade_is_ok:
                        #Genere l'image
                        geoloc1 = ""
                        geoloc2 = ""
                        for i in ls:
                            if str(i[0]) == str(trade_id):
                                geoloc1 = i[1]
                                geoloc2 = i[2]
                        result_img(geoloc1,geoloc2,trade_id + trade_id)
                        print("Image Result trade ",trade_id," générée")
                        

    #Get la geoloc pour l'utilisateur (1 ou 2)
    for i in ls:
        if str(i[0]) == str(trade_id):
            if user == 1:
                geoloc = str(i[1])
            else :
                geoloc = str(i[2])

    #Trouve user uid
    uid = get_uid(trade_id)
    print("Trade",trade_id, "uid",uid)
    user_uid = uid[user-1]

    return render(request,"trade_sample.html",context={"USER_ID":f"{str(user)}", "USER_GEOLOC" : f"{geoloc}", "TRADE_ID" : f"{trade_id}", "USER_UID": f"{user_uid}"})

def trade_post(request,trade_id,ls,user):
    #Fonction appelé lorsqu'un utilisateur à complété ses coordonnées
    new_geoloc = request.POST["geoloc"]
    try:
        user=int(request.COOKIES[f"{trade_id}"])
    except:
        user=2
    result=[]
    for i in ls:
        if str(i[0]) == str(trade_id):
            i[user] = str(new_geoloc)
        result.append(":::".join(i))
    file = open("trade.txt","w")
    file.write("\n".join(result))
    file.close()

    #Geoloc picture
    try:
        loc = new_geoloc.split(",")
        x=float(loc[0])
        y=float(loc[1])
        print(x,y)
        geoloc_picture([x,y],f"{trade_id}{user}")
    except:
        print("ERREUR GEOLOC")
    #Trouve user uid
    uid = get_uid(trade_id)
    user_uid = uid[user-1]

    return render(request,"trade_sample.html",context={"USER_ID":f"{str(user)}", "USER_GEOLOC" : f"{new_geoloc}", "TRADE_ID" : f"{trade_id}",  "USER_UID": f"{user_uid}"})

def result_img(c1,c2,name):
    x=max([len(c1),len(c2)])*30
    mode="RGB"
    size=(x,135)
    color=(255,33,33)
    img = Image.new(mode,size,color)
    __draw_text(img,c1,int(x/2),30,0,40)
    __draw_text(img,c2,int(x/2),100,0,40)
    img.save(f"urbex_share/picture/{name}.png")

def __draw_text(img,text,x,y,space,size):
    img1 = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", size)
    d=font.getsize(text)
    img1.text((x+((space-d[0])/2),((y+(space-d[1])/2))),text,align="left",font=font)

def allow_add(trade_id,user):
    #Allow file :
    # <TRADE_ID>:no:no
    file = open("allow.txt","r")
    c = file.read().split("\n")
    file.close()
    new=[]
    for i in c:
        r = i.split(":")
        if str(r[0]) == str(trade_id):
            if str(user) == "1":
                r[1] = "yes"
            else :
                r[2] = "yes"
            new.append(":".join(r))
        elif i != '':
            new.append(i)
    file = open("allow.txt","w")
    file.write("\n".join(new)) 
    file.close()

def allow_init(trade_id):
    #Lors de la création d'un trade
    file = open("allow.txt","r")
    c = file.read().split("\n")
    file.close()
    new=[]
    for i in c:
        r = i.split(":")
        if r[0] != trade_id and i != '':
            new.append(i)
    new.append(f"{trade_id}:no:no")
    file = open("allow.txt","w")
    file.write("\n".join(new)) 
    file.close()

def allow_check(trade_id):
    #Check si le trade est ok
    #retourne True ou False
    file = open("allow.txt","r")
    c = file.read().split("\n")
    file.close()
    for i in c:
        r = i.split(":")
        if r[0] == trade_id:
            if r[1] == "yes" and r[2] == "yes":
                return True
            else :
                return False
    return False

def geoloc_picture(geoloc,name):
    #Get a picture from geoloc
    """
    geoloc = [x,y]
    """
    from selenium import webdriver

    x=geoloc[0] #49.3527203
    y=geoloc[1] #6.1532284
    zone=30
    zoom=30
    #url = f"https://www.google.com/maps/@{x},{y},{zone}m/data=!3m1!1e3!5m1!1e4"
    url = f"https://satellites.pro/France_map#{x},{y},{zoom}"

    option=webdriver.ChromeOptions()
    option.headless = True
    driver = webdriver.Chrome("./chromedriver", chrome_options=option)
    driver.get(url)
    find=True
    while find:
        try:
            bt= driver.find_element_by_id("sw_but")
            bt.click()
            find=False
        except:pass
    find=True
    while find:
        try:
            bt= driver.find_element_by_id("sw-map-labels")
            bt.click()
            find=False
        except:pass
    find=True
    while find:
        try:
            bt= driver.find_element_by_id("sw_but")
            bt.click()
            find=False
        except:pass
    time.sleep(3)
    driver.save_screenshot(f"urbex_share/picture/{name}.png")
    driver.close()

    resize_screen(name)

def resize_screen(name):
    from PIL import Image
    #/urbex_share/picture/
    img = Image.open(f"urbex_share/picture/{name}.png")
    x, y = img.size

    new = img.crop((int(x/8),int(y/6),int(x/8)*7,int(y/6)*5))
    new.save(f"urbex_share/picture/{name}.png")
    

def create_uid(trade_id):
    #Lors de la création d'un trade
    """
    Content :
    <trade_id>:<uid1>:<uid2>
    """
    file = open("uid.txt","r")
    c = file.read().split("\n")
    file.close()
    
    new_ls=[]
    for i in c:
        if str(i.split(":")[0]) != str(trade_id) and i != '' :
            new_ls.append(i)
    
    uid1 = ""
    uid2 = ""
    for i in range(10):
        uid1 += str(random.choice(list("azertyuiopqsdfghjklmwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBN")))
        uid2 += str(random.choice(list("azertyuiopqsdfghjklmwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBN")))
    
    new_ls.append(f"{trade_id}:{uid1}:{uid2}")

    file = open("uid.txt","w")
    file.write("\n".join(new_ls))
    file.close()

def get_uid(trade_id):
    file = open("uid.txt","r")
    c = file.read().split("\n")
    file.close()
    user=None
    for i in c:
        r = i.split(":")
        if str(r[0]) == trade_id:
            user=[r[1],r[2]]
    return user

def create_trade():
    #Init un nouveau trade et return l'id
    try:
        file = open("trade.txt","r")
        c = file.read().split("\n") # c = ["<ID>:::<GEO1>:::<GEO2>:::<TIME>"]
        c = delete_empty(c)
        file.close()
        id_exist = []
        for i in c:
            id_exist.append(i.split(':::')[0])
    except:
        c = []
        id_exist = []
    print(c)

    #Génération de id /trade/<ID>
    find=False
    while not find :
        r = ""
        for i in range(3):
            r += str(random.choice(list("azertyuiopqsdfghjklmwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBN")))
        if r not in id_exist:
            find=True
    print("New ID : ", r)

    #Generation Temps
    current = int(time.time())
    delete_time = str(current + 1000)

    #Ajoute du nouvel id
    geoloc="" #Vide au début
    c.append(f"{r}:::{geoloc}:::{geoloc}:::{delete_time}")

    #Ajoute l'id au trade file
    file = open("trade.txt","w")
    file.write("\n".join(c))
    file.close()

    #Creer les uid
    create_uid(r)

    #Creer les autorisations (allow : les 2 sont ok)
    allow_init(r)

    #Supprime les images si existent d'avant (normalement elles doivent être supprimées mais en cas d'erreur...)
    try:os.remove(f"urbex_share/picture/{r}1.png")
    except:pass
    try:os.remove(f"urbex_share/picture/{r}2.png")
    except:pass
    try:os.remove(f"urbex_share/picture/{r}{r}.png")
    except:pass

    return r

def check_time():
    #Supp les trades expirés
    try:
        file = open("trade.txt","r")
        c = file.read().split("\n") # c = ["<ID>:::<GEO1>:::<GEO2>:::<TIME>"]
        file.close()
        c = delete_empty(c)
    except:
        c = []
    
    new_ls = [] #Liste sans les trades expirés
    for i in c:
        time_ = int(i.split(":::")[-1])
        if int(time.time()) < time_:
            new_ls.append(i)
        else :
            id_ = str(i.split(":::")[0])
            try:os.remove(f"urbex_share/picture/{id_}1.png")
            except:pass
            try:os.remove(f"urbex_share/picture/{id_}2.png")
            except:pass
            try:os.remove(f"urbex_share/picture/{id_}.png")
            except:pass
            
    
    file = open("trade.txt","w")
    file.write("\n".join(new_ls))
    file.close()

def delete_empty(ls):
    #Delete '' in a liste
    return [i for i in ls if i != '']

def trade_url(request):
    check_time()
    #Call when someone go at 127.0.0.1/trade
    #To a new trade
    ID=create_trade()
    rep = HttpResponseRedirect(f"/trade/{ID}")
    rep.set_cookie(f"{ID}","1") 
    """
    Cookie :
        <ID> /permet de dire si, sur le trade d'id <ID> c'est l'utilisateur 1 ou 2 qui se connecte/
            1 - HOST
            2 - Celui qui doit trade avec l'HOST
    """
    return rep

def check_file_exist():
    try:
        file = open("trade.txt","r")
        file.close()
    except:
        print("Création du fichier trade")
        file = open("trade.txt","w")
        file.close()
    try:
        file = open("uid.txt", "r")
        file.close()
    except:
        print("Création du fichier uid")
        file = open("uid.txt","w")
        file.close()
    try:
        file = open("allow.txt", "r")
        file.close()
    except:
        print("Création du fichier Allow")
        file = open("allow.txt","w")
        file.close()

check_file_exist()
