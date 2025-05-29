# 微信公众号自动发布API

这是一个基于FastAPI的微信公众号自动发布系统API接口，支持文章内容处理、模板应用和自动发布到微信公众号。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置微信公众号

在 `config.yaml` 文件中配置您的微信公众号信息：

```yaml
wechat:
  credentials:
    - appid: "your_wechat_appid"
      appsecret: "your_wechat_appsecret"
      author: "your_author_name"
```

### 3. 启动API服务器

```bash
# 方式1: 使用启动脚本
python api_server.py

# 方式2: 直接使用uvicorn
uvicorn src.ai_auto_wxgzh.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问API文档

启动后访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/api/v1/health

## 📋 API接口说明

### 核心接口

#### 1. 发布文章 (同步)

```http
POST /api/v1/publish
```

**请求参数:**

```json
{
  "content": "文章内容（HTML格式）",
  "template_id": "模板编号（可选）",
  "title": "文章标题（可选）",
  "digest": "文章摘要（可选）",
  "author": "作者名称（可选）",
  "appid": "微信AppID（可选）",
  "appsecret": "微信AppSecret（可选）"
}
```

**响应示例:**

```json
{
  "status": "success",
  "message": "成功发布文章到微信公众号",
  "article_url": "https://mp.weixin.qq.com/s/...",
  "media_id": "media_id_string",
  "publish_id": "publish_id_string"
}
```

#### 2. 发布文章 (异步)

```http
POST /api/v1/publish-async
```

立即返回任务ID，发布过程在后台进行。

**响应示例:**

```json
{
  "task_id": "uuid-task-id",
  "status": "processing",
  "message": "文章发布任务已提交，正在后台处理"
}
```

#### 3. 获取模板列表

```http
GET /api/v1/templates
```

**响应示例:**

```json
{
  "templates": [
    {
      "id": "template1",
      "name": "template1",
      "description": "模板 template1",
      "preview_url": null
    }
  ],
  "total": 1
}
```

#### 4. 获取模板内容

```http
GET /api/v1/templates/{template_id}
```

**响应示例:**

```json
{
  "template_id": "template1",
  "content": "<html>模板HTML内容...</html>"
}
```

#### 5. 获取微信配置

```http
GET /api/v1/config/wechat
```

**响应示例:**

```json
{
  "wechat_accounts": [
    {
      "appid": "wx1234567890",
      "author": "作者名称",
      "has_secret": true
    }
  ],
  "total": 1
}
```

#### 6. 健康检查

```http
GET /api/v1/health
```

**响应示例:**

```json
{
  "status": "healthy",
  "config_loaded": true,
  "config_valid": true,
  "message": "API服务运行正常"
}
```

## 💻 使用示例

### Python客户端示例

```python
import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 发布文章
def publish_article():
    url = f"{BASE_URL}/publish"
    
    data = {
        "content": """
        <h1>AI技术发展趋势</h1>
        <p>人工智能技术正在快速发展...</p>
        """,
        "title": "AI技术发展趋势分析",
        "digest": "探讨人工智能技术的最新发展趋势",
        "author": "AI研究员"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}")

# 运行示例
publish_article()
```

### cURL示例

```bash
# 发布文章
curl -X POST "http://localhost:8000/api/v1/publish" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "<h1>测试文章</h1><p>这是一篇测试文章</p>",
       "title": "测试文章标题",
       "digest": "这是文章摘要",
       "author": "测试作者"
     }'

# 获取模板列表
curl -X GET "http://localhost:8000/api/v1/templates"

# 健康检查
curl -X GET "http://localhost:8000/api/v1/health"
```

## 🎨 模板系统

### 模板目录结构

```
knowledge/
└── templates/
    ├── template1.html
    ├── template2.html
    └── ...
```

### 模板使用

1. **自动选择**: 不指定 `template_id` 时随机选择模板
2. **指定模板**: 通过 `template_id` 参数指定特定模板
3. **模板变量**: 模板中可使用 `{{content}}` 占位符

### 模板示例

```html
<!DOCTYPE html>
<html>
<head>
    <title>文章模板</title>
    <style>
        .article { padding: 20px; }
        .title { color: #333; }
    </style>
</head>
<body>
    <div class="article">
        {{content}}
    </div>
</body>
</html>
```

## ⚙️ 配置说明

### 必需配置

1. **微信公众号配置**
   - `appid`: 微信公众号AppID
   - `appsecret`: 微信公众号AppSecret
   - `author`: 默认作者名称

2. **AI模型配置**
   - API密钥和模型设置
   - 图片生成API配置

### 可选配置

- `use_template`: 是否使用模板系统
- `template`: 指定默认模板
- `need_auditor`: 是否需要内容审核
- `use_compress`: 是否压缩HTML
- `img_api_type`: 图片生成API类型

## 🔧 开发指南

### 项目结构

```
src/ai_auto_wxgzh/api/
├── __init__.py          # 模块初始化
├── main.py              # FastAPI应用主文件
├── routes.py            # API路由定义
├── models.py            # 数据模型
└── services.py          # 业务逻辑服务
```

### 扩展API

1. **添加新路由**: 在 `routes.py` 中添加新的端点
2. **添加数据模型**: 在 `models.py` 中定义请求/响应模型
3. **添加业务逻辑**: 在 `services.py` 中实现具体功能

### 错误处理

API使用标准HTTP状态码和统一的错误响应格式：

```json
{
  "error": "错误类型",
  "message": "错误消息",
  "detail": "错误详情"
}
```

## 🚨 注意事项

1. **微信限制**: 
   - 需要认证的微信公众号才能使用所有功能
   - 发布频率有限制，避免过于频繁调用

2. **安全性**:
   - 不要在客户端暴露AppSecret
   - 生产环境中应配置适当的CORS策略

3. **性能**:
   - 图片生成和上传可能耗时较长
   - 建议使用异步接口处理大量发布任务

4. **日志**:
   - 所有操作都会记录日志
   - 可通过日志文件查看详细执行信息

## 📞 支持

如有问题或建议，请：

1. 查看API文档: http://localhost:8000/docs
2. 检查日志文件
3. 运行健康检查接口
4. 查看示例代码: `examples/api_usage_examples.py`

## �� 许可证

MIT License 