1. Enrollment System with Grades Distribution, and Grades Viewer for Students.

Framework: Python Flask
Template: Tailwind
Database Integration: MySQL
API Integration: REST API

2. Here are Dependencies:

pip install Flask 
pip install Flask-Login 
pip install Flask-SQLAlchemy 
pip install Flask-WTF 
pip install PyMySQL 
pip installpython-dotenv

3. Database Structure/Database Query

CREATE DATABASE IF NOT EXISTS uni_ver_city_db;

USE uni_ver_city_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    PASSWORD VARCHAR(255) NOT NULL,
    ROLE VARCHAR(20) DEFAULT 'student'
);

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    CODE VARCHAR(20) UNIQUE NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    units INT NOT NULL,
    SCHEDULE VARCHAR(100),
    slots INT DEFAULT 40
);

CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    STATUS VARCHAR(20) DEFAULT 'enrolled',
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT NOT NULL,
    grade FLOAT,
    remarks VARCHAR(20),
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
);

INSERT INTO users (NAME, email, PASSWORD, ROLE) 
VALUES ('n1ghtj4r', 'n1ghtj4r@gmail.com', '123456', 'admin');
