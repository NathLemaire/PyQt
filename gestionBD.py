#!/usr/bin/python
from BDRegMat import BDRegMat
import sqlite3 as lite
import sys

# Classe de gestion de la base de données sur les militaires

class BD(BDRegMat):
    # Constructeur
    def __init__(self, output,nom='defaut.db'):
        BDRegMat.__init__(self,output,nom)
        self.out=output
        self.ouvrir(nom)

    # Ouverture de la base
    def ouvrir(self,nom):
        if nom=="":
            self.nomBD="defaut.bd"
        else:
            self.nomBD=nom

    # Changer de base de données
    def setNom(self,nom):
        self.fermeture()
        self.ouvrir(nom)

    # Création effective de la base de données
    def creerBD(self):
        # Destruction des tables antérieures
        self.requete("DROP TABLE resider")
        self.requete("DROP TABLE personnes")
        self.requete("DROP TABLE lieux")

        # Création des nouvelles tables
        # Q2 ...
        self.requete("CREATE TABLE lieux (codeINSEE INT PRIMARY KEY,"+
 					      "nomCommune TEXT, " +
 					      "nomDepartement TEXT)")

        self.requete("CREATE TABLE personnes (ident TEXT PRIMARY KEY,"+
					      "sexe TEXT NOT NULL,"+
                                            "nom TEXT NOT NULL,"+
                                            "prenom TEXT NOT NULL,"+
                                            "profession TEXT NOT NULL,"+
                                            "dateNaissance TEXT,"+
                                            "codeINSEE INT REFERENCES lieux(codeINSEE),"+
                                            "CHECK(sexe IN ('M','F')))")

        self.requete("CREATE TABLE resider (ident TEXT REFERENCES personnes, "+
        		"codeINSEE INT REFERENCES lieux(codeINSEE),"+
        		"date TEXT, PRIMARY KEY (ident, codeINSEE, date))")

        
        # Insertion matricule 1 année 1896 division Caen, M. Victor Oullet
        self.requete("INSERT INTO lieux VALUES(14149,'Cesny-aux-Vignes','Calvados')")
        self.requete("INSERT INTO lieux VALUES(14225,'Dives-sur-Mer','Calvados')")
        self.requete("INSERT INTO lieux VALUES(14126,'Cambremer','Calvados')")
        self.requete("INSERT INTO lieux VALUES(14070,'Beuvron-en-Auge','Calvados')")
        self.requete("INSERT INTO lieux VALUES(14560,'Saint-Aubin-Lebizay','Calvados')")
        self.requete("INSERT INTO personnes VALUES('C1896_1','M','Oullet',"+
                            "'Victor Louis Eugène','domestique','1876-05-24',14149)")
        self.requete("INSERT INTO resider VALUES('C1896_1',14225,'1914-02-21')")
        self.requete("INSERT INTO resider VALUES('C1896_1',14126,'1919-07-12')")
        self.requete("INSERT INTO resider VALUES('C1896_1',14070,'1922-03-05')")
        self.requete("INSERT INTO resider VALUES('C1896_1',14560,'1923-03-03')")

        # Insertion matricule 515 année 1896 division Caen, M. Ferdinand Guibert
        self.requete("INSERT INTO lieux VALUES(14667,'Saon','Calvados')")
        self.requete("INSERT INTO lieux VALUES(14369,'Litteau','Calvados')")
        self.requete("INSERT INTO lieux VALUES({0},'{1}','{2}')".format(14727,'Vaubadon','Calvados'))
        self.requete("INSERT INTO personnes VALUES('C1895_515','M','Guibert',"+
                            "'Ferdinand Maurice','sabotier','1875-03-20',14727)")
        self.requete("INSERT INTO resider VALUES('C1895_515',14667,'1896-01-01')")
        self.requete("INSERT INTO resider VALUES('C1895_515',14369,'1900-10-19')")

        # Insertion matricule 777 année 1903 division Caen, M. Fernand Leplumey
        self.requete("INSERT INTO lieux VALUES(50178,'Fermanville','Manche')")
        self.requete("INSERT INTO lieux VALUES(14574,'Saint-Desir','Calvados')")
        self.requete("INSERT INTO lieux VALUES(14345,'Jort','Calvados')")
        self.requete("INSERT INTO lieux VALUES(14366,'Lisieux','Calvados')")
        self.requete("INSERT INTO personnes VALUES('C1903_777','M','Leplumey',"+
                            "'Fernand Casimir Alexis','élève écclésiastique','1883-03-23',50178)")
        self.requete("INSERT INTO resider VALUES('C1903_777',14574,'1907-10-22')")
        self.requete("INSERT INTO resider VALUES('C1903_777',14345,'1911-01-28')")
        self.requete("INSERT INTO resider VALUES('C1903_777',14345,'1923-09-06')")
        self.requete("INSERT INTO resider VALUES('C1903_777',14366,'1932-01-12')")
        print("insert done")
        
    # Remplissage de la table des lieux
    def initTableLieux(self,nomCSV):
        # Ouverture du fichier
        try:
            f=open(nomCSV,"r")
            for line in f:
                line=line.strip()
                liste=line.split(";")
                if (len(liste)==2):
                    self.requete("INSERT INTO lieux VALUES("+liste[0]+",'"+liste[1]+"','Calvados')")
                    pass
            f.close()
        except IOError as e:
            self.out.afficher("Erreur [initTableLieux] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        except lite.Error as e:
            self.out.afficher("Erreur [initTableLieux] : {0}\n".format(e.args[0]))
  
    # Test de l'existence d'une personne
    def personneExistence(self,ident):
        res=0
        table=[]
        try:
            table = self.question(("SELECT * FROM personnes WHERE ident='{0}'").format(ident))
            pass
            if (len(table)>0):
                return table[0]
                pass
        except Exception as e:
            self.out.afficher("Erreur [personneExistence] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        return res

    # Lecture d'une personne à partir de son code
    def personneCode(self,ident):
        res=["M","","","","","",""]
        table=[]
        try:
            table = self.question(("SELECT * FROM personnes WHERE ident='{0}'").format(ident))
            pass
            if (len(table)>0):
                if (len(table)==1):
                    # Construction du vecteur résultat sans le nom de commune
                    res[1]=table[0][1]
                    res[2]=table[0][2]
                    res[3]=table[0][3]
                    res[4]=table[0][4]
                    res[5]=table[0][5]
                    res[6]=str(table[0][6])
                    
                else:
                    self.out.afficher("Plusieurs personnes répondent à la requête\n")
            else:
                self.out.afficher("Aucune personne n'est inscrite avec ce code dans la base de données ({0})\n".format(ident))

        except Exception as e:
            self.out.afficher("Erreur [personneCode] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        return res

    # Insertion d'une nouvelle personne
    def personneInsertion(self,t):
        # Prévoir le cas où le lieu ne serait pas renseigné (lieu non enregistré, lieu non lisible...)
        if t[6]!=0:
              self.requete("INSERT INTO personnes VALUES('{0}','{1}','{2}','{3}','{4}','{5}',{6})".format(t[0],t[1],t[2],t[3],t[4],t[5],t[6]))
        else:
              self.requete("INSERT INTO personnes(ident,sexe,nom,prenom,profession,dateNaissance) VALUES('{0}','{1}','{2}','{3}','{4}','{5}')".format(t[0],t[1],t[2],t[3],t[4],t[5]))

    # Mise à jour d'une personne
    def personneMiseAJour(self,t):
        if t[5]!=0:
              self.requete("UPDATE personnes SET sexe='{0}',nom='{1}',prenom='{2}',profession='{3}',dateNaissance='{4}',codeINSEE={5} WHERE ident='{6}'".format(t[0],t[1],t[2],t[3],t[4],t[5],t[6]))
        else:
              self.requete("UPDATE personnes SET sexe='{0}',nom='{1}',prenom='{2}',profession='{3}',dateNaissance='{4}',codeINSEE=NULL WHERE ident='{5}'".format(t[0],t[1],t[2],t[3],t[4],t[6]))

    # Effacement d'une personne
    def effacerPersonne(self,ident):
        self.requete("BEGIN")
        # Q12 ...
        pass
        self.requete("END")

    # Insertion d'une nouvelle personne
    def residenceInsertion(self,t):
        # Q14 ...
        pass

    # Effacement d'un lieu de résidence pour une personne
    def effacerResidence(self,t):
        # Q15 ...
        pass

    # Conversion du nom de lieu en code
    def lieuCode(self,lieu):
        res=""
        table=[]
        try:
            table = self.question(("SELECT codeINSEE FROM lieux WHERE nomCommune = '{0}'").format(lieu))
            pass
            if (len(table)>0):
                if (len(table)==1):
                    res=str(table[0][0])
                    pass
                else:
                    self.out.afficher("Plusieurs lieux répondent à la requête\n")
            else:
                self.out.afficher("Aucun lieu avec ce code n'est inscrit dans la base de données\n")

        except Exception as e:
            self.out.afficher("Erreur [lieuCode] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        return res

    # Affichage de la liste des lieux
    def listeLieux(self):
        table=[]
        try:
            table = self.question("SELECT * FROM lieux ORDER BY codeINSEE")
            pass
            if (len(table)>0):
                self.out.afficher("Nombre de lieux : {0}\n".format(len(table)))
                # Affichage de chaque lieu
                for lieu in table:
                    print(("{0} : {1}, {2}").format(lieu[0], lieu[1], lieu[2]))
                    pass
            else:
                self.out.afficher("Aucun lieu n'est inscrit dans la base de données\n")

        except Exception as e:
            self.out.afficher("Erreur [listeLieux] : {0}\n".format(e.args[0]))
            #sys.exit(1)

    # Affichage de la liste des militaires
    def listeMilitaires(self):
        table=[]
        try:
            # Recherche des militaires
            # Q11 ...
            pass
          
            if (len(table)>0):
                self.out.afficher("Nombre d'individus : {0}\n".format(len(table)))
                # Affichage de chaque militaire
                for personne in table:
                    # ...
                    pass
            else:
                self.out.afficher("Aucune personne n'est inscrite dans la base de données avec un lieu de naissance valide\n")

        except Exception as e:
            self.out.afficher("Erreur [listeMilitaires] : {0}\n".format(e.args[0]))
            #sys.exit(1)

    # Test de l'existence d'une résidence pour une personne
    def residenceExistence(self,identP,identL,date):
        res=0
        try:
            # Recherche des militaires
            table=self.question("SELECT count(*) FROM resider WHERE ident='{0}' and codeINSEE={1} and date='{2}'".format(identP, identL, date))
            if (len(table)>0):
                # Retour du résultat de la requête
                res=int(table[0][0])

        except Exception as e:
            self.out.afficher("Erreur [residenceExistence] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        return res

    # Affichage de la liste des résidences connues
    def listeResidences(self):
        table=[]
        try:
            # Recherche des résidences
            # Q13 ...
            pass
            if (len(table)>0):
                self.out.afficher("Nombre de résidences connues : {0}\n".format(len(table)))
                # Affichage de chaque lieu
                for lieu in table:
                    # ...
                    pass
            else:
                self.out.afficher("Aucun lieu de résidence n'est inscrit dans la base de données\n")

        except Exception as e:
            self.out.afficher("Erreur [listeResidences] : {0}\n".format(e.args[0]))
            #sys.exit(1)

# ===================================================================
#                         Programme principal
# ===================================================================
if __name__ == "__main__":
    print("\nCe programme n'est pas le programme principal!\n")
