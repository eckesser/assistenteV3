import os
import datetime
import sys
import traceback

class ErrorLogger:
    
    LOG_DIR = os.path.dirname(os.path.abspath(__file__))
    MAX_LOG_FILES = 10
    
    def log_error(self, error_message):
        current_time = datetime.datetime.now()
        log_filename = current_time.strftime('%d_%m_%Y_%H_%M_log.txt')
        log_path = os.path.join(self.LOG_DIR, log_filename)
        
        with open(log_path, 'w') as log_file:
            log_file.write(str(error_message))
        
        self._maintain_log_limit()
    
    def _maintain_log_limit(self):
        log_files = [f for f in sorted(os.listdir(self.LOG_DIR)) if f.endswith('_log.txt')]
        while len(log_files) > self.MAX_LOG_FILES:
            os.remove(os.path.join(self.LOG_DIR, log_files[0]))
            log_files.pop(0)

def handle_exception(exc_type, exc_value, exc_traceback):
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger = ErrorLogger()
    logger.log_error(error_message)

sys.excepthook = handle_exception
