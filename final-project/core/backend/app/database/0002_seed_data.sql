-- migrations/0002_seed_data.sql

-- Insert or update sample words
INSERT OR REPLACE INTO words (id, word_level, japanese, kana, romaji, english) VALUES
(1, 'N5', 'こんにちは', 'こんにちは', 'Konnichiwa', 'Hello'),
(2, 'N5', '私', 'わたし', 'Watashi', 'I'),
(3, 'N5', 'さようなら', 'さようなら', 'Sayounara', 'Goodbye');

-- Insert or update sample kanji
INSERT OR REPLACE INTO kanji (id, kanji_level, symbol, primary_meaning, primary_reading, primary_reading_type) VALUES
(1, 'N5', '大', 'Big', 'たい', 'onyomi'),
(2, 'N3', '菜', 'Vegetable', 'さい', 'onyomi');

-- Insert or update sample groups
INSERT OR REPLACE INTO groups (id, name) VALUES
(1, 'Basic Greetings'),
(2, 'JLPT N5 Essential'),
(3, 'Common Kanji'),
(4, 'Daily Vocabulary');

-- Link items to groups (using INSERT OR IGNORE since we have a UNIQUE constraint)
INSERT OR IGNORE INTO group_items (group_id, item_type, item_id) VALUES
-- Words in groups
(1, 'word', 1),  -- こんにちは -> Basic Greetings
(2, 'word', 1),  -- こんにちは -> JLPT N5 Essential
(2, 'word', 2),  -- 私 -> JLPT N5 Essential
(4, 'word', 2),  -- 私 -> Daily Vocabulary
(1, 'word', 3),  -- さようなら -> Basic Greetings
(2, 'word', 3),  -- さようなら -> JLPT N5 Essential
-- Kanji in groups
(2, 'kanji', 1), -- 大 -> JLPT N5 Essential
(3, 'kanji', 1), -- 大 -> Common Kanji
(3, 'kanji', 2); -- 菜 -> Common Kanji
