-- migrations/0002_seed_data.sql

-- Insert sample words
INSERT INTO words (word_level, japanese, kana, romaji, english) VALUES
('N5', 'こんにちは', 'こんにちは', 'Konnichiwa', 'Hello'),
('N5', '私', 'わたし', 'Watashi', 'I'),
('N5', 'さようなら', 'さようなら', 'Sayounara', 'Goodbye');

-- Insert sample kanji
INSERT INTO kanji (kanji_level, symbol, primary_meaning, primary_reading, primary_reading_type) VALUES
('N5', '大', 'Big', 'たい', 'onyomi'),
('N3', '菜', 'Vegetable', 'さい', 'onyomi');
