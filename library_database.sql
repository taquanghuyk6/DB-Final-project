-- ========================================================
-- Library management database
-- Database: lib
-- ========================================================

CREATE DATABASE IF NOT EXISTS `lib`;
USE `lib`;

-- 1. TẠO CẤU TRÚC BẢNG (TABLES)
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100) NOT NULL
);

CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    AuthorName VARCHAR(100) NOT NULL
);

CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    BookName VARCHAR(255) NOT NULL,
    AuthorID INT,
    PublishYear INT,
    AvailableQuantity INT,
    TotalQuantity INT,  
    CategoryID INT,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE Readers (
    ReaderID INT PRIMARY KEY AUTO_INCREMENT,
    ReaderName VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15)
);

CREATE TABLE Borrowing (
    BorrowID INT PRIMARY KEY AUTO_INCREMENT,
    ReaderID INT,
    BookID INT,
    BorrowDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (ReaderID) REFERENCES Readers(ReaderID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

-- 2.TRIGGERS (Tự động cập nhật số lượng sách trong kho)
DELIMITER $$
CREATE TRIGGER After_Borrow_Book
AFTER INSERT ON Borrowing
FOR EACH ROW
BEGIN
    UPDATE Books 
    SET AvailableQuantity = AvailableQuantity - 1 
    WHERE BookID = NEW.BookID AND AvailableQuantity > 0;
END $$

CREATE TRIGGER After_Return_Book
AFTER UPDATE ON Borrowing
FOR EACH ROW
BEGIN
    IF OLD.ReturnDate IS NULL AND NEW.ReturnDate IS NOT NULL THEN
        UPDATE Books 
        SET AvailableQuantity = AvailableQuantity + 1 
        WHERE BookID = NEW.BookID;
    END IF;
END $$
DELIMITER ;

-- 3. SAMPLE DATA (10 RECORDS)
INSERT INTO Categories (CategoryName) VALUES
('Computer Science'), ('Data Science'), ('Science Fiction'), ('Fantasy'), ('History'),
('Biography'), ('Mystery'), ('Philosophy'), ('Business & Finance'), ('Mathematics');

INSERT INTO Authors (AuthorName) VALUES
('Alan Turing'), ('Guido van Rossum'), ('Isaac Asimov'), ('J.R.R. Tolkien'), ('Yuval Noah Harari'),
('Walter Isaacson'), ('Arthur Conan Doyle'), ('Friedrich Nietzsche'), ('Robert Kiyosaki'), ('Alan V. Oppenheim');

INSERT INTO Books (BookName, AuthorID, PublishYear, AvailableQuantity, TotalQuantity, CategoryID) VALUES
('Computing Machinery and Intelligence', 1, 1950, 5, 5, 1),
('Python Crash Course', 2, 2015, 12, 12, 1),
('Foundation', 3, 1951, 8, 8, 3),
('The Hobbit', 4, 1937, 10, 10, 4),
('Sapiens: A Brief History of Humankind', 5, 2011, 15, 15, 5),
('Steve Jobs: The Exclusive Biography', 6, 2011, 7, 7, 6),
('The Adventures of Sherlock Holmes', 7, 1892, 4, 4, 7),
('Thus Spoke Zarathustra', 8, 1883, 3, 3, 8),
('Rich Dad Poor Dad', 9, 1997, 20, 20, 9),
('Discrete-Time Signal Processing', 10, 1989, 6, 6, 10);

INSERT INTO Readers (ReaderName, Address, PhoneNumber) VALUES
('Nguyễn Văn A', '123 Cầu Giấy, Hà Nội', '0901111111'),
('Trần Thị B', '456 Hai Bà Trưng, Hà Nội', '0902222222'),
('Lê Hoàng C', '789 Nguyễn Trãi, HCM', '0903333333'),
('Phạm Thị D', '321 Lê Lợi, Đà Nẵng', '0904444444'),
('Hoàng Văn E', '654 Trần Phú, Hải Phòng', '0905555555'),
('Vũ Thị F', '987 Quang Trung, Cần Thơ', '0906666666'),
('Đặng Văn G', '159 Bạch Đằng, Nha Trang', '0907777777'),
('Bùi Thị H', '753 Hùng Vương, Huế', '0908888888'),
('Đỗ Hoàng I', '852 Đống Đa, Đà Lạt', '0909999999'),
('Hồ Tấn K', '951 Lý Thái Tổ, HCM', '0910000000');

INSERT INTO Borrowing (ReaderID, BookID, BorrowDate, ReturnDate) VALUES
(1, 2, '2026-04-01', '2026-04-10'), 
(2, 5, '2026-04-05', '2026-04-15'), 
(3, 9, '2026-04-10', '2026-04-12'), 
(4, 1, '2026-04-12', NULL),           
(5, 3, '2026-04-15', NULL),           
(6, 4, '2026-04-20', NULL),           
(7, 7, '2026-03-01', NULL),           
(8, 10, '2026-04-15', NULL),          
(9, 6, '2026-04-18', NULL),           
(10, 8, '2026-05-01', NULL);          

-- 4. SECURITIES
-- Librarian's account
CREATE USER IF NOT EXISTS 'librarian_user'@'localhost' IDENTIFIED BY 'StrongPass_Lib2026!';
GRANT SELECT, INSERT, UPDATE, DELETE ON `lib`.* TO 'librarian_user'@'localhost';

-- Reader's account
CREATE USER IF NOT EXISTS 'reader_user'@'localhost' IDENTIFIED BY 'StrongPass_Read2026!';
GRANT SELECT ON `lib`.Books TO 'reader_user'@'localhost';
GRANT SELECT ON `lib`.Authors TO 'reader_user'@'localhost';
GRANT SELECT ON `lib`.Categories TO 'reader_user'@'localhost';

FLUSH PRIVILEGES;