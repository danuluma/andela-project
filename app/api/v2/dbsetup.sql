DROP TABLE if EXISTS users CASCADE;
CREATE TABLE users (
       id serial primary key,
       first_name varchar(20) not null,
       last_name varchar(20) not null,
       username varchar(80) unique not null,
       email varchar(80) unique not null,
       password varchar(80) not null,
       phone varchar(12) unique
);

DROP TABLE  if exists orders;
CREATE TABLE orders (
       id serial primary key,
       -- title varchar(80),
       price integer not null,
       -- body text not null,
       ordered_by varchar(80) references users (username),
       order_date timestamp,
       status integer
);

DROP TABLE  if exists categories CASCADE;
CREATE TABLE categories (
       id serial primary key,
       name varchar(80) unique not null,
       -- category varchar not null,
       description text
);

DROP TABLE  if exists menu;
CREATE TABLE menu (
       id serial primary key,
       title varchar not null,
       category varchar(80) references categories (name),
       description text,
       image_url varchar,
       price integer not null
);
