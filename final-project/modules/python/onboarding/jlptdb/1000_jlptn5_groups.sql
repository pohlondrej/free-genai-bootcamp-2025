-- JLPT N5 Group Import Script

BEGIN TRANSACTION;

INSERT INTO groups (id, name) VALUES
(1001,'JLPT N5'),
(1002,'JLPT N5 Kanji'),
(1003,'JLPT N5 Words'),
(1004,'JLPT N5 Nouns'),
(1005,'JLPT N5 Verbs'),
(1006,'JLPT N5 Adjectives'),
(1007,'JLPT N5 Adverbs'),
(1008,'JLPT N5 Rentaishi'),
(1009,'JLPT N5 Katakana');

COMMIT;

