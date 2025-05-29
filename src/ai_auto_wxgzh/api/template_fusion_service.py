import os
import json
from typing import Optional, Dict, Any
from openai import OpenAI
from langchain_openai import ChatOpenAI

from src.ai_auto_wxgzh.config.config import Config
from src.ai_auto_wxgzh.utils import log, utils


class TemplateFusionService:
    """智能模板融合服务 - 使用大模型进行模板内容融合"""
    
    def __init__(self):
        self.config = Config.get_instance()
        self._setup_llm_client()
    
    def _setup_llm_client(self):
        """设置大模型客户端"""
        try:
            # 获取API配置
            api_key = self.config.api_key
            api_base = self.config.api_apibase
            model = self.config.api_model
            
            if not api_key:
                raise ValueError("API密钥未配置")
            
            # 创建OpenAI客户端
            self.client = OpenAI(
                api_key=api_key,
                base_url=api_base
            )
            self.model = model
            
            log.print_log(f"LLM客户端初始化成功，使用模型: {model}")
            
        except Exception as e:
            log.print_log(f"LLM客户端初始化失败: {str(e)}", "error")
            self.client = None
            self.model = None
    
    def fuse_content_with_template(
        self, 
        content: str, 
        template_content: str,
        title: Optional[str] = None,
        digest: Optional[str] = None
    ) -> str:
        """
        使用大模型将内容与模板进行智能融合
        
        Args:
            content: 原始文章内容
            template_content: HTML模板内容
            title: 文章标题（可选）
            digest: 文章摘要（可选）
            
        Returns:
            融合后的HTML内容
        """
        if not self.client:
            log.print_log("LLM客户端未初始化，使用简单替换", "warning")
            return self._simple_merge(content, template_content)
        
        try:
            # 构建提示词
            prompt = self._build_fusion_prompt(content, template_content, title, digest)
            
            # 调用大模型
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=8192
            )
            
            # 提取生成的内容
            generated_content = response.choices[0].message.content.strip()
            
            # 提取HTML代码块
            html_content = self._extract_html_from_response(generated_content)
            
            if html_content:
                log.print_log("模板内容融合成功")
                return html_content
            else:
                log.print_log("未能从响应中提取HTML，使用简单替换", "warning")
                return self._simple_merge(content, template_content)
                
        except Exception as e:
            log.print_log(f"模板融合过程中出错: {str(e)}", "error")
            return None
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一位专业的HTML模板内容融合专家，擅长将新的文章内容智能地适配到现有的HTML模板中。

你的任务是：
1. 分析HTML模板的结构、样式和布局特点
2. 理解新文章内容的结构和要点
3. 将新内容按照模板的风格和布局进行智能适配
4. 保持模板的视觉效果、色彩方案和交互特性不变
5. 确保内容呈现自然流畅

重要要求：
- 必须保持所有<section>标签的布局结构和内联样式
- 保持原有的视觉层次、色彩方案和排版风格
- 保持卡片式布局、圆角和阴影效果
- 保持SVG动画元素和交互特性
- 不添加新的style标签或外部CSS
- 不改变原有的色彩方案
- 标题替换标题、段落替换段落、列表替换列表
- 当新内容比原模板内容长或短时，合理调整，不破坏布局

请直接输出融合后的HTML代码，用```html标记包围。"""
    
    def _build_fusion_prompt(
        self, 
        content: str, 
        template_content: str,
        title: Optional[str] = None,
        digest: Optional[str] = None
    ) -> str:
        """构建融合提示词"""
        
        # 压缩模板内容以减少token消耗
        compressed_template = utils.compress_html(template_content, True)
        
        # 提取文章的纯文本内容
        clean_content = utils.extract_text_from_html(content)
        if len(clean_content) > 3000:  # 限制内容长度
            clean_content = clean_content[:3000] + "..."
        
        prompt = f"""请将以下新文章内容适配到给定的HTML模板中：

【HTML模板 - 必须作为最终输出的基础】
{compressed_template}

【新文章内容】
标题：{title or "未指定"}
摘要：{digest or "未指定"}
正文：
{clean_content}

【任务要求】
1. 分析模板的结构、样式和布局特点
2. 识别所有内容占位区域（标题、副标题、正文段落、引用、列表等）
3. 将新文章内容按照原模板的结构和布局规则填充
4. 保持模板的视觉效果和风格不变
5. 确保内容适配自然流畅

【输出要求】
- 直接输出完整的HTML代码
- 用```html标记包围
- 保持原模板的所有样式和布局
- 只替换内容部分，不修改结构和样式"""

        return prompt
    
    def _extract_html_from_response(self, response: str) -> Optional[str]:
        """从响应中提取HTML代码"""
        try:
            # 查找HTML代码块
            import re
            
            # 匹配```html...```格式
            html_pattern = r'```html\s*(.*?)\s*```'
            match = re.search(html_pattern, response, re.DOTALL | re.IGNORECASE)
            
            if match:
                return match.group(1).strip()
            
            # 如果没有找到代码块，尝试查找HTML标签
            if '<section' in response and '</section>' in response:
                # 提取从第一个<section>到最后一个</section>的内容
                start = response.find('<section')
                end = response.rfind('</section>') + len('</section>')
                if start != -1 and end != -1:
                    return response[start:end]
            
            return None
            
        except Exception as e:
            log.print_log(f"提取HTML代码时出错: {str(e)}", "error")
            return None
    
    def _simple_merge(self, content: str, template: str) -> str:
        """简单的内容合并（备用方案）"""
        if "{{content}}" in template:
            return template.replace("{{content}}", content)
        else:
            # 如果模板没有占位符，尝试智能插入内容
            return template + content


class EnhancedTemplateService:
    """增强的模板服务，集成智能融合功能"""
    
    def __init__(self):
        self.template_dir = utils.get_res_path(
            "templates",
            os.path.join(utils.get_current_dir("knowledge", False))
        )
        self.fusion_service = TemplateFusionService()
    
    def apply_template_with_ai(
        self,
        content: str,
        template_id: str,
        title: Optional[str] = None,
        digest: Optional[str] = None
    ) -> str:
        """使用AI进行模板内容融合"""
        try:
            # 获取模板内容
            template_content = self._get_template_content(template_id)
            if not template_content:
                log.print_log(f"模板 {template_id} 不存在，返回原内容")
                return content
            
            # 使用AI进行融合
            fused_content = self.fusion_service.fuse_content_with_template(
                content, template_content, title, digest
            )
            if not fused_content:
                log.print_log(f"模板 {template_id} 融合失败，返回原内容")
                return content
            return fused_content
            
        except Exception as e:
            log.print_log(f"AI模板融合失败: {str(e)}", "error")
            return content
    
    def _get_template_content(self, template_id: str) -> Optional[str]:
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