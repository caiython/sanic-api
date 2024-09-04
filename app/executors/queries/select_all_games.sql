SELECT *
FROM app_game
ORDER BY creation_datetime DESC
LIMIT $limit_value
OFFSET $offset_value;