import os
import glob
import random
from typing import Optional, Tuple, List, Dict
from pathlib import Path

from src.ai_auto_wxgzh.tools.wx_publisher import WeixinPublisher
from src.ai_auto_wxgzh.config.config import Config
from src.ai_auto_wxgzh.utils import utils, log
from src.ai_auto_wxgzh.api.models import PublishStatus, TemplateInfo
from src.ai_auto_wxgzh.api.template_fusion_service import EnhancedTemplateService


class ArticlePublishService:
    """文章发布服务"""
    
    def __init__(self):
        self.config = Config.get_instance()
        # 使用增强的模板服务
        self.enhanced_template_service = EnhancedTemplateService()
    
    def publish_article(
        self,
        content: str,
        template_id: Optional[str] = None,
        title: Optional[str] = None,
        digest: Optional[str] = None,
        author: Optional[str] = None,
        appid: Optional[str] = None,
        appsecret: Optional[str] = None
    ) -> Tuple[PublishStatus, str, Optional[str], Optional[str], Optional[str]]:
        """
        发布文章到微信公众号
        
        Args:
            content: 文章内容
            template_id: 模板ID
            title: 文章标题
            digest: 文章摘要
            author: 作者
            appid: 微信AppID
            appsecret: 微信AppSecret
            
        Returns:
            Tuple[状态, 消息, 文章链接, 媒体ID, 发布ID]
        """
        try:
            # 获取微信配置
            wx_appid, wx_appsecret, wx_author = self._get_wechat_config(appid, appsecret, author)
            if not wx_appid or not wx_appsecret:
                return PublishStatus.FAILED, "微信公众号配置不完整", None, None, None
            
            # 提取标题和摘要（在应用模板之前）
            if not title or not digest:
                extracted_title, extracted_digest = utils.extract_html(content)
                title = title or extracted_title
                digest = digest or extracted_digest
            
            # 处理模板（传递标题和摘要）
            if template_id:
                content = self._apply_template(content, template_id, title, digest)
            
            if not title:
                return PublishStatus.FAILED, "无法提取文章标题", None, None, None
            
            # 创建发布器
            publisher = WeixinPublisher(wx_appid, wx_appsecret, wx_author)
            
            # 生成封面图片
            image_url = publisher.generate_img(
                f"主题：{title.split('|')[-1]}，内容：{digest}",
                "900*384"
            )
            
            if image_url is None:
                log.print_log("生成图片出错，使用默认图片")
                image_url = utils.get_res_path("UI\\bg.png", os.path.dirname(__file__) + "/../gui/")
            
            # 上传封面图片
            media_id, _, err_msg = publisher.upload_image(image_url)
            if media_id is None:
                return PublishStatus.FAILED, f"封面{err_msg}，无法发布文章", None, None, None
            
            # 处理文章中的图片
            content = self._process_article_images(content, publisher)
            
            # 添加草稿
            add_draft_result, err_msg = publisher.add_draft(content, title, digest, media_id)
            if add_draft_result is None:
                return PublishStatus.FAILED, f"{err_msg}，无法发布文章", None, None, None
            
            # 发布文章
            publish_result, err_msg = publisher.publish(add_draft_result.publishId)
            if publish_result is None:
                return PublishStatus.FAILED, f"{err_msg}，无法继续发布文章", None, None, None
            
            # 获取文章链接
            article_url = publisher.poll_article_url(publish_result.publishId)
            log.print_log(f"文章链接: {article_url}")
            # # 创建菜单（可选）
            # if article_url:
            #     publisher.create_menu(article_url)
            
            # # 群发文章（使文章显示在公众号列表）
            # ret, news_media_id = publisher.media_uploadnews(content, title, digest, media_id)
            # if news_media_id:
            #     publisher.message_mass_sendall(news_media_id)
            
            # 保存最终文章
            self._save_final_article(content)
            
            return (
                PublishStatus.SUCCESS,
                "成功发布文章到微信公众号",
                article_url,
                media_id,
                publish_result.publishId
            )
            
        except Exception as e:
            log.print_log(f"发布文章时出错: {str(e)}", "error")
            return PublishStatus.FAILED, f"发布失败: {str(e)}", None, None, None
    
    def _get_wechat_config(
        self, 
        appid: Optional[str], 
        appsecret: Optional[str], 
        author: Optional[str]
    ) -> Tuple[str, str, str]:
        """获取微信配置"""
        if appid and appsecret:
            return appid, appsecret, author or "AI助手"
        
        # 使用配置文件中的第一个有效配置
        for credential in self.config.wechat_credentials:
            if credential["appid"] and credential["appsecret"]:
                return (
                    credential["appid"],
                    credential["appsecret"],
                    author or credential["author"] or "AI助手"
                )
        
        return "", "", ""
    
    def _apply_template(self, content: str, template_id: str, title: Optional[str] = None, digest: Optional[str] = None) -> str:
        """应用模板到内容 - 使用AI智能融合"""
        try:
            # 使用AI进行模板内容融合
            fused_content = self.enhanced_template_service.apply_template_with_ai(
                content, template_id, title, digest
            )
            return fused_content
        except Exception as e:
            log.print_log(f"应用模板时出错: {str(e)}")
            return content
    
    def _process_article_images(self, content: str, publisher: WeixinPublisher) -> str:
        """处理文章中的图片"""
        try:
            image_urls = utils.extract_image_urls(content)
            for image_url in image_urls:
                local_filename = utils.download_and_save_image(
                    image_url,
                    utils.get_current_dir("image")
                )
                if local_filename:
                    _, wx_url, _ = publisher.upload_image(local_filename)
                    if wx_url:
                        content = content.replace(image_url, wx_url)
        except Exception as e:
            log.print_log(f"处理文章图片时出错: {str(e)}")
        
        return content
    
    def _save_final_article(self, content: str):
        """保存最终文章"""
        try:
            final_article_path = os.path.join(utils.get_current_dir(), "final_article.html")
            with open(final_article_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            log.print_log(f"保存最终文章时出错: {str(e)}")


class TemplateService:
    """模板服务"""
    
    def __init__(self):
        self.template_dir = utils.get_res_path(
            "templates",
            os.path.join(utils.get_current_dir("knowledge", False))
        )
    
    def get_template_list(self) -> List[TemplateInfo]:
        """获取模板列表"""
        templates = []
        try:
            if not os.path.exists(self.template_dir):
                return templates
            
            template_files = glob.glob(os.path.join(self.template_dir, "*.html"))
            
            for template_file in template_files:
                template_name = Path(template_file).stem
                templates.append(TemplateInfo(
                    id=template_name,
                    name=template_name,
                    description=f"模板 {template_name}",
                    preview_url=None
                ))
        except Exception as e:
            log.print_log(f"获取模板列表时出错: {str(e)}")
        
        return templates
    
    def get_template_content(self, template_id: str) -> Optional[str]:
        """获取模板内容"""
        try:
            template_filename = template_id if template_id.endswith(".html") else f"{template_id}.html"
            template_path = os.path.join(self.template_dir, template_filename)
            
            if os.path.exists(template_path):
                with open(template_path, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            log.print_log(f"读取模板内容时出错: {str(e)}")
        
        return None
    
    def get_random_template(self) -> Optional[str]:
        """获取随机模板"""
        templates = self.get_template_list()
        if templates:
            return random.choice(templates).id
        return None 