import vlc
import time

def auto_play_audio(file_path):
    # Tạo đối tượng VLC instance
    instance = vlc.Instance("--no-xlib")

    # Tạo đối tượng MediaPlayer từ VLC instance
    player = instance.media_player_new()

    # Tạo đối tượng Media từ đường dẫn của file âm thanh
    media = instance.media_new(file_path)

    # Gắn đối tượng Media với MediaPlayer
    player.set_media(media)

    # Bắt đầu phát
    player.play()

    # Lấy tổng thời lượng của file âm thanh
    duration = media.get_duration()

    # Phát tự động từng chunk mỗi 2 giây
    start_time = 0
    chunk_duration = 2
    while start_time < duration:
        # Đặt thời gian bắt đầu và kết thúc cho chunk
        media.get_mrl()  # Bắt buộc gọi hàm này trước khi set_time
        player.set_time(start_time * 1000)  # Chuyển đổi sang mili giây

        # Đợi cho đến khi kết thúc chunk
        time.sleep(chunk_duration)

        # Tăng thời gian bắt đầu cho chunk tiếp theo
        start_time += chunk_duration

        # Chờ kết thúc phát chunk hiện tại
        while player.get_state() == vlc.State.Playing:
            time.sleep(0.1)

    # Đóng MediaPlayer và VLC instance khi xong
    player.stop()
    instance.release()

# Đặt đường dẫn của file âm thanh
audio_file_path = "D:\\Project\\Database\\Dataset\\1 - Shape of You - Ed Sheeran - Ed Sheeran - 263.wav"

# Phát âm thanh tự động với cửa sổ VLC
auto_play_audio(audio_file_path)
