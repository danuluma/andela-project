CREATE TABLE users (
       id serial primary key,
       first_name varchar(20) not null,
       last_name varchar(20) not null,
       username varchar(80) unique not null,
       email varchar(80) unique not null,
       password varchar(80) not null,
       phone varchar(12) unique,
);

CREATE TABLE  roles (
       id serial primary key,
       role_id varchar not null,
       access_level varchar not null

);

CREATE TABLE  users_roles (
       id serial primary key,
       roles_id varchar not null,
       users_id varchar not null

);

CREATE TABLE orders (
       id serial primary key,
       price integer not null,
       description text,
       ordered_by varchar(80),
       order_date timestamp,
       status integer
);

CREATE TABLE categories (
       id serial primary key,
       name varchar(80) unique not null,
       description text
);

CREATE TABLE menu (
       id serial primary key,
       title varchar not null,
       category varchar(80),
       description text,
       image_url varchar,
       price integer not null
);
