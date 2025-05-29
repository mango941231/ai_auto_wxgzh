from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List

from src.ai_auto_wxgzh.api.models import (
    PublishArticleRequest,
    PublishArticleResponse,
    TemplateListResponse,
    TemplateInfo,
    ErrorResponse,
    PublishStatus
)
from src.ai_auto_wxgzh.api.services import ArticlePublishService, TemplateService
from src.ai_auto_wxgzh.config.config import Config
from src.ai_auto_wxgzh.utils import log

router = APIRouter(prefix="/api/v1", tags=["微信公众号发布"])


@router.post(
    "/publish",
    response_model=PublishArticleResponse,
    summary="发布文章到微信公众号",
    description="接收文章内容和模板编号，发布到微信公众号"
)
async def publish_article(request: PublishArticleRequest):
    """
    发布文章到微信公众号
    
    - **content**: 文章内容，支持HTML格式
    - **template_id**: 模板编号（可选），如果不指定则随机选择模板
    - **title**: 文章标题（可选），如果不指定则从内容中提取
    - **digest**: 文章摘要（可选），如果不指定则从内容中提取
    - **author**: 作者名称（可选），如果不指定则使用配置中的默认作者
    - **appid**: 微信公众号AppID（可选），如果不指定则使用配置中的第一个
    - **appsecret**: 微信公众号AppSecret（可选），如果不指定则使用配置中的第一个
    """
    try:
        # 检查配置
        config = Config.get_instance()
        if not config.load_config():
            raise HTTPException(
                status_code=500,
                detail="加载配置失败，请检查配置文件"
            )
        
        if not config.validate_config():
            raise HTTPException(
                status_code=500,
                detail=f"配置验证失败: {config.error_message}"
            )
        
        # 创建发布服务
        publish_service = ArticlePublishService()
        
        # 发布文章
        status, message, article_url, media_id, publish_id = publish_service.publish_article(
            content=request.content,
            template_id=request.template_id,
            title=request.title,
            digest=request.digest,
            author=request.author,
            appid=request.appid,
            appsecret=request.appsecret
        )
        
        return PublishArticleResponse(
            status=status,
            message=message,
            article_url=article_url,
            media_id=media_id,
            publish_id=publish_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.print_log(f"发布文章API出错: {str(e)}", "error")
        raise HTTPException(
            status_code=500,
            detail=f"发布文章时出现内部错误: {str(e)}"
        )


@router.post(
    "/publish-async",
    response_model=dict,
    summary="异步发布文章到微信公众号",
    description="异步发布文章，立即返回任务ID，可通过任务ID查询发布状态"
)
async def publish_article_async(request: PublishArticleRequest, background_tasks: BackgroundTasks):
    """
    异步发布文章到微信公众号
    
    立即返回任务ID，发布过程在后台进行
    """
    try:
        import uuid
        task_id = str(uuid.uuid4())
        
        # 添加后台任务
        background_tasks.add_task(
            _background_publish_task,
            task_id,
            request
        )
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": "文章发布任务已提交，正在后台处理"
        }
        
    except Exception as e:
        log.print_log(f"异步发布文章API出错: {str(e)}", "error")
        raise HTTPException(
            status_code=500,
            detail=f"提交发布任务时出现错误: {str(e)}"
        )


@router.get(
    "/templates",
    response_model=TemplateListResponse,
    summary="获取模板列表",
    description="获取所有可用的文章模板"
)
async def get_templates():
    """
    获取模板列表
    
    返回所有可用的文章模板信息
    """
    try:
        template_service = TemplateService()
        templates = template_service.get_template_list()
        
        return TemplateListResponse(
            templates=[template.dict() for template in templates],
            total=len(templates)
        )
        
    except Exception as e:
        log.print_log(f"获取模板列表API出错: {str(e)}", "error")
        raise HTTPException(
            status_code=500,
            detail=f"获取模板列表时出现错误: {str(e)}"
        )


@router.get(
    "/templates/{template_id}",
    response_model=dict,
    summary="获取模板内容",
    description="根据模板ID获取模板的HTML内容"
)
async def get_template_content(template_id: str):
    """
    获取模板内容
    
    - **template_id**: 模板ID
    """
    try:
        template_service = TemplateService()
        content = template_service.get_template_content(template_id)
        
        if content is None:
            raise HTTPException(
                status_code=404,
                detail=f"模板 {template_id} 不存在"
            )
        
        return {
            "template_id": template_id,
            "content": content
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.print_log(f"获取模板内容API出错: {str(e)}", "error")
        raise HTTPException(
            status_code=500,
            detail=f"获取模板内容时出现错误: {str(e)}"
        )


@router.get(
    "/config/wechat",
    response_model=dict,
    summary="获取微信配置信息",
    description="获取当前配置的微信公众号信息（不包含敏感信息）"
)
async def get_wechat_config():
    """
    获取微信配置信息
    
    返回配置的微信公众号信息，但不包含AppSecret等敏感信息
    """
    try:
        config = Config.get_instance()
        if not config.load_config():
            raise HTTPException(
                status_code=500,
                detail="加载配置失败"
            )
        
        # 返回脱敏的配置信息
        wechat_info = []
        for credential in config.wechat_credentials:
            if credential["appid"]:
                wechat_info.append({
                    "appid": credential["appid"],
                    "author": credential["author"],
                    "has_secret": bool(credential["appsecret"])
                })
        
        return {
            "wechat_accounts": wechat_info,
            "total": len(wechat_info)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.print_log(f"获取微信配置API出错: {str(e)}", "error")
        raise HTTPException(
            status_code=500,
            detail=f"获取微信配置时出现错误: {str(e)}"
        )


@router.get(
    "/health",
    summary="健康检查",
    description="检查API服务状态"
)
async def health_check():
    """
    健康检查
    
    检查API服务和相关配置的状态
    """
    try:
        config = Config.get_instance()
        config_loaded = config.load_config()
        config_valid = config.validate_config() if config_loaded else False
        
        return {
            "status": "healthy",
            "config_loaded": config_loaded,
            "config_valid": config_valid,
            "message": "API服务运行正常"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "API服务出现问题"
        }


async def _background_publish_task(task_id: str, request: PublishArticleRequest):
    """后台发布任务"""
    try:
        # 这里可以实现任务状态存储（如Redis、数据库等）
        # 目前简单记录日志
        log.print_log(f"开始处理发布任务: {task_id}")
        
        # 检查配置
        config = Config.get_instance()
        if not config.load_config() or not config.validate_config():
            log.print_log(f"任务 {task_id} 配置检查失败")
            return
        
        # 创建发布服务并发布
        publish_service = ArticlePublishService()
        status, message, article_url, media_id, publish_id = publish_service.publish_article(
            content=request.content,
            template_id=request.template_id,
            title=request.title,
            digest=request.digest,
            author=request.author,
            appid=request.appid,
            appsecret=request.appsecret
        )
        
        log.print_log(f"任务 {task_id} 完成: {message}")
        
    except Exception as e:
        log.print_log(f"后台任务 {task_id} 出错: {str(e)}", "error") 