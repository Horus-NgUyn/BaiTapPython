import time
import os
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('invoice_download.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class MeInvoiceDownloader:
    def __init__(self, download_dir: Optional[str] = None):
        self.url = "https://www.meinvoice.vn/tra-cuu"
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.download_dir = download_dir or os.path.join(os.path.expanduser("~"), "Downloads", "InvoiceMisa")
        os.makedirs(self.download_dir, exist_ok=True)
        logging.info(f"Thư mục tải xuống: {self.download_dir}")

    def setup_driver(self) -> bool:
        try:
            logging.info("Đang khởi tạo trình duyệt...")
            chrome_options = Options()
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 15)
            logging.info(" Trình duyệt đã khởi tạo thành công")
            return True
        except Exception as e:
            logging.error(f" Lỗi khi thiết lập WebDriver: {str(e)}")
            return False

    def navigate_to_page(self) -> bool:
        try:
            if not self.driver or not self.wait:
                return False
            logging.info(f"Đang truy cập: {self.url}")
            self.driver.get(self.url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)  # Chờ trang tải hoàn toàn
            logging.info(" Đã truy cập trang thành công")
            return True
        except Exception as e:
            logging.error(f" Lỗi khi truy cập trang: {str(e)}")
            return False

    def input_invoice_code(self, code: str) -> bool:
        try:
            if not self.wait:
                return False
            logging.info(f"Đang nhập mã tra cứu: {code}")
            selectors = [
                'input[placeholder="Nhập mã tra cứu hóa đơn"]',
                'input[type="text"]'
            ]
            for selector in selectors:
                try:
                    field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    if field.is_displayed() and field.is_enabled():
                        field.clear()
                        field.send_keys(code)
                        logging.info(f" Đã nhập mã thành công: {code}")
                        return True
                except:
                    continue
            logging.error(" Không tìm thấy trường nhập mã tra cứu")
            return False
        except Exception as e:
            logging.error(f" Lỗi khi nhập mã tra cứu: {str(e)}")
            return False

    def click_search_button(self) -> bool:
        try:
            if not self.wait or not self.driver:
                return False
            logging.info("Đang tìm nút tìm kiếm...")
            time.sleep(1)  # Chờ một chút
            
            # Sử dụng id chính xác của button
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btnSearchInvoice")))
                btn.click()
                logging.info(" Đã nhấn nút tìm kiếm: btnSearchInvoice")
                return True
            except:
                logging.warning("Không tìm thấy button với id btnSearchInvoice, thử các cách khác...")
            
            # Fallback: thử xpath
            xpath_variants = [
                "//button[@id='btnSearchInvoice']",
                "//button[contains(text(), 'Tìm kiếm')]",
                "//button[contains(text(), 'Tra cứu')]",
                "//input[@value='Tìm kiếm']",
                "//input[@value='Tra cứu']"
            ]
            for xpath in xpath_variants:
                try:
                    btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    if btn.is_displayed():
                        btn.click()
                        logging.info(f" Đã nhấn nút tìm kiếm: {xpath}")
                        return True
                except:
                    continue
            
            # Fallback cuối: nhấn Enter
            logging.info("Thử nhấn Enter trên input field...")
            input_field = self.driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
            input_field.send_keys(Keys.RETURN)
            logging.info(" Đã nhấn Enter")
            return True
        except Exception as e:
            logging.error(f" Lỗi khi nhấn nút tìm kiếm: {str(e)}")
            return False

    def wait_for_results(self) -> bool:
        try:
            if not self.driver or not self.wait:
                return False
            logging.info("Đang chờ kết quả tra cứu...")
            
            # Kiểm tra xem có button download xuất hiện không
            for i in range(20):  # Tăng thời gian chờ lên 20 giây
                try:
                    # Thử tìm button download trực tiếp
                    download_btn = self.driver.find_element(By.ID, "download")
                    if download_btn.is_displayed():
                        logging.info(" Phát hiện button tải xuống - hóa đơn hợp lệ")
                        return True
                except:
                    pass
                
                # Kiểm tra các từ khóa trong trang
                page_source = self.driver.page_source.lower()
                
                # Kiểm tra lỗi
                error_keywords = ['không tìm thấy', 'not found', 'error', 'không có dữ liệu', 'mã tra cứu không đúng']
                if any(k in page_source for k in error_keywords):
                    logging.warning(" Phát hiện thông báo lỗi - hóa đơn không tồn tại")
                    return False
                
                # Kiểm tra thành công (fallback)
                success_keywords = ['download', 'tải xuống', 'pdf', 'file-download']
                if any(k in page_source for k in success_keywords):
                    logging.info(" Phát hiện từ khóa tải xuống")
                    time.sleep(2)  # Chờ thêm 2 giây để button load
                    return True
                    
                logging.info(f"Chờ kết quả... ({i+1}/20)")
                time.sleep(1)
                
            logging.warning(" Timeout chờ kết quả (20 giây)")
            return False
        except Exception as e:
            logging.error(f" Lỗi khi chờ kết quả: {str(e)}")
            return False

    def download_invoice(self) -> bool:
        try:
            if not self.driver or not self.wait:
                return False
            logging.info("Đang tìm nút tải xuống...")
            
            # Sử dụng id chính xác của button download
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.ID, "download")))
                btn.click()
                logging.info(" Đã nhấn nút tải xuống: download")
                time.sleep(5)  # Chờ file tải xuống
                return True
            except:
                logging.warning("Không tìm thấy button với id download, thử các cách khác...")
            
            # Fallback: thử các selector khác
            selectors = [
                'cr-icon-button[id="download"]',
                'button[id="download"]',
                '[aria-label="Tải xuống"]',
                '[title="Tải xuống"]',
                'a[href*="download"]',
                'a[href*="pdf"]'
            ]
            for selector in selectors:
                try:
                    btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    if btn.is_displayed():
                        btn.click()
                        logging.info(f" Đã nhấn nút tải xuống: {selector}")
                        time.sleep(5)
                        return True
                except:
                    continue
            
            logging.error(" Không tìm thấy nút tải xuống")
            return False
        except Exception as e:
            logging.error(f" Lỗi khi tải hóa đơn: {str(e)}")
            return False

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"Lỗi khi đóng trình duyệt: {str(e)}")

    def download_invoice_by_code(self, code: str) -> bool:
        try:
            if not self.setup_driver(): return False
            if not self.navigate_to_page(): return False
            if not self.input_invoice_code(code): return False
            if not self.click_search_button(): return False
            if not self.wait_for_results(): return False
            if not self.download_invoice(): return False
            return True
        finally:
            self.close()

def read_invoice_codes_from_file(file_path: str) -> list:
    if not os.path.exists(file_path):
        logging.error(f"File không tồn tại: {file_path}")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-16') as f:
            return [line.strip() for line in f if line.strip()]

def main():
    codes = read_invoice_codes_from_file("invoice_codes.txt")
    if not codes:
        print("Không có mã hóa đơn để xử lý.")
        return
    for code in codes:
        print(f"Đang xử lý mã: {code}")
        bot = MeInvoiceDownloader()
        if bot.download_invoice_by_code(code):
            print(f" Thành công: {code}")
        else:
            print(f" Thất bại: {code}")

if __name__ == "__main__":
    main()
