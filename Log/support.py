# support.py

import zipfile
import os
import webbrowser

class Support:
    
    LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    ZIP_NAME = os.path.join(LOG_PATH, "log.zip")
    SUPPORT_EMAIL = "rs.assist.log@gmail.com"
    
    @classmethod
    def zip_logs(cls):
        with zipfile.ZipFile(cls.ZIP_NAME, 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(cls.LOG_PATH):
                for filename in filenames:
                    zipf.write(os.path.join(foldername, filename))
    
    @classmethod
    def notify_user(cls):
        webbrowser.open(cls.LOG_PATH)
        print(f"Por favor, envie o arquivo {cls.ZIP_NAME} para {cls.SUPPORT_EMAIL} para obter suporte.")
