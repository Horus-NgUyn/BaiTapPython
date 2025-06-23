# RPA Tải Hóa Đơn Điện Tử từ MeInvoice.vn

Script Python tự động hóa việc tra cứu và tải hóa đơn điện tử từ trang web https://www.meinvoice.vn/tra-cuu sử dụng Selenium WebDriver.

## Tính năng

- ✅ Tự động truy cập trang tra cứu hóa đơn
- ✅ Nhập mã tra cứu hóa đơn tự động
- ✅ Tìm kiếm và tải xuống hóa đơn
- ✅ Xử lý lỗi và ghi log chi tiết
- ✅ Hỗ trợ nhiều loại selector khác nhau
- ✅ Tự động tạo thư mục tải xuống

## Yêu cầu hệ thống

- Python 3.7+
- Google Chrome browser
- Windows 10/11 (đã test)

## Cài đặt

1. **Clone hoặc tải về project:**
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Hoặc cài đặt thủ công:**
   ```bash
   pip install selenium==4.15.0
   pip install webdriver-manager==4.0.1
   ```

## Sử dụng

### Chạy với mã test có sẵn:
```bash
python DownloadInvoiceMisa.py
```

### Sử dụng trong code Python khác:
```python
from DownloadInvoiceMisa import MeInvoiceDownloader

# Khởi tạo downloader
downloader = MeInvoiceDownloader()

# Tải hóa đơn theo mã tra cứu
success = downloader.download_invoice_by_code("YOUR_INVOICE_CODE")

if success:
    print("Tải hóa đơn thành công!")
else:
    print("Tải hóa đơn thất bại!")
```

### Tùy chỉnh thư mục tải xuống:
```python
# Chỉ định thư mục tải xuống tùy chỉnh
custom_download_dir = r"C:\MyInvoices"
downloader = MeInvoiceDownloader(download_dir=custom_download_dir)
```

## Cấu hình

### Thư mục tải xuống mặc định:
- Windows: `%USERPROFILE%\Downloads\InvoiceMisa`
- Ví dụ: `C:\Users\YourName\Downloads\InvoiceMisa`

### Chế độ headless (không hiển thị trình duyệt):
Mở file `DownloadInvoiceMisa.py` và bỏ comment dòng:
```python
# chrome_options.add_argument("--headless")
```

## Logs

Script sẽ tạo file log `invoice_download.log` trong thư mục hiện tại với thông tin chi tiết về quá trình thực thi.

## Xử lý lỗi

Script có xử lý các lỗi phổ biến:
- ❌ Không tìm thấy hóa đơn
- ❌ Mã tra cứu không đúng
- ❌ Lỗi kết nối mạng
- ❌ Timeout khi tải trang
- ❌ Không tìm thấy các element trên trang

## Mã test

Mã hóa đơn test được cung cấp trong tài liệu: `B1HEIRR8N0WP`

## Lưu ý quan trọng

1. **Tuân thủ Terms of Service:** Đảm bảo việc sử dụng script tuân thủ điều khoản sử dụng của meinvoice.vn
2. **Rate limiting:** Tránh gửi quá nhiều request trong thời gian ngắn
3. **Captcha:** Nếu trang web yêu cầu captcha, script sẽ cần can thiệp thủ công
4. **Cập nhật giao diện:** Nếu trang web thay đổi giao diện, có thể cần cập nhật selector

## Troubleshooting

### Lỗi ChromeDriver:
```
WebDriverException: 'chromedriver' executable needs to be in PATH
```
**Giải pháp:** Script sử dụng `webdriver-manager` để tự động tải ChromeDriver, đảm bảo đã cài đặt đúng.

### Lỗi timeout:
```
TimeoutException: Message: 
```
**Giải pháp:** Kiểm tra kết nối internet và thử lại. Có thể tăng timeout trong code.

### Không tìm thấy element:
```
NoSuchElementException: Unable to locate element
```
**Giải pháp:** Trang web có thể đã thay đổi cấu trúc. Kiểm tra và cập nhật selector trong code.

## Tác giả

Script được phát triển dựa trên tài liệu hướng dẫn RPA cho việc tự động hóa tải hóa đơn điện tử.

## License

MIT License - Sử dụng cho mục đích học tập và nghiên cứu. 