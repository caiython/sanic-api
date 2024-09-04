INSERT INTO app_game (uuid, title, release_date, creation_datetime) 
VALUES ($uuid, $title, $release_date, $creation_datetime)
RETURNING uuid, title, release_date, creation_datetime