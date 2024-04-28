CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(26) NOT NULL
);

CREATE TABLE Posts (
    id SERIAL PRIMARY KEY,
    post_name VARCHAR(50) NOT NULL,
    post_content VARCHAR(300) NOT NULL
);
