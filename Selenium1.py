from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time

# Danh sách tài khoản test
usernames = [
    'standard_user',
    'locked_out_user',
    'problem_user',
    'performance_glitch_user',
    'error_user',
    'visual_user'
]
password = 'secret_sauce'

# Khởi tạo trình duyệt Chrome
options = Options()
driver = webdriver.Chrome(options=options)

# Danh sách lưu dữ liệu
all_data = []

def get_product_data(username):
    """Lấy thông tin sản phẩm sau khi đăng nhập thành công"""
    try:
        # Đợi lâu hơn cho performance_glitch_user
        wait_time = 30 if username == 'performance_glitch_user' else 20
        
        # Đợi cho đến khi tất cả sản phẩm được hiển thị
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )
        
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        print(f"    Tìm thấy {len(products)} sản phẩm")
        
        if not products:
            all_data.append({
                'Tài khoản': username,
                'Trạng thái': 'Đăng nhập thành công nhưng không tìm thấy sản phẩm',
                'Tên sản phẩm': '',
                'Giá': ''
            })
            return

        for product in products:
            try:
                name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
                price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
                all_data.append({
                    'Tài khoản': username,
                    'Trạng thái': 'Đăng nhập thành công',
                    'Tên sản phẩm': name,
                    'Giá': price
                })
            except:
                continue

    except TimeoutException:
        print("    Không thể tải danh sách sản phẩm - Timeout")
        all_data.append({
            'Tài khoản': username,
            'Trạng thái': 'Timeout khi tải sản phẩm',
            'Tên sản phẩm': '',
            'Giá': ''
        })

print("\n=== BẮT ĐẦU KIỂM TRA CÁC TÀI KHOẢN ===\n")

# Thử đăng nhập với từng tài khoản
for username in usernames:
    print(f"\nĐang kiểm tra: {username}")
    try:
        # Truy cập trang
        driver.get('https://www.saucedemo.com')
        
        # Đợi lâu hơn cho performance_glitch_user
        wait_time = 30 if username == 'performance_glitch_user' else 10
        
        # Đăng nhập
        username_field = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Kiểm tra đăng nhập thành công
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_container"))
        )
        print("    Đăng nhập thành công")
        
        # Lấy thông tin sản phẩm
        get_product_data(username)
        
        # Đăng xuất
        try:
            menu_button = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
            )
            menu_button.click()
            time.sleep(1)
            
            logout_link = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
            )
            logout_link.click()
            print("    Đã đăng xuất thành công")
            
        except Exception:
            print("    Không thể đăng xuất, tiếp tục với tài khoản tiếp theo")
        
    except TimeoutException:
        print("    Không thể đăng nhập - Timeout")
        all_data.append({
            'Tài khoản': username,
            'Trạng thái': 'Đăng nhập không thành công - Timeout',
            'Tên sản phẩm': '',
            'Giá': ''
        })
    except Exception as e:
        print(f"    Không thể đăng nhập - {str(e)}")
        all_data.append({
            'Tài khoản': username,
            'Trạng thái': 'Đăng nhập không thành công',
            'Tên sản phẩm': '',
            'Giá': ''
        })

# Đóng trình duyệt
driver.quit()

# Lưu dữ liệu vào file Excel
if all_data:
    df = pd.DataFrame(all_data)
    df = df.sort_values(['Tài khoản', 'Trạng thái'])
    df.to_excel("Selenium1.xlsx", index=False)
    print("\n=== KẾT QUẢ ===")
    print("Đã lưu thông tin vào file: Selenium1.xlsx")
    
    # Hiển thị thống kê
    success_accounts = df[df['Trạng thái'] == 'Đăng nhập thành công']['Tài khoản'].unique()
    failed_accounts = df[df['Trạng thái'] != 'Đăng nhập thành công']['Tài khoản'].unique()
    
    print("\nTài khoản đăng nhập thành công:")
    for acc in success_accounts:
        products_count = len(df[(df['Tài khoản'] == acc) & (df['Trạng thái'] == 'Đăng nhập thành công')])
        print(f"- {acc}: {products_count} sản phẩm")
    
    if len(failed_accounts) > 0:
        print("\nTài khoản đăng nhập thất bại:")
        for acc in failed_accounts:
            status = df[df['Tài khoản'] == acc]['Trạng thái'].iloc[0]
            print(f"- {acc}: {status}")
