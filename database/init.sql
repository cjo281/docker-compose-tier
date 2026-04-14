-- Create a simple table for testing
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL
);

-- Insert sample data
INSERT INTO messages (content) VALUES ('Hello from PostgreSQL!');