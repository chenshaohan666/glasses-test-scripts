import subprocess
import time

# adb路径
ADB_PATH = "C:\\Users\\chenshaohan\\Downloads\\platform-tools-latest-windows\\platform-tools\\adb.exe"

def adb_shell(cmd):
    """执行adb shell命令"""
    full_cmd = [ADB_PATH, "shell"] + cmd.split()
    r = subprocess.run(full_cmd, capture_output=True, text=True)
    return r.stdout

def adb(cmd):
    """执行adb命令"""
    full_cmd = [ADB_PATH] + cmd.split()
    r = subprocess.run(full_cmd, capture_output=True, text=True)
    return r.stdout

def clear_logcat():
    """清空logcat"""
    adb("logcat -c")

def get_logcat():
    """获取当前logcat"""
    return adb("logcat -d")

def tap(x, y):
    """点击屏幕坐标"""
    adb_shell(f"input tap {x} {y}")

def swipe(start_x, start_y, end_x, end_y, duration=300):
    """滑动屏幕"""
    adb_shell(f"input swipe {start_x} {start_y} {end_x} {end_y} {duration}")

def kill_app(package_name):
    """强制停止APP"""
    adb_shell(f"am force-stop {package_name}")

def start_app(package_name, activity):
    """启动APP"""
    adb_shell(f"am start -n {package_name}/{activity}")

def is_app_in_foreground(package_name):
    """判断APP是否在前台"""
    r = adb_shell("dumpsys activity activities | grep mCurrentFocus")
    return package_name in r

def screenshot(filename):
    """截图"""
    adb_shell(f"screencap -p /sdcard/{filename}.png")
    adb(f"pull /sdcard/{filename}.png ./screenshots/")
