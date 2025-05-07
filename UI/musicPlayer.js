var audio = document.getElementById("myAudio");

// Gọi hàm để lấy danh sách bài hát khi trang được tải
loadSongList();

function loadSongList() {
    // Sử dụng AJAX để gửi yêu cầu đến server và lấy danh sách bài hát
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'getSongs.php', true);

    xhr.onload = function() {
        if (xhr.status == 200) {
            // Xử lý dữ liệu khi nhận được từ server
            var songs = JSON.parse(xhr.responseText);
            displaySongList(songs);
        }
    };

    xhr.send();
}

function displaySongList(songs) {
    var songListContainer = document.getElementById("songListContainer");

    // Tạo danh sách ul
    var ul = document.createElement("ul");

    // Thêm mỗi bài hát vào danh sách
    songs.forEach(function(song) {
        var li = document.createElement("li");
        li.textContent = song.title;

        // Gán một sự kiện click cho mỗi bài hát
        li.addEventListener("click", function() {
            loadSelectedSong(song.path);
        });

        ul.appendChild(li);
    });

    // Xóa nội dung hiện tại của songListContainer và thêm danh sách mới
    songListContainer.innerHTML = "";
    songListContainer.appendChild(ul);
}

function loadSelectedSong(songPath) {
    // Cập nhật phần tử <audio> với đường dẫn mới
    audio.src = songPath;
    audio.load();
    playPause();
}

function playPause() {
    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
    }
}

function rewind() {
    audio.currentTime -= 10;
}

function forward() {
    audio.currentTime += 10;
}
