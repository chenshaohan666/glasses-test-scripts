# -*- coding: utf-8 -*-
# 开关自动化测试脚本
import sys
sys.path.append("..")

import time
from common.adb_utils import tap, swipe, clear_logcat, get_logcat, start_app
from common.report import TestReport
from config import *

# ============ 配置参数 ============
ROUNDS = TEST_ROUNDS
# ==================================

def goto_settings_page():
    """跳转到设置页面"""
    # 先回到首页
    start_app(APP_PACKAGE, APP_ACTIVITY)
    time.sleep(2)
    
    # 第一步点击
    tap(STEP1_X, STEP1_Y)
    time.sleep(1)
    
    # 第二步点击
    tap(STEP2_X, STEP2_Y)
    time.sleep(1)
    
    # 下滑
    swipe(SWIPE_START_X, SWIPE_START_Y, SWIPE_END_X, SWIPE_END_Y, SWIPE_DURATION)
    time.sleep(1)
    
    # 下滑后点击进入
    tap(ENTER_BTN_X, ENTER_BTN_Y)
    time.sleep(1)

def toggle_switch(switch_x, switch_y, keyword):
    """切换一次开关状态，返回是否成功"""
    clear_logcat()
    tap(switch_x, switch_y)
    time.sleep(SWITCH_WAIT)
    log = get_logcat()
    return keyword in log

def test_status_switch_round(rounds=ROUNDS):
    """状态显示开关：一开一关算一轮"""
    report = TestReport("状态显示开关测试")
    
    for i in range(1, rounds + 1):
        print(f"第 {i}/{rounds} 轮", end="... ")
        
        # 开一次
        open_ok = toggle_switch(STATUS_SWITCH_X, STATUS_SWITCH_Y, "setStatusDisplay")
        time.sleep(ROUND_INTERVAL)
        
        # 关一次
        close_ok = toggle_switch(STATUS_SWITCH_X, STATUS_SWITCH_Y, "setStatusDisplay")
        
        # 一开一关都成功才算这一轮成功
        success = open_ok and close_ok
        print("成功" if success else "失败")
        
        report.add_result(success, f"开:{open_ok}, 关:{close_ok}")
        time.sleep(ROUND_INTERVAL)
    
    report.print_summary()
    report.save_csv()
    return report

def test_indicator_switch_round(rounds=ROUNDS):
    """操作指示栏开关：一开一关算一轮"""
    report = TestReport("操作指示栏开关测试")
    
    for i in range(1, rounds + 1):
        print(f"第 {i}/{rounds} 轮", end="... ")
        
        # 开一次
        open_ok = toggle_switch(INDICATOR_SWITCH_X, INDICATOR_SWITCH_Y, "operationHint")
        time.sleep(ROUND_INTERVAL)
        
        # 关一次
        close_ok = toggle_switch(INDICATOR_SWITCH_X, INDICATOR_SWITCH_Y, "operationHint")
        
        # 一开一关都成功才算这一轮成功
        success = open_ok and close_ok
        print("成功" if success else "失败")
        
        report.add_result(success, f"开:{open_ok}, 关:{close_ok}")
        time.sleep(ROUND_INTERVAL)
    
    report.print_summary()
    report.save_csv()
    return report

def test_switch(rounds=ROUNDS):
    print("=" * 50)
    print("  开关自动化测试")
    print(f"  总轮数: 每个开关 {rounds} 轮（一开一关算一轮）")
    print("=" * 50)
    print()
    
    # 先跳转到设置页面
    print("正在跳转到设置页面...")
    goto_settings_page()
    time.sleep(2)
    
    # 测试状态显示开关
    print("\n【状态显示开关测试】")
    test_status_switch_round(rounds)
    
    # 测试操作指示栏开关
    print("\n【操作指示栏开关测试】")
    test_indicator_switch_round(rounds)
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    test_switch()
