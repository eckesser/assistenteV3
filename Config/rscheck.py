import psutil

def is_runescape_running():
    for process in psutil.process_iter(attrs=["name"]):
        if "runescape" in process.info["name"].lower():
            return True
    return False
