import numpy as np
import matplotlib.pyplot as plt
import librosa

# Đọc file âm thanh
data, sample_rate = librosa.load("D:\\Project\\Audio\\Plain2.wav", sr=None, dtype=np.float32)
data_int16 = (data * np.iinfo(np.int16).max).astype(np.int16)

# Tính thời gian
duration = len(data)/sample_rate
time = np.arange(0,duration,1/sample_rate) 

# Vẽ biểu đồ
plt.figure(figsize=(20, 5))
plt.plot(time, data_int16)
plt.xlabel('Thời gian (s)')
plt.ylabel('Biên độ')
plt.title('Biểu đồ dạng sóng của file âm thanh')
plt.show()
