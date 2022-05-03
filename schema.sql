DROP TABLE if exists ads;
DROP TABLE if exists users;

CREATE TABLE ads (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    image_url varchar(200),
    price_in_cents integer NOT NULL
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    email varchar(50) NOT NULL,
    password varchar(200) NOT NULL
);