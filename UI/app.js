const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const multer = require('multer');
const path = require('path');

const app = express();
const port = 3000;

// Khởi tạo cơ sở dữ liệu SQLite
const db = new sqlite3.Database('audio.db');

// Tạo bảng Audio nếu chưa tồn tại
db.serialize(() => {
    db.run('CREATE TABLE IF NOT EXISTS Audio (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, path TEXT)');
});

// Thiết lập Multer để xử lý tải lên file âm thanh
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});

const upload = multer({ storage: storage });

// Trang chủ
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API lấy danh sách âm thanh
app.get('/api/audio', (req, res) => {
    db.all('SELECT * FROM Audio', (err, rows) => {
        if (err) {
            res.status(500).send(err.message);
        } else {
            res.json(rows);
        }
    });
});

// API tải lên file âm thanh
app.post('/api/upload', upload.single('audio'), (req, res) => {
    const title = req.body.title || 'Untitled';
    const path = req.file.path;
    
    db.run('INSERT INTO Audio (title, path) VALUES (?, ?)', [title, path], (err) => {
        if (err) {
            res.status(500).send(err.message);
        } else {
            res.redirect('/');
        }
    });
});

// Khởi động máy chủ
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
