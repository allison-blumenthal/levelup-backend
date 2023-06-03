SELECT * FROM levelupapi_gamer;

SELECT * FROM levelupapi_eventgamer;

DELETE FROM levelupapi_eventgamer WHERE gamer_id = 2;

INSERT INTO levelupapi_gamer (id, uid, bio)
VALUES (1, "123456asddfg123456asddfg", "My name is Hex");
