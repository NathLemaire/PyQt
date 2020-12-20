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
        self.requete("CREATE TABLE recettes (nomRecette TEXT PRIMARY KEY,"+
 					      "prix_cent INT)")

    # Test de l'existence d'une personne
    def personneExistence(self,ident):
        res=0
        table=[]
        try:
            table = self.question(("SELECT * FROM recettes WHERE nomRecette='{0}'").format(ident))
            pass
            if (len(table)>0):
                return table[0]
                pass
        except Exception as e:
            self.out.afficher("Erreur [personneExistence] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        return res

    # Insertion d'une nouvelle personne
    def personneInsertion(self,t):
        try:
            self.requete("INSERT INTO recettes VALUES('{0}',{1})".format(t[0],t[1]))
            pass
        except Exception as e:
            self.out.afficher("Erreur [personneInsertion] : {0}\n".format(e.args[0]))
            #sys.exit(1)
        

    # Mise à jour d'une personne
    def personneMiseAJour(self,t):
        try:
            self.requete("UPDATE recettes SET nomRecette='{0}', prix_cent={1} WHERE nomRecette='{2}'".format(t[0],t[1],t[0]))
            pass
        except Exception as e:
            self.out.afficher("Erreur [personneMiseAJour] : {0}\n".format(e.args[0]))
            #sys.exit(1)

    # Effacement d'une personne
    def effacerPersonne(self,ident):
        try:
            self.requete("DELETE FROM recettes WHERE nomRecette='{0}'".format(ident))
            pass
        except Exception as e:
            self.out.afficher("Erreur [effacerPersonne] : {0}\n".format(e.args[0]))
            #sys.exit(1)
            
        # Montrer toutes les recettes de la db
    def showtable(self):
        table = []
        try:
            table = self.question("SELECT * FROM Recettes")
            if len(table)>0:
                for item in table:
                    self.out.afficher("Recette {0} : {1} euros \n".format(item[0], item[1]/100))
            else:
            	self.out.afficher("No recipe in the database")
        except Exception as e:
            self.out.afficher("Erreur [showtable] : {0}\n".format(e.args[0]))
            #sys.exit(1)
  
# ===================================================================
#                         Programme principal
# ===================================================================
if __name__ == "__main__":
    print("\nCe programme n'est pas le programme principal!\n")
