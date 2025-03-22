-- migrations/0002_seed_data.sql

-- Insert sample words
INSERT INTO words (japanese, romaji, english) VALUES
('こんにちは', 'Konnichiwa', 'Hello'),
('ありがとう', 'Arigatou', 'Thank you'),
('おはようございます', 'Ohayou gozaimasu', 'Good morning'),
('こんばんは', 'Konbanwa', 'Good evening'),
('さようなら', 'Sayounara', 'Goodbye');