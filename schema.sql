DROP TABLE IF EXISTS urls;
/*
 delete the urls table if it already exists.
*/

CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT, /* ID for each url */
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, /*Date the URL was shortened.*/
    original_url TEXT NOT NULL, /* original URL for which users will be redirected*/
    username TEXT NOT NULL,
    clicks INTEGER NOT NULL DEFAULT 0 /*number of times url has been clicked. Optional. Remove latter*/
);

DROP TABLE IF EXISTS users;
/*
 delete users table if it already exists.
*/

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    senha TEXT NOT NULL
);
