from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import pyperclip
import re

def setup_driver():
    """Thiết lập trình duyệt"""
    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def process_clipboard_data():
    """Xử lý dữ liệu từ clipboard"""
    # Lấy dữ liệu từ clipboard
    data = pyperclip.paste()
    
    # Tách thành các dòng
    lines = data.strip().split('\n')
    
    # Danh sách lưu kết quả
    results = []
    
    # Biến tạm để lưu thông tin doanh nghiệp
    current_company = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Nếu là mã số thuế (kiểm tra bằng regex)
        if re.match(r'^\d{10}$', line):
            # Nếu có thông tin công ty cũ, lưu vào kết quả
            if current_company:
                results.append(current_company)
            # Tạo công ty mới
            current_company = {'Mã số thuế': line}
            
        # Nếu là tên công ty (viết hoa)
        elif line.isupper():
            if 'Mã số thuế' in current_company:
                current_company['Tên doanh nghiệp'] = line
                
        # Nếu là ngày cấp (định dạng MM/YYYY)
        elif re.match(r'^\d{2}/\d{4}$', line):
            if 'Tên doanh nghiệp' in current_company:
                current_company['Ngày cấp'] = line
    
    # Thêm công ty cuối cùng
    if current_company:
        results.append(current_company)
    
    return results

def main():
    print("Bắt đầu chương trình...")
    driver = setup_driver()
    
    try:
        # Mở trang web
        url = "https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep"
        driver.get(url)
        
        print("\nHướng dẫn:")
        print("1. Tìm kiếm thông tin doanh nghiệp trên trang web")
        print("2. Bôi đen và copy (Ctrl+C) thông tin cần lưu")
        print("3. Nhấn Enter để xử lý dữ liệu")
        print("4. Nhập 'q' để thoát hoặc Enter để tiếp tục\n")
        
        while True:
            input("Nhấn Enter khi đã copy dữ liệu...")
            
            # Xử lý dữ liệu từ clipboard
            results = process_clipboard_data()
            
            if results:
                # Tạo DataFrame
                df = pd.DataFrame(results)
                
                # Lưu vào Excel
                df.to_excel('ThongTinDoanhNghiep.xlsx', index=False)
                
                print("\n=== THỐNG KÊ ===")
                print(f"Đã xử lý {len(results)} doanh nghiệp:")
                for company in results:
                    print(f"- {company['Tên doanh nghiệp']}")
                print("\nĐã lưu vào file: ThongTinDoanhNghiep.xlsx")
            else:
                print("Không tìm thấy dữ liệu hợp lệ trong clipboard!")
            
            choice = input("\nNhấn 'q' để thoát hoặc Enter để tiếp tục: ")
            if choice.lower() == 'q':
                break
    
    except Exception as e:
        print(f"Lỗi: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
