"""测试完整流程"""
import io
import sys

# 设置 UTF-8 编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 临时修改获取日期为 2024-12-20（有论文数据的日期）
import os

os.environ['TEST_DATE'] = '2024-12-20'

from daily_paper.main import main

if __name__ == "__main__":
    main()
