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

-- Insert sample groups
INSERT INTO groups (name) VALUES
('Basic Greetings'),      -- id 1
('JLPT N5 Essential'),    -- id 2
('Common Kanji'),         -- id 3
('Daily Vocabulary');     -- id 4

-- Link words to groups
INSERT INTO word_groups (word_id, group_id) VALUES
(1, 1),  -- こんにちは -> Basic Greetings
(1, 2),  -- こんにちは -> JLPT N5 Essential
(2, 2),  -- 私 -> JLPT N5 Essential
(2, 4),  -- 私 -> Daily Vocabulary
(3, 1),  -- さようなら -> Basic Greetings
(3, 2);  -- さようなら -> JLPT N5 Essential
