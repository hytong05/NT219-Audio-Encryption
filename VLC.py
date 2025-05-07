import os
import time
import subprocess

def get_audio_duration(file_path):
    # Sử dụng subprocess để lấy thời lượng của file âm thanh
    result = subprocess.run(['vlc', '--no-xlib', '--run-time', '1', '--novideo', '--quiet', '--intf', 'dummy', '--dummy-quiet', file_path], capture_output=True, text=True)
    duration_line = next(line for line in result.stdout.split('\n') if "input length" in line)
    duration = int(duration_line.split()[-1].strip())
    return duration

def play_audio_chunk(file_path, start, stop):
    # Sử dụng subprocess để phát một đoạn cụ thể của file âm thanh
    subprocess.run(['vlc', '--no-xlib', '--start-time=' + start, '--stop-time=' + stop, file_path, '--intf', 'dummy', '--dummy-quiet', '--play-and-exit', '--no-loop'])

def auto_play_audio():
    # Trỏ vào khay tạm
    file_path = 'D:\\Project\\Database\\tmp\\tmp.wav'
    
    # Mở VLC bằng subprocess để hiển thị cửa sổ
    vlc_process = subprocess.Popen(['C:\\VLC\\vlc.exe', '--no-xlib', file_path])

    # Đợi 1 giây để VLC chuẩn bị hoàn toàn
    time.sleep(1)

    # Lấy tổng thời lượng của file âm thanh
    duration = get_audio_duration(file_path)

    # Phát tự động từng chunk mỗi 2 giây
    start_time = 0
    chunk_duration = 2
    first_chunk_played = False

    while start_time < duration:
        # Đặt thời gian bắt đầu và kết thúc cho chunk
        play_audio_chunk(file_path, str(start_time), str(start_time + chunk_duration))

        # Tăng thời gian bắt đầu cho chunk tiếp theo
        start_time += chunk_duration

        # Nếu chunk đầu tiên đã được phát, hãy đợi cho quá trình VLC kết thúc
        if not first_chunk_played:
            vlc_process.terminate()
            vlc_process.wait()
            first_chunk_played = True

    # Đợi cho quá trình VLC kết thúc nếu nó chưa kết thúc
    vlc_process.wait()
    
    # Xóa file âm thanh sau khi phát xong
    os.remove('D:\\Project\\Database\\tmp\\tmp.wav')