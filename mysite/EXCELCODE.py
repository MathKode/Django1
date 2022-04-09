"""
import argparse

parser = argparse.ArgumentParser(description="Code pour automatiser le rangement d'un classeur excel de Linde")

parser.add_argument("-f","--file",type=str,help="Le nom du fichier .csv à traiter")
parser.add_argument("-e","--equipment",type=str,default="equipment.csv",help="Le nom du fichier .csv contenant les équipement (Nom modèle;fabriquant;traitement)")
parser.add_argument("-o","--output",type=str,default="NEW_FILE",help="Le nom du fichier créer par le code")

args = parser.parse_args()
"""
import os

def _save(ls,equipment,new_name):
    import xlsxwriter
    
    workbook = xlsxwriter.Workbook(f'{new_name}.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.name = "Data"
    y = 0
    t = 0
    for line in ls:
        x = 0
        for column in line:
            worksheet.write(y,x,column)
            print("Creation :",int(t*100/(len(ls)*len(ls[0]))),"%",end='\r')
            x += 1
            t += 1
        y += 1
    
    worksheet2 = workbook.add_worksheet()
    worksheet2.name = "Equipment type"
    y = 0
    for line in equipment:
        x = 0
        for column in line:
            worksheet2.write(y,x,column)
            x += 1
        y += 1
    
    workbook.close()

def main(name_file,equipment,outname):
    print("Open File :",name_file)
    file = open("media/" + name_file,"r")
    content = file.read().split('\n')
    file.close()
    data = [] # [[ "A0", "A1"... ], ["B0", "B1" ...]]
    for i in content:
        data.append(i.split(';'))
    header = data[0]
    del data[0]

    dt=data.copy();data = []
    for i in dt:
        if i != ['']:
            data.append(i)
    h=header.copy();header = []
    for i in h:
        if i != '':
            header.append(i)
    
    print("Loading Equipment :",equipment)
    file = open(equipment,"r")
    content = file.read().split('\n')
    file.close()
    equipment = [] # [[ "A0", "A1"... ], ["B0", "B1" ...]]
    for i in content:
        if i != '':
            equipment.append(i.split(';'))
    print(equipment)
    #Création des colonnes Fabriquant/Traitement (14,15) à partir de Nom modèle (13 si on commence à 0)
    header.insert(14,"Traitement");header.insert(14,"Farbriquant")
    y = 0
    for lign in data:
        try:
            fr_name = lign[13] #Fr pour FabRiquant
            p = 0
            pp = -1
            for i in equipment:
                if i[0] == fr_name:
                    pp = p
                p += 1
            if pp == -1:
                print("ERREUR : Pas de nom de fabriquant correspondant lg",y+1,fr_name)
                lign.insert(14,"None");lign.insert(14,"None")
            else :
                ls = equipment[pp]
                lign.insert(14,ls[2])
                lign.insert(14,ls[1])
        except: pass
        y += 1
    #Création de la colonne Observance (18) à partir de obs. 28j (17)
    header.insert(18,"Observance")
    for lign in data:
        h = lign[17]
        if h == '':
            #Pas d'observance
            lign.insert(18,"Pas d'observance")
        else :
            heure = int(str(h.split(":")[0]))
            if heure < 2:
                lign.insert(18,"<2h")
            elif heure > 3:
                lign.insert(18,"≥4h")
            else:
                lign.insert(18,"2≤ <4h")
    
    data.insert(0,header)
    _save(data,equipment,"media/" + outname)
    os.remove("media/" + name_file)

"""
if __name__ == "__main__":
    main(args.file,args.equipment,args.output)
"""