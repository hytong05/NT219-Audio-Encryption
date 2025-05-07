document.addEventListener('DOMContentLoaded', function() {
    // Gọi hàm để lấy danh sách bài hát khi trang được tải
    loadSongs();
});

function loadSongs() {
    // Sử dụng AJAX để gửi yêu cầu đến server
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'get_songs.php', true);

    xhr.onload = function() {
        if (xhr.status == 200) {
            // Xử lý dữ liệu khi nhận được từ server
            var songs = JSON.parse(xhr.responseText);
            displaySongs(songs);
        }
    };

    xhr.send();
}

function displaySongs(songs) {
    var songList = document.getElementById('song-list');

    // Xóa danh sách bài hát hiện tại (nếu có)
    songList.innerHTML = '';

    // Thêm mỗi bài hát vào danh sách
    songs.forEach(function(song) {
        var li = document.createElement('li');
        li.textContent = song.title + ' - ' + song.artist;
        songList.appendChild(li);
    });
}
