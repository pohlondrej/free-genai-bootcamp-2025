-- JLPT N5 Rentaishi Import Script

BEGIN TRANSACTION;

INSERT INTO words (id, word_level, japanese, kana, romaji, english) VALUES
(60001,'N5', 'あの', 'あの', 'ano', 'that'),
(60002,'N5', '小さな', 'ちいさな', 'chiisana', 'small'),
(60003,'N5', 'どんな', 'どんな', 'donna', 'what kind of'),
(60004,'N5', 'どの', 'どの', 'dono', 'which'),
(60005,'N5', 'こんな', 'こんな', 'konna', 'such'),
(60006,'N5', 'この', 'この', 'kono', 'this'),
(60007,'N5', '大きな', 'おおきな', 'ookina', 'big'),
(60008,'N5', 'その', 'その', 'sono', 'that');

COMMIT;

-- Add JLPT N5 Rentaishi to JLPT N5 Group

BEGIN TRANSACTION;

INSERT INTO group_items (group_id, item_type, item_id) VALUES
(1001,'word',60001),
(1001,'word',60002),
(1001,'word',60003),
(1001,'word',60004),
(1001,'word',60005),
(1001,'word',60006),
(1001,'word',60007),
(1001,'word',60008);

COMMIT;

-- Add JLPT N5 Rentaishi to JLPT N5 Words Group

BEGIN TRANSACTION;

INSERT INTO group_items (group_id, item_type, item_id) VALUES
(1003,'word',60001),
(1003,'word',60002),
(1003,'word',60003),
(1003,'word',60004),
(1003,'word',60005),
(1003,'word',60006),
(1003,'word',60007),
(1003,'word',60008);

COMMIT;

-- Add JLPT N5 Rentaishi to JLPT N5 Rentaishi Group

BEGIN TRANSACTION;

INSERT INTO group_items (group_id, item_type, item_id) VALUES
(1008,'word',60001),
(1008,'word',60002),
(1008,'word',60003),
(1008,'word',60004),
(1008,'word',60005),
(1008,'word',60006),
(1008,'word',60007),
(1008,'word',60008);

COMMIT;