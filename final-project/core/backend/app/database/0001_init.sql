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
CREATE TABLE IF NOT EXISTS group_items (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    item_type TEXT NOT NULL CHECK (item_type IN ('word', 'kanji')),
    item_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups (id),
    -- Note: We can't have a single FK for item_id since it references different tables
    -- Instead, we ensure integrity at the application level
    UNIQUE(group_id, item_type, item_id)  -- Prevent duplicate items in a group
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

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_group_items_lookup ON group_items(item_type, item_id);
CREATE INDEX IF NOT EXISTS idx_word_reviews_word ON word_review_items(word_id);
CREATE INDEX IF NOT EXISTS idx_word_reviews_session ON word_review_items(study_session_id);
