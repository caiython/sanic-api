DELETE FROM app_game
WHERE uuid = $uuid
RETURNING *;