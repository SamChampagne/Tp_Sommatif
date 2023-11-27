use tp_sommatif;

DROP USER IF EXISTS 'tp_sommatif';

CREATE USER 'tp_sommatif' IDENTIFIED BY 'tp_sommatif';


GRANT SELECT, INSERT, DELETE, UPDATE ON tp_sommatif. * TO 'tp_sommatif';
