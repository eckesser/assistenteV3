import pyzipper
import time
import os
from plyer import notification

class Support:
    
    LOG_PATH = os.path.dirname(os.path.abspath(__file__))
    ZIP_NAME = os.path.join(LOG_PATH, "Log.zip")
    SUPPORT_EMAIL = ""
    PASSWORD = "Y7d9K3f0A2m8" 

    @classmethod
    def zip_logs(cls):
        if os.path.exists(cls.ZIP_NAME):
            os.remove(cls.ZIP_NAME)
        with pyzipper.AESZipFile(cls.ZIP_NAME, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(cls.PASSWORD.encode('utf-8')) 
            for foldername, subfolders, filenames in os.walk(cls.LOG_PATH):
                for filename in filenames:
                    if filename.endswith('.txt'):
                        zipf.write(os.path.join(foldername, filename), arcname=filename)
    
    @classmethod
    def open_log_folder(cls):
        os.startfile(cls.LOG_PATH)
    
    @classmethod
    def notify_user(cls):
        message = f"Por favor, envie o arquivo Log.zip gerado dentro da pasta Log para {cls.SUPPORT_EMAIL} para obter suporte, descrevendo o erro e com seu Nome no ASSUNTO."
        
        notification.notify(
            title="Suporte RS3 Assist",
            message=message,
            app_name="RS3 Assist",
            app_icon=None,
            timeout=10,
            ticker='',
            toast=False
        )

        time.sleep(10) 
        cls.open_log_folder()
