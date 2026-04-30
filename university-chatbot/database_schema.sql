CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(50),
    question TEXT,
    answer TEXT,
    intent_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(100),
    query TEXT,
    intent_detected VARCHAR(100),
    confidence_score FLOAT,
    response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER,
    rating INTEGER,
    comment TEXT,
    FOREIGN KEY (query_id) REFERENCES user_queries(id)
);
