import pytest
import os
import shutil
from datetime import datetime

def run_tests():
    """运行测试并生成报告"""
    
    # 清理旧的截图
    if os.path.exists("reports/screenshots"):
        shutil.rmtree("reports/screenshots")
    os.makedirs("reports/screenshots", exist_ok=True)
    
    # 运行测试
    print("开始运行自动化测试...")
    
    # 使用pytest运行测试
    # 生成HTML报告
    report_dir = "reports"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = f"{report_dir}/test_report_{timestamp}.html"
    
    pytest_args = [
        "tests/",
        f"--html={html_report}",
        "--self-contained-html",
        "--capture=sys",
        "-v",
        "--alluredir=reports/allure-results"
    ]
    
    # 执行测试
    pytest.main(pytest_args)
    
    print(f"\n测试完成！")
    print(f"HTML报告: {html_report}")
    
    # 生成Allure报告
    try:
        os.system("allure generate reports/allure-results -o reports/allure-report --clean")
        print(f"Allure报告: reports/allure-report/index.html")
    except:
        print("注意: 需要安装Allure才能生成Allure报告")

if __name__ == "__main__":
    run_tests()