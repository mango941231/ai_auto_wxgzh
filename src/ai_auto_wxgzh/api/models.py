from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class PublishStatus(str, Enum):
    """发布状态枚举"""
    SUCCESS = "success"
    FAILED = "failed"
    PROCESSING = "processing"


class PublishArticleRequest(BaseModel):
    """发布文章请求模型"""
    content: str = Field(..., description="文章内容，支持HTML格式")
    template_id: Optional[str] = Field(None, description="模板编号，如果不指定则随机选择模板")
    title: Optional[str] = Field(None, description="文章标题，如果不指定则从内容中提取")
    digest: Optional[str] = Field(None, description="文章摘要，如果不指定则从内容中提取")
    author: Optional[str] = Field(None, description="作者名称，如果不指定则使用配置中的默认作者")
    appid: Optional[str] = Field(None, description="微信公众号AppID，如果不指定则使用配置中的第一个")
    appsecret: Optional[str] = Field(None, description="微信公众号AppSecret，如果不指定则使用配置中的第一个")


class PublishArticleResponse(BaseModel):
    """发布文章响应模型"""
    status: PublishStatus = Field(..., description="发布状态")
    message: str = Field(..., description="响应消息")
    article_url: Optional[str] = Field(None, description="发布成功后的文章链接")
    media_id: Optional[str] = Field(None, description="微信媒体ID")
    publish_id: Optional[str] = Field(None, description="发布ID")


class TemplateListResponse(BaseModel):
    """模板列表响应模型"""
    templates: list[dict] = Field(..., description="模板列表")
    total: int = Field(..., description="模板总数")


class TemplateInfo(BaseModel):
    """模板信息模型"""
    id: str = Field(..., description="模板ID")
    name: str = Field(..., description="模板名称")
    description: Optional[str] = Field(None, description="模板描述")
    preview_url: Optional[str] = Field(None, description="模板预览链接")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    detail: Optional[str] = Field(None, description="错误详情") 