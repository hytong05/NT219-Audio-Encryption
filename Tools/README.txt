Phần 1: Chương trình chính
1. Nhập vào
    - Đọc từ file .wav tạo thành một mảng âm thanh
    - Xử lý dữ liệu để chuyển mảng âm thanh thành kiểu int16

2. Khởi tạo
    - Tạo một mảng CipherVoice rỗng kiểu int16 để lưu mảng âm thanh đã mã hoá
    - Tạo ra (Nhập vào) 
        + ShareKey: Khoá bí mật với kích thước 128 bit
        + InivialVector: Một giá trị ngẫu nhiên 128 bit dùng để tạo ra các giá trị khởi tạo
    - Chuyển đổi mảng InivialVector có 128 phần từ (0,1) thành mảng kiểu Hex (32 phần từ)
    - Tạo ra các giá trị ban đầu từ mảng InivialVector dạng Hex, chia theo theo thứ tự sau:
        + I0 = IntialVector_hex[0 : 8]
        + I1 = IntialVector_hex[8 : 16]
        + I2 = IntialVector_hex[16 : 24]
        + I3 = IntialVector_hex[24 : 32]
    - Sau đó chuyển những số vừa tạo thành dạng int
    - Tạo ra các giá trị seed và control parameter của hai Map:
        + Sine Cosine Map
            Seed: IP_SC
            Control parameter: CP_SC
        + Logistic Sine Cosine Map
            Seed: IP_LSC
            Control parameter: CP_LSC
    - Tạo ra IntermediateKey1 và IntermediateKey2 từ các giá trị của ShareKey, I0 và I1
    - Tạo ra hai mảng chaotic map (Phần 2)
    - Tạo các pha dành cho quá trình hoá vị (Phần 3)


-----------------------------------------------------------------------------------------------
Phần 2. Hàm tạo mảng chaotic map
    - Input: 
        + x0 -> giá trị ban đầu của chaotic map (intial seed)
        + m hoặc r -> giá trị tham gia vào biểu thức tạo hỗn loạn (control parameter)
        + n -> số lượng giá trị mong muốn nhận được (chiều dài của mảng)
    - Dựa vào các công thức của chaotic map, xây dựng giá trị trước
    - Output: trả về mảng bao gồm n phần từ có các giá trị khác nhau

-----------------------------------------------------------------------------------------------
Phần 3. Hàm tạo pha hoá vị
    - Khởi tạo các giá trị ban đầu:
        + div là số lượng đoạn đầy đủ (mỗi đoạn 16 phần tử) có thể tách ra từ mảng âm thanh
        + rem là số lượng phần tử còn lại sau khi chia mảng âm thanh thành các đoạn
    - Tạo mảng giá trị khởi tạo cho quá trình hoán vị (Initial_Seq) - mảng này có 16 phần tử (Phần 4)
    - Tạo mảng tương tự đối với phần còn lại của mảng âm thành (kích thước rem)
    - Tạo mảng output là một mảng rỗng dạng int16
    - Tạo mảng Permutated_Val dạng int16 với 16 giá trị ban đầu bằng 0
    - Duyệt qua từng đoạn 16 phần tử của mảng âm thanh
        + Xoay vòng các giá trị của mảng InitialSequence1 với số bước là IV3 * (i + 1) % 16, rồi lưu vào mảng Sequence
        + Lần lược lấy 16 phần từ thuộc đoạn đang xét lưu vào mảng Audio_16_val
            a. 

-----------------------------------------------------------------------------------------------
Phần 4. Hàm tạo mảng giá trị khởi tạo cho quá trình hoán vị
    - Tạo một mảng kiểu bool với các giá trị ban đầu đều bằng 0 (arr) - hàm đánh dấu
    - Tạo một mảng kiểu unsigned-integer 8 bit với các giá trị ban đầu đều bằng 0 (outputarr) - hàm ghi kết quả
    - Quá trình dùng vòng lặp while dùng để lưu các giá trị đôi một khác nhau lần lượt từ biểu thức tạo value_data vào mảng outputarr và đánh dấu các giá trị đã xuất hiện vào arr
    - Trả về mảng outputarr (gồm các phần từ khác nhau được tạo từ biểu thức value_data trong khoảng bé hơn SequenceSize)

-----------------------------------------------------------------------------------------------