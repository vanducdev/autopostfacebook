# Facebook Auto Post Tool

## Mô tả
Công cụ tự động đăng bài lên Facebook với giao diện dòng lệnh đẹp mắt.

<img width="1105" height="586" alt="image" src="https://github.com/user-attachments/assets/2bcd1a40-434d-4293-a8ac-9eac1ad6f4f5" />

## Tính năng
- Tự động đăng bài lên Facebook
- Hỗ trợ đăng ảnh và nội dung text
- Giao diện terminal với màu sắc đẹp
- Xác thực bằng key

## Cài đặt

### Yêu cầu
- Python 3.7+
- Chrome Browser

### Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Cấu hình
1. Đặt file cookie vào thư mục `input/cookie.txt`
2. Đặt nội dung bài đăng vào `input/ngon.txt`
3. Đặt danh sách nhóm vào `input/nhom.txt`
4. Đặt ảnh vào thư mục `input/`

## Sử dụng

### Chạy trực tiếp
```bash
python main.py
```

### Chạy bằng batch file (Windows)
```bash
run.bat
```

## Cấu trúc thư mục
```
AutoFacebook/
├── main.py              # File chính
├── config.py            # Cấu hình
├── requirements.txt     # Dependencies
├── setup.py            # Cài đặt package
├── .gitignore          # Git ignore
├── run.bat             # Batch file
├── README.md           # Documentation
├── input/              # Thư mục input
│   ├── cookie.txt      # Cookie Facebook
│   ├── ngon.txt        # Nội dung bài đăng
│   ├── nhom.txt        # Danh sách groups
│   └── *.jpg           # Ảnh đăng bài
├── output/             # Thư mục output
└── img/               # Thư mục ảnh
```

## Hỗ trợ
- Zalo: 0359261551
- Author: Trần Minh Triết

## Lưu ý
- Sử dụng công cụ này có thể vi phạm điều khoản sử dụng của Facebook
- Vui lòng sử dụng có trách nhiệm
- Công cụ chỉ dành cho mục đích học tập
