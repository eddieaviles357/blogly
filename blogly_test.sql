-- from the terminal run:
-- psql < blogly.sql

DROP DATABASE IF EXISTS blogly;
CREATE DATABASE blogly;

\c blogly

CREATE TABLE users
(
  id SERIAL PRIMARY KEY,
  f_name VARCHAR(20) NOT NULL,
  l_name VARCHAR(20) NOT NULL,
  img_url VARCHAR(200) NOT NULL
);

CREATE TABLE posts
(
  id SERIAL PRIMARY KEY,
  title VARCHAR(30) NOT NULL,
  content VARCHAR(300) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  user_id INTEGER REFERENCES users ON DELETE CASCADE
);

INSERT INTO users (f_name,l_name,img_url) 
VALUES 
('ed', 'aviles', 'https://images.unsplash.com/photo-1568602471122-7832951cc4c5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80'), 
('noah', 'aviles', 'https://images.unsplash.com/photo-1552374196-c4e7ffc6e126?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80'), 
('eric', 'aviles', 'https://images.unsplash.com/photo-1623605931891-d5b95ee98459?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1494&q=80'),
('nancy', 'aviles', 'https://images.unsplash.com/photo-1614436163996-25cee5f54290?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1042&q=80'),
('shirley', 'temple', 'https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80');


INSERT INTO posts (title, content, created_at, user_id)
VALUES
('titleone', 'just testing this table', '2022-04-20 09:00:00',1),
('titleone', 'sencode test nad i dont know hwat im doing', '2021-04-20 09:22:00',1),
('hahah', 'just laughing away', '2021-02-04 04:05:00',2),
('hahah', 'tmi will be the death of me', '2019-02-04 04:05:00',3),
('lolololo', 'lol is laugh out loud and doing many times', '2020-04-20 10:00:00',4),
('lolololo', 'psting is hard', '2020-04-20 10:00:00',4);