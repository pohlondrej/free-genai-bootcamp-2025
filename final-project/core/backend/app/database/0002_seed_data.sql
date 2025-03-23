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

-- Insert sample study sessions
INSERT OR REPLACE INTO study_sessions (id, group_id, activity_type, created_at, completed_at) VALUES
(1, 1, 'vocabulary_quiz', '2025-03-23 05:00:00', '2025-03-23 05:10:00'),
(2, 2, 'kanji_practice', '2025-03-23 05:15:00', NULL),
(3, 3, 'writing_practice', '2025-03-23 05:30:00', '2025-03-23 05:45:00');

-- Insert sample word review items
INSERT OR REPLACE INTO word_review_items (id, word_id, study_session_id, correct, created_at) VALUES
(1, 1, 1, TRUE, '2025-03-23 05:05:00'),  -- こんにちは correct
(2, 2, 1, FALSE, '2025-03-23 05:07:00'), -- 私 incorrect
(3, 3, 1, TRUE, '2025-03-23 05:09:00');  -- さようなら correct
