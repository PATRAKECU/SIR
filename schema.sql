-- ===========================================
-- USERS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- ===========================================
-- ANALYSIS TABLE (SIR PARAMETERS)
-- Stores each SIR simulation executed by a user
-- ===========================================
CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    population INTEGER NOT NULL,
    beta REAL NOT NULL,
    gamma REAL NOT NULL,
    days INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ===========================================
-- REPORTS TABLE
-- Stores metadata for generated PDF reports
-- ===========================================
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    file_path TEXT NOT NULL,
    FOREIGN KEY (analysis_id) REFERENCES analysis(id)
);