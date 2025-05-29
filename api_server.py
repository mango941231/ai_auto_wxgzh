#!/usr/bin/env python
"""
微信公众号自动发布API服务器启动脚本

使用方法:
    python api_server.py

或者使用uvicorn直接启动:
    uvicorn src.ai_auto_wxgzh.api.main:app --host 0.0.0.0 --port 8000 --reload
"""

import os
import sys
import uvicorn
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """启动API服务器"""
    print("🚀 启动微信公众号自动发布API服务器...")
    print("📖 API文档地址: http://localhost:8000/docs")
    print("🔧 ReDoc文档地址: http://localhost:8000/redoc")
    print("💡 健康检查: http://localhost:8000/api/v1/health")
    print("=" * 50)
    
    # 启动服务器
    uvicorn.run(
        "src.ai_auto_wxgzh.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main() 