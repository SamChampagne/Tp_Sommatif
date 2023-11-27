USE tp_sommatif;

/*
DELIMITER $$

CREATE FUNCTION trouver_id_fiche_avec_nom(nom_sauvegarde VARCHAR(255))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE id_fiche INT;

    -- Requête pour récupérer l'ID de l'arme avec le nom donné
    SELECT id_fiche_sauvegarde INTO id_fiche FROM sauvegarde

    -- Retourne l'ID de l'arme
    RETURN id_fiche;
END $$

DELIMITER ;
*/

# fonction qui sert à trouver id chapitre actuelle d'une sauvegarde
DELIMITER $$

CREATE FUNCTION trouver_id_chapitre_avec_sauvegarde(nom_sauvegarde VARCHAR(255))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE chapitre_id INT;

    SELECT id_chapitre INTO chapitre_id
    FROM sauvegarde
    WHERE nom_sauvegarde = nom_sauvegarde
    LIMIT 1;

    RETURN chapitre_id;
END $$

DELIMITER ;

# permet de trouver une id_arme à partir de son nom
CREATE FUNCTION trouver_id_arme_avec_nom(nom_arme VARCHAR(255))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE id_arme INT;

    -- Requête pour récupérer l'ID de l'arme avec le nom donné
    SELECT id INTO id_arme
    FROM armes
    WHERE nom = nom_arme;

    -- Retourne l'ID de l'arme
    RETURN id_arme;
END $$

DELIMITER ;


SELECT trouver_id_arme_avec_nom("Le poignard");
SHOW FUNCTION STATUS WHERE Db = 'tp_sommatif' AND Name = 'trouver_id_arme_avec_nom';
SELECT no_chapitre_destination FROM lien_chapitre WHERE id = 1
