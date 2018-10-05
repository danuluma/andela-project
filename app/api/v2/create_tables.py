q1 = """CREATE TABLE users (
       id serial primary key,
       first_name varchar(20) not null,
       last_name varchar(20) not null,
       username varchar(80) unique not null,
       email varchar(80) unique not null,
       password varchar(80) not null,
       phone varchar(12) unique,
       role integer
);"""

q5 = """CREATE TABLE  roles (
       id integer primary key,
       access_level varchar not null

);"""

q6 = """CREATE TABLE  users_roles (
       users_id integer references users(id),
       roles_id integer references roles(id)
);"""


q2 = """CREATE TABLE orders (
       id serial primary key,
       price integer not null,
       description text,
       ordered_by int references users(id),
       order_date timestamp,
       status integer
);"""

q3 = """CREATE TABLE categories (
       name varchar(80) primary key,
       description text
);"""

q4 = """CREATE TABLE menu (
       id serial primary key,
       title varchar not null,
       category varchar(80) references categories(name),
       description text,
       image_url varchar,
       price integer not null
);"""

q7 = """
       INSERT INTO users (first_name, last_name, username, email, password, phone, role) VALUES ('admin', 'user', 'admin1', 'secret@admin.com', 'admintest', '0701234567', 1);
       INSERT INTO roles (id, access_level)VALUES (1, 'admin');
       INSERT INTO roles (id, access_level)VALUES (2, 'user');
       INSERT INTO categories (name, description)VALUES ('fish', 'Lorem ipsum');
    """

create_tables = [q1, q5, q2, q3, q4, q7]
