import csv
import os
from datetime import datetime

class TestReport:
    # 所有报告都保存到同一个时间文件夹
    REPORT_DIR = None
    
    @classmethod
    def init_report_dir(cls):
        """初始化报告文件夹（在所有测试开始前调用一次）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cls.REPORT_DIR = f"测试报告_{timestamp}"
        os.makedirs(cls.REPORT_DIR, exist_ok=True)
        print(f"报告保存目录: {cls.REPORT_DIR}")
    
    def __init__(self, test_name):
        self.test_name = test_name
        self.results = []
        self.start_time = datetime.now()
    
    def add_result(self, success, message=""):
        """添加一条测试结果"""
        self.results.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "success": "成功" if success else "失败",
            "message": message
        })
    
    def print_summary(self):
        """打印统计结果"""
        total = len(self.results)
        success = sum(1 for r in self.results if r["success"] == "成功")
        rate = (success / total * 100) if total > 0 else 0
        
        print(f"\n===== 测试结果 =====")
        print(f"测试名称: {self.test_name}")
        print(f"总次数: {total}")
        print(f"成功: {success}")
        print(f"失败: {total - success}")
        print(f"成功率: {rate:.1f}%")
    
    def save_csv(self, filename=None):
        """保存CSV报告到时间文件夹"""
        if not filename:
            filename = f"{self.test_name}.csv"
        
        # 如果没有初始化报告目录，就初始化
        if not self.REPORT_DIR:
            self.init_report_dir()
        
        filepath = os.path.join(self.REPORT_DIR, filename)
        
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["time", "success", "message"])
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"报告已保存: {filepath}")
