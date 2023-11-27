import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from tpsommatif import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connecter les boutons 
        self.ui.pushButton.clicked.connect(self.CreerUser)
        self.ui.pushButton_lancer_sauvegarde.clicked.connect(self.CreerSauvegarde)
        self.ui.pushButton_lancer_sauvegarde_2.clicked.connect(self.charger_sauvegarde)
        self.ui.pushButton_2.clicked.connect(self.supprimer_sauvegarde)
        self.ui.pushButton_2_sauvegarder.clicked.connect(self.enregistrer_fiche_joueur)
        self.ui.pushButton_3.clicked.connect(self.charger_lien_chapitre)
        # Connexion à la base de données avec user sécurisé
        self.connexion_bd = mysql.connector.connect(
            host='localhost',
            user='tp_sommatif',
            password='tp_sommatif',
            database='tp_sommatif'
        )

        # Remplir la Combo Box avec les informations
        self.remplir_combo_box_livres()
        self.remplir_combo_box_usager()
        self.remplir_combo_box_sauvegarder()
        self.remplir_combo_box_suppression()
        
    # créer un utilisateur dans la bd
    def CreerUser(self):
        # Récupérer le nom de l'utilisateur depuis le champ de texte
        nom_utilisateur = self.ui.lineEdit.text()

        # Vérifier si le champ de texte n'est pas vide
        if not nom_utilisateur:
            QMessageBox.warning(self, "Avertissement", "Veuillez saisir un nom d'utilisateur.")
            return

        try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()

            # Exécuter la requête pour insérer l'utilisateur dans la table
            requete = "INSERT INTO usager (nom) VALUES (%s)"
            valeurs = (nom_utilisateur,)
            curseur.execute(requete, valeurs)

            # Valider la transaction
            self.connexion_bd.commit()

            # afficher message pour comprendre la situation
            QMessageBox.information(self, "Succès", "Utilisateur enregistré avec succès.")

            # Mettre à jour le contenu du QComboBox 
            self.remplir_combo_box_usager()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement de l'utilisateur : {str(e)}")
    # Créer sauvegarde
    def CreerSauvegarde(self):
        # Récupérer le nom de l'utilisateur depuis le combobox
        nom_utilisateur = self.ui.comboBox_utilisateur_sauvegarde.currentText()
  
        # Appeler la fonction pour obtenir l'ID de l'utilisateur
        id_utilisateur = self.obtenir_id_utilisateur(nom_utilisateur)

        # Récupérer l'ID du livre depuis la combobox
        nom_livre = self.ui.comboBox_livre_sauvegarde.currentText()
        
        id_livre = self.obtenir_id_livre(nom_livre)
        
        # Récupérer le nom de la sauvegarde depuis le champ de texte
        nom_sauvegarde = self.ui.lineEdit_nom_sauvegarde.text()

        # Vérifier si le champ de texte du nom de sauvegarde n'est pas vide
        if not nom_sauvegarde:
            QMessageBox.warning(self, "Avertissement", "Veuillez saisir un nom de sauvegarde.")
            return
        try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()
            
            id_discipline1 = None
            id_discipline2 = None
            id_discipline3 = None
            id_discipline4 = None
            id_discipline5 = None
            repas = ""
            objet = ""
            id_armes1 = None
            id_armes2 = None
            bourse = None
            object_special = ""
            
            # Exécuter la requête pour insérer une nouvelle fiche de personnage (remplacez 'fiches_personnage', 'colonne1', 'colonne2', ... par vos noms réels)
            requete_fiche_personnage = "INSERT INTO fiche_personnage (id_discipline1,id_discipline2,id_discipline3,id_discipline4,id_discipline5, repas, objet, id_armes1,id_armes2, bourse, objet_special) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valeurs_fiche = (id_discipline1,id_discipline2,id_discipline3,id_discipline4,id_discipline5, repas, objet, id_armes1,id_armes2, bourse, object_special,)
            curseur.execute(requete_fiche_personnage,valeurs_fiche)

            # Récupérer l'ID de la fiche de personnage que nous venons de créer
            id_fiche_personnage = curseur.lastrowid
            id_chapitre = "1"
            # Exécuter la requête pour insérer la sauvegarde dans la table (remplacez 'sauvegardes', 'id_usager', 'id_livre', 'nom_sauvegarde', 'id_fiche_personnage' par vos noms réels)
            requete_sauvegarde = "INSERT INTO sauvegarde (id_usager, id_livre, nom_sauvegarde, id_fiche_personnage, id_chapitre) VALUES (%s, %s, %s, %s,%s)"
            valeurs_sauvegarde = (id_utilisateur, id_livre, nom_sauvegarde, id_fiche_personnage, id_chapitre)
            curseur.execute(requete_sauvegarde, valeurs_sauvegarde)
            
            # Valider la transaction
            self.remplir_combo_box_suppression()
            self.remplir_combo_box_sauvegarder()
            self.connexion_bd.commit()

            QMessageBox.information(self, "Succès", "Fiche de personnage et sauvegarde créées avec succès.")
        # le e ses l'erreur et on affiche un string 
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création de la fiche de personnage et de la sauvegarde : {str(e)}")
    # obtenir id utilisateur        
    def obtenir_id_utilisateur(self, nom_utilisateur):
        print(f"Tentative de récupération de l'ID pour l'utilisateur : {nom_utilisateur}")
        # Récupérer l'ID de l'utilisateur depuis la base de données en utilisant le nom
        requete_id_usager = "SELECT id FROM usager WHERE nom = %s"
        valeurs_id_usager = (nom_utilisateur,)
        print(f"Requête SQL : {requete_id_usager} ")
        try:
            
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor(buffered=True)
            
            # Exécuter la requête pour récupérer l'ID de l'utilisateur
            curseur.execute(requete_id_usager, valeurs_id_usager)

            # Récupérer le résultat de la requête
            resultat_id_usager = curseur.fetchone() 
            
            # Fermer le curseur
            curseur.close()
            
            # Vérifier si un résultat a été trouvé
            if resultat_id_usager:
                
                id_usager = resultat_id_usager[0]
                return id_usager
            else:
                # retourne rien
                return None

        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération de l'ID de l'utilisateur : {str(e)}")
            return None
    # obtenir id du livre
    def obtenir_id_livre(self, nom_livre):
        # Récupérer l'ID de l'utilisateur depuis la base de données en utilisant le nom
        requete_id_livre = "SELECT id FROM livre WHERE titre = %s"
        valeurs_id_livre = (nom_livre,)
        try:
            
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor(buffered=True)
            
            # Exécuter la requête pour récupérer l'ID de l'utilisateur
            curseur.execute(requete_id_livre, valeurs_id_livre)

            # Récupérer le résultat de la requête
            resultat_id_livre = curseur.fetchone() 
            
            # Fermer le curseur
            curseur.close()
            
            # Vérifier si un résultat a été trouvé
            if resultat_id_livre:
                id_usager = resultat_id_livre[0]
                return id_usager
            else:
                # retourne rien
                return None

        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération de l'ID de l'utilisateur : {str(e)}")
            return None
    # obtenir id sauvegarde
    def obtenir_id_sauvegarde(self, nom_sauvegarde):
        
        # Récupérer l'ID de l'utilisateur depuis la base de données en utilisant le nom
        requete_id_sauvegarde = "SELECT id FROM sauvegarde WHERE nom_sauvegarde = %s"
        valeurs_id_livre = (nom_sauvegarde,)
        try:
            
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor(buffered=True)
            
            # Exécuter la requête pour récupérer l'ID de l'utilisateur
            curseur.execute(requete_id_sauvegarde, valeurs_id_livre)

            # Récupérer le résultat de la requête
            resultat_id_sauvegarde = curseur.fetchone() 
            
            # Fermer le curseur
            curseur.close()
            
            # Vérifier si un résultat a été trouvé
            if resultat_id_sauvegarde:
                requete_id_sauvegarde = resultat_id_sauvegarde[0]
                return requete_id_sauvegarde
            else:
                print(f"Aucun ID trouvé pour l'utilisateur {nom_sauvegarde}")
                return None

        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération de l'ID de l'utilisateur : {str(e)}")
            return None
    # obtenir livre par id
    def obtenir_titre_livre_par_id(self, id_livre):
    # Fonction similaire à obtenir_id_utilisateur, mais inverse
        # Récupérer l'ID de l'utilisateur depuis la base de données en utilisant le nom
        requete_nom_livre = "SELECT titre FROM livre WHERE id = %s"
        valeurs_nom_livre = (id_livre,)
        try:
            
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor(buffered=True)
            
            # Exécuter la requête pour récupérer l'ID de l'utilisateur
            curseur.execute(requete_nom_livre, valeurs_nom_livre)

            # Récupérer le résultat de la requête
            resultat_nom_livre = curseur.fetchone() 
            
            # Fermer le curseur
            curseur.close()
            
            # Vérifier si un résultat a été trouvé
            if resultat_nom_livre:
                nom_livre = resultat_nom_livre[0]
                return nom_livre
            else:
                return None

        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération de l'ID de l'utilisateur : {str(e)}")
            return None
    # obtenir le nom avec l'id de l'utilisateur    
    def obtenir_nom_utilisateur_par_id(self, id_usager):
        requete_nom_usager = "SELECT nom FROM usager WHERE id = %s"
        valeurs_nom_usager = (id_usager,)
        try:
            curseur = self.connexion_bd.cursor(buffered=True)
            curseur.execute(requete_nom_usager, valeurs_nom_usager)
            resultat_nom_usager = curseur.fetchone()
            curseur.close()
            
            # si je trouve des résultats
            if resultat_nom_usager:
                nom_usager = resultat_nom_usager[0]
                return nom_usager
            else:
                return None

        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération du nom de l'utilisateur : {str(e)}")
            return None
    # obtenir le id du nom de l'arme    
    def obtenir_id_arme_par_nom(self, nom_arme):
        try:
            curseur = self.connexion_bd.cursor()

            # Appel de la fonction stockée pour obtenir l'ID de l'arme avec le nom donné
            requete_id_arme = "SELECT trouver_id_arme_avec_nom(%s)"
            curseur.execute(requete_id_arme, (nom_arme,))

            # Récupérer le résultat de la fonction
            id_arme = curseur.fetchone()[0]

            curseur.close()
            return id_arme

        except mysql.connector.Error as e:
            print(f"Erreur lors de l'obtention de l'ID de l'arme : {str(e)}")
            return None
    # récup la fiche de perso    
    def recuperer_id_fiche_perso(self, nom_sauvegarde):
        try:
              # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()

            # Exécuter la requête pour récupérer l'ID de la fiche personnage
            requete = "SELECT id_fiche_personnage FROM sauvegarde WHERE nom_sauvegarde = %s"
            curseur.execute(requete, (nom_sauvegarde,))

            # Récupérer l'ID de la fiche personnage
            id_fiche = curseur.fetchone()

            # Fermer le curseur
            curseur.close()

            # Vérifier si un résultat a été trouvé
            if id_fiche:
                return id_fiche[0]
            else:
                return None

        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération de l'ID de la fiche personnage : {str(e)}")
            return None           
    # remplir la suppression  
    def remplir_combo_box_suppression(self):
        try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()

            # Exécuter la requête pour récupérer les noms des usagers depuis la base de données
            requete = "SELECT nom_sauvegarde FROM sauvegarde"
            curseur.execute(requete)

            # Récupérer les résultats de la requête
            resultats = curseur.fetchall()

            # Fermer le curseur
            curseur.close()

            # Effacer le contenu actuel du QComboBox
            self.ui.comboBox_3.clear()
            print("je suis la")
            # Ajouter les noms des usagers à la QComboBox
            for resultat in resultats:
                nom_sauvegarde = resultat[0]
                self.ui.comboBox_3.addItem(nom_sauvegarde)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération des usagers : {str(e)}")         
    # remplir la boîte des livres        
    def remplir_combo_box_livres(self):
        try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()
            # Exécuter la requête pour récupérer les noms des livres depuis la base de données (remplacez 'livres', 'nom' par vos noms réels)
            requete = "SELECT titre FROM livre"
            curseur.execute(requete)
            # Récupérer les résultats de la requête
            resultats = curseur.fetchall()
            # Fermer le curseur
            curseur.close()

            # Ajouter les noms des livres à la QComboBox
            for resultat in resultats:
                nom_livre = resultat[0]  # Supposons que le nom du livre est dans la première colonne
                self.ui.comboBox_livre_sauvegarde.addItem(nom_livre)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération des livres : {str(e)}")
    # remplir la boîte usager        
    def remplir_combo_box_usager(self):
        try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()

            # Exécuter la requête pour récupérer les noms des usagers depuis la base de données
            requete = "SELECT nom FROM usager"
            curseur.execute(requete)

            # Récupérer les résultats de la requête
            resultats = curseur.fetchall()

            # Fermer le curseur
            curseur.close()

            # Effacer le contenu actuel du QComboBox
            self.ui.comboBox_utilisateur_sauvegarde.clear()

            # Ajouter les noms des usagers à la QComboBox
            for resultat in resultats:
                nom_usager = resultat[0]
                self.ui.comboBox_utilisateur_sauvegarde.addItem(nom_usager)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération des usagers : {str(e)}")
    # remplir la boîte de sauvegarde
    def remplir_combo_box_sauvegarder(self):
         try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()

            # Exécuter la requête pour récupérer les noms des usagers depuis la base de données
            requete = "SELECT nom_sauvegarde FROM sauvegarde"
            curseur.execute(requete)

            # Récupérer les résultats de la requête
            resultats = curseur.fetchall()

            # Fermer le curseur
            curseur.close()

            # Effacer le contenu actuel du QComboBox
            self.ui.comboBox_chargernom_sauvegarde.clear()
            self.ui.comboBox_3.clear()
            # Ajouter les noms des usagers à la QComboBox
            for resultat in resultats:
                nom_sauvegarde = resultat[0]
                self.ui.comboBox_chargernom_sauvegarde.addItem(nom_sauvegarde)
                self.ui.comboBox_3.addItem(nom_sauvegarde)

         except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération des usagers : {str(e)}")          
    # remplir la boîte de discipline       
    def remplir_combo_box_discipline(self):
        try:
            
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()

            # Exécuter la requête pour récupérer les noms des usagers depuis la base de données
            requete = "SELECT text FROM discipline"
            curseur.execute(requete)

            # Récupérer les résultats de la requête
            resultats = curseur.fetchall()

            # Fermer le curseur
            curseur.close()

            # Ajouter les noms des usagers à la QComboBox
            for resultat in resultats:
                nom_discipline = resultat[0]
                # ajouter pour les 5 combobox
                self.ui.comboBox_3_discipline1.addItem(nom_discipline )
                self.ui.comboBox_4_discipline2.addItem(nom_discipline )
                self.ui.comboBox_5_discipline3.addItem(nom_discipline )
                self.ui.comboBox_6_discipline4.addItem(nom_discipline )
                self.ui.comboBox_7_discipline5.addItem(nom_discipline )

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération des usagers : {str(e)}")
    # remplir la boîte arme
    def remplir_combo_box_armes(self):
        try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor()

            # Exécuter la requête pour récupérer les noms des usagers depuis la base de données
            requete = "SELECT nom FROM armes"
            curseur.execute(requete)

            # Récupérer les résultats de la requête
            resultats = curseur.fetchall()

            # Fermer le curseur
            curseur.close()
            
            # Ajouter les noms des usagers à la QComboBox
            for resultat in resultats:
                armes = resultat[0]
                self.ui.Combobox_arme1.addItem(armes)
                self.ui.Combobox_arme2.addItem(armes)
              

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération des usagers : {str(e)}")       
    # pour charger une sauvegarde       
    def charger_sauvegarde(self):
         # Récupérer le nom de la sauvegarde depuis le combobox
        nom_sauvegarde = self.ui.comboBox_chargernom_sauvegarde.currentText()

        # Appeler la fonction pour obtenir l'ID de la sauvegarde
        id_sauvegarde = self.obtenir_id_sauvegarde(nom_sauvegarde)

        if id_sauvegarde is not None:
            # Appeler une fonction pour charger les informations de la sauvegarde
            self.remplir_combo_box_discipline()
            self.remplir_combo_box_armes()
            self.charger_sauvegarde_information(id_sauvegarde)
        else:
            QMessageBox.warning(self, "Avertissement", "Sauvegarde non trouvée.") 
    # modifier id du chapitre après avoir charger       
    def modifier_id_chapitre_sauvegarde(self, id_sauvegarde, id_chapitre):
        try:
            curseur = self.connexion_bd.cursor()

            # Requête SQL pour mettre à jour l'id_chapitre de la sauvegarde
            requete = "UPDATE sauvegarde SET id_chapitre = %s WHERE id = %s"
            curseur.execute(requete, (id_chapitre, id_sauvegarde))

            # Valider la transaction
            self.connexion_bd.commit()

            QMessageBox.information(self, "Succès", "Id_chapitre de la sauvegarde modifié avec succès.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification de l'id_chapitre : {str(e)}")          
    
    ### charger chapitre ###
    def charger_chapitre(self, id_chapitre) :
        # Assumez que self.connexion_bd est votre connexion à la base de données
        try:
            nom_sauvegarde = self.ui.comboBox_chargernom_sauvegarde.currentText()
            id_sauvegarde = self.obtenir_id_sauvegarde(nom_sauvegarde)
            curseur = self.connexion_bd.cursor(dictionary=True)
            
            print("l'id de chapitre :", id_chapitre)
            # Remplacez "votre_table_chapitre" par le nom réel de votre table de chapitres
            requete = "SELECT texte FROM chapitre WHERE id = %s"
            curseur.execute(requete, (id_chapitre,))

            resultat = curseur.fetchone()
            
            if resultat:
                texte_chapitre = resultat['texte']
                self.ui.textEdit_chapitre.setPlainText(texte_chapitre)
            else:
                self.ui.textEdit_chapitre.setPlainText("Chapitre non trouvé")

            curseur.close()

            curseur = self.connexion_bd.cursor(dictionary=True)

            # Exécutez la requête SQL pour obtenir les numéros de chapitre de destination
            requete = "SELECT no_chapitre_destination FROM lien_chapitre WHERE no_chapitre_origine = %s"
            
            curseur.execute(requete, (id_chapitre,))

            # Récupérez les résultats de la requête
            resultats = curseur.fetchall()

            # on clear pour éviter l'ajout
            self.ui.comboBox_choix_chapitre.clear()

            # on sort les résultats
            for resultat in resultats:
                no_chapitre_destination = resultat['no_chapitre_destination']
                self.ui.comboBox_choix_chapitre.addItem(str(no_chapitre_destination))

            # je close le curseur
            curseur.close()
            self.modifier_id_chapitre_sauvegarde(id_sauvegarde,id_chapitre)
            
        except mysql.connector.Error as e:
            print(f"Erreur lors du chargement du chapitre : {str(e)}")
    
    ### charger lien chapitre ###     
    def charger_lien_chapitre(self):
        id_chapitre_direction = self.ui.comboBox_choix_chapitre.currentText()
        self.charger_chapitre(id_chapitre_direction)
    
    ### charger les sauvegardes informations ###       
    def charger_sauvegarde_information(self, id_sauvegarde): 
        try:
            # Créer un curseur pour exécuter les requêtes SQL
            curseur = self.connexion_bd.cursor(dictionary=True)

            # Exécuter la requête pour récupérer les informations de la sauvegarde
            requete = """
            SELECT nom_sauvegarde, id_usager, id_livre, id_fiche_personnage, id_chapitre
            FROM sauvegarde
            WHERE id = %s
            """
            curseur.execute(requete, (id_sauvegarde,))

            # Récupérer les résultats de la requête
            resultat_sauvegarde = curseur.fetchone()
            print(resultat_sauvegarde)
            # Fermer le curseur
            curseur.close()

            if resultat_sauvegarde:
                nom_sauvegarde = resultat_sauvegarde['nom_sauvegarde']
                id_usager = resultat_sauvegarde['id_usager']
                id_fiche_personnage = resultat_sauvegarde['id_fiche_personnage']
                id_chapitre = resultat_sauvegarde['id_chapitre']
                
                # Mettre à jour les champs dans l'interface graphique avec les informations de la sauvegarde
                self.ui.lineEdit_nom_sauvegarde.setText(nom_sauvegarde)
                 # Mettre à jour la QComboBox pour l'utilisateur
                nom_utilisateur = self.obtenir_nom_utilisateur_par_id(id_usager)
                self.ui.comboBox.addItem(nom_utilisateur)
                self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(nom_utilisateur))
                # Mettre à jour la QComboBox pour le livre
                self.ui.comboBox_2.addItem(nom_sauvegarde)
                self.ui.comboBox_2.setCurrentIndex(self.ui.comboBox_2.findText(nom_sauvegarde))
                
                self.charger_chapitre(id_chapitre)
                
                requete_fiche_personnage = """
                SELECT id_discipline1,id_discipline2,id_discipline3,id_discipline4,id_discipline5, repas, objet, id_armes1, id_armes2, bourse, objet_special
                FROM fiche_personnage
                WHERE id = %s
                """
                
                curseur = self.connexion_bd.cursor(dictionary=True)
                curseur.execute(requete_fiche_personnage, (id_fiche_personnage,))
                resultat_fiche_personnage = curseur.fetchone()
                
                curseur.close()
                if resultat_fiche_personnage:
                    id_discipline1 = resultat_fiche_personnage['id_discipline1']
                    id_discipline2 = resultat_fiche_personnage['id_discipline2']
                    id_discipline3 = resultat_fiche_personnage['id_discipline3']
                    id_discipline4 = resultat_fiche_personnage['id_discipline4']
                    id_discipline5 = resultat_fiche_personnage['id_discipline5']
                    repas = resultat_fiche_personnage['repas']
                    objet = resultat_fiche_personnage['objet']
                    id_armes1 = resultat_fiche_personnage['id_armes1']
                    id_armes2 = resultat_fiche_personnage['id_armes2']
                    bourse = resultat_fiche_personnage['bourse']
                    objet_special = resultat_fiche_personnage['objet_special']
                    
                    # inséré les données dans chaque boite

                    # Disciplines et gestion des disciplines vide pour empêcher de planter
                    if id_discipline3 is not None:
                        self.ui.comboBox_3_discipline1.setCurrentIndex(id_discipline1)
                    else:
                        self.ui.comboBox_3_discipline1.setCurrentIndex(0)
                    if id_discipline3 is not None:
                        self.ui.comboBox_4_discipline2.setCurrentIndex(id_discipline2)
                    else:
                        self.ui.comboBox_4_discipline2.setCurrentIndex(0) 
                    if id_discipline3 is not None:
                        self.ui.comboBox_5_discipline3.setCurrentIndex(id_discipline3)
                    else:
                        self.ui.comboBox_5_discipline3.setCurrentIndex(0) 
                    if id_discipline3 is not None:
                        self.ui.comboBox_6_discipline4.setCurrentIndex(id_discipline4)
                    else:
                        self.ui.comboBox_6_discipline4.setCurrentIndex(0) 
                    if id_discipline3 is not None:
                        self.ui.comboBox_7_discipline5.setCurrentIndex(id_discipline5)
                    else:
                        self.ui.comboBox_7_discipline5.setCurrentIndex(0)  
                    
                    # Repas et Objet
                    self.ui.textEdit_Repas.setText(repas)
                    self.ui.textEdit_objet.setText(objet)

                    # Armes
                    if id_armes1 is not None:
                        self.ui.Combobox_arme1.setCurrentIndex(id_armes1)
                    else:
                        self.ui.Combobox_arme1.setCurrentIndex(0)
                    if id_armes2 is not None:
                        self.ui.Combobox_arme2.setCurrentIndex(id_armes2)
                    else:
                        self.ui.Combobox_arme2.setCurrentIndex(0)
                        
                    # Bourse
                    if bourse is not None:
                        self.ui.spinBox_bourse.setValue(bourse)

                    # Objet spécial
                    self.ui.textEdit_objet_special.setText(objet_special)
                
                QMessageBox.information(self, "Succès", "Sauvegarde chargée avec succès.")
            else:
                QMessageBox.warning(self, "Avertissement", "Sauvegarde non trouvée.")
             
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement de la sauvegarde : {str(e)}")

    ### Supprimer ###
    def supprimer_sauvegarde(self):
        nom_sauvegarde = self.ui.comboBox_3.currentText()
        id_sauvegarde = self.obtenir_id_sauvegarde(nom_sauvegarde)
        
        try:
            curseur = self.connexion_bd.cursor()
            # Requête SQL pour supprimer la sauvegarde en utilisant son ID
            requete = "DELETE FROM sauvegarde WHERE id = %s"
            curseur.execute(requete, (id_sauvegarde,))
        
            # Valider la transaction
            self.connexion_bd.commit()

            # Mise à jour de la QComboBox après la suppression
            
            self.remplir_combo_box_sauvegarder()
            
            # message d'erreur
            QMessageBox.information(self, "Succès", "Sauvegarde supprimée avec succès.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression de la sauvegarde : {str(e)}")
    
    ### Enregistrer ###
    def enregistrer_fiche_joueur(self):
        try:
            # Récupérer les informations depuis l'interface graphique
            nom_fiche = self.ui.comboBox_2.currentText()
            id_fiche_personnage =  self.recuperer_id_fiche_perso(nom_fiche)
            # empêcher de lancer sans sauvegarde
            if id_fiche_personnage == None:
                QMessageBox.information(self, "problème d'enregistrement", "Vous devez lancer une partie pour enregistrer", QMessageBox.Ok, QMessageBox.NoButton)

                return
            
            discipline1 = self.ui.comboBox_3_discipline1.currentText()
            discipline2 = self.ui.comboBox_4_discipline2.currentText()
            discipline3 = self.ui.comboBox_5_discipline3.currentText()
            discipline4 = self.ui.comboBox_6_discipline4.currentText()
            discipline5 = self.ui.comboBox_7_discipline5.currentText()
            repas = self.ui.textEdit_Repas.toPlainText()
            objet = self.ui.textEdit_objet.toPlainText()
            id_armes1 = self.obtenir_id_arme_par_nom(self.ui.Combobox_arme1.currentText())
            id_armes2 = self.obtenir_id_arme_par_nom(self.ui.Combobox_arme2.currentText())
            bourse = self.ui.spinBox_bourse.value()
            objet_special = self.ui.textEdit_objet_special.toPlainText()

            

            # Mettre à jour les informations dans la base de données
            curseur = self.connexion_bd.cursor()
            requete_update = """
            UPDATE fiche_personnage
            SET id_discipline1 = (SELECT id FROM discipline WHERE text = %s),
                id_discipline2 = (SELECT id FROM discipline WHERE text = %s),
                id_discipline3 = (SELECT id FROM discipline WHERE text = %s),
                id_discipline4 = (SELECT id FROM discipline WHERE text = %s),
                id_discipline5 = (SELECT id FROM discipline WHERE text = %s),
                repas = %s, objet = %s, id_armes1 = %s,id_armes2 = %s, bourse = %s, objet_special = %s
            WHERE id = %s
            """
            valeurs_update = (discipline1, discipline2, discipline3, discipline4, discipline5,
                              repas, objet, id_armes1,id_armes2, bourse, objet_special, id_fiche_personnage)
            curseur.execute(requete_update, valeurs_update)
            self.connexion_bd.commit()
            curseur.close()

            # message d'erreur
            QMessageBox.information(self, "Succès", "Informations du personnage enregistrées avec succès.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement des informations du personnage : {str(e)}")
        
# le main pour lancer l'écran
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
