CREATE DATABASE  study_portal;
USE study_portal;

-- =========================================================
-- 1. USERS TABLE
-- =========================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student','admin') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 2. SUBJECTS TABLE
-- =========================================================

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);


-- =========================================================
-- 3. RESOURCES TABLE
-- =========================================================

CREATE TABLE resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    subject_id INT NOT NULL,
    resource_type ENUM('notes','ebook','paper','video') NOT NULL,
    url VARCHAR(500) NOT NULL,
    verified TINYINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id)
        REFERENCES subjects(id)
        ON DELETE CASCADE
);


-- =========================================================
-- 4. INSERT SUBJECTS
-- =========================================================

INSERT IGNORE INTO subjects (name) VALUES
('Java'),
('DBMS'),
('Python'),
('Computer Networks'),
('Mathematics');


ALTER TABLE resources AUTO_INCREMENT = 1;


-- =========================================================
-- 6. JAVA - 4 RESOURCES
-- =========================================================

INSERT INTO resources
(title, description, subject_id, resource_type, url, verified)
VALUES

(
'Java Previous Year Papers - JNTU Kakinada',
'JNTU Kakinada B.Tech 2-2 Java Programming previous year question papers.',
(SELECT id FROM subjects WHERE name = 'Java'),
'paper',
'https://www.manabadi.co.in/institute/DownLoadBQP-Syllabuswise.aspx?ClsId=18&QPT=P&SubjectId=1942&SysId=118&title=JNTU+Kakinada-Java+Programming-II+Year+BTech+II+Sem-Previous+year+Question+papers',
1
),

(
'Programming in Java - NPTEL Video Lectures',
'NPTEL course covering Java programming concepts with structured lectures and demonstrations.',
(SELECT id FROM subjects WHERE name = 'Java'),
'video',
'https://www.nptel.ac.in/courses/106105191',
1
),

(
'Introduction to Programming in Java - Princeton',
'Online Java textbook covering programming fundamentals, Java programming, algorithms, code examples and exercises.',
(SELECT id FROM subjects WHERE name = 'Java'),
'ebook',
'https://introcs.cs.princeton.edu/java/home/',
1
),

(
'MIT Introduction to Programming in Java – Lecture Notes',
'University lecture notes covering variables, operators, methods, conditionals, loops, arrays, classes, objects, packages, inheritance, exceptions, and file I/O.',
(SELECT id FROM subjects WHERE name = 'Java'),
'notes',
'https://ocw.mit.edu/courses/6-092-introduction-to-programming-in-java-january-iap-2010/resources/lecture-notes/?utm_source=chatgpt.com',
1
);


-- =========================================================
-- 7. DBMS - 4 RESOURCES
-- =========================================================

INSERT INTO resources
(title, description, subject_id, resource_type, url, verified)
VALUES

(
    'DBMS – Lecture Notes',
    'MIT OpenCourseWare lecture notes covering relational models, schema design, query processing, indexing, transactions, recovery and database systems.',
    2,
    'notes',
    'https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/lecture-notes/',
    1
),

(
'Database Design - 2nd Edition',
'Complete database design textbook covering database systems, relational models, ER modeling, functional dependencies, normalization and SQL.',
(SELECT id FROM subjects WHERE name = 'DBMS'),
'ebook',
'https://opentextbc.ca/dbdesign01/',
1
),

(
'B.Tech DBMS Previous Year Papers',
'JNTU B.Tech 2-2 Database Management Systems previous year question papers.',
(SELECT id FROM subjects WHERE name = 'DBMS'),
'paper',
'https://www.manabadi.co.in/institute/DownLoadBQP-Syllabuswise.aspx?ClsId=18&QPT=P&SubjectId=308&SysId=6&title=JNTU-DATA+BASE+MANAGEMENT+SYSTEMS-II+Year+BTech+II+Sem-Previous+year+Question+papers&utm_source=chatgpt.com',
1
),


(
    'Database Management System - NPTEL Video Lectures',
    'NPTEL video course covering relational database models, ER modeling, SQL, normalization, database design, storage, indexing, query processing, query optimization, transactions, concurrency control and recovery.',
    2,
    'video',
    'https://nptel.ac.in/courses/106105175',
    1
);


-- =========================================================
-- 8. PYTHON - 4 RESOURCES
-- =========================================================

INSERT INTO resources
(title, description, subject_id, resource_type, url, verified)
VALUES

(
'Python Official Documentation',
'Official Python tutorial covering syntax, variables, control flow, functions, data structures, modules and more.',
(SELECT id FROM subjects WHERE name = 'Python'),
'ebook',
'https://docs.python.org/3/tutorial/',
1
),

(
    'Python Programming Notes',
    'Undergraduate lecture notes covering Python programming, strings, loops, functions, lists, dictionaries, recursion, object-oriented programming, inheritance, exceptions and algorithms.',
    3,
    'notes',
    'https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/lists/lecture-notes/?utm_source=chatgpt.com',
    1
),

(
'B.Tech Python Previous Year Papers',
'JNTU Kakinada B.Tech 2-2 Python previous year question papers.',
(SELECT id FROM subjects WHERE name = 'Python'),
'paper',
'https://www.manabadi.co.in/institute/DownLoadBQP-Syllabuswise.aspx?QPT=p&SYSID=118&SubjectId=3346&clsid=18&utm_source=chatgpt.com',
1
),

(
'Programming, Data Structures and Algorithms Using Python - NPTEL',
'NPTEL course covering Python programming, algorithms, data structures and problem solving.',
(SELECT id FROM subjects WHERE name = 'Python'),
'video',
'https://www.nptel.ac.in/courses/106106145',
1
);


-- =========================================================
-- 9. COMPUTER NETWORKS - 4 RESOURCES
-- =========================================================

INSERT INTO resources
(title, description, subject_id, resource_type, url, verified)
VALUES

(
'B.Tech Computer Networks Previous Year Papers',
'JNTU Kakinada B.Tech 3-1 Computer Networks previous year question papers.',
(SELECT id FROM subjects WHERE name = 'Computer Networks'),
'paper',
'https://www.manabadi.co.in/institute/DownLoadBQP-Syllabuswise.aspx?QPT=p&SYSID=118&SubjectId=121&clsid=15&title=JNTU+Kakinada-BTech+3-1-COMPUTER+NETWORKS-Previous-Year-Question-Papers',
1
),

(
'Computer Networks and Internet Protocol - NPTEL',
'NPTEL course covering TCP/IP architecture, application, transport and network layers.',
(SELECT id FROM subjects WHERE name = 'Computer Networks'),
'video',
'https://www.nptel.ac.in/courses/106105183',
1
),

(
'Computer Networks - A System Approach',
'Open computer networking textbook covering networking fundamentals, protocols, packet switching, routing, transport protocols and network security.',
(SELECT id FROM subjects WHERE name = 'Computer Networks'),
'ebook',
'https://book.systemsapproach.org/',
1
),

(
'Computer Networks And Internet Protocol Notes',
'Lecture notes covering packet switching, internetworking, routing, IPv6, DNS and related networking topics.',
(SELECT id FROM subjects WHERE name = 'Computer Networks'),
'notes',
'https://ocw.mit.edu/courses/6-829-computer-networks-fall-2002/resources/lecture-notes/',
1
);


-- =========================================================
-- 10. MATHEMATICS - 4 RESOURCES
-- =========================================================

INSERT INTO resources
(title, description, subject_id, resource_type, url, verified)
VALUES

(
    'Engineering Mathematics Notes',
    'Lecture notes covering differential equations, linear algebra, numerical methods, Fourier series, Laplace transforms, matrices, eigenvalues and eigenvectors.',
    5,
    'notes',
    'https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/lecture-notes/',
    1
),

(
'Engineering Mathematics – OpenStax',
'Free mathematical reference covering calculus and other mathematical concepts useful for engineering studies.',
(SELECT id FROM subjects WHERE name = 'Mathematics'),
'ebook',
'https://openstax.org/subjects/math',
1
),

(
'Engineering Mathematics Previous Year Papers',
'JNTU B.Tech 1-1 Mathematics previous year question papers.',
(SELECT id FROM subjects WHERE name = 'Mathematics'),
'paper',
'https://www.manabadi.co.in/institute/DownLoadBQP-Syllabuswise.aspx?QPT=P&SYSID=6&SubjectId=71&clsid=14&title=JNTU+B.Tech+1-1+Sem+Mathematics+Aug+2018+QP&utm_source=chatgpt.com',
1
),

(
    'Engineering Mathematics - NPTEL Video Lectures',
    'NPTEL Engineering Mathematics video lectures covering vector calculus, complex analysis, numerical methods, linear equations and related engineering mathematics topics.',
    5,
    'video',
    'https://www.nptel.ac.in/courses/111105134',
    1
);


-- =========================================================
-- 11. VERIFY TOTAL RESOURCES
-- =========================================================

SELECT COUNT(*) AS total_resources
FROM resources;


-- =========================================================
-- 12. SHOW ALL RESOURCES
-- =========================================================

SELECT
    id,
    title,
    subject_id,
    resource_type,
    url,
    verified
FROM resources
ORDER BY subject_id, id;