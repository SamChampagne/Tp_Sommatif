DROP DATABASE IF EXISTS tp_sommatif;
CREATE DATABASE IF NOT EXISTS tp_sommatif;
USE tp_sommatif;


### Création des tables ###
CREATE TABLE discipline(
	id INT AUTO_INCREMENT PRIMARY KEY,
	text VARCHAR(255) NOT NULL
);


CREATE TABLE armes(
	id INT AUTO_INCREMENT PRIMARY KEY,
	nom VARCHAR(255) NOT NULL
);


CREATE TABLE fiche_personnage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_discipline1 INT NULL,
    id_discipline2 INT NULL,
    id_discipline3 INT NULL,
    id_discipline4 INT NULL,
    id_discipline5 INT NULL,
    repas VARCHAR(255) NULL,
    objet VARCHAR(255) NULL,
    id_armes1 INT NULL,
    id_armes2 INT NULL,
    bourse INT NULL,
    objet_special VARCHAR(255) NULL,
    FOREIGN KEY (id_discipline1) REFERENCES discipline(id),
    FOREIGN KEY (id_discipline2) REFERENCES discipline(id),
    FOREIGN KEY (id_discipline3) REFERENCES discipline(id),
    FOREIGN KEY (id_discipline4) REFERENCES discipline(id),
    FOREIGN KEY (id_discipline5) REFERENCES discipline(id),
    FOREIGN KEY (id_armes1) REFERENCES armes(id),
    FOREIGN KEY (id_armes2) REFERENCES armes(id),
    UNIQUE (id_discipline1,id_discipline2,id_discipline3,id_discipline4,id_discipline5)
);

CREATE TABLE usager (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nom VARCHAR(64)
);

CREATE TABLE livre(
	id INT AUTO_INCREMENT PRIMARY KEY,
	titre VARCHAR(255)
);

CREATE TABLE chapitre(
	id INT AUTO_INCREMENT PRIMARY KEY,
	id_livre INT,
	no_chapitre VARCHAR(255),
	texte TEXT,
	FOREIGN KEY (id_livre) REFERENCES livre(id)
);

CREATE TABLE lien_chapitre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no_chapitre_origine INT NULL,
    no_chapitre_destination INT NULL,
    FOREIGN KEY (no_chapitre_origine) REFERENCES chapitre(id),
    FOREIGN KEY (no_chapitre_destination) REFERENCES chapitre(id)
);


CREATE TABLE sauvegarde (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_sauvegarde VARCHAR(255),
    id_usager INT,
    id_livre INT,
    id_chapitre INT,
    id_fiche_personnage INT,
    FOREIGN KEY (id_usager) REFERENCES usager(id) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES livre(id) ON DELETE CASCADE,
    FOREIGN KEY (id_chapitre) REFERENCES chapitre(id) ON DELETE CASCADE,
    FOREIGN KEY (id_fiche_personnage) REFERENCES fiche_personnage(id) ON DELETE CASCADE
);






