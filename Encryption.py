import soundfile as sf
import numpy as np
import math
import random
import librosa

# Hàm nhập dữ liệu âm thanh từ file
def Input(filename):
    # Đọc dữ liệu âm thanh bằng librosa
    data, sample_rate = librosa.load(filename, sr=None, mono=True)

    # Chuyển đổi dữ liệu âm thanh sang int16
    data_int16 = (data * np.iinfo(np.int16).max).astype(np.int16)

    return data_int16, sample_rate

def Output(filename, sample_rate, data):
    # Ghi dữ liệu âm thanh bằng soundfile
    sf.write(filename, data, sample_rate, format='wav')

# Tạo random ra hai mảng ShareKey và IntialVector với 128 bits       
def Generation():
  #ShareKey = [random.randint(0, 1) for i in range(128)]
  IntialVector = [random.randint(0, 1) for i in range(128)]
  #return "".join(str(bit) for bit in ShareKey), "".join(str(bit) for bit in IntialVector)
  return "".join(str(bit) for bit in IntialVector)

# Hàm chuẩn hoá từ dạng binary sang dạng hex
def Hex(bin_string):
  return format(int(bin_string, 2), "02x")

# Hàm dời qua trái số bit cho trước
def left_rotate(x, n):
  if isinstance(x, str):
    x = int(x, 2)
  n %= 128  # Đảm bảo n không vượt quá 128
  result = ((x << n) | (x >> (128 - n))) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
  return bin(result)[2:].zfill(128)

# Tạo ra Sine Cosine Sequence
def SineCosineChaoticMap(x0, m, n):
  # Khởi tạo mảng kết quả
  SineCosineSequence = np.zeros(n, dtype=np.float64)

  # Gán giá trị hạt giống ban đầu
  SineCosineSequence[0] = x0

  # Tính các giá trị tiếp theo của map
  for i in range(1, n):
    A = np.sin(-m * SineCosineSequence[i - 1] + pow(SineCosineSequence[i - 1], 3) - m * np.sin(SineCosineSequence[i - 1]))
    B = np.cos(-m * SineCosineSequence[i - 1] + pow(SineCosineSequence[i - 1], 3) - m * np.sin(SineCosineSequence[i - 1]))
    SineCosineSequence[i] = abs(abs(A) - abs(B))

  return SineCosineSequence

# Tạo ra Logistic Sine Cosine Sequence
def LogisticSineCosine(x0, r, n):
  # Khởi tạo mảng kết quả
  LogisticSineCosineSequence = np.zeros(n)

  # Gán giá trị hạt giống ban đầu
  LogisticSineCosineSequence[0] = x0
  
  # Tạo biến pi
  pi = math.pi

  # Tính các giá trị tiếp theo của map
  for i in range(1, n):
    LogisticSineCosineSequence[i] = np.cos(pi * (4 * r * LogisticSineCosineSequence[i - 1] * (1 - LogisticSineCosineSequence[i-1]) + (1 - r) * np.sin(pi * LogisticSineCosineSequence[i-1]) - 0.5))

  return LogisticSineCosineSequence

def Initial_Seq(IV3, SineCosineSequence, SequenceSize):
  arr = np.zeros(SequenceSize, dtype = np.bool_)
  outputarr = np.zeros(SequenceSize, dtype='uint8')
  inc = 1 # Used for creating different value of the value_data
  flag = 0
  while flag < SequenceSize:
    value_data = int(IV3 * inc * SineCosineSequence[inc]) % SequenceSize
    inc = inc + 1 # Increase inc to create diffirent values of the value_data
    if arr[value_data] == False:
      outputarr[flag - 1] = value_data
      flag = flag + 1
      arr[value_data] = True
  return outputarr 

def Permutation(Audio, IV3, SineCosineSequence):
  Length = len(Audio)
  rem = Length % 16 # used for calculating the total number of the variables SequenceSize
  div = int(Length / 16) # used for calculating the remaining number    
      
  # the 16 different dynamic sequence for the permutation process 
  InitialSequence1 = Initial_Seq(IV3, SineCosineSequence, 16) 
  InitialSequence2 = Initial_Seq(IV3, SineCosineSequence, rem)  
        
  audio_pos = 0
  output = np.array([], dtype = np.int16)
  Permutated_Val = np.zeros(16, dtype = np.int16)
      
  for i in range(div):    
    # Rotate the variable InitialSequence1 by I3 * (i + 1) % 16 and store in variable Sequence
    Sequence = np.roll(InitialSequence1, IV3 * (i + 1) % 16)
    Audio_16_val = Audio[audio_pos : audio_pos + 16]
    
    # Take 16 values of the audio data, and then permute these values according to the Sequence variable
    for j in range(16):
      Permutated_Val[j] = Audio_16_val[Sequence[j]] 
    output = np.concatenate((output, Permutated_Val))
    audio_pos = audio_pos + 16
        
  Audio_16_val = Audio[audio_pos:audio_pos + rem]  
  Permutated_Val1 = np.zeros(rem, dtype = np.int16)
      
  for i in range(rem):
    Permutated_Val1[i] = Audio_16_val[InitialSequence2[i]]
  output = np.concatenate((output, Permutated_Val1))

  return output

def int16_array_to_binary16(array):
    # Chuyển đổi mảng int16 sang chuỗi nhị phân 16 bit
    binary_array = [np.binary_repr(x, width=16) for x in array]
    return binary_array

def Binary_to_DNA_Seq(rule, binary_arr):
  encoding_rules = {
    0: ['A', 'C', 'T', 'G'],
    1: ['A', 'G', 'T', 'C'],
    2: ['T', 'C', 'A', 'G'],
    3: ['T', 'G', 'A', 'C'],
    4: ['C', 'A', 'G', 'T'],
    5: ['C', 'T', 'G', 'A'],
    6: ['G', 'A', 'C', 'T'],
    7: ['G', 'T', 'C', 'A']
  }
    
  # Chuyển đổi binary_arr thành chuỗi DNA
  dna_seq_arr = []
  for binary_str in binary_arr:
    dna_seq = ''
    for i in range(0, len(binary_str), 2):
      index = int(binary_str[i:i+2], 2)
      dna_seq += encoding_rules[rule][index]
    dna_seq_arr.append(dna_seq)
    
  return dna_seq_arr

def DNA_addition(dnaseq_arr_1, dnaseq_arr_2):
    # Tạo bảng cộng
    addition_table = {
        'A': ['A', 'C', 'G', 'T'],
        'C': ['C', 'G', 'T', 'A'],
        'G': ['G', 'T', 'A', 'C'],
        'T': ['T', 'A', 'C', 'G']
    }

    # Thực hiện phép cộng
    add_dna_arr = []
    for dna1, dna2 in zip(dnaseq_arr_1, dnaseq_arr_2):
        result = ''
        for base1, base2 in zip(dna1, dna2):
            # Chuyển đổi base2 thành số tương ứng
            tmp2 = 'ACGT'.index(base2)

            # Thực hiện cộng và thêm vào kết quả
            result += addition_table[base1][tmp2]
        add_dna_arr.append(result)

    return add_dna_arr

def DNA_Seq_to_Binary(rule, dna_seq_arr):
    # Tạo bảng giải mã
    decoding_rules = {
        0: {'A': '00', 'C': '01', 'T': '10', 'G': '11'},
        1: {'A': '00', 'G': '01', 'T': '10', 'C': '11'},
        2: {'T': '00', 'C': '01', 'A': '10', 'G': '11'},
        3: {'T': '00', 'G': '01', 'A': '10', 'C': '11'},
        4: {'C': '00', 'A': '01', 'G': '10', 'T': '11'},
        5: {'C': '00', 'T': '01', 'G': '10', 'A': '11'},
        6: {'G': '00', 'A': '01', 'C': '10', 'T': '11'},
        7: {'G': '00', 'T': '01', 'C': '10', 'A': '11'}
    }

    # Chuyển đổi chuỗi DNA thành chuỗi nhị phân
    binary_arr = []
    for dna_seq in dna_seq_arr:
        binary_str = ''
        for dna in dna_seq:
            binary_str += decoding_rules[rule][dna]
        binary_arr.append(binary_str)

    return binary_arr

def dna_apply(Key, binary_audio, binary_chaosValue1, binary_chaosValue2):
  rule = Key % 8
  dnaseq_audio = Binary_to_DNA_Seq(rule, binary_audio)
  dnaseq_val1 = Binary_to_DNA_Seq(rule, binary_chaosValue1)
  dnaseq_val2 = Binary_to_DNA_Seq(rule, binary_chaosValue2)
  
  AddValue1 = DNA_addition(dnaseq_audio, dnaseq_val1)  
  Result = DNA_addition(AddValue1, dnaseq_val2)
  
  dnaseq_output = DNA_Seq_to_Binary(rule, Result)
  return dnaseq_output

def generate_encryption_key(Length, ShareKey, InitialVector):
    
    InitialVector_hex = Hex(InitialVector)

    I0 = int(InitialVector_hex[0:8], 16)
    I1 = int(InitialVector_hex[8:16], 16)
    I2 = int(InitialVector_hex[16:24], 16)
    I3 = int(InitialVector_hex[24:32], 16)

    IP_SC = 1 / (np.floor(int(ShareKey, 2)) + 1)
    CP_SC = 2.2 + ((I2 ^ I3) % 5)
    IP_LSC = 1 / (np.floor(int(InitialVector, 2)) + 1)
    CP_LSC = 1 / (np.floor(I3) + 1)

    val = I0 % 64
    IntermediateKey1 = ShareKey[val:val + 32]
    d = (2 * math.floor(np.floor(int(InitialVector, 2)) / 2)) + 1
    Tmp_Key = left_rotate(ShareKey, d)
    val1 = I1 % 64
    IntermediateKey2 = Tmp_Key[val1:val1 + 32]

    # CHAOTIC MAP GENERATION
    SineCosineSequence = SineCosineChaoticMap(IP_SC, CP_SC, Length)
    LogisticSineCosineSequence = LogisticSineCosine(IP_LSC, CP_LSC, Length)

    return IntermediateKey1, IntermediateKey2, SineCosineSequence, LogisticSineCosineSequence, I0, I1, I2, I3

def encrypt_song(Audio, ShareKey, InitialVector):
    Length = len(Audio)

    # Tạo mảng rỗng kiểu int16
    CipherVoice = np.zeros(Length, dtype=np.int16)

    # Tạo key cho mỗi bài hát
    IntermediateKey1, IntermediateKey2, SineCosineSequence, LogisticSineCosineSequence , I0, I1, I2, I3 = generate_encryption_key(Length, ShareKey, InitialVector)

    # PERMUTATION PHASE
    Permutated_Audio = Permutation(Audio, I3, SineCosineSequence)

    # DIFFUSION PHASE
    IntermediateKey1_int = int(IntermediateKey1, 2)
    IntermediateKey2_int = int(IntermediateKey2, 2)

    CM1 = ((IntermediateKey1_int * SineCosineSequence) / pow(2, 16)).astype(np.int16)
    CM2 = ((IntermediateKey2_int * LogisticSineCosineSequence) / pow(2, 16)).astype(np.int16)

    binary_audio = int16_array_to_binary16(Permutated_Audio)
    binary_val1 = int16_array_to_binary16(CM1)
    binary_val2 = int16_array_to_binary16(CM2)

    DNA_data = dna_apply(IntermediateKey2_int, binary_audio, binary_val1, binary_val2)

    # DYNAMIC SEQUENCE GENERATION
    I01 = np.zeros(Length, dtype=np.int16)
    I02 = np.zeros(Length, dtype=np.int16)

    for i in range(Length):
        I01[i] = np.int16((I1 * SineCosineSequence[i]))
        I02[i] = np.int16((I2 * LogisticSineCosineSequence[i]))

    DNA_Voice_data = np.zeros(Length, dtype=np.int16)
    for i in range(Length):
        DNA_Voice_data[i] = np.array(int(DNA_data[i], 2), dtype=np.uint16)

    for i in range(Length):
        val = (I0 * (i + 1)) % 2
        if val == 0:
            CipherVoice[i] = np.int16((DNA_Voice_data[i] + I01[i] * (i + 1)) % pow(2, 16))
        else:
            CipherVoice[i] = np.int16((DNA_Voice_data[i] + I02[i] * (i + 1)) % pow(2, 16))

    return CipherVoice

def encryption(path, ShareKey, pathOutput):
  # Đọc file âm thanh
  Audio, sample_rate = Input(path)
  
  # Tạo InitialVector một cách ngẫu nhiên
  InitialVector = Generation()
  
  chunk_size = 5000
  # Tính số chunks cần chia
  num_chunks = len(Audio) // chunk_size
  
  # Chuẩn bị list để lưu bản mã của từng chunk
  chunk_cipher_list = []
  start_time = 0
  end_time = 0

  # Chia bài hát thành các chunks
  for i in range(num_chunks):
    start_time = i * chunk_size
    end_time = (i + 1) * chunk_size
    chunk = Audio[start_time:end_time]
    
    # Mã hoá từng chunk
    chunk_encrypt = encrypt_song(chunk, ShareKey, InitialVector)
    
    # Lưu chunk được mã hoá vào danh sách
    chunk_cipher_list.append(chunk_encrypt)
    
  chunk_cipher = np.concatenate(chunk_cipher_list)  
  
  if num_chunks * chunk_size != len(Audio):
    chunk = Audio[end_time:len(Audio)]
    
    # Mã hoá từng chunk
    chunk_encrypt = encrypt_song(chunk, ShareKey, InitialVector)

    # Nối các mảng trong danh sách để có mảng cuối cùng
    chunk_cipher = np.concatenate([chunk_cipher, chunk_encrypt])
    
  Output(pathOutput, sample_rate, chunk_cipher)
  
  return InitialVector
 
# -------------- ENCRYPTION -------------- #
 