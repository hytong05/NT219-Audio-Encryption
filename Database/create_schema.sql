CREATE DATABASE MUSIC;
USE MUSIC; 

-- Tạo bảng User
CREATE TABLE IF NOT EXISTS User (
    idUser INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(256) NOT NULL
);

-- Tạo bảng Song
CREATE TABLE IF NOT EXISTS Song (
    idSong INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    artist VARCHAR(100) NOT NULL,
    duration INT NOT NULL,
    dataPath VARCHAR(200) NOT NULL
);

-- Tạo bảng KeyDistribution
CREATE TABLE IF NOT EXISTS KeyDistribution (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    songID INT NOT NULL,
    keyValue VARCHAR(256) NOT NULL,
    isUsed BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (userID) REFERENCES User(idUser) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (songID) REFERENCES Song(idSong) ON DELETE NO ACTION ON UPDATE NO ACTION,
    INDEX userID_idx (userID),
    INDEX songID_idx (songID)
);

INSERT INTO User (username, password) VALUES
('hytong', '39d1da1f4f9fda75ac2c0b29b76c2149fe57256e3240ce35e1e74d6b6d898222'),
('Bob', 'b50b22901ba019b7f48327a891d21a9af254749359c76f1f4755bd28c49c33ab'),
('Alice', 'ada0018bcd09ed8fc81b323331950a89541d2416fc08b8b1de496d2dd35826b3');

INSERT INTO Song (title, author, artist, duration, dataPath) VALUES
('Shape of You', 'Ed Sheeran', 'Ed Sheeran', 263, 'D:\\Project\\Database\\Dataset\\1 - Shape of You - Ed Sheeran - Ed Sheeran - 263.wav'),
('vaicaunoicokhiennguoithaydoi', 'GREY D', 'GREY D', 225, 'D:\\Project\\Database\\Dataset\\2 - vaicaunoicokhiennguoithaydoi - GREY D - GREY D - 225.wav'),
('comethru', 'Jeremy Zucker', 'Jeremy Zucker', 180, 'D:\\Project\\Database\\Dataset\\3 - comethru - Jeremy Zucker - Jeremy Zucker - 180.wav'),
('Glimpse of Us', 'Joji', 'Joji', 233, 'D:\\Project\\Database\\Dataset\\4 - Glimpse of Us - Joji - Joji - 233.wav');