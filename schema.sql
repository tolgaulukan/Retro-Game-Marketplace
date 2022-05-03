DROP TABLE if exists ads;

CREATE TABLE ads (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    image_url varchar(200),
    price_in_cents integer NOT NULL
);