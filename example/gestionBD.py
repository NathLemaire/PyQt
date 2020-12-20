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
        self.requete("DROP TABLE recettes")
        self.requete("CREATE TABLE recettes (id INT PRIMARY KEY,"+
 					      "nomRecette TEXT UNIQUE,"+
 					      "prix_centimes INT)")
        
        self.requete("INSERT INTO recettes VALUES('Gratin_de_chou', 600)")
   
    def retrieveprice(self, recettename):
        table=[]
        try:
            table = self.question(("SELECT prix_centimes FROM recettes WHERE nomRecette='{0}'").format(recettename))
            pass
            if (len(table)>0):
                return table[0][0]/100
                pass
        except Exception as e:
            self.out.afficher("Erreur [retriverprice] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        return res    
        
    """
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
            table=self.question("SELECT count(*) FROM resider WHERE ident='{0}' and codeINSEE={1} and date='{2}'".format(identP, identL, date))
        try:
            # Recherche des militaires
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
"""
# ===================================================================
#                         Programme principal
# ===================================================================
if __name__ == "__main__":
    print("\nCe programme n'est pas le programme principal!\n")
