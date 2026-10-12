# -*- coding: utf-8 -*-
# 蓝牙回连压力测试脚本
import sys
sys.path.append("..")

import time
from common.adb_utils import kill_app, start_app, adb_shell
from common.report import TestReport
from config import *

# ============ 配置参数 ============
DISCONNECT_WAIT = 4             # 杀APP后等待蓝牙断开
RECONNECT_TIMEOUT = 30          # 回连超时时间(秒)
ROUND_INTERVAL = 3              # 每轮间隔几秒
# ==================================

def is_bluetooth_connected(mac):
    """检测蓝牙是否已连接"""
    r = adb_shell("dumpsys bluetooth_manager")
    return "RSSI:" in r and mac in r

def test_reconnect(rounds=TEST_ROUNDS):
    report = TestReport("蓝牙回连测试")
    
    print(f"开始测试,共 {rounds} 轮")
    print("-" * 40)
    
    for i in range(1, rounds + 1):
        print(f"第 {i} 轮开始...")
        t1 = time.time()
        
        # 1. 杀掉APP
        kill_app(APP_PACKAGE)
        print("  已杀掉APP")
        time.sleep(DISCONNECT_WAIT)  # 等待蓝牙断开
        
        # 2. 启动APP
        start_app(APP_PACKAGE, APP_ACTIVITY)
        print("  已启动APP,等待蓝牙回连...")
        
        # 3. 循环检测蓝牙是否回连成功
        success = False
        for _ in range(RECONNECT_TIMEOUT):
            if is_bluetooth_connected(DEVICE_MAC):
                success = True
                break
            time.sleep(1)
        
        # 4. 计算本轮耗时
        elapsed = int(time.time() - t1)
        
        # 5. 输出结果
        if success:
            print(f"  [成功] 回连成功,耗时 {elapsed} 秒")
        else:
            print(f"  [失败] {RECONNECT_TIMEOUT}秒内未回连,耗时 {elapsed} 秒")
        
        report.add_result(success, f"耗时{elapsed}秒")
        
        print("-" * 40)
        time.sleep(ROUND_INTERVAL)
    
    # 统计结果
    report.print_summary()
    report.save_csv()
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    test_reconnect()
