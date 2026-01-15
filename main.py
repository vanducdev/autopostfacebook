import os
import time
import random
import requests
import pyperclip
from datetime import datetime
from colorama import init
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from pystyle import Colors, Colorate, Center
import sys
import threading

# Khởi tạo colorama
init(autoreset=True)

# Màu sắc tùy chỉnh
màu = Colors.DynamicMIX([Colors.cyan, Colors.white, Colors.pink])

class KeyAuth:
    def __init__(self):
        self.correct_key = "ducvannguyen"
        self.loading_chars = ["|", "/", "-", "\\"]
        
    def show_bigtext(self):
        bigtext = f"""
           ▄▄▄     ▄▄▄                    ▄▄▄▄▄▄           ▄▄       
            ███▄ ▄███                    █▀▀██▀▀▀           ██      
 ▄▄         ██ ▀█▀ ██         ▀▀ ▄          ██               ██      
  ▀█▄       ██     ██   ▄▀▀█▄ ██ ████▄      ██   ▄███▄ ▄███▄ ██ ▄██▀█
   ▄█▀      ██     ██   ▄█▀██ ██ ██ ██      ██   ██ ██ ██ ██ ▀███▄
 ▄█▀      ▀██▀     ▀██▄▄▀█▄██▄██▄██ ▀█      ▀██▄▄▀███▀▄▀███▀▄███▄▄██▀
                                                                 
                                                                 
    Tool Facebook Auto Post
    [ Zalo: 0359261551 ]                                                              
    [ Athur: Trần Minh Triết ]
 
"""
        print(Colorate.Horizontal(màu, Center.XCenter(bigtext)))
        
    def loading_animation(self, stop_event, message="Đang xử lý"):
        i = 0
        dots = [".  ", ".. ", "..."]
        while not stop_event.is_set():
            print(f"\r{Colorate.Horizontal(màu, f'{message}{dots[i % 3]}')}", end="")
            time.sleep(1)  # 1 giây mỗi lần
            i += 1
        print("\r" + " " * 50 + "\r", end="")
        
    def authenticate(self):
        self.clear_screen()
        self.show_bigtext()
        
        while True:
            key = input(Colorate.Horizontal(màu, "   Nhập key để vào tool: "))
            
            if key == self.correct_key:
                print(Colorate.Horizontal(màu, "   ✓ Key đúng! Đang xác thực..."))
                
                # Loading chi tiết 1 giây mỗi bước
                steps = [
                    "   Đang kiểm tra key...",
                    "   Đang tải cấu hình...",
                    "   Đang khởi tạo hệ thống...",
                    "   Đang chuẩn bị môi trường..."
                ]
                
                for step in steps:
                    print(f"\r{Colorate.Horizontal(màu, step)}", end="")
                    time.sleep(1)
                
                print("\r" + " " * 50 + "\r", end="")
                print(Colorate.Horizontal(Colors.green_to_white, "   ✓ Xác thực thành công! Đang vào tool..."))
                time.sleep(1)
                return True
            else:
                print(Colorate.Horizontal(Colors.red_to_white, "   ✗ Key sai! Vui lòng thử lại."))
                time.sleep(1)
                self.clear_screen()
                self.show_bigtext()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

class FacebookAutomationUltimate:
    def __init__(self):
        # Kiểm tra key trước khi khởi tạo
        auth = KeyAuth()
        if not auth.authenticate():
            sys.exit(0)
            
        self.api_key = ""
        self.driver = None
        self.author = "Trần Minh Triết"
        self.cookie_file = "input/cookie.txt"
        self.content_file = "input/ngon.txt"
        self.groups_file = "input/nhom.txt"
        self.img_dir = "input"
        self.output_dir = "output"
        self.multi_account_mode = False  # Chế độ nhiều tài khoản
        self.proxy_list = []  # Danh sách proxy đa luồng
        self.current_proxy_index = 0  # Index proxy hiện tại
        self.cookie_str = self.load_cookie()
        
        # Tạo thư mục nếu chưa tồn tại
        self.create_directories()

        self.ascii_banner = """
                                                                                  
  ▄▄▄▄▄▄              ▄▄▄                   ▄▄     ▄▄▄                            
 █▀██▀▀██            █▀██  ██▀▀             ██▄   ██▀                             
   ██   ██             ██  ██       ▄       ███▄  ██    ▄▄                   ▄    
   ██   ██ ██ ██ ▄███▀ ██  ██ ▄▀▀█▄ ████▄   ██ ▀█▄██ ▄████ ██ ██ ██ ██ ▄█▀█▄ ████▄
 ▄ ██   ██ ██ ██ ██    ██▄ ██ ▄█▀██ ██ ██   ██   ▀██ ██ ██ ██ ██ ██▄██ ██▄█▀ ██ ██
 ▀██▀███▀ ▄▀██▀█▄▀███▄  ▀███▀▄▀█▄██▄██ ▀█ ▀██▀    ██▄▀████▄▀██▀█▄▄▀██▀▄▀█▄▄▄▄██ ▀█
                                                        ██         ██             
                                                      ▀▀▀        ▀▀▀              
        """

    def create_directories(self):
        """Tạo các thư mục cần thiết"""
        directories = ["input", "img", "output"]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Thư mục] Đã tạo thư mục: {directory}"))
    
    def check_multi_account_mode(self):
        """Kiểm tra xem có phải chế độ nhiều tài khoản không"""
        # Kiểm tra xem có nhiều file cookie không
        cookie_files = []
        for file in os.listdir("input"):
            if file.startswith("cookie") and file.endswith(".txt"):
                cookie_files.append(file)
        
        if len(cookie_files) > 1:
            self.multi_account_mode = True
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đa tài khoản] Phát hiện {len(cookie_files)} file cookie, kích hoạt chế độ nhiều tài khoản"))
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Sẽ sử dụng proxy đa luồng, mỗi Chrome 1 proxy"))
            # Tự động load proxy đa luồng
            self.load_multiple_proxies()
        else:
            self.multi_account_mode = False
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đơn tài khoản] Chế độ đơn tài khoản, không sử dụng proxy"))
    
    def load_multiple_proxies(self):
        """Load proxy đa luồng từ file hoặc API"""
        timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
        
        # Ưu tiên 1: Load từ file proxy.txt
        proxy_file = "input/proxy.txt"
        if os.path.exists(proxy_file):
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đang load proxy từ file {proxy_file}..."))
            with open(proxy_file, "r", encoding="utf-8") as f:
                proxies = [line.strip() for line in f if line.strip()]
            self.proxy_list = proxies
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đã load {len(proxies)} proxy từ file"))
            return
        
        # Ưu tiên 2: Load từ API WWProxy
        if self.api_key:
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đang load proxy đa luồng từ API WWProxy..."))
            try:
                # Lấy nhiều proxy từ API
                for i in range(5):  # Lấy 5 proxy
                    url = f"https://wwproxy.com/api/client/proxy/available?key={self.api_key}&provinceId=-1"
                    res = requests.get(url).json()
                    if res.get("status") == "OK":
                        proxy = res["data"]["proxy"]
                        self.proxy_list.append(proxy)
                        print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đã lấy proxy {i+1}: {proxy}"))
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Proxy] API lỗi proxy {i+1}: {res.get('message', 'Unknown error')}"))
                    time.sleep(1)
                
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đã load {len(self.proxy_list)} proxy từ API"))
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Proxy] Lỗi load proxy API: {e}"))
        
        # Nếu không có proxy nào
        if not self.proxy_list:
            print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Proxy] Không tìm thấy proxy nào! Vui lòng thêm proxy vào file input/proxy.txt hoặc nhập API Key"))

    def load_cookie(self):
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                return f.read().strip()

    def save_cookie(self, new_cookie):
        with open(self.cookie_file, "w", encoding="utf-8") as f:
            f.write(new_cookie)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        self.clear_screen()
        print(Colorate.Horizontal(màu, Center.XCenter(self.ascii_banner)))
        
        status_cookie = "Đã nạp" if self.cookie_str else "Chưa có"
        info_menu = f"""
 Author: {self.author}  |  Time: {datetime.now().strftime("%d/%m/%Y | %H:%M:%S")}
 Status: {status_cookie}
 
[1] »» Nhập API Key WWProxy
[2] »» Cập nhật Cookie Facebook
[3] »» Quét tất cả nhóm đã tham gia
[4] »» Auto Post Facebook (Có dạo lướt)
[5] »» Auto Post Facebook (Nhanh)
[6] »» Đóng trình duyệt & Thoát
        """
        print(Colorate.Horizontal(màu, Center.XCenter(info_menu)))

    def get_proxy(self):
        # Chỉ sử dụng proxy ở chế độ nhiều tài khoản
        if not self.multi_account_mode:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Chế độ đơn tài khoản, không sử dụng proxy"))
            return None
            
        # Chế độ nhiều tài khoản - sử dụng proxy đa luồng
        if not self.proxy_list:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Proxy] Chưa có proxy nào trong danh sách!"))
            return None
            
        # Lấy proxy hiện tại theo vòng tròn
        current_proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        
        timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
        print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Sử dụng proxy {self.current_proxy_index}/{len(self.proxy_list)}: {current_proxy}"))
        return current_proxy

    def log_result(self, group_url, result, current, total):
        """Ghi kết quả đăng bài vào file output"""
        timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
        
        # Tạo file output nếu chưa tồn tại
        output_file = os.path.join(self.output_dir, f"ket_qua_dang_bai_{datetime.now().strftime('%d%m%Y')}.txt")
        
        with open(output_file, "a", encoding="utf-8") as f:
            if result["success"]:
                f.write(f"[{timestamp}] ✓ THÀNH CÔNG - Nhóm {current}/{total}: {group_url}\n")
            else:
                f.write(f"[{timestamp}] ✗ LỖI - Nhóm {current}/{total}: {group_url} - Lỗi: {result['error']}\n")
    
    def browse_and_like_posts(self, duration_minutes=5):
        """Dạo lướt nhóm và like bài viết như người thật"""
        try:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Dạo lướt] Bắt đầu dạo lướt và like bài viết trong {duration_minutes} phút..."))
            
            end_time = time.time() + (duration_minutes * 60)
            actions_count = 0
            
            while time.time() < end_time:
                # Lướt trang ngẫu nhiên
                scroll_actions = random.randint(2, 5)
                for i in range(scroll_actions):
                    self.driver.execute_script("window.scrollBy(0, random.randint(200, 600));")
                    time.sleep(random.uniform(1, 3))
                    actions_count += 1
                
                # Tìm và like bài viết
                try:
                    # Tìm các nút like
                    like_buttons = self.driver.find_elements(By.XPATH, "//div[@aria-label='Thích' or @aria-label='Like']")
                    if like_buttons:
                        # Like ngẫu nhiên 1-2 bài
                        num_likes = min(random.randint(1, 2), len(like_buttons))
                        for i in range(num_likes):
                            if i < len(like_buttons):
                                try:
                                    # Hover vào bài viết trước khi like
                                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", like_buttons[i])
                                    time.sleep(random.uniform(1, 2))
                                    
                                    # Click like
                                    like_buttons[i].click()
                                    time.sleep(random.uniform(0.5, 1.5))
                                    actions_count += 1
                                    
                                    timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Like] Đã like bài viết {i+1}"))
                                except:
                                    continue
                except:
                    pass
                
                # Nghỉ ngẫu nhiên
                time.sleep(random.uniform(3, 8))
                
                # Kiểm tra thởi gian
                if time.time() >= end_time:
                    break
            
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(Colors.green_to_white, f" » [{timestamp}] » [Hoàn tất] Đã dạo lướt xong! Thực hiện {actions_count} hành động"))
            
        except Exception as e:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Lỗi] Lỗi khi dạo lướt: {e}"))

    def post_to_group_with_browsing(self, group_url, content, browse_duration=3):
        """Đăng bài kèm dạo lướt như người thật"""
        try:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bắt đầu] Đang xử lý nhóm: {group_url}"))
            
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đang mở] Truy cập vào nhóm Facebook..."))
            self.driver.get(group_url)
            time.sleep(random.uniform(7, 10))
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã mở] Đã truy cập thành công vào nhóm"))
            
            # Dạo lướt trước khi đăng bài
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Dạo lướt] Đang dạo lướt {browse_duration} phút trước khi đăng bài..."))
            self.browse_and_like_posts(browse_duration)
            
            # Mở ô đăng bài
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 1/4] Tìm ô đăng bài..."))
            time.sleep(1)
            post_box = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Bạn viết gì đi') or contains(text(), 'Viết thảo luận')]")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 2/4] Đã tìm thấy ô đăng bài"))
            time.sleep(1)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 3/4] Click vào ô đăng bài..."))
            post_box.click()
            time.sleep(1)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 4/4] Đã mở ô đăng bài thành công"))
            time.sleep(1)

            # Dán TOÀN BỘ nội dung từ ngon.txt
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 1/4] Sao chép nội dung từ file {self.content_file}..."))
            time.sleep(1)
            pyperclip.copy(content)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 2/4] Nội dung đã được sao chép vào clipboard"))
            time.sleep(1)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 3/4] Dán nội dung vào ô đăng bài..."))
            time.sleep(1)
            active_element = self.driver.switch_to.active_element
            active_element.send_keys(Keys.CONTROL, 'v') 
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 4/4] Nội dung đã được điền thành công"))
            time.sleep(1)

            # Upload 3 ảnh
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 1/5] Bắt đầu upload 3 ảnh từ thư mục {self.img_dir}..."))
            time.sleep(1)
            image_input = self.driver.find_element(By.XPATH, "//input[@type='file' and @multiple]")
            
            # Lấy danh sách ảnh từ thư mục img
            img_files = []
            if os.path.exists(self.img_dir):
                for file in os.listdir(self.img_dir):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        img_files.append(os.path.join(self.img_dir, file))
            
            # Sử dụng 3 ảnh đầu tiên (hoặc tất cả nếu ít hơn 3)
            images_to_upload = img_files[:3] if len(img_files) >= 3 else img_files
            
            if not images_to_upload:
                print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] Không tìm thấy ảnh trong thư mục {self.img_dir}!"))
                return
            
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 2/5] Đã chọn các file ảnh: {', '.join([os.path.basename(img) for img in images_to_upload])}"))
            time.sleep(1)
            full_paths = "\n".join([os.path.abspath(img) for img in images_to_upload])
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 3/5] Đang gửi ảnh lên trình duyệt..."))
            time.sleep(1)
            image_input.send_keys(full_paths)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 4/5] Đang xử lý upload ảnh..."))
            time.sleep(1)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 5/5] Chờ 15 giây để upload hoàn tất..."))
            time.sleep(15) 
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [HOÀN TẤT] Upload ảnh hoàn tất"))

            # Bấm Đăng
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 1/3] Tìm nút Đăng..."))
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//div[@aria-label='Đăng' or @aria-label='Post']").click()
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 2/3] Đã click nút Đăng"))
            time.sleep(1)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bước 3/3] Bài viết đang được đăng..."))
            time.sleep(5)
            print(Colorate.Horizontal(Colors.green_to_white, f" » [{timestamp}] » [SUCCESS] Đã đăng bài thành công vào nhóm!"))
            
            # Dạo lướt sau khi đăng bài
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Dạo lướt] Dạo lướt thêm 2 phút sau khi đăng bài..."))
            self.browse_and_like_posts(2)
            
        except Exception as e:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] {e}"))

    def scan_all_groups(self):
        try:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bắt đầu] Bắt đầu quét tất cả nhóm đã tham gia"))
            
            # Khởi tạo trình duyệt nếu chưa có
            if not self.driver:
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đang lấy proxy..."))
                proxy = self.get_proxy()
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Trình duyệt] Đang khởi tạo Chrome..."))
                options = uc.ChromeOptions()
                if proxy: options.add_argument(f'--proxy-server={proxy}')
                self.driver = uc.Chrome(options=options)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Trình duyệt] Đã khởi tạo Chrome thành công"))
                
                # Đăng nhập bằng Cookie
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đăng nhập] Đang truy cập Facebook..."))
                self.driver.get("https://www.facebook.com")
                time.sleep(3)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Đang thêm cookie vào trình duyệt..."))
                for item in self.cookie_str.split(';'):
                    if '=' in item:
                        n, v = item.strip().split('=', 1)
                        self.driver.add_cookie({'name': n, 'value': v, 'domain': '.facebook.com'})
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Đã thêm cookie thành công"))
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Làm mới] Đang làm mới trang để áp dụng cookie..."))
                self.driver.refresh()
                time.sleep(5)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đăng nhập] Đăng nhập thành công vào Facebook"))
            
            # Truy cập trang nhóm đã tham gia
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đang truy cập] Đang truy cập trang nhóm đã tham gia..."))
            self.driver.get("https://www.facebook.com/groups/joins/?nav_source=tab")
            time.sleep(5)
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã truy cập] Đã truy cập trang nhóm thành công"))
            
            # Cuộn trang để tải tất cả nhóm
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đang tải] Đang cuộn trang để tải tất cả nhóm..."))
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 10  # Giới hạn số lần cuộn để tránh vô tận
            
            while scroll_attempts < max_scrolls:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_attempts += 1
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đang cuộn] Đã cuộn {scroll_attempts}/{max_scrolls} lần..."))
            
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã tải] Hoàn tất tải tất cả nhóm"))
            
            # Tìm tất cả link nhóm
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đang quét] Đang quét link nhóm..."))
            group_links = []
            
            # Tìm các link nhóm theo nhiều selector khác nhau
            selectors = [
                "a[href*='/groups/']",
                "div[role='article'] a[href*='/groups/']",
                "span a[href*='/groups/']",
                "div[role='feed'] a[href*='/groups/']",
                "div[data-overviewsection='groups'] a[href*='/groups/']"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute('href')
                        if href and '/groups/' in href and 'facebook.com' in href:
                            # Làm sạch link
                            clean_link = href.split('?')[0].rstrip('/')
                            # Kiểm tra link hợp lệ (phải có ID nhóm)
                            if len(clean_link.split('/')) >= 5 and clean_link != 'https://www.facebook.com/groups':
                                if clean_link not in group_links:
                                    group_links.append(clean_link)
                                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Tìm thấy] Link nhóm: {clean_link}"))
                except Exception as e:
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Lỗi selector] {selector}: {e}"))
                    continue
            
            # Loại bỏ các link trùng lặp và không hợp lệ
            unique_links = list(set(group_links))
            valid_links = []
            
            for link in unique_links:
                if len(link.split('/')) >= 4 and link != 'https://www.facebook.com/groups':
                    valid_links.append(link)
            
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã quét] Đã tìm thấy {len(valid_links)} nhóm"))
            
            # Lưu vào file trong thư mục output
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
                
            filename = os.path.join(self.output_dir, f"nhom_quet_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt")
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đang lưu] Đang lưu vào file {filename}..."))
            
            with open(filename, "w", encoding="utf-8") as f:
                for link in valid_links:
                    f.write(link + "\n")
            
            print(Colorate.Horizontal(Colors.green_to_white, f" » [{timestamp}] » [HOÀN TẤT] Đã lưu {len(valid_links)} link nhóm vào file {filename}"))
            
            # Hiển thị một vài link mẫu
            print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Mẫu] Một vài link nhóm:"))
            for i, link in enumerate(valid_links[:5], 1):
                print(Colorate.Horizontal(màu, f"   {i}. {link}"))
            
            if len(valid_links) > 5:
                print(Colorate.Horizontal(màu, f"   ... và {len(valid_links) - 5} link khác"))
            
            input("Hoàn thành! Nhấn Enter...")
        except Exception as e:
            timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
            print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] {e}"))
            input("Đã xảy ra lỗi! Nhấn Enter...")

    def run(self):
        while True:
            self.show_menu()
            choice = input(Colorate.Horizontal(màu, " »» Chọn: "))
            
            if choice == "1":
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [API Key] Nhập API Key WWProxy:"))
                self.api_key = input(" »» Nhập API Key: ")
                if self.api_key:
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [API Key] Đã lưu API Key thành công"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [API Key] API Key trống!"))
            elif choice == "2":
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Nhập Cookie Facebook:"))
                new_ck = input(" »» Dán Cookie mới vào đây: ")
                if new_ck:
                    self.save_cookie(new_ck)
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Đã lưu cookie vào file thành công!"))
                    time.sleep(1)
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Cookie] Cookie trống!"))
            elif choice == "3":
                if not self.cookie_str:
                    timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] Chưa nhập Cookie Facebook!"))
                    time.sleep(2)
                    continue
                
                # Kiểm tra chế độ nhiều tài khoản trước khi quét
                self.check_multi_account_mode()
                self.scan_all_groups()
            elif choice == "4":
                if not self.cookie_str:
                    timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] Chưa nhập Cookie Facebook!"))
                    time.sleep(2)
                    continue
                
                # Kiểm tra chế độ nhiều tài khoản trước khi đăng bài
                self.check_multi_account_mode()
                
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bắt đầu] Bắt đầu quá trình Auto Post Facebook có dạo lướt"))
                
                # Đọc dữ liệu từ file
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đọc file] Đọc danh sách nhóm từ {self.groups_file}..."))
                if not os.path.exists(self.groups_file):
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] File {self.groups_file} không tồn tại!"))
                    time.sleep(2)
                    continue
                    
                with open(self.groups_file, "r", encoding="utf-8") as f: nhoms = [l.strip() for l in f if l.strip()]
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đọc] Đã đọc {len(nhoms)} nhóm từ file"))
                
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đọc file] Đọc nội dung từ {self.content_file}..."))
                if not os.path.exists(self.content_file):
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] File {self.content_file} không tồn tại!"))
                    time.sleep(2)
                    continue
                    
                with open(self.content_file, "r", encoding="utf-8") as f: content = f.read()
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đọc] Đã đọc nội dung bài viết ({len(content)} ký tự)"))
                
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đang lấy proxy..."))
                proxy = self.get_proxy()
                if proxy:
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đã lấy proxy: {proxy}"))
                else:
                    if self.multi_account_mode:
                        print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Proxy] Không lấy được proxy, có thể bị checkpoint!"))
                    else:
                        print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Chế độ đơn tài khoản, không sử dụng proxy"))
                
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Trình duyệt] Đang khởi tạo Chrome..."))
                options = uc.ChromeOptions()
                if proxy: options.add_argument(f'--proxy-server={proxy}')
                self.driver = uc.Chrome(options=options)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Trình duyệt] Đã khởi tạo Chrome thành công"))
                
                # Đăng nhập bằng Cookie
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đăng nhập] Đang truy cập Facebook..."))
                self.driver.get("https://www.facebook.com")
                time.sleep(3)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Đang thêm cookie vào trình duyệt..."))
                for item in self.cookie_str.split(';'):
                    if '=' in item:
                        n, v = item.strip().split('=', 1)
                        self.driver.add_cookie({'name': n, 'value': v, 'domain': '.facebook.com'})
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Đã thêm cookie thành công"))
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Làm mới] Đang làm mới trang để áp dụng cookie..."))
                self.driver.refresh()
                time.sleep(5)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đăng nhập] Đăng nhập thành công vào Facebook"))

                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bắt đầu] Bắt đầu đăng bài vào {len(nhoms)} nhóm (có dạo lướt)..."))
                for i, link in enumerate(nhoms, 1):
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Tiến trình] Đang xử lý nhóm {i}/{len(nhoms)}"))
                    result = self.post_to_group_with_browsing(link, content, browse_duration=3)
                    
                    # Ghi kết quả vào file output
                    self.log_result(link, result, i, len(nhoms))
                    
                    wait_time = random.randint(40, 60)
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Nghỉ] Đợi {wait_time} giây trước khi đăng nhóm tiếp theo..."))
                    time.sleep(wait_time)
                
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(Colors.green_to_white, f" » [{timestamp}] » [HOÀN TẤT] Đã hoàn tất quá trình đăng bài! Kết quả đã được lưu vào thư mục output"))
                input("Hoàn thành! Nhấn Enter...")
            elif choice == "5":
                if not self.cookie_str:
                    timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] Chưa nhập Cookie Facebook!"))
                    time.sleep(2)
                    continue
                
                # Kiểm tra chế độ nhiều tài khoản trước khi đăng bài
                self.check_multi_account_mode()
                
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bắt đầu] Bắt đầu quá trình Auto Post Facebook nhanh"))
                
                # Đọc dữ liệu từ file
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đọc file] Đọc danh sách nhóm từ {self.groups_file}..."))
                if not os.path.exists(self.groups_file):
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] File {self.groups_file} không tồn tại!"))
                    time.sleep(2)
                    continue
                    
                with open(self.groups_file, "r", encoding="utf-8") as f: nhoms = [l.strip() for l in f if l.strip()]
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đọc] Đã đọc {len(nhoms)} nhóm từ file"))
                
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đọc file] Đọc nội dung từ {self.content_file}..."))
                if not os.path.exists(self.content_file):
                    print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [LỖI] File {self.content_file} không tồn tại!"))
                    time.sleep(2)
                    continue
                    
                with open(self.content_file, "r", encoding="utf-8") as f: content = f.read()
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đọc] Đã đọc nội dung bài viết ({len(content)} ký tự)"))
                
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đang lấy proxy..."))
                proxy = self.get_proxy()
                if proxy:
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Đã lấy proxy: {proxy}"))
                else:
                    if self.multi_account_mode:
                        print(Colorate.Horizontal(Colors.red_to_white, f" » [{timestamp}] » [Proxy] Không lấy được proxy, có thể bị checkpoint!"))
                    else:
                        print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Proxy] Chế độ đơn tài khoản, không sử dụng proxy"))
                
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Trình duyệt] Đang khởi tạo Chrome..."))
                options = uc.ChromeOptions()
                if proxy: options.add_argument(f'--proxy-server={proxy}')
                self.driver = uc.Chrome(options=options)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Trình duyệt] Đã khởi tạo Chrome thành công"))
                
                # Đăng nhập bằng Cookie
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đăng nhập] Đang truy cập Facebook..."))
                self.driver.get("https://www.facebook.com")
                time.sleep(3)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Đang thêm cookie vào trình duyệt..."))
                for item in self.cookie_str.split(';'):
                    if '=' in item:
                        n, v = item.strip().split('=', 1)
                        self.driver.add_cookie({'name': n, 'value': v, 'domain': '.facebook.com'})
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Cookie] Đã thêm cookie thành công"))
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Làm mới] Đang làm mới trang để áp dụng cookie..."))
                self.driver.refresh()
                time.sleep(5)
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đăng nhập] Đăng nhập thành công vào Facebook"))

                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Bắt đầu] Bắt đầu đăng bài vào {len(nhoms)} nhóm (nhanh)..."))
                for i, link in enumerate(nhoms, 1):
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Tiến trình] Đang xử lý nhóm {i}/{len(nhoms)}"))
                    result = self.post_to_group(link, content)
                    
                    # Ghi kết quả vào file output
                    self.log_result(link, result, i, len(nhoms))
                    
                    wait_time = random.randint(40, 60)
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Nghỉ] Đợi {wait_time} giây trước khi đăng nhóm tiếp theo..."))
                    time.sleep(wait_time)
                
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(Colors.green_to_white, f" » [{timestamp}] » [HOÀN TẤT] Đã hoàn tất quá trình đăng bài! Kết quả đã được lưu vào thư mục output"))
                input("Hoàn thành! Nhấn Enter...")
            elif choice == "6":
                timestamp = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Thoát] Đang đóng trình duyệt..."))
                if self.driver: 
                    self.driver.quit()
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Đã đóng] Trình duyệt đã được đóng"))
                else:
                    print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Thông báo] Không có trình duyệt nào đang mở"))
                print(Colorate.Horizontal(màu, f" » [{timestamp}] » [Thoát] Tạm biệt!"))
                break

if __name__ == "__main__":
    FacebookAutomationUltimate().run()