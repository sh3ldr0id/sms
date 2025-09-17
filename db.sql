CREATE DATABASE smsdb;
USE smsdb;

CREATE TABLE Customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    points INT NOT NULL DEFAULT 0
);

CREATE TABLE Employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    -- rating FLOAT NOT NULL DEFAULT 0
);

CREATE TABLE Products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    stock INT DEFAULT 0,
    cost DECIMAL(10,2) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE Billing (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customerId INT,
    products VARCHAR(1024) NOT NULL,
    discount FLOAT NOT NULL DEFAULT 0,
    method VARCHAR(50) NOT NULL,
    cashier VARCHAR(100) NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (customerId) REFERENCES Customers(id)
);

-- first employee (admin)
INSERT INTO Employees (first_name, last_name, email, phone, password, rating) VALUES
('Sheldon', 'Sinu', 'sh3ldr0id@gmail.com', '9207543203', 'password', 5.0);

-- sample customers
INSERT INTO Customers (first_name, last_name, phone, points) VALUES
('Sonu', 'Philip', '9207543209', 0),
('Alice', 'Johnson', '9207543210', 10),
('Bob', 'Smith', '9207543211', 20),
('Charlie', 'Brown', '9207543212', 15);

INSERT INTO Products (name, stock, cost, price) VALUES
('Apple', 100, 0.30, 0.50),
('Banana', 150, 0.20, 0.40),
('Orange', 120, 0.25, 0.45),
('Milk', 80, 1.00, 1.50),
('Bread', 60, 1.20, 1.80),
('Eggs (dozen)', 50, 1.50, 2.00),
('Rice (1kg)', 70, 2.00, 3.00),
('Chicken (1kg)', 40, 5.00, 7.00),
('Fish (1kg)', 30, 6.00, 8.00),
('Vegetable Mix (500g)', 90, 2.50, 4.00);






(1, 'Sheldon', 'Sinu', 'sh3ldr0id@gmail.com', '9207543203', 'password', 5.0)
(2, 'Sonu', 'Philip', 'sonup@gmail.com', '9207543209', 'wordpass', 0.0)