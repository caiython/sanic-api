CREATE TABLE app_game (
    uuid TEXT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    creation_datetime DATE NOT NULL
);
