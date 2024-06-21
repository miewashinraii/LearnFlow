CREATE DATABASE my_database;
USE my_database;
CREATE TABLE my_table (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO my_table (name, email, password) VALUES
    ('John Doe', 'johndoe@example.com', 'password123'),
    ('Jane Smith', 'janesmith@example.com', 'secret456'),
    ('Bob Johnson', 'bobjohnson@example.com', 'abc123'),
    ('Alice Williams', 'alicewilliams@example.com', 'qwerty'),
    ('Tom Davis', 'tomdavis@example.com', 'password789');
