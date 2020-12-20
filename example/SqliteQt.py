#!/usr/bin/ruby
#require 'Math'
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QMenu, QAction, QToolBar, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QComboBox, QSpinBox
from PyQt5.QtWidgets import QLineEdit, QTabWidget, QDateEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
from gestionBD import BD
import os.path

# =============================================================================
# Zone textuelle sauvegardable qui va servir de zone d'affichage si nécessaire
class Texte(QTextEdit):
  # Constructeur
  def __init__(self):
    # Appel constructeur de la classe mère
    QTextEdit.__init__(self)
    # Affichage du widget
    self.show()

  # Afficher texte
  def afficher(self,t):
    # Affichage message d'erreur dans l'interface Qt
    cursor=self.textCursor()
    cursor.insertText(t)

  # Effacement du texte de la fenêtre
  def effacer(self):
    self.setPlainText("")

class Fenetre(QMainWindow):
  def __init__(self):
    # Appel constructeur de la classe mère
    QMainWindow.__init__(self)

    # Mise d'une base de données par défaut
    self.nomBD="recettes.bd"
    # Allocation d'un objet base de données
    self.bd=BD(self,self.nomBD)

    # Initialisation de l'interface
    self.init_ui()

    # Visualisation de la fenêtre
    self.show()

    # Emission d'un signal de modification sur le champ d'édition du matricule
    self.editMatric.setValue(2)
    self.editMatric.setValue(1)

  # Mise en place de zones non éditables
  def zoneNonEditable(self,zone):
    # Mise en place d'une zone non modifiable
    zone.setReadOnly(True)
    zone.setStyleSheet("QLineEdit { background-color : lightGray; color : darkGray; }");
      
  # Ajout d'un choix à un menu
  def ajoutChoixMenu(self,texte,menu,fonction,image=""):
    action = QAction(texte, self)
    if image!="": action.setIcon(QIcon(image))
    menu.addAction(action)
    action.triggered.connect(fonction)
    return(action)
    
  # Ajout du menu Fichiers
  def ajoutMenuFichiers(self):
    # Création et ajout du menu Fichiers
    self.menuFichier=QMenu("&Fichier")
    self.menubar.addMenu(self.menuFichier)
    
    # Gestion du choix ouvrir
    self.actionOuvrir=self.ajoutChoixMenu("&Ouvrir",self.menuFichier,
                                          self.ouvrirClicked,"./icones/ouvrir.png")
    # Gestion du choix sauver
    self.actionSauver=self.ajoutChoixMenu("&Sauver sous...",self.menuFichier,
                                          self.sauverClicked,"./icones/SauverSous.png")
    # Gestion du choix effacer la fenêtre texte
    self.actionEffacer=self.ajoutChoixMenu("&Effacer texte",self.menuFichier,
                                          self.effacerTexteClicked,"./icones/gomme.png")
    # Gestion du choix informations
    self.actionInformations=self.ajoutChoixMenu("&Informations",self.menuFichier,
                                          self.informationsClicked,"./icones/informations.png")
    # Gestion du choix quitter
    self.actionQuitter=self.ajoutChoixMenu("&Quitter",self.menuFichier,
                                          self.close,"./icones/quitter.png")
    
  # Ajout du menu BD
  def ajoutMenuBD(self):
    # Création et ajout du menu base de données
    self.menuBD=QMenu("&Base de données")
    self.menubar.addMenu(self.menuBD)

    # Gestion du choix de création de la base de données
    self.actionCreerBD=self.ajoutChoixMenu("&Créer BD",self.menuBD,
                                          self.creerBDClicked,"./icones/bd.png")
    
  # Ajout de la barre de menu
  def ajoutMenu(self):
    self.menubar=self.menuBar()
    self.ajoutMenuFichiers()
    self.ajoutMenuBD()
   
  # Création d'une barre d'outils
  def ajoutToolBar(self):
    # Création d'une barre d'outils
    self.toolBar=self.addToolBar("Raccourcis")

    # Gestion des boutons de la barre d'outils
    self.toolBar.addAction(self.actionOuvrir)
    self.toolBar.addAction(self.actionSauver)
    self.toolBar.addAction(self.actionEffacer)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.actionCreerBD)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.actionInformations)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.actionQuitter)
    
    # Invalidation des boutons non nécessaires
    self.actionSauver.setEnabled(False)
    self.actionEffacer.setEnabled(False)

  # Ajout de l'onglet Personne
  def ajoutOngletPersonne(self):
    # Gestion de l'onglet personne
    self.personneWidget=QWidget()
    self.gridP1=QGridLayout()
    self.labelNom=QLabel("Nom")
    self.editNom=QLineEdit()
    self.labelPrenom=QLabel("Prénom")
    self.editPrenom=QLineEdit()
    
    # Mise en place des widgets dans le layout
    lig=0; col=0
    self.gridP1.addWidget(self.labelNom,lig,col)
    col+=1; self.gridP1.addWidget(self.editNom,lig,col)
    col+=1; self.gridP1.addWidget(self.labelPrenom,lig,col)
    col+=1; self.gridP1.addWidget(self.editPrenom,lig,col)
    self.personneWidget.setLayout(self.gridP1)
    
    # Ajout de l'onglet
    self.tabWidget.addTab(self.personneWidget,"&Personne")

   # Ajout de la partie onglet du formulaire
  def ajoutOngletsFormulaire(self):
    # Gestion des onglets
    self.tabWidget=QTabWidget()
    lig=1; col=0
    self.gridL.addWidget(self.tabWidget,lig,col,1,7)
    self.ajoutOngletPersonne()

  # Ajout de la partie formulaire
  def ajoutFormulaire(self):
    # Objet de positionnement des widgets du formulaire
    self.gridL=QGridLayout()

    # Gestion de la première ligne du formulaire
    self.labelBureau=QLabel("Bureau")
    self.editBureau=QComboBox()
    self.editBureau.addItems(["Caen","Falaise","Lisieux"])
    self.labelAnnee=QLabel("Année")
    self.editAnnee=QSpinBox()
    self.editAnnee.setRange(1850,1950)
    self.labelMatric=QLabel("Matricule")
    self.editMatric=QSpinBox()
    self.editMatric.setRange(1,4000)
    self.editCode=QLineEdit()
    self.zoneNonEditable(self.editCode)


    # Ajout de la partie à onglets
    self.ajoutOngletsFormulaire()
    
    # Gestion des boutons
    self.boutonEnregistrer=QPushButton("Enregistrer")
    self.boutonEffacerPersonne=QPushButton("Effacer personne")
    self.boutonEffacerChamps=QPushButton("Effacer champs")
    self.boutonShowRecipe=QPushButton("Montrer les recettes")
    lig=2; col=0
    self.gridL.addWidget(self.boutonEnregistrer,lig,col)
    col+=1; self.gridL.addWidget(self.boutonEffacerPersonne,lig,col)
    col+=1; self.gridL.addWidget(self.boutonEffacerChamps,lig,col)
    col+=1; self.gridL.addWidget(self.boutonShowRecipe,lig,col)

    # Gestion des signaux des deux boutons du formulaire
    self.boutonEnregistrer.clicked.connect(self.enregistrerDonnees)
    self.boutonEffacerPersonne.clicked.connect(self.effacerPersonne)
    self.boutonEffacerChamps.clicked.connect(self.effacerChamps)
    self.boutonShowRecipe.clicked.connect(self.showRecipe)

   
    # Ajout du formulaire à la boite verticale principale
    self.boxVPrinc.addLayout(self.gridL)

  # Initialisation de l'interface
  def init_ui(self):
    # Mise d'un titre à la fenêtre
    self.setWindowTitle("Application SQLite")

    # Allocation de la zone textuelle pour afficher les résultats
    self.texte=Texte()
    
    # Le widget principal
    self.window = QWidget()
    # Création d'une boite verticale (associée à un widget)
    self.boxVPrinc=QVBoxLayout()
    self.window.setLayout(self.boxVPrinc)
  
    # Ajout du formulaire complet
    self.ajoutFormulaire()
    self.boxVPrinc.addWidget(self.texte)
    # Gestion des signaux de changement de la zone textuelle
    self.texte.textChanged.connect(self.changementTexte)    
    # Mise de la zone centrale
    self.setCentralWidget(self.window)
    
    # Mise en place du Menu
    self.ajoutMenu()
    # Création d'une barre d'outils
    self.ajoutToolBar()

  # Afficher texte
  def afficher(self,t):
    self.texte.afficher(t)

  # Gestion du changement de la zone de texte
  def changementTexte(self):
    if self.texte.toPlainText()=="":
      self.actionSauver.setEnabled(False)
      self.actionEffacer.setEnabled(False)
    else:
      self.actionSauver.setEnabled(True)
      self.actionEffacer.setEnabled(True)


  # Enregistrement des données
  def enregistrerDonnees(self):
      if self.nomBD!="":
          exist=self.bd.personneExistence(self.editNom.text())
          if True:
              # Création/modification d'une personne
              if exist==1:
                  # Modification d'un individu existant
                  t=[self.editNom.text(),self.editPrenom.text()]
                  self.bd.personneMiseAJour(t)
              else:
                  # Insertion d'un nouvel individu
                  t=[self.editNom.text(),self.editPrenom.text()]
                  self.bd.personneInsertion(t)
      else:
          self.afficher("Veuillez choisir au préalable une base de données\n")

  # Effacement des champs des formulaires
  def effacerChamps(self):
      # Effacement de tous les champs de saisie
      self.editNom.setText("")
      self.editPrenom.setText("")
      
      
  # Effacement d'une personne de la base de données
  def effacerPersonne(self):
      exist=self.bd.personneExistence(self.editNom.text())
      if exist!=0:
          self.bd.effacerPersonne(self.editNom.text())
      else:
          self.afficher("La recette %s n'existe pas...\n" % self.editNom.text())

  # On montre les entrées
  def showRecipe(self):
      self.bd.showtable()
      
  # Gestion de l'ouverture de la base de données
  def ouvrirClicked(self):
      fileName=QFileDialog.getOpenFileName(self, "Sélection de la base de données")
      if (not fileName.isNull()) and fileName.length!=0:
          self.nomBD=fileName
          self.bd.setNom(self.nomBD)
          self.actionInformations.setEnabled(True)

  # Gestion du bouton de sauvegarde
  def sauverClicked(self):
      # Récupération du texte de la fenêtre
      texte = self.texte.toPlainText()

      # Affichage d'une fenêtre de dialogue pour fixer le nom du fichier de sauvegarde
      fileName=QFileDialog.getSaveFileName(self, "Sauvegarde de la trace","trace.txt")

      # On ne peut effectuer une sauvegarde que dans un nouveau fichier
      if (not fileName.isNull()) and fileName.length!=0 and not isFile(fileName):
          # Ouverture du fichier en écriture
          fh=QFile(fileName)
          if not fh.open(QIODevice.WriteOnly):
              QMessageBox.information(self,"Erreur","La sauvegarde de la trace n'a pas été effectuée")
              return
          stream=QTextStream(fh)
          # Sauvegarde du texte
          stream << texte
          fh.close()

  # Gestion du bouton d'effacement du texte
  def effacerTexteClicked(self):
      self.texte.effacer()

  # Gestion du bouton de récupération d'information sur la base de données
  def informationsClicked(self):
      QMessageBox.information(self,"Information","\nNom de la base de données : "+self.nomBD)

  # Gestion du bouton de création de la base de données
  def creerBDClicked(self):
      # Création de la base de données
      self.bd.creerBD()

# ===================================================================
#                         Programme principal
# ===================================================================
if __name__ == "__main__":
    print("\nCe programme n'est pas le programme principal!\n")
