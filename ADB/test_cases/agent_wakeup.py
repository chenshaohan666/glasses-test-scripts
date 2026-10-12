# -*- coding: utf-8 -*-
# 语音唤醒成功率统计脚本(手动说,自动统计)
import sys
sys.path.append("..")

import time
from common.adb_utils import clear_logcat, get_logcat
from common.report import TestReport
from config import *

# ============ 配置参数 ============
WAIT_TIME = 5                   # 每轮等待几秒内检测唤醒
MANUAL_EXIT_WAIT = 3            # 判断结果后等待几秒,用于手动退出对话页面
WAKEUP_KEYWORD = "BIZ_VOICE_ASSISTANT_GROUP"  # 唤醒成功的logcat关键字
# ==================================

def test_wakeup(rounds=TEST_ROUNDS):
    report = TestReport("语音唤醒测试")
    
    print("=" * 40)
    print("  语音唤醒成功率测试")
    print(f"  总轮数: {rounds}")
    print("=" * 40)
    print()
    print("操作说明:")
    print("  每轮脚本会提示你说 hello agent")
    print("  对着眼镜说,脚本自动判断成功失败")
    print("  脚本不会退出APP,直接进入下一轮")
    print()
    input("按回车键开始...")
    print()
    
    for i in range(1, rounds + 1):
        print(f"第 {i}/{rounds} 轮")
        print(f"  >>> 请说 hello agent <<<")
        
        # 清空logcat
        clear_logcat()
        
        # 等待检测唤醒
        success = False
        for sec in range(WAIT_TIME):
            time.sleep(1)
            log = get_logcat()
            if WAKEUP_KEYWORD in log:
                success = True
                break
        
        if success:
            print(f"  [成功] 唤醒触发")
        else:
            print(f"  [失败] {WAIT_TIME}秒内未检测到唤醒")
        
        report.add_result(success, "唤醒成功" if success else "唤醒失败")
        
        print(f"  请在 {MANUAL_EXIT_WAIT} 秒内手动退出对话页面...")
        time.sleep(MANUAL_EXIT_WAIT)
        print("-" * 40)
    
    # 统计结果
    report.print_summary()
    report.save_csv()
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    test_wakeup()
