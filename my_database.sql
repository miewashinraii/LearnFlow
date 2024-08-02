CREATE DATABASE my_database;
USE my_database;
CREATE TABLE my_table (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
    );

USE my_database;
INSERT INTO my_table (name, email, password) VALUES
    ('Miera Honey', 'mierahoney@example.com', 'password123'),
    ('Jane Smith', 'janesmith@example.com', 'secret456'),
    ('Bob Johnson', 'bobjohnson@example.com', 'abc123'),
    ('Alice Williams', 'alicewilliams@example.com', 'qwerty'),
    ('Tom Davis', 'tomdavis@example.com', 'password789');

SELECT * FROM my_table

USE my_database;
CREATE TABLE courses (
	faculty VARCHAR(100) NOT NULL,
	code VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    semester VARCHAR(7) NOT NULL,
    lecturer VARCHAR(100) NOT NULL,
    UNIQUE (code)
	);
    
USE my_database;
ALTER TABLE courses
MODIFY COLUMN semester VARCHAR(100) NOT NULL;

USE my_database;
INSERT INTO courses (faculty, code, name, semester, lecturer) VALUES
    ('Faculty of Science and Information Technology', 'TEB3113', 'Big Data Analytics', 'May 2024', 'Ts Dr Norshakirah Ab Aziz'),
    ('Faculty of Science and Information Technology', 'TEB3024', 'Final Year Project II', 'May 2024', 'AP Ts Dr Said Jadid A Kadir'),
    ('Faculty of Science and Information Technology', 'TEB3133', 'Data Visualization', 'September 2023', 'Dr Shakirah Bt M Taib' );

USE my_database;
ALTER TABLE my_table
ADD COLUMN student_id INT;

USE my_database;
UPDATE my_table
SET student_id = 20000440
WHERE name = 'Miera Honey';

UPDATE my_table
SET student_id = 20000441
WHERE name = 'Jane Smith';

UPDATE my_table
SET student_id = 20000442
WHERE name = 'Bob Johnson';

UPDATE my_table
SET student_id = 20000443
WHERE name = 'Alice Williams';

UPDATE my_table
SET student_id = 20000444
WHERE name = 'Tom Davis';

USE my_database;
ALTER TABLE my_table
DROP COLUMN id;

USE my_database;
ALTER TABLE my_table
ADD PRIMARY KEY (student_id);

USE my_database;
ALTER TABLE courses
ADD COLUMN student_id INT,
ADD CONSTRAINT fk_student_id FOREIGN KEY (student_id) REFERENCES my_table(student_id);

ALTER TABLE courses
DROP COLUMN student_id;

USE my_database;
INSERT INTO courses (faculty, code, name, semester, lecturer) VALUES
    ('Faculty of Engineering', 'EMM3023', 'Mechanical Design', 'January 2024', 'AP Dr. Md Radzai bin Said'),
    ('Faculty of Business', 'BUS2013', 'Organizational Behavior', 'August 2023', 'Dr. Siti Fatimah binti Mohd Yassin'),
    ('Faculty of Medicine', 'MED4112', 'Clinical Pharmacology', 'June 2024', 'AP Dr. Azrul Azwar bin Ahmad Zainuddin' );

ALTER TABLE courses
ADD COLUMN student_id INT;
INSERT INTO courses (faculty, code, name, semester, lecturer, student_id)
VALUES
  ('Faculty of Science and Information Technology', 'TEB3024', 'Final Year Project II', 'May 2024', 'AP Ts Dr Said Jadid A Kadir', (SELECT student_id FROM my_table WHERE name = 'Miera Honey')),
  ('Faculty of Science and Information Technology', 'TEB3113', 'Big Data Analytics', 'May 2024', 'Ts Dr Norshakirah Ab Aziz', (SELECT student_id FROM my_table WHERE name = 'Miera Honey')),
  ('Faculty of Science and Information Technology', 'TEB3133', 'Data Visualization', 'September 2023', 'Dr Shakirah Bt M Taib', (SELECT student_id FROM my_table WHERE name = 'Miera Honey'));

SELECT * FROM courses WHERE student_id = (SELECT student_id FROM my_table WHERE name = 'Miera Honey');
INSERT INTO courses (code, student_id)
VALUES 
  ('TEB3024', (SELECT student_id FROM my_table WHERE name = 'Miera Honey')),
  ('TEB3133', (SELECT student_id FROM my_table WHERE name = 'Miera Honey')),
  ('TEB3113', (SELECT student_id FROM my_table WHERE name = 'Miera Honey'));

UPDATE courses
SET student_id = (SELECT student_id FROM my_table WHERE name = 'Miera Honey'),
    faculty = 'Faculty of Science and Information Technology',
    name = 'Big Data Analytics',
    semester = 'May 2024',
    lecturer = 'Ts Dr Norshakirah Ab Aziz'
WHERE code = 'TEB3113';

UPDATE courses
SET student_id = (SELECT student_id FROM my_table WHERE name = 'Miera Honey'),
    faculty = 'Faculty of Science and Information Technology',
    name = 'Final Year Project II',
    semester = 'May 2024',
    lecturer = 'AP Ts Dr Said Jadid A Kadir'
WHERE code = 'TEB3024';

UPDATE courses
SET student_id = (SELECT student_id FROM my_table WHERE name = 'Miera Honey'),
    faculty = 'Faculty of Science and Information Technology',
    name = 'Big Data Analytics',
    semester = 'May 2024',
    lecturer = 'Ts Dr Norshakirah Ab Aziz'
WHERE code = 'TEB3113';

UPDATE courses
SET student_id = (SELECT student_id FROM my_table WHERE name = 'Miera Honey'),
    faculty = 'Faculty of Science and Information Technology',
    name = 'Data Visualization',
    semester = 'September 2023',
    lecturer = 'Dr Shakirah Bt M Taib'
WHERE code = 'TEB3133';

UPDATE courses
SET student_id = array_agg(DISTINCT (SELECT student_id FROM my_table WHERE name IN ('Miera Honey', 'Jane Smith', 'Bob Johnson'))),
    faculty = 'Faculty of Science and Information Technology',
    name = 'Data Visualization',
    semester = 'September 2023',
    lecturer = 'Dr Shakirah Bt M Taib'
WHERE code = 'TEB3133';

UPDATE courses
SET student_id = CONCAT(
    IFNULL(student_id, ''),
    IFNULL(CONCAT(',', (
        SELECT GROUP_CONCAT(DISTINCT student_id)
        FROM my_table
        WHERE name IN ('Miera Honey', 'Jane Smith', 'Bob Johnson')
    )), '')
),
    faculty = 'Faculty of Science and Information Technology',
    name = 'Data Visualization',
    semester = 'September 2023',
    lecturer = 'Dr Shakirah Bt M Taib'
WHERE code = 'TEB3133';

UPDATE courses
SET student_id = CONCAT_WS(',',
    IFNULL(student_id, ''),
    (SELECT GROUP_CONCAT(DISTINCT student_id)
     FROM my_table
     WHERE name IN ('Miera Honey', 'Jane Smith', 'Bob Johnson'))
)
WHERE code = 'TEB3133';

UPDATE courses
SET student_id = (
  SELECT GROUP_CONCAT(DISTINCT CONCAT(
    IFNULL(student_id, ''),
    IFNULL(CONCAT(',', (
      SELECT GROUP_CONCAT(DISTINCT student_id)
      FROM my_table
      WHERE name IN ('Miera Honey', 'Jane Smith', 'Bob Johnson')
    )), '')
  ))
  FROM courses
  WHERE code = 'TEB3133'
),
faculty = 'Faculty of Science and Information Technology',
name = 'Data Visualization',
semester = 'September 2023',
lecturer = 'Dr Shakirah Bt M Taib'
WHERE code = 'TEB3133';

UPDATE courses
SET student_id = (SELECT student_id FROM my_table WHERE name = 'Jane Smith'),
    faculty = 'Faculty of Business',
    name = 'Organizational Behavior',
    semester = 'August 2023',
    lecturer = 'Dr. Siti Fatimah binti Mohd Yassin'
WHERE code = 'BUS2013';

USE my_database;
ALTER TABLE courses
ADD COLUMN task1_title VARCHAR(100),
ADD COLUMN task1_desc TEXT,
ADD COLUMN task1_due DATE,
ADD COLUMN task1_progress INT;

UPDATE courses
SET 
    task1_title = 'Assignment 1',
    task1_desc = '1. Interim Report - with Similarity Report at the end of the report
    2. Corrected version of Presentation Slides - post proposal defense
    Submission deadline is extended till 5 PM 27/8/24, FINAL CALL',
    task1_due = '2024-08-27',
    task1_prog = NULL
WHERE code = 'TEB3024' AND semester = 'May 2024';

UPDATE courses
SET
    task1_title = 'Mechanical Design',
    task1_desc = NULL,
    task1_due = NULL,
    task1_progress = NULL,
    task1 = 'Mechanical Design'
WHERE code = 'EMM3023' AND semester = 'January 2024';

USE my_database;

USE my_database;
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    progress VARCHAR(50) NOT NULL DEFAULT 'Not Started',
    student_id INT NOT NULL,
    course_code VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES my_table(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(code)
);

INSERT INTO tasks (title, description, due_date, progress, student_id, course_code, created_at, updated_at)
SELECT 
    t.task1_title AS title,
    t.task1_desc AS description,
    t.task1_due AS due_date,
    COALESCE(t.task1_prog, 0) AS progress,
    m.student_id,
    c.code AS course_code,
    CURRENT_TIMESTAMP AS created_at,
    CURRENT_TIMESTAMP AS updated_at
FROM courses c
JOIN my_table m ON c.student_id = m.student_id
LEFT JOIN courses t ON c.student_id = t.student_id AND c.code = t.code
WHERE t.task1_title IS NOT NULL;

ALTER TABLE tasks ADD COLUMN name VARCHAR(255);

INSERT INTO tasks (title, name)
SELECT COALESCE(title, 'Default Title'), name
FROM courses;


USE my_database;
INSERT INTO courses (faculty, code, name, semester,lecturer, student_id, task1_title, task1_desc, task1_due, task1_prog ) VALUES
    ('Faculty of Science and Information Technology', 'TFB1013', 'Structured Programming', 'May 2024', 'Dr Arif', NULL, NULL, NULL, NULL, NULL ),
    ('Faculty of Science and Information Technology', 'TFB1023', 'Database Systems', 'May 2024', 'Dr Afifah' , NULL, NULL, NULL, NULL, NULL ),
    ('Faculty of Science and Information Technology', 'TFB2063', 'Statistics and Empirical Method', 'May 2024', 'Dr Rajesh', NULL, NULL, NULL, NULL, NULL ),
	('Faculty of Science and Information Technology', 'TFB2113', 'Technopreneurship Team Project', 'May 2024', 'Dr Misha', NULL, NULL, NULL, NULL, NULL ),
    ('Faculty of Science and Information Technology', 'TEB3413', 'Software Requirement Engineering', 'May 2024', 'Dr Ong', NULL, NULL, NULL, NULL, NULL ),
    ('Faculty of Science and Information Technology', 'TEB3423', 'Software Design and Architecture', 'May 2024', 'Dr Haris', NULL, NULL, NULL, NULL, NULL );
    
USE my_database;
ALTER TABLE tasks
ADD COLUMN notification_interval INT DEFAULT 1;

ALTER TABLE tasks
ADD COLUMN notification_sent INT DEFAULT 0;

USE my_database;
ALTER TABLE tasks
DROP COLUMN notification_sent;

USE my_database;
ALTER TABLE tasks
DROP COLUMN notification_interval;

USE my_database;
ALTER TABLE tasks
ADD COLUMN test VARCHAR(255) DEFAULT null;

USE my_database;
INSERT INTO tasks (faculty, code, name, semester,lecturer, student_id, task1_title, task1_desc, task1_due, task1_prog ) VALUES
    ('Faculty of Science and Information Technology', 'TFB1013', 'Structured Programming', 'May 2024', 'Dr Arif', NULL, NULL, NULL, NULL, NULL ),
    
 
USE my_database;   
CREATE TABLE `reminder` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `task` int DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci