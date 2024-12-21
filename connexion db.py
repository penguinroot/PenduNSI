# Module Imports
import mariadb
import sys
import csv
import unidecode




def mettre_lettre():
    curseur.execute("DELETE FROM LETTRES")
    for i in range(26):
        curseur.execute("INSERT INTO LETTRES VALUES (?, ?, ?)", (chr(65 + i), 0, 0))
        conn.commit()



conn = mariadb.connect(
    user="project",
    password="pm",
    host="109.10.114.61",
    port=3306,
    database="PenduNSI"

)

curseur = conn.cursor()


def remplir_mots():
    i=1
    curseur.execute("DELETE FROM MOTS")
    conn.commit()
    with open('Liste_mots_nsi.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row2 in reader:
            row=unidecode.unidecode(''.join(row2).upper().strip())
            print(i,row)
            x=row.find("'")
            if x == -1 :
                wrequete="INSERT INTO MOTS VALUES ('"+row+"','0')"
                curseur.execute(wrequete)
            i=i+1
    conn.commit()
         
            
        
        
def calcul_proba_lettres():
    wtotal=0       
    curseur.execute("DELETE FROM LETTRES")
    conn.commit()
    mettre_lettre()
    wrequete = ("SELECT mot FROM MOTS")
    curseur.execute(wrequete)
    wresultat=curseur.fetchall()
    for wmot2 in wresultat:
        wmot=''.join(wmot2)
        wlongueur=len(wmot)
        print(wlongueur,wmot)
        for i in range(wlongueur):
            wtotal=wtotal+1
            wcar=wmot[i]
            wrequete = ("UPDATE LETTRES SET nb_occurence=nb_occurence+1 WHERE lettre='"+wcar+"';")
            curseur.execute(wrequete)
    wrequete="UPDATE LETTRES SET taux = (nb_occurence/"+str(wtotal)+")"
    curseur.execute(wrequete)
    conn.commit()
def difficulte():
        
    wrequete = ("UPDATE MOTS SET difficulte=0")
    curseur.execute(wrequete) 
    conn.commit()    
    wrequete = ("SELECT mot FROM MOTS")
    curseur.execute(wrequete)
    wresultat=curseur.fetchall()
    for wmot2 in wresultat:
        wmot=''.join(wmot2)
        wlongueur=len(wmot)
        print(wlongueur,wmot)
        wnote=0
        wcar=wmot[0]
        wrequete = ("SELECT taux FROM LETTRES WHERE LETTRE = '"+wcar+"'")
        curseur.execute(wrequete)
        wstrtaux=curseur.fetchone()
        for wtaux in wstrtaux:
            wnote=wnote+1/wtaux
        for i in range(1,len(wmot)):
            wcar=wmot[i]
            wpartiemot=wmot[1:i-1]
            if wcar !='-' and wcar != ' ' and wcar != '.':
                if wpartiemot.find(wcar) == -1 :
                    wrequete = ("SELECT taux FROM LETTRES WHERE LETTRE = '"+wcar+"'")
                    curseur.execute(wrequete)
                    wstrtaux=curseur.fetchone()
        
                    for wtaux in wstrtaux :
                        #print(wtaux)
                        wnote=wnote+1/wtaux
        if len(wmot)>4:            
            wnote=wnote/len(wmot)
        
        wrequete2 = "UPDATE MOTS SET difficulte = '"+str(wnote)+"' WHERE mot = '"+wmot+"'"
        #print(wrequete2)
        curseur.execute(wrequete2)
        conn.commit()
    
        
    
mettre_lettre()
remplir_mots()
calcul_proba_lettres()
difficulte()

    
    



conn.close()