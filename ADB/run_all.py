# -*- coding: utf-8 -*-
# 一键运行所有测试
import sys
sys.path.append(".")

from common.report import TestReport
from test_cases.test_reconnect import test_reconnect
from test_cases.agent_wakeup import test_wakeup
from test_cases.test_taskbar import test_switch
from config import TEST_ROUNDS

if __name__ == "__main__":
    print("=" * 50)
    print("  开始执行所有测试")
    print("=" * 50)
    print()
    
    # 1. 蓝牙回连测试（包含APP启停）
    print("\n>>> 1/3 蓝牙回连测试")
    test_reconnect(TEST_ROUNDS)
    
    # 2. 语音唤醒测试
    print("\n>>> 2/3 语音唤醒测试")
    test_wakeup(TEST_ROUNDS)
    
    # 3. 开关测试
    print("\n>>> 3/3 开关测试")
    test_switch(TEST_ROUNDS)
    
    print("\n" + "=" * 50)
    print("  所有测试完成！")
    print("=" * 50)
