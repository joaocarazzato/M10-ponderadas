CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(26) NOT NULL,
    token_id VARCHAR(200) NULL
);

CREATE TABLE Images (
    id SERIAL PRIMARY KEY,
    content BYTEA NOT NULL,
    user_id INT NOT NULL
)