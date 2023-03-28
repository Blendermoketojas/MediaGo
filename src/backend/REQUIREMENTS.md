RASYK CIA KO REIKIA
(#. "Kam skirtas metodas" / "Ka siusi per linka" / "ka nori gauti is linko" : "Vardas, kaz uzprase")
pvz.:
1. Registruoju vartotoja / nickname, email, password / id, nickname, "personal access token" : Tadas;
2. GET/POST/PUT/DELETE song many to one playlist / playlist_id, link / id, playlist_id, link : Tadas
3. GET/POST/PUT/DELETE playlist / user_id, name, description, is_selected, (Default False) / id, name, description, is_selected (boolean) : Tadas
4. GET/POST/PUT/DELETE Server / name, owner (default owneris kuris sukure, siusiu user id), theme (Default - 'default') / id, name, owner, theme, users = (Array: id, nickname, level) : Tadas
5. Gauti users kambaryje / server_id / users = (Array: id, nickname, level) : Renaldas

1. NOTE: User ir Server turetu turet many to many rysi, kadangi serveris tures daug useriu ir useris tures daug issaugotu serveriu is kuriu gali pasirinkti : Tadas
2. NOTE: server table admins gali but json array su useriu ids kurie adminai arba atskiras table : Tadas
3. NOTE: GET song turetu turet ir GET all kad gauti visas dainas pagal playlist_id
4. Del playlist tai one to many su user, useris turi daug playlist
-------------------------------------------------------------------------------------------

song_name varchar(20)

curl -X POST -H "Content-type: application/json" -d "{\"nickname\" : \"tadelis\", \"email\" : \"tadelistadelis@gmail.com\", \"password\" : \"tadelis123\"}" "localhost:5000/register"

curl -X POST -H "Content-type: application/json" -d "{\"email\" : \"tadelistadelis@gmail.com\", \"password\" : \"tadelis123\"}" "localhost:5000/login"
