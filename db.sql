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
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    stock INT DEFAULT 0 NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE Billing (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customerId INT,
    products VARCHAR(8192) NOT NULL,
    discount FLOAT NOT NULL DEFAULT 0,
    method VARCHAR(50) NOT NULL,
    cashier VARCHAR(100) NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (customerId) REFERENCES Customers(id)
);

-- first employee (admin)
INSERT INTO Employees (first_name, last_name, email, phone, password) VALUES
('John', 'Doe', 'john@test.com', '1234567890', 'password');

-- sample customers
INSERT INTO Customers (first_name, last_name, phone, points) VALUES
('Alice', 'Johnson', '123456785', 10),
('Bob', 'Smith', '123456786', 20),
('Charlie', 'Brown', '123456785', 15);

-- sample products
INSERT INTO Products (name, stock, cost, price) VALUES
('Apple', 100, 30.00, 50.00),
('Banana', 150, 20.00, 40.00),
('Orange', 120, 25.00, 45.00),
('Milk', 80, 100.00, 150.00),
('Bread', 60, 120.00, 180.00),
('Eggs (dozen)', 50, 150.00, 200.00),
('Rice (1kg)', 70, 200.00, 300.00),
('Chicken (1kg)', 40, 500.00, 700.00),
('Fish (1kg)', 30, 600.00, 800.00),
('Vegetable Mix (500g)', 90, 250.00, 400.00),
('Yogurt (500g)', 75, 180.00, 250.00),
('Cheese (200g)', 65, 220.00, 300.00),
('Butter (200g)', 55, 170.00, 230.00),
('Cereal (500g)', 85, 300.00, 450.00),
('Juice (1L)', 95, 150.00, 220.00),
('Coffee (250g)', 45, 400.00, 550.00),
('Tea (100g)', 35, 250.00, 350.00),
('Sugar (1kg)', 100, 100.00, 150.00),
('Salt (500g)', 110, 80.00, 120.00),
('Flour (1kg)', 120, 120.00, 180.00);