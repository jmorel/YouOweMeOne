DROP TABLE creditor;
CREATE TABLE creditor (
	id INTEGER PRIMARY KEY,
	name TEXT
);

DROP TABLE debitor;
CREATE TABLE debitor (
	id INTEGER PRIMARY KEY,
	creditor INTEGER,
	name TEXT,
	amount INTEGER
);

INSERT INTO creditor(name) VALUES ('Pifi');
INSERT INTO debitor(creditor, name, amount) VALUES (1, 'Basicgeek', 2);
INSERT INTO debitor(creditor, name, amount) VALUES (1, 'Popiet',182);
INSERT INTO debitor(creditor, name, amount) VALUES (1, 'Snihf', 3);
INSERT INTO debitor(creditor, name, amount) VALUES (1, 'Sab', 1);
INSERT INTO debitor(creditor, name, amount) VALUES (1, 'Delaf', 0);