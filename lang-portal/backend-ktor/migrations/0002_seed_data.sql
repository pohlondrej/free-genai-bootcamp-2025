-- migrations/0002_seed_data.sql

-- Insert sample words
INSERT INTO words (japanese, romaji, english) VALUES
('こんにちは', 'Konnichiwa', 'Hello'),
('ありがとう', 'Arigatou', 'Thank you'),
('おはようございます', 'Ohayou gozaimasu', 'Good morning'),
('こんばんは', 'Konbanwa', 'Good evening'),
('さようなら', 'Sayounara', 'Goodbye');

-- Insert sample groups
INSERT INTO groups (name) VALUES
('Basic Greetings'),
('Numbers'),
('Days of the week');

-- Insert word_groups relationships
INSERT INTO word_groups (word_id, group_id) VALUES
(1, 1), -- こんにちは in Basic Greetings
(2, 1), -- ありがとう in Basic Greetings
(3, 1), -- おはようございます in Basic Greetings
(4, 1), -- こんばんは in Basic Greetings
(5, 1), -- さようなら in Basic Greetings
(2, 2), -- ありがとう (can be in multiple groups if needed) in Numbers - example of re-use
(3, 3); -- おはようございます in Days of the week - example of re-use

-- Insert sample study_activities (assuming you have some predefined activities, for now just names)
INSERT INTO study_activities (study_session_id, group_id, created_at) VALUES
(1, 1, '2024-01-01 10:00:00'), -- Example study activity for Basic Greetings
(2, 2, '2024-01-02 14:00:00'); -- Example study activity for Numbers

-- Insert sample study_sessions
INSERT INTO study_sessions (group_id, created_at, study_activity_id) VALUES
(1, '2024-01-01 10:00:00', 1), -- Study session for Basic Greetings
(2, '2024-01-02 14:00:00', 2); -- Study session for Numbers

-- Insert sample word_review_items (assuming some study sessions have occurred)
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES
(1, 1, TRUE, '2024-01-01 10:05:00'), -- User got "こんにちは" correct in session 1
(2, 1, FALSE, '2024-01-01 10:10:00'), -- User got "ありがとう" wrong in session 1
(3, 1, TRUE, '2024-01-01 10:15:00'),
(4, 2, TRUE, '2024-01-02 14:05:00'),
(5, 2, TRUE, '2024-01-02 14:10:00');
