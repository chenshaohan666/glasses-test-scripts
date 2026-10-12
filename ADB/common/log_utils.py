import time
from .adb_utils import clear_logcat, get_logcat

def wait_for_log(keyword, timeout=10):
    """等待日志出现，返回是否成功"""
    start = time.time()
    while time.time() - start < timeout:
        log = get_logcat()
        if keyword in log:
            return True
        time.sleep(0.5)
    return False

def detect_log_after_action(keyword, action_func, wait_time=2):
    """执行操作后检测日志"""
    clear_logcat()
    action_func()
    time.sleep(wait_time)
    log = get_logcat()
    return keyword in log
