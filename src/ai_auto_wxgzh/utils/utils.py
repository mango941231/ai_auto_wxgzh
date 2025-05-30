import re
import os
import random
import warnings
from bs4 import BeautifulSoup
import requests
import time
import sys
import shutil
import webbrowser
from src.ai_auto_wxgzh.utils import log


def copy_file(src_file, dest_file):
    mkdir(os.path.dirname(dest_file))

    # 存在不复制
    if os.path.exists(dest_file):
        return False

    try:
        shutil.copy2(src_file, dest_file)
    except Exception as e:  # noqa 841
        pass


def mkdir(path, clean=False):
    if os.path.exists(path):
        if clean:
            shutil.rmtree(path)
            os.makedirs(path)
    else:
        os.makedirs(path)


def get_is_release_ver():
    if getattr(sys, "frozen", None):
        return True
    else:
        return False


def get_res_path(file_name, basedir=""):
    if get_is_release_ver():
        return os.path.join(sys._MEIPASS, file_name)

    return os.path.join(basedir, file_name)


def get_current_dir(dir_name="", need_create_dir=True):
    current_dir = ""
    if get_is_release_ver():
        exe_path = sys.executable
        install_dir = os.path.dirname(exe_path)
        current_dir = os.path.join(os.path.normpath(install_dir), dir_name)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_dir = os.path.join(current_dir, "../../../", dir_name)

    # 不为空时创建目录，为空说明只是获取根目录路径
    if dir_name != "" and need_create_dir:
        mkdir(current_dir)

    return current_dir


def get_random_platform(platforms):
    """
    根据权重随机选择一个平台。
    """
    total_weight = sum(p["weight"] for p in platforms)

    if int(total_weight * 100) / 100 != 1:
        warnings.warn(f"平台权重总和应为1，当前为{total_weight:.2f}，将默认选择微博", UserWarning)
        return "微博"

    rand = random.uniform(0, total_weight)
    cumulative_weight = 0
    for platform in platforms:
        cumulative_weight += platform["weight"]
        if rand <= cumulative_weight:
            return platform["name"]


def extract_modified_article(content):
    match = re.search(r"```(?:html)?\s*([\s\S]*?)```", content, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        # 分别去除开头和结尾的反引号（保留其他字符）
        stripped = content.strip()
        stripped = stripped.lstrip("`").rstrip("`")
        return stripped.strip()  # 最后再去除可能的空白


def extract_html(html, max_length=64):
    title = None
    digest = None

    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    h1_tag = soup.find("h1")

    # 标题优先级：<title> > <h1>
    if title_tag:
        title = " ".join(title_tag.get_text(strip=True).split())
    elif h1_tag:
        title = " ".join(h1_tag.get_text(strip=True).split())

    # 摘要
    # 提取所有文本内容，并去除多余的空格和换行符
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()

    if text:
        # 如果文本长度超过最大长度，则截取前max_length个字符
        if len(text) > max_length:
            digest = text[:max_length] + "..."
        else:
            digest = text

    return title, digest

def extract_html_with_ai(
    html_content: str,
    target_audience: str = "年轻人",
    style: str = "新颖有趣"
) -> tuple:
    """
    使用AI从HTML内容中提取并生成吸引人的标题和摘要
    
    Args:
        html_content: HTML内容
        target_audience: 目标受众，如"年轻人"、"职场人士"、"科技爱好者"等
        style: 标题风格，如"新颖有趣"、"专业严谨"、"幽默风趣"等
        
    Returns:
        tuple[标题, 摘要]
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        from src.ai_auto_wxgzh.config.config import Config
        
        # 获取配置
        config = Config.get_instance()
        api_key = config.api_key
        api_base = config.api_apibase
        model = config.api_model
        
        if not api_key:
            log.print_log("API密钥未配置，使用传统方法提取标题摘要")
            return extract_html(html_content, max_length=120)
        
        # 初始化AI模型
        llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=api_base,
            timeout=600,
            temperature=0.7
        )
        
        # 提取HTML中的纯文本内容
        clean_content = extract_text_from_html(html_content)
        if len(clean_content) > 2000:  # 限制内容长度以节省token
            clean_content = clean_content[:2000] + "..."
        
        if not clean_content.strip():
            log.print_log("HTML内容为空，无法生成标题和摘要")
            return None, None
        
        # 构建AI提示词
        system_prompt = """你是一位专业的微信公众号内容编辑专家，擅长创作吸引读者的标题和摘要。

你的任务是：
1. 分析文章内容的核心主题和亮点
2. 创作符合微信公众号特点的吸引人标题
3. 撰写简洁有力的文章摘要

标题要求：
- 长度控制在15-30个字符
- 具有吸引力和点击欲望
- 体现文章核心价值
- 符合目标受众喜好
- 可以适当使用数字、疑问句、感叹句等技巧
- 避免标题党，确保与内容相符
- 可以使用热门词汇和网络流行语（适度）

摘要要求：
- 长度控制在80-150个字符
- 概括文章主要内容和价值点
- 激发读者阅读兴趣
- 语言简洁明了
- 可以包含关键信息或亮点
- 突出文章的实用性或趣味性

输出格式：
标题：[生成的标题]
摘要：[生成的摘要]"""

        user_prompt = f"""请为以下文章内容生成吸引人的微信公众号标题和摘要：

【文章内容】
{clean_content}

【目标受众】
{target_audience}

【标题风格】
{style}

【创作要求】
1. 标题要新颖有趣，能够吸引{target_audience}的注意
2. 体现{style}的特点
3. 摘要要简洁有力，突出文章价值
4. 确保标题和摘要与内容高度相关
5. 适合微信公众号传播特点
6. 可以使用一些吸引眼球的技巧，如：
   - 数字化表达（如"3个方法"、"5分钟学会"）
   - 疑问句式（如"你知道吗？"、"为什么..."）
   - 对比反差（如"竟然"、"没想到"）
   - 实用价值（如"必看"、"干货"、"攻略"）

请按照以下格式输出：
标题：[你生成的标题]
摘要：[你生成的摘要]"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        generated_content = response.content.strip()
        
        # 解析AI生成的标题和摘要
        title, digest = _parse_ai_title_digest_response(generated_content)
        
        if title and digest:
            log.print_log("AI生成标题和摘要成功")
            return title, digest
        else:
            log.print_log("AI生成标题和摘要失败，使用传统方法", "warning")
            # 回退到传统方法
            return extract_html(html_content, max_length=120)
            
    except Exception as e:
        log.print_log(f"AI提取标题和摘要时出错: {str(e)}", "error")
        # 回退到传统方法
        return extract_html(html_content, max_length=120)


def _parse_ai_title_digest_response(response: str) -> tuple:
    """解析AI响应中的标题和摘要"""
    try:
        # 使用正则表达式提取标题和摘要
        title_pattern = r'标题[：:]\s*(.+?)(?=\n|摘要|$)'
        digest_pattern = r'摘要[：:]\s*(.+?)(?=\n|$)'
        
        title_match = re.search(title_pattern, response, re.DOTALL)
        digest_match = re.search(digest_pattern, response, re.DOTALL)
        
        title = title_match.group(1).strip() if title_match else None
        digest = digest_match.group(1).strip() if digest_match else None
        
        # 清理标题和摘要中的多余字符
        if title:
            title = re.sub(r'["\'\[\]【】]', '', title).strip()
            # 限制标题长度
            if len(title) > 50:
                title = title[:47] + "..."
        
        if digest:
            digest = re.sub(r'["\'\[\]【】]', '', digest).strip()
            # 限制摘要长度
            if len(digest) > 200:
                digest = digest[:197] + "..."
        
        return title, digest
        
    except Exception as e:
        log.print_log(f"解析标题摘要响应时出错: {str(e)}", "error")
        return None, None


def generate_attractive_title(
    content: str,
    keywords: str = None,
    style: str = "吸引眼球"
) -> str:
    """
    专门生成吸引人的标题
    
    Args:
        content: 文章内容
        keywords: 关键词（可选）
        style: 标题风格
        
    Returns:
        生成的标题
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        from src.ai_auto_wxgzh.config.config import Config
        
        # 获取配置
        config = Config.get_instance()
        api_key = config.api_key
        api_base = config.api_apibase
        model = config.api_model
        
        if not api_key:
            log.print_log("API密钥未配置，无法生成AI标题")
            return None
        
        # 初始化AI模型
        llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=api_base,
            timeout=600,
            temperature=0.8  # 提高创造性
        )
        
        prompt = f"""请为以下内容生成一个非常吸引人的微信公众号标题：

【内容】
{content[:1000]}...

【关键词】
{keywords or "无特定关键词"}

【风格要求】
{style}

【标题技巧】
- 使用数字（如"3个秘诀"、"10分钟"）
- 制造悬念（如"你绝对想不到"、"真相是..."）
- 突出价值（如"必看"、"干货"、"实用"）
- 情感共鸣（如"太真实了"、"说到心坎里"）
- 时效性（如"最新"、"刚刚发现"）
- 对比反差（如"竟然"、"没想到"）

请只输出一个最佳标题，不要其他内容："""

        messages = [
            SystemMessage(content="你是微信公众号标题创作专家，专门创作高点击率的标题。"),
            HumanMessage(content=prompt)
        ]
        
        response = llm.invoke(messages)
        title = response.content.strip()
        
        # 清理标题
        title = re.sub(r'["\'\[\]【】]', '', title).strip()
        if len(title) > 50:
            title = title[:47] + "..."
        
        return title
        
    except Exception as e:
        log.print_log(f"生成吸引人标题时出错: {str(e)}", "error")
        return None


def get_latest_file_os(dir_path):
    """
    使用 os 模块获取目录下最近创建/保存的文件。
    """

    files = [
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, f))
    ]
    if not files:
        return None  # 如果目录为空，则返回 None

    latest_file = max(files, key=os.path.getmtime)
    return latest_file


def extract_image_urls(html_content):
    patterns = [
        r'<img[^>]*?src=["\'](.*?)["\']',  # 匹配 src
        r'<img[^>]*?srcset=["\'](.*?)["\']',  # 匹配 srcset
        r'<img[^>]*?data-(?:src|image)=["\'](.*?)["\']',  # 匹配 data-src/data-image
        r'background(?:-image)?\s*:\s*url$["\']?(.*?)["\']?$',  # 匹配 background
    ]
    urls = []
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        urls.extend(
            [url.replace("amp;", "") for match in matches for url in (match.split(",") if "," in match else [match])]
        )
    return list(set(urls))


def download_and_save_image(image_url, local_image_folder):
    """
    下载图片并保存到本地。

    Args:
        image_url (str): 图片链接。
        local_image_folder (str): 本地图片保存文件夹。

    Returns:
        str: 本地图片文件路径，如果下载失败则返回 None。
    """
    try:
        # 创建本地图片保存文件夹
        if not os.path.exists(local_image_folder):
            os.makedirs(local_image_folder)

        # 下载图片，允许重定向
        response = requests.get(image_url, stream=True, allow_redirects=True)
        response.raise_for_status()

        # 生成本地文件名
        timestamp = str(int(time.time()))
        local_filename = os.path.join(local_image_folder, f"{timestamp}.jpg")
        # 保存图片到本地
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return local_filename

    except requests.exceptions.RequestException as e:
        log.print_log(f"下载图片失败：{image_url}，错误：{e}")
        return None
    except Exception as e:
        log.print_log(f"处理图片失败：{image_url}，错误：{e}")
        return None


def compress_html(html_content: str, aggressive: bool = False) -> str:
    """压缩HTML内容以减少token消耗"""
    try:
        import re
        
        if not aggressive:
            return html_content
        
        # 移除多余的空白字符
        html_content = re.sub(r'\s+', ' ', html_content)
        
        # 移除注释
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # 移除标签间的空白
        html_content = re.sub(r'>\s+<', '><', html_content)
        
        return html_content.strip()
    except Exception as e:
        log.print_log(f"压缩HTML时出错: {str(e)}")
        return html_content


def decompress_html(compressed_content, use_compress=True):
    """
    格式化 HTML 内容，处理压缩和未压缩 HTML，确保输出的内容适合网页渲染。

    参数：
        compressed_content (str): 输入的 HTML 字符串
        use_compress (bool): 是否作为压缩 HTML 处理（True）或直接返回（False）

    返回：
        str: 格式化后的 HTML 字符串
    """
    # 如果 use_compress 为 False 或内容已格式化（有换行和缩进），直接返回
    if not use_compress or re.search(r"\n\s{2,}", compressed_content):
        return compressed_content.strip()

    try:
        # 使用 lxml 解析器处理 HTML，支持不规范的 HTML
        soup = BeautifulSoup(compressed_content, "lxml")

        # 移除多余空白和注释，清理输出
        for element in soup.find_all(text=True):
            if element.strip() == "":
                element.extract()  # 移除空文本节点
            elif element.strip().startswith("<!--") and element.strip().endswith("-->"):
                element.extract()  # 移除注释

        # 判断是否为 HTML 片段（无 DOCTYPE 或 <html> 标签）
        is_fragment = not (
            compressed_content.strip().startswith("<!DOCTYPE")
            or compressed_content.strip().startswith("<html")
        )

        if is_fragment:
            # 对于片段，避免包裹 <html> 或 <body> 标签
            formatted_lines = []
            for child in soup.contents:
                if hasattr(child, "prettify"):
                    formatted_lines.append(child.prettify().strip())
                else:
                    formatted_lines.append(str(child).strip())
            return "\n".join(line for line in formatted_lines if line)

        # 对于完整 HTML 文档，返回格式化输出
        return soup.prettify(formatter="minimal").strip()

    except Exception as e:
        # 错误处理：解析失败时返回原始内容
        print(f"HTML 格式化错误：{e}")
        return compressed_content.strip()


def open_url(file_url):
    try:
        # 检查是否为网络 URL（以 http:// 或 https:// 开头）
        if file_url.startswith(("http://", "https://")):
            # 直接打开网络 URL
            webbrowser.open(file_url)
        else:
            # 视为本地文件路径，转换为 file:// 格式
            if not os.path.exists(file_url):
                return "文件不存在！"

            html_url = f"file://{os.path.abspath(file_url).replace(os.sep, '/')}"
            webbrowser.open(html_url)
        return ""
    except Exception as e:
        return str(e)


def extract_text_from_html(html_content: str) -> str:
    """从HTML中提取纯文本内容"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除script和style标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 获取文本内容
        text = soup.get_text()
        
        # 清理文本
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        log.print_log(f"提取HTML文本时出错: {str(e)}")
        return html_content
