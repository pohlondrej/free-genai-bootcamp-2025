-- Initialize database schema

-- Independent tables first
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    word_level TEXT NOT NULL,
    japanese TEXT NOT NULL,
    kana TEXT NOT NULL,
    romaji TEXT,
    english TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS kanji (
    id INTEGER PRIMARY KEY,
    kanji_level TEXT NOT NULL,
    symbol TEXT NOT NULL,
    primary_meaning TEXT NOT NULL,
    primary_reading TEXT NOT NULL,
    primary_reading_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- Tables with foreign keys
CREATE TABLE IF NOT EXISTS word_groups (
    id INTEGER PRIMARY KEY,
    word_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words (id),
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY,
    study_session_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (study_session_id) REFERENCES study_sessions (id),
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

CREATE TABLE IF NOT EXISTS word_review_items (
    id INTEGER PRIMARY KEY,
    word_id INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words (id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions (id)
);
