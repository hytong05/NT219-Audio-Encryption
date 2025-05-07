import mysql.connector
import hashlib
import time
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from Encryption import encryption
from Decryption import decryption
from VLC import auto_play_audio
import json

# Thêm biến logged_in
logged_in = False

def load_db_config(filename="D:\\Project\\db_config.json"):
    with open(filename) as config_file:
        config = json.load(config_file)
    return config

def connect_to_database():
    try:
        db_config = load_db_config()
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối đến cơ sở dữ liệu: {err}")
        return None

def get_song_list(cursor):
    query_songs = "SELECT idSong, title, artist, duration FROM Song"
    cursor.execute(query_songs)
    songs = cursor.fetchall()

    song_info_list = []
    for song in songs:
        song_id, title, artist, duration = song
        formatted_duration = "{:02}:{:02}".format(*divmod(duration, 60))
        song_info_list.append(f"{song_id} - {title} - {artist} - {formatted_duration}")

    return song_info_list

def open_vlc(file_path):
    vlc_path = 'C:\\VLC\\vlc.exe'
    command = [vlc_path, file_path]
    process = subprocess.Popen(command, shell=True)
    time.sleep(10)
    process.terminate()

def sha3_256_hash(data):
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(data.encode('utf-8'))
    return sha3_256.hexdigest()

def shake_128_hash(data):
    shake_128 = hashlib.shake_128()
    shake_128.update(data.encode('utf-8'))
    return "".join(format(byte, '08b') for byte in shake_128.digest(16))

def save_key_distribution(connection, cursor, user_id, song_id, keyValue):
    query = "INSERT INTO keydistribution (userID, songID, keyValue) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, song_id, keyValue))
    connection.commit()

def EN(connection, cursor, user_id, song_id, song_path, ShareKey):
    # Địa chỉ khay tạm
    tmp_path = 'D:\\Project\\Database\\tmp\\tmp.wav'

    InitialVector = encryption(song_path, ShareKey, tmp_path)

    save_key_distribution(connection, cursor, user_id, song_id, InitialVector)

def DE(cursor, user_id):
    # Địa chỉ khay tạm
    tmp_path = 'D:\\Project\\Database\\tmp\\tmp.wav'

    query = "SELECT kd.keyValue, u.password FROM KeyDistribution kd JOIN User u ON kd.userID = u.idUser WHERE kd.userID = %s ORDER BY kd.ID DESC LIMIT 1"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result:
        keyValue, password = result
        decryption(tmp_path, shake_128_hash(password), keyValue, tmp_path)

def get_song_path(cursor, song_id):
    query_song = "SELECT dataPath FROM Song WHERE idSong = %s"
    cursor.execute(query_song, (song_id,))
    result_song = cursor.fetchone()

    return result_song[0] if result_song else None

def get_song_info(cursor, song_id):
    query = "SELECT idSong, title, artist, duration FROM Song WHERE idSong = %s"
    cursor.execute(query, (song_id,))
    song_info = cursor.fetchone()

    if song_info:
        song_id, title, artist, duration = song_info
        formatted_duration = "{:02}:{:02}".format(*divmod(duration, 60))
        return song_id, title, artist, formatted_duration
    else:
        return None

def register_user(cursor, connection):
    username = simpledialog.askstring("Đăng ký", "Nhập tên người dùng:")
    password = simpledialog.askstring("Đăng ký", "Nhập mật khẩu:", show="*")
    confirm_password = simpledialog.askstring("Đăng ký", "Xác nhận mật khẩu:", show="*")

    if password == confirm_password:
        # Thêm thông tin người dùng vào cơ sở dữ liệu
        password_hash = sha3_256_hash(password)
        query = "INSERT INTO User (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password_hash))
        connection.commit()
        messagebox.showinfo("Đăng ký thành công", "Bạn đã đăng ký thành công!")
    else:
        messagebox.showerror("Lỗi", "Mật khẩu không khớp. Vui lòng thử lại.")

def show_main_interface(user_id, username, cursor, connection):
    root = tk.Toplevel()
    root.title("Giao diện chính")
    root.attributes("-fullscreen", True)

    label_user_info = tk.Label(root, text=f"Chào {username} (ID: {user_id})", font=("Arial", 12))
    label_user_info.pack(pady=10)

    song_frame = tk.Frame(root)
    tree_columns = ("ID", "Tên Bài Hát", "Nghệ Sĩ", "Thời Lượng")
    treeview = ttk.Treeview(song_frame, columns=tree_columns, show="headings", height=20)
    for col in tree_columns:
        treeview.heading(col, text=col)
    treeview.pack(expand=tk.YES, fill=tk.BOTH)

    treeview.bind("<ButtonRelease-1>", lambda event: on_song_click(treeview, cursor))

    logout_button = tk.Button(root, text="Đăng xuất", command=root.destroy)
    logout_button.pack(pady=10)

    song_frame.pack()

    song_list = get_song_list(cursor)
    for song_id in song_list:
        song_info = get_song_info(cursor, int(song_id.split()[0]))
        if song_info is not None:
            treeview.insert("", "end", values=song_info)


    root.mainloop()
    
def user_login(username, password, label_user_info, treeview, input_frame, song_frame, cursor, connection, logout_button, register_button):
    global logged_in  # Sử dụng biến toàn cục

    try:
        query = "SELECT idUser, username FROM User WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            user_id, username = result

            # Hiển thị tên người dùng và ID của họ
            label_user_info.config(text=f"Chào {username} (ID: {user_id})")

            # Hiển thị thông báo trực tiếp trên giao diện chính
            messagebox.showinfo("Đăng nhập thành công", f"User ID của bạn là: {user_id}")

            # Lấy danh sách bài hát và hiển thị trong Treeview
            song_list = get_song_list(cursor)
            for song_id in song_list:
                song_info = get_song_info(cursor, int(song_id.split()[0]))
                treeview.insert("", "end", values=song_info)

            # Ẩn ô nhập thông tin
            input_frame.grid_forget()

            # Hiển thị ô danh sách bài hát ở hàng cuối cùng và giữa màn hình
            song_frame.grid(row=2, column=0, pady=(10, 20))

            song_id = simpledialog.askinteger("Nhập ID bài hát", "Nhập ID của bài hát mong muốn:")
            song_path = get_song_path(cursor, song_id)

            if song_path:
                ShareKey = shake_128_hash(password)

                messagebox.showinfo("Chuẩn bị", "Vui lòng chờ trong giây lát. Quá trình chuẩn bị đang diễn ra.")

                EN(connection, cursor, user_id, song_id, song_path, ShareKey)

                messagebox.showinfo("Hoàn tất", "Quá trình chuẩn bị đã hoàn tất!")

            else:
                messagebox.showerror("Lỗi", "Không tìm thấy bài hát với ID đã nhập.")

            messagebox.showinfo("Bắt đầu giải mã", "Bắt đầu quá trình giải mã.")
            DE(cursor, user_id)

            query = "UPDATE KeyDistribution SET isUsed = 1 WHERE userID = %s AND songID = %s ORDER BY ID DESC LIMIT 1"
            cursor.execute(query, (user_id, song_id))
            connection.commit()

            auto_play_audio()

            # Ẩn nút "Đăng ký" khi đã đăng nhập
            register_button.grid_forget()
            # Hiển thị nút "Đăng xuất" khi đã đăng nhập
            logout_button.grid(row=5, column=0, columnspan=2, pady=5)

            # Đặt trạng thái đăng nhập là True
            logged_in = True

            # Thay đổi tại đây để trả về user_id và result
            return user_id, True

        else:
            messagebox.showerror("Đăng nhập thất bại", "Vui lòng kiểm tra lại username và password.")
            # Thay đổi tại đây để trả về user_id và result
            return None, False

    except Exception as err:
        messagebox.showerror("Lỗi", f"Lỗi: {err}")
        # Thay đổi tại đây để trả về user_id và result
        return None, False

    finally:
        if connection and connection.is_connected():
            connection.close()

def on_login_button_click(entry_username, entry_password, label_user_info, treeview, input_frame, song_frame, cursor, connection, logout_button, register_button):
    global user_id

    username = entry_username.get()
    password = entry_password.get()

    password = sha3_256_hash(password)

    user_id, result = user_login(username, password, label_user_info, treeview, input_frame, song_frame, cursor, connection, logout_button, register_button)

    if result:
        logout_button.grid(row=5, column=0, columnspan=2, pady=5)
    else:
        messagebox.showerror("Lỗi", "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu.")

def show_song_info(song_id, cursor):
    query = "SELECT title, artist, duration FROM Song WHERE idSong = %s"
    cursor.execute(query, (song_id,))
    result = cursor.fetchone()

    if result:
        title, artist, duration = result
        formatted_duration = "{:02}:{:02}".format(*divmod(duration, 60))
        messagebox.showinfo("Thông tin bài hát", f"ID: {song_id}\nTên: {title}\nNghệ sĩ: {artist}\nThời lượng: {formatted_duration}")
    else:
        messagebox.showerror("Lỗi", "Không thể lấy thông tin bài hát.")

def on_song_click(treeview, cursor):
    selected_item = treeview.selection()

    if selected_item:
        song_id = treeview.item(selected_item, "values")[0]
        song_id = int(song_id.split()[0])  # Lấy ID bài hát từ chuỗi "ID - ..."
        song_path = get_song_path(cursor, song_id)

        if song_path:
            password = simpledialog.askstring("Nhập mật khẩu", "Nhập mật khẩu để xem thông tin bài hát:", show="*")
            password_hash = sha3_256_hash(password)

            user_id = simpledialog.askinteger("Nhập ID người dùng", "Nhập ID người dùng để xem thông tin bài hát:")

            query = "SELECT COUNT(*) FROM User WHERE idUser = %s AND password = %s"
            cursor.execute(query, (user_id, password_hash))
            result = cursor.fetchone()

            if result and result[0] > 0:
                messagebox.showinfo("Xác nhận thành công", "Xác nhận thành công. Bạn có quyền xem thông tin bài hát.")
                show_song_info(song_id, cursor)
            else:
                messagebox.showerror("Xác nhận thất bại", "Xác nhận thất bại. Vui lòng kiểm tra lại thông tin.")
                
def open_registration_interface(cursor, connection, root):
    registration_window = tk.Toplevel()
    registration_window.title("Đăng ký mới")

    # Lấy kích thước màn hình để căn giữa cửa sổ đăng ký
    screen_width = registration_window.winfo_screenwidth()
    screen_height = registration_window.winfo_screenheight()

    # Đặt kích thước và vị trí cho cửa sổ đăng ký
    width = 400
    height = 200
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    registration_window.geometry(f"{width}x{height}+{x}+{y}")

    label_username = tk.Label(registration_window, text="Tên người dùng:")
    label_username.grid(row=0, column=0, padx=5)
    entry_username = tk.Entry(registration_window, width=20)
    entry_username.grid(row=0, column=1, padx=5)

    label_password = tk.Label(registration_window, text="Mật khẩu:")
    label_password.grid(row=1, column=0, padx=5)
    entry_password = tk.Entry(registration_window, show="*", width=20)
    entry_password.grid(row=1, column=1, padx=5)

    label_confirm_password = tk.Label(registration_window, text="Xác nhận mật khẩu:")
    label_confirm_password.grid(row=2, column=0, padx=5)
    entry_confirm_password = tk.Entry(registration_window, show="*", width=20)
    entry_confirm_password.grid(row=2, column=1, padx=5)

    register_button = tk.Button(registration_window, text="Đăng ký", command=lambda: register_user_interface(entry_username, entry_password, entry_confirm_password, cursor, connection, registration_window))
    register_button.grid(row=3, column=0, columnspan=2, pady=5)

def register_user_interface(entry_username, entry_password, entry_confirm_password, cursor, connection, registration_window):
    global logged_in  # Sử dụng biến toàn cục

    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    if password == confirm_password:
        # Thêm thông tin người dùng vào cơ sở dữ liệu
        password_hash = sha3_256_hash(password)
        query = "INSERT INTO User (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password_hash))
        connection.commit()
        messagebox.showinfo("Đăng ký thành công", "Bạn đã đăng ký thành công!")

        # Đóng cửa sổ đăng ký
        registration_window.destroy()

        # Nếu đăng ký thành công, tự động đăng nhập và hiển thị nút "Đăng xuất"
        logged_in = True
    else:
        messagebox.showerror("Lỗi", "Mật khẩu không khớp. Vui lòng thử lại.")
        
def logout(root, connection, cursor, entry_username, entry_password, label_user_info, treeview, input_frame, song_frame, logout_button, register_button):
    global user_id
    global logged_in  # Sử dụng biến toàn cục

    if connection and connection.is_connected():
        connection.close()

    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    label_user_info.config(text="")

    logout_button.grid_forget()
    register_button.grid(row=3, column=0, columnspan=2, pady=5)

    input_frame.grid(row=0, column=0, pady=(50, 0))
    song_frame.grid_forget()

    for item in treeview.get_children():
        treeview.delete(item)

    # user_id = None

    # Đặt trạng thái đăng nhập là False khi đăng xuất
    logged_in = False

def main():
    global logged_in  # Sử dụng biến toàn cục

    root = tk.Tk()
    root.title("Ứng dụng phát nhạc")

    connection = connect_to_database()

    if connection:
        cursor = connection.cursor()

        input_frame = tk.Frame(root)
        input_frame.grid(row=0, column=0, pady=(50, 0))

        label_username = tk.Label(input_frame, text="Username:")
        label_username.grid(row=0, column=0, padx=5)
        entry_username = tk.Entry(input_frame, width=20)
        entry_username.grid(row=0, column=1, padx=5)

        label_password = tk.Label(input_frame, text="Password:")
        label_password.grid(row=1, column=0, padx=5)
        entry_password = tk.Entry(input_frame, show="*", width=20)
        entry_password.grid(row=1, column=1, padx=5)

        label_user_info = tk.Label(root, text="", font=("Arial", 12))
        label_user_info.grid(row=1, column=0, pady=(10, 0))

        login_button = tk.Button(input_frame, text="Đăng nhập", command=lambda: on_login_button_click(entry_username, entry_password, label_user_info, treeview, input_frame, song_frame, cursor, connection, logout_button, register_button))
        login_button.grid(row=2, column=0, columnspan=2, pady=5)

        register_button = tk.Button(input_frame, text="Đăng ký", command=lambda: open_registration_interface(cursor, connection, root))
        register_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        logout_button = tk.Button(input_frame, text="Đăng xuất", command=lambda: logout(root, connection, cursor, entry_username, entry_password, label_user_info, treeview, input_frame, song_frame, logout_button, register_button))
        logout_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        if logged_in:
            # Ẩn nút "Đăng ký" khi đã đăng nhập
            register_button.grid_forget()
            # Hiển thị nút "Đăng xuất" khi đã đăng nhập
            logout_button.grid(row=5, column=0, columnspan=2, pady=5)

        song_frame = tk.Frame(root)
        tree_columns = ("ID", "Tên Bài Hát", "Nghệ Sĩ", "Thời Lượng")
        treeview = ttk.Treeview(song_frame, columns=tree_columns, show="headings", height=20)
        for col in tree_columns:
            treeview.heading(col, text=col)
        treeview.pack(expand=tk.YES, fill=tk.BOTH)

        song_frame.grid(row=2, column=0, pady=(10, 20))

        root.mainloop()

        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()