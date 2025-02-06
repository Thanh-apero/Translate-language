import os

APP_NAME = "XML Translator"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Đường dẫn đến thư mục cài đặt
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# API Keys configuration
API_KEYS = [
    "AIzaSyB_59fjCUN_vGW8FnPf5CZdl267_yfiOBs",
    "AIzaSyCN7x2uMvL2cHq0jdBq9aMJ9ijJYct4QJ0"
]

# Supported languages
SUPPORTED_LANGUAGES = [
    ("Vietnamese", "vi"), 
    ("Chinese", "zh"),
    ("Korean", "ko"), 
    ("Japanese", "ja"),
    ("Italian", "it"), 
    ("French", "fr"),
    ("German", "de"), 
    ("Spanish", "es")
] 