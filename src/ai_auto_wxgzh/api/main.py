import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.ai_auto_wxgzh.api.routes import router
from src.ai_auto_wxgzh.config.config import Config
from src.ai_auto_wxgzh.utils import log

# 创建FastAPI应用
app = FastAPI(
    title="微信公众号自动发布API",
    description="""
    ## 微信公众号自动发布系统API
    
    这是一个基于AI的微信公众号自动发布系统的API接口。
    
    ### 主要功能：
    - 📝 发布文章到微信公众号
    - 🎨 支持多种文章模板
    - 🖼️ 自动生成和处理文章图片
    - ⚡ 支持同步和异步发布
    - 🔧 配置管理和健康检查
    
    ### 使用说明：
    1. 首先确保已正确配置微信公众号信息
    2. 可选择使用模板或直接发布原始内容
    3. 支持自定义标题、摘要、作者等信息
    4. 发布后会自动处理图片上传和文章格式化
    
    ### 注意事项：
    - 需要有效的微信公众号AppID和AppSecret
    - 图片会自动上传到微信服务器
    - 发布的文章会自动添加到公众号菜单
    """,
    version="1.0.0",
    contact={
        "name": "AI Auto WeChat",
        "url": "https://github.com/your-repo",
        "email": "your-email@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    log.print_log(f"API全局异常: {str(exc)}", "error")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "服务器内部错误",
            "detail": str(exc)
        }
    )


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    log.print_log("微信公众号发布API服务启动")
    
    # 检查配置
    try:
        config = Config.get_instance()
        if config.load_config():
            log.print_log("配置加载成功")
            if config.validate_config():
                log.print_log("配置验证通过")
            else:
                log.print_log(f"配置验证失败: {config.error_message}", "warning")
        else:
            log.print_log("配置加载失败", "warning")
    except Exception as e:
        log.print_log(f"启动时检查配置出错: {str(e)}", "error")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    log.print_log("微信公众号发布API服务关闭")


@app.get("/", include_in_schema=False)
async def root():
    """根路径重定向到文档"""
    return {
        "message": "微信公众号自动发布API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "version": "1.0.0"
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """自定义Swagger UI"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - 接口文档",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


def custom_openapi():
    """自定义OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # 添加自定义标签
    openapi_schema["tags"] = [
        {
            "name": "微信公众号发布",
            "description": "微信公众号文章发布相关接口"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    
    # 开发环境配置
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 