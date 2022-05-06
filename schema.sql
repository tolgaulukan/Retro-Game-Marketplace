DROP TABLE if exists ads;
DROP TABLE if exists users;
DROP TABLE if exists wishlist;
CREATE TABLE ads (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    image_url varchar(500),
    price_in_cents integer NOT NULL,
    description varchar(250) NOT NULL,
    mobile varchar(20) NOT NULL
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    password varchar(200) NOT NULL
     
);

CREATE TABLE wishlist (
    id serial PRIMARY KEY, 
    name varchar(50),
    customer_id integer NOT NULL
);