const express = require('express');
const mysql = require('mysql');
const app = express();
const port = 3000;

// Kết nối cơ sở dữ liệu MySQL
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '1234',
    database: 'MUSIC'
});

function login() {
    // Xử lý đăng nhập
 
    // Nếu đăng nhập thành công, chuyển hướng đến trang songs.html
    window.location.href = 'index.html';
}

connection.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err);
    } else {
        console.log('Connected to MySQL database');
    }
});

// Endpoint để lấy danh sách bài hát
app.get('/api/songs', (req, res) => {
    const query = 'SELECT idSong, title, artist, duration FROM Song';
    connection.query(query, (err, results) => {
        if (err) {
            console.error('Error executing MySQL query:', err);
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            res.json(results);
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
