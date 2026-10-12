import subprocess
import time
import pandas as pd
import re
import os

# ===================== 配置区（直接改） =====================
ADB_DEVICE = "6f4fb2e8"  # adb devices查到的设备号，空字符串代表默认连接的设备
TEST_ROUND = 1  # 每个用例循环测试次数
PERF_THRESHOLD_MS = 500  # 性能阈值，超过标记FAIL
OUTPUT_CSV = "G31性能测试结果.csv"
# APP在手机上的日志文件路径（你上传的就是这种格式的日志）
PHONE_APP_LOG_PATH = "/storage/emulated/0/Android/data/com.metabounds.mojieglass/files/app_log.txt"
LOCAL_TMP_LOG = "./tmp_g31_log.txt"

# 性能测试用例列表（对应你daily功能清单）
test_cases = [
    {
        "case_name": "触控板单击响应",
        "precondition": "亮屏AI桌面首页",
        "trigger_desc": "单击眼镜触控板",
        "success_keyword": r"pushReqEvent: \{type=.*\}", # 任意触控事件回调
    },
    {
        "case_name": "打开提词器",
        "precondition": "亮屏AI桌面首页",
        "trigger_desc": "触控板滑动选中提词器并确认",
        "success_keyword": r"glass enters teleprompter: start",
    },
    {
        "case_name": "关闭提词器",
        "precondition": "提词器页面打开",
        "trigger_desc": "双击触控板返回",
        "success_keyword": r"glass exits teleprompter: stop",
    },
    {
        "case_name": "打开直播",
        "precondition": "亮屏AI桌面首页",
        "trigger_desc": "触控板滑动选中直播并确认",
        "success_keyword": r"glass enters live room: start",
    },
    {
        "case_name": "打开相机",
        "precondition": "亮屏AI桌面首页",
        "trigger_desc": "按眼镜相机键",
        "success_keyword": r"pushReqEvent: \{type=cameraAppOpen\}",
    },
    {
        "case_name": "关闭相机",
        "precondition": "相机页面打开",
        "trigger_desc": "再按一次相机键",
        "success_keyword": r"pushReqEvent: \{type=cameraAppClose\}",
    },
    {
        "case_name": "切换录像模式",
        "precondition": "相机已打开",
        "trigger_desc": "双击相机键切换录像",
        "success_keyword": r"pushReqEvent: \{type=switchVideoMode\}",
    },
    {
        "case_name": "语音唤醒助手",
        "precondition": "亮屏AI桌面首页",
        "trigger_desc": "说唤醒词唤醒语音助手",
        "success_keyword": r"注册成功 sessionDir=",
    },
]

# ===================== 工具函数 =====================
def adb_cmd(cmd_list):
    """执行adb命令"""
    full_cmd = ["adb"] + (["-s", ADB_DEVICE] if ADB_DEVICE else []) + cmd_list
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return res.stdout, res.stderr

def get_latest_log_tail():
    """从手机拉取最新的APP日志文件到本地"""
    adb_cmd(["pull", PHONE_APP_LOG_PATH, LOCAL_TMP_LOG])
    if os.path.exists(LOCAL_TMP_LOG):
        with open(LOCAL_TMP_LOG, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    return []

def measure_response_time(keyword, timeout=8):
    """
    手动触发操作模式：脚本等待你手动操作眼镜，自动匹配日志关键字计算耗时
    你现在操作眼镜的同时脚本开始计时，匹配到对应关键字就停止计时
    """
    print(f"\n>>> 请现在执行操作：{current_trigger_desc}")
    input("准备好后按回车开始计时...")
    start_time = time.time()
    print("⏳ 正在等待操作完成...")
    
    start_poll = time.time()
    log_history = set()
    
    while time.time() - start_poll < timeout:
        lines = get_latest_log_tail()
        for line in lines[-200:]: # 只读最近200行新日志
            if line in log_history:
                continue
            log_history.add(line)
            if re.search(keyword, line):
                end_time = time.time()
                cost_ms = (end_time - start_time) * 1000
                print(f"✅ 检测到操作完成，耗时：{cost_ms:.2f} ms")
                return cost_ms
        time.sleep(0.1)
    print("❌ 超时未检测到对应日志，本轮失败")
    return None

# ===================== 主测试流程 =====================
if __name__ == "__main__":
    print("="*60)
    print("G31 AR眼镜 性能自动化测试工具")
    print("="*60)
    results = []
    
    for case in test_cases:
        case_name = case["case_name"]
        precond = case["precondition"]
        global current_trigger_desc
        current_trigger_desc = case["trigger_desc"]
        keyword = case["success_keyword"]
        
        print(f"\n📋 测试用例：{case_name}")
        print(f"   前置条件：{precond}")
        print(f"   请先将眼镜调整到前置状态")
        input("调整完成后按回车开始本轮测试...")
        
        samples = []
        for round_idx in range(TEST_ROUND):
            print(f"\n--- 第 {round_idx+1}/{TEST_ROUND} 轮 ---")
            cost = measure_response_time(keyword)
            if cost is not None:
                samples.append(cost)
            time.sleep(1)
        
        # 统计数据
        if samples:
            avg = sum(samples)/len(samples)
            max_t = max(samples)
            min_t = min(samples)
            verdict = "PASS" if avg <= PERF_THRESHOLD_MS else "FAIL"
        else:
            avg, max_t, min_t = 0,0,0
            verdict = "无有效数据"
        
        results.append({
            "测试项": case_name,
            "前置条件": precond,
            "平均响应(ms)": round(avg,2),
            "最大响应(ms)": round(max_t,2),
            "最小响应(ms)": round(min_t,2),
            "有效采样数": len(samples),
            "判定": verdict
        })
    
    # 输出CSV
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print("\n" + "="*60)
    print(f"✅ 测试完成！结果已保存到 {OUTPUT_CSV}")
    print("="*60)
    print(df.to_string(index=False))
