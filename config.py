"""
Cấu hình cho Facebook Auto Post Tool
"""

import os
from pathlib import Path

class Config:
    # Đường dẫn thư mục
    BASE_DIR = Path(__file__).parent
    INPUT_DIR = BASE_DIR / "input"
    OUTPUT_DIR = BASE_DIR / "output"
    IMG_DIR = BASE_DIR / "img"
    
    # File paths
    COOKIE_FILE = INPUT_DIR / "cookie.txt"
    CONTENT_FILE = INPUT_DIR / "ngon.txt"
    GROUPS_FILE = INPUT_DIR / "nhom.txt"
    
    # Cấu hình Chrome
    CHROME_OPTIONS = {
        "headless": False,
        "disable_gpu": False,
        "no_sandbox": False,
        "disable_dev_shm_usage": False,
        "disable_blink_features": "AutomationControlled",
        "exclude_switches": ["enable-automation"],
        "disable_extensions": False,
        "profile_directory": "default",
    }
    
    # Cấu hình thời gian
    DELAY_MIN = 5
    DELAY_MAX = 15
    POST_DELAY_MIN = 30
    POST_DELAY_MAX = 60
    
    # Cấu hình khác
    MAX_RETRIES = 3
    TIMEOUT = 30
    
    # Key xác thực
    AUTH_KEY = "ducvannguyen"
    
    @classmethod
    def ensure_directories(cls):
        """Tạo các thư mục cần thiết nếu chưa tồn tại"""
        for directory in [cls.INPUT_DIR, cls.OUTPUT_DIR, cls.IMG_DIR]:
            directory.mkdir(exist_ok=True)
            # Tạo file .gitkeep để giữ thư mục trong git
            gitkeep = directory / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
    
    @classmethod
    def validate_files(cls):
        """Kiểm tra các file cần thiết có tồn tại không"""
        required_files = [cls.COOKIE_FILE, cls.CONTENT_FILE, cls.GROUPS_FILE]
        missing_files = [f for f in required_files if not f.exists()]
        
        if missing_files:
            print("❌ Thiếu các file cần thiết:")
            for file in missing_files:
                print(f"   - {file}")
            return False
        
        print("✅ Tất cả file cần thiết đã sẵn sàng")
        return True
