-- JLPT N5 Rentaishi Import Script

BEGIN TRANSACTION;

INSERT INTO words (word_level, japanese, kana, romaji, english) VALUES
('N5', 'あの', 'あの', 'ano', 'that'),
('N5', '小さな', 'ちいさな', 'chiisana', 'small'),
('N5', 'どんな', 'どんな', 'donna', 'what kind of'),
('N5', 'どの', 'どの', 'dono', 'which'),
('N5', 'こんな', 'こんな', 'konna', 'such'),
('N5', 'この', 'この', 'kono', 'this'),
('N5', '大きな', 'おおきな', 'ookina', 'big'),
('N5', 'その', 'その', 'sono', 'that');

COMMIT;