---
sidebar_position: 2
---

# Google AI SDK

## 目录

1. [概述](#概述)
2. [安装与配置](#安装与配置)
3. [客户端初始化](#客户端初始化)
4. [核心模块详解](#核心模块详解)
   - [genai.client 模块](#genai-client-模块)
   - [genai.models 模块](#genai-models-模块)
   - [genai.chats 模块](#genai-chats-模块)
   - [genai.files 模块](#genai-files-模块)
   - [genai.batches 模块](#genai-batches-模块)
   - [genai.caches 模块](#genai-caches-模块)
   - [genai.tunings 模块](#genai-tunings-模块)
   - [genai.tokens 模块](#genai-tokens-模块)
   - [genai.types 模块](#genai-types-模块)
5. [实用示例](#实用示例)
6. [最佳实践](#最佳实践)
7. [错误处理](#错误处理)

---

## 概述

Google Generative AI Python SDK (`google-genai`) 是一个用于与Google生成式AI API交互的Python客户端库。该SDK支持两种API服务：
- **Gemini Developer API**: 面向开发者的API服务
- **Vertex AI API**: Google Cloud的企业级AI平台

### 主要特性

- 支持同步和异步操作
- 完整的类型提示支持
- 支持文本、图像、视频等多模态内容生成
- 提供批处理、缓存、模型微调等高级功能
- 支持函数调用和工具使用
- 内置安全设置和内容过滤

---

## 安装与配置

### 安装

```bash
pip install google-genai
```

### 可选依赖

```bash
# 支持更快的异步客户端
pip install google-genai[aiohttp]

# 支持SOCKS5代理
pip install httpx[socks]
```

### 环境变量配置

#### Gemini Developer API

```bash
export GOOGLE_API_KEY='your-api-key'
```

#### Vertex AI API

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='us-central1'
```

---

## 客户端初始化

### 基本导入

```python
from google import genai
from google.genai import types
```

### Gemini Developer API 客户端

```python
# 直接指定API密钥
client = genai.Client(api_key='your-api-key')

# 使用环境变量
client = genai.Client()
```

### Vertex AI API 客户端

```python
# 直接指定参数
client = genai.Client(
    vertexai=True,
    project='your-project-id',
    location='us-central1'
)

# 使用环境变量
client = genai.Client()
```

### 高级配置选项

#### API版本选择

```python
# 使用稳定版本 v1
client = genai.Client(
    vertexai=True,
    project='your-project-id',
    location='us-central1',
    http_options=types.HttpOptions(api_version='v1')
)

# 使用预览版本 v1alpha (Gemini Developer API)
client = genai.Client(
    api_key='your-api-key',
    http_options=types.HttpOptions(api_version='v1alpha')
)
```

#### 代理配置

```python
# HTTP/HTTPS 代理
import os
os.environ['HTTPS_PROXY'] = 'http://username:password@proxy_uri:port'
os.environ['SSL_CERT_FILE'] = 'client.pem'

# SOCKS5 代理
http_options = types.HttpOptions(
    client_args={'proxy': 'socks5://user:pass@host:port'},
    async_client_args={'proxy': 'socks5://user:pass@host:port'},
)
client = genai.Client(http_options=http_options)
```

#### 异步客户端优化

```python
# 使用 aiohttp 提升异步性能
http_options = types.HttpOptions(
    async_client_args={'cookies': ..., 'ssl': ...},
)
client = genai.Client(http_options=http_options)
```

---

## 核心模块详解

### genai.client 模块

#### Client 类

`Client` 类是SDK的核心入口点，提供同步操作接口。

**主要属性：**
- `models`: 模型相关操作
- `chats`: 对话会话管理
- `files`: 文件上传和管理
- `batches`: 批处理作业
- `caches`: 缓存内容管理
- `tunings`: 模型微调
- `auth_tokens`: 认证令牌管理
- `aio`: 异步客户端实例

**初始化参数：**
- `vertexai` (bool): 是否使用Vertex AI API
- `api_key` (str): Gemini Developer API密钥
- `credentials`: Vertex AI认证凭据
- `project` (str): Google Cloud项目ID
- `location` (str): API请求地区
- `debug_config`: 调试配置
- `http_options`: HTTP选项配置

#### AsyncClient 类

`AsyncClient` 类提供异步操作接口，属性与 `Client` 类似但所有方法都是异步的。

**使用示例：**

```python
# 同步客户端
client = genai.Client(api_key='your-api-key')

# 异步客户端
async_client = client.aio
# 或直接创建
async_client = genai.AsyncClient(api_key='your-api-key')
```

#### DebugConfig 类

用于测试和调试的配置选项。

**字段：**
- `client_mode` (str | None): 客户端模式
- `replays_directory` (str | None): 重放目录
- `replay_id` (str | None): 重放ID

---

### genai.models 模块

模型模块提供内容生成、嵌入计算、图像生成等核心AI功能。

#### 内容生成

##### 基本文本生成

```python
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='为什么天空是蓝色的？'
)
print(response.text)
```

##### 多模态内容生成

```python
# 文本 + 图像
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=[
        '这张图片显示了什么？',
        types.Part.from_uri(
            file_uri='gs://example/image.jpg',
            mime_type='image/jpeg'
        )
    ]
)
```

##### 配置选项

```python
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='讲一个故事',
    config=types.GenerateContentConfig(
        system_instruction='你是一个专业的故事讲述者',
        max_output_tokens=1000,
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        candidate_count=1,
        stop_sequences=['结束'],
        safety_settings=[
            types.SafetySetting(
                category='HARM_CATEGORY_HATE_SPEECH',
                threshold='BLOCK_MEDIUM_AND_ABOVE'
            )
        ]
    )
)
```

#### 流式生成

```python
# 同步流式生成
for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash-001',
    contents='写一首诗'
):
    print(chunk.text, end='')

# 异步流式生成
async for chunk in client.aio.models.generate_content_stream(
    model='gemini-2.0-flash-001',
    contents='写一首诗'
):
    print(chunk.text, end='')
```

#### 函数调用

##### 自动函数调用

```python
def get_weather(location: str) -> str:
    """获取指定地点的天气信息
    
    Args:
        location: 城市和州，例如 San Francisco, CA
    """
    return '晴天'

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='北京的天气怎么样？',
    config=types.GenerateContentConfig(
        tools=[get_weather]
    )
)
print(response.text)
```

##### 手动函数声明

```python
function = types.FunctionDeclaration(
    name='get_weather',
    description='获取指定地点的当前天气',
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'location': types.Schema(
                type='STRING',
                description='城市和州，例如 San Francisco, CA'
            )
        },
        required=['location']
    )
)

tool = types.Tool(function_declarations=[function])

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='北京的天气怎么样？',
    config=types.GenerateContentConfig(tools=[tool])
)

# 处理函数调用
if response.function_calls:
    function_call = response.function_calls[0]
    print(f"函数名: {function_call.name}")
    print(f"参数: {function_call.args}")
```

#### JSON响应模式

```python
# 使用Pydantic模型
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    instructions: list[str]

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='给我一个简单的蛋炒饭食谱',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=Recipe
    )
)

recipe = Recipe.model_validate_json(response.text)
print(f"食谱名称: {recipe.name}")
```

#### 令牌计算

```python
# 计算令牌数量
response = client.models.count_tokens(
    model='gemini-2.0-flash-001',
    contents='这段文本有多少个令牌？'
)
print(f"令牌数量: {response.total_tokens}")

# 详细令牌信息
response = client.models.compute_tokens(
    model='gemini-2.0-flash-001',
    contents='分析这段文本的令牌'
)
for token_info in response.tokens_info:
    print(f"角色: {token_info.role}")
    print(f"令牌: {token_info.tokens}")
```

#### 内容嵌入

```python
response = client.models.embed_content(
    model='text-embedding-004',
    contents='这是要嵌入的文本'
)
print(f"嵌入向量维度: {len(response.embeddings[0].values)}")
```

#### 图像生成 (Imagen)

```python
# 生成图像
response = client.models.generate_image(
    model='imagen-3.0-generate-001',
    prompt='一只可爱的小猫在花园里玩耍',
    config=types.GenerateImageConfig(
        number_of_images=2,
        include_rai_reason=True,
        output_mime_type='image/png'
    )
)

for i, image in enumerate(response.generated_images):
    image.save(f'generated_image_{i}.png')
```

#### 视频生成 (Veo)

```python
# 生成视频
response = client.models.generate_video(
    model='veo-001',
    prompt='一只鸟在蓝天中飞翔',
    config=types.GenerateVideoConfig(
        duration_seconds=5,
        output_compression_quality='OPTIMIZED'
    )
)

response.generated_video.save('generated_video.mp4')
```

#### 模型列表

```python
# 列出可用模型
for model in client.models.list():
    print(f"模型名称: {model.name}")
    print(f"显示名称: {model.display_name}")
    print(f"描述: {model.description}")
    print("---")

# 分页列表
pager = client.models.list(config={'page_size': 10})
print(f"当前页大小: {pager.page_size}")
for model in pager:
    print(model.name)

# 获取下一页
pager.next_page()
```

---

### genai.chats 模块

对话模块提供持续的多轮对话功能。

#### Chat 类

**主要方法：**
- `send_message()`: 发送消息并获取回复
- `send_message_stream()`: 流式发送消息

#### 创建对话会话

```python
# 创建对话
chat = client.chats.create(
    model='gemini-2.0-flash-001',
    config=types.GenerateContentConfig(
        system_instruction='你是一个友好的AI助手',
        temperature=0.7
    )
)

# 发送消息
response = chat.send_message('你好！')
print(response.text)

# 继续对话
response = chat.send_message('请告诉我关于Python的信息')
print(response.text)
```

#### 带历史记录的对话

```python
# 预设对话历史
history = [
    types.Content(
        role='user',
        parts=[types.Part.from_text('你好')]
    ),
    types.Content(
        role='model',
        parts=[types.Part.from_text('你好！我是AI助手，有什么可以帮助你的吗？')]
    )
]

chat = client.chats.create(
    model='gemini-2.0-flash-001',
    history=history
)

response = chat.send_message('请继续我们之前的对话')
print(response.text)
```

#### 流式对话

```python
chat = client.chats.create(model='gemini-2.0-flash-001')

# 流式发送消息
for chunk in chat.send_message_stream('讲一个长故事'):
    print(chunk.text, end='')
```

#### 异步对话

```python
# 异步对话
async_chat = client.aio.chats.create(model='gemini-2.0-flash-001')

# 异步发送消息
response = await async_chat.send_message('你好')
print(response.text)

# 异步流式对话
async for chunk in async_chat.send_message_stream('写一首诗'):
    print(chunk.text, end='')
```

---

### genai.files 模块

文件模块用于上传、管理和使用文件资源。

#### Files 类

**主要方法：**
- `upload()`: 上传文件
- `get()`: 获取文件信息
- `list()`: 列出文件
- `delete()`: 删除文件
- `download()`: 下载文件

#### 文件上传

```python
# 上传本地文件
file = client.files.upload(
    file='path/to/document.pdf',
    config=types.UploadFileConfig(
        display_name='重要文档',
        mime_type='application/pdf'
    )
)
print(f"文件URI: {file.uri}")
print(f"文件名称: {file.name}")

# 上传二进制数据
with open('image.jpg', 'rb') as f:
    file = client.files.upload(
        file=f,
        config=types.UploadFileConfig(
            display_name='示例图片',
            mime_type='image/jpeg'
        )
    )
```

#### 文件管理

```python
# 获取文件信息
file_info = client.files.get(name='files/abc123')
print(f"文件大小: {file_info.size_bytes}")
print(f"创建时间: {file_info.create_time}")

# 列出所有文件
for file in client.files.list():
    print(f"文件名: {file.display_name}")
    print(f"URI: {file.uri}")
    print(f"状态: {file.state}")

# 删除文件
client.files.delete(name='files/abc123')
```

#### 在生成中使用文件

```python
# 上传文件
file = client.files.upload(file='document.pdf')

# 在内容生成中使用文件
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=['请总结这个文档的内容', file]
)
print(response.text)
```

#### 异步文件操作

```python
# 异步上传
file = await client.aio.files.upload(file='document.pdf')

# 异步获取文件列表
async for file in await client.aio.files.list():
    print(file.name)
```

---

### genai.batches 模块

批处理模块用于处理大量请求的批处理作业。

#### Batches 类

**主要方法：**
- `create()`: 创建批处理作业
- `get()`: 获取作业状态
- `list()`: 列出作业
- `cancel()`: 取消作业
- `delete()`: 删除作业

#### 创建批处理作业

```python
# Vertex AI 批处理 (使用GCS)
batch_job = client.batches.create(
    model='gemini-2.0-flash-001',
    src='gs://my-bucket/input-data.jsonl',
    config=types.CreateBatchJobConfig(
        output_uri='gs://my-bucket/output/',
        display_name='文本分析批处理'
    )
)
print(f"作业ID: {batch_job.name}")
print(f"状态: {batch_job.state}")

# Gemini Developer API 批处理 (使用文件)
requests = [
    {'contents': '翻译：Hello'},
    {'contents': '翻译：Goodbye'},
    {'contents': '翻译：Thank you'}
]

batch_job = client.batches.create(
    model='gemini-2.0-flash-001',
    src=requests
)
```

#### 监控批处理作业

```python
# 获取作业状态
job = client.batches.get(name='batch-job-id')
print(f"作业状态: {job.state}")
print(f"创建时间: {job.create_time}")
print(f"完成时间: {job.end_time}")

# 等待作业完成
import time
while True:
    job = client.batches.get(name='batch-job-id')
    if job.state in ['JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED']:
        break
    time.sleep(30)  # 等待30秒后重新检查

print(f"最终状态: {job.state}")
```

#### 批处理作业管理

```python
# 列出所有批处理作业
for job in client.batches.list():
    print(f"作业: {job.name}")
    print(f"状态: {job.state}")
    print(f"模型: {job.model}")

# 分页列表
pager = client.batches.list(config={'page_size': 10})
for job in pager:
    print(job.name)

# 取消运行中的作业
client.batches.cancel(name='batch-job-id')

# 删除作业
client.batches.delete(name='batch-job-id')
```

#### 异步批处理操作

```python
# 异步创建批处理
batch_job = await client.aio.batches.create(
    model='gemini-2.0-flash-001',
    src='gs://my-bucket/input.jsonl'
)

# 异步监控
job = await client.aio.batches.get(name=batch_job.name)
print(f"状态: {job.state}")
```

---

### genai.caches 模块

缓存模块用于缓存常用内容以提高性能和降低成本。

#### Caches 类

**主要方法：**
- `create()`: 创建缓存内容
- `get()`: 获取缓存信息
- `list()`: 列出缓存
- `update()`: 更新缓存
- `delete()`: 删除缓存

#### 创建缓存

```python
# 创建缓存内容
contents = [
    types.Part.from_text('这是要缓存的长文档内容...'),
    # 可以包含多个部分
]

cache = client.caches.create(
    model='gemini-2.0-flash-001',
    contents=contents,
    config=types.CreateCachedContentConfig(
        display_name='文档缓存',
        system_instruction='你是一个文档分析专家',
        ttl='3600s'  # 缓存1小时
    )
)
print(f"缓存名称: {cache.name}")
```

#### 使用缓存生成内容

```python
# 使用缓存进行内容生成
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='请总结缓存的文档内容',
    config=types.GenerateContentConfig(
        cached_content=cache.name
    )
)
print(response.text)
```

#### 缓存管理

```python
# 获取缓存信息
cache_info = client.caches.get(name=cache.name)
print(f"过期时间: {cache_info.expire_time}")
print(f"使用次数: {cache_info.usage_metadata}")

# 更新缓存TTL
updated_cache = client.caches.update(
    name=cache.name,
    config=types.UpdateCachedContentConfig(
        ttl='7200s'  # 延长到2小时
    )
)

# 列出所有缓存
for cached_content in client.caches.list():
    print(f"缓存: {cached_content.display_name}")
    print(f"模型: {cached_content.model}")

# 删除缓存
client.caches.delete(name=cache.name)
```

#### 异步缓存操作

```python
# 异步创建缓存
cache = await client.aio.caches.create(
    model='gemini-2.0-flash-001',
    contents=contents,
    config={'display_name': '异步缓存', 'ttl': '3600s'}
)

# 异步列出缓存
async for cache in await client.aio.caches.list():
    print(cache.name)
```

---

### genai.tunings 模块

模型微调模块用于创建和管理自定义微调模型。

#### Tunings 类

**主要方法：**
- `create()`: 创建微调作业
- `get()`: 获取微调作业信息
- `list()`: 列出微调作业
- `cancel()`: 取消微调作业

#### 创建微调作业

```python
# 准备训练数据
training_data = [
    types.TuningExample(
        text_input='翻译成中文：Hello',
        output='你好'
    ),
    types.TuningExample(
        text_input='翻译成中文：Goodbye',
        output='再见'
    ),
    types.TuningExample(
        text_input='翻译成中文：Thank you',
        output='谢谢'
    )
]

# 创建微调作业
tuning_job = client.tunings.create(
    base_model='gemini-1.5-flash-001',
    training_dataset=types.TuningDataset(examples=training_data),
    config=types.CreateTuningJobConfig(
        tuned_model_display_name='中文翻译模型',
        epoch_count=5,
        learning_rate=0.001,
        batch_size=4
    )
)
print(f"微调作业ID: {tuning_job.name}")
print(f"状态: {tuning_job.state}")
```

#### 使用GCS数据集微调

```python
# 使用GCS存储的训练数据
tuning_job = client.tunings.create(
    base_model='gemini-1.5-flash-001',
    training_dataset=types.TuningDataset(
        gcs_uri='gs://my-bucket/training-data.jsonl'
    ),
    config=types.CreateTuningJobConfig(
        tuned_model_display_name='GCS训练模型',
        epoch_count=3
    )
)
```

#### 监控微调进度

```python
# 获取微调作业状态
job = client.tunings.get(name=tuning_job.name)
print(f"状态: {job.state}")
print(f"进度: {job.tuning_data_stats}")

# 等待微调完成
import time
while not job.has_ended:
    time.sleep(60)  # 等待1分钟
    job = client.tunings.get(name=tuning_job.name)
    print(f"当前状态: {job.state}")

if job.has_succeeded:
    print(f"微调成功！模型: {job.tuned_model}")
else:
    print(f"微调失败: {job.error}")
```

#### 使用微调模型

```python
# 使用微调后的模型
if job.has_succeeded:
    response = client.models.generate_content(
        model=job.tuned_model.model,
        contents='翻译成中文：How are you?'
    )
    print(response.text)
```

#### 微调作业管理

```python
# 列出所有微调作业
for job in client.tunings.list():
    print(f"作业: {job.tuned_model_display_name}")
    print(f"基础模型: {job.base_model}")
    print(f"状态: {job.state}")
    print("---")

# 取消运行中的微调作业
client.tunings.cancel(name='tuning-job-id')
```

#### 微调模型管理

```python
# 列出微调模型
for model in client.models.list_tuned():
    print(f"模型名称: {model.name}")
    print(f"基础模型: {model.base_model}")
    print(f"创建时间: {model.create_time}")

# 获取特定微调模型
tuned_model = client.models.get_tuned(name='tunedModels/my-model')
print(f"模型信息: {tuned_model}")

# 更新微调模型
updated_model = client.models.update_tuned(
    name='tunedModels/my-model',
    config=types.UpdateModelConfig(
        display_name='更新后的模型名称',
        description='更新后的描述'
    )
)
```

---

### genai.tokens 模块

令牌管理模块用于处理认证令牌相关操作。

#### Tokens 类

**主要方法：**
- `generate_access_token()`: 生成访问令牌
- `get_access_token()`: 获取当前访问令牌

#### 令牌操作

```python
# 生成新的访问令牌
token_response = client.auth_tokens.generate_access_token()
print(f"访问令牌: {token_response.access_token}")
print(f"过期时间: {token_response.expires_in}")

# 获取当前令牌
current_token = client.auth_tokens.get_access_token()
print(f"当前令牌: {current_token}")
```

---

### genai.types 模块

类型模块包含SDK中使用的所有数据类型和配置类。

#### 核心类型

##### Content 相关类型

```python
# 创建用户内容
user_content = types.UserContent(
    parts=[
        types.Part.from_text('这是文本内容'),
        types.Part.from_uri(
            file_uri='gs://bucket/image.jpg',
            mime_type='image/jpeg'
        )
    ]
)

# 创建模型内容
model_content = types.ModelContent(
    parts=[types.Part.from_text('这是模型的回复')]
)

# 创建通用内容
content = types.Content(
    role='user',
    parts=[types.Part.from_text('通用内容')]
)
```

##### Part 类型

```python
# 文本部分
text_part = types.Part.from_text('文本内容')

# 图像部分
image_part = types.Part.from_uri(
    file_uri='gs://bucket/image.jpg',
    mime_type='image/jpeg'
)

# 视频部分
video_part = types.Part.from_uri(
    file_uri='gs://bucket/video.mp4',
    mime_type='video/mp4'
)

# 函数调用部分
function_call_part = types.Part.from_function_call(
    name='get_weather',
    args={'location': 'Beijing'}
)

# 函数响应部分
function_response_part = types.Part.from_function_response(
    name='get_weather',
    response={'weather': 'sunny', 'temperature': '25°C'}
)
```

##### 配置类型

```python
# 生成内容配置
config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    max_output_tokens=1000,
    candidate_count=1,
    stop_sequences=['停止'],
    response_mime_type='application/json',
    system_instruction='你是一个专业助手',
    safety_settings=[
        types.SafetySetting(
            category='HARM_CATEGORY_HARASSMENT',
            threshold='BLOCK_MEDIUM_AND_ABOVE'
        )
    ],
    tools=[
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name='search',
                    description='搜索信息',
                    parameters=types.Schema(
                        type='OBJECT',
                        properties={
                            'query': types.Schema(
                                type='STRING',
                                description='搜索查询'
                            )
                        }
                    )
                )
            ]
        )
    ]
)
```

##### 安全设置

```python
# 安全设置配置
safety_settings = [
    types.SafetySetting(
        category='HARM_CATEGORY_HATE_SPEECH',
        threshold='BLOCK_MEDIUM_AND_ABOVE'
    ),
    types.SafetySetting(
        category='HARM_CATEGORY_DANGEROUS_CONTENT',
        threshold='BLOCK_ONLY_HIGH'
    ),
    types.SafetySetting(
        category='HARM_CATEGORY_HARASSMENT',
        threshold='BLOCK_LOW_AND_ABOVE'
    ),
    types.SafetySetting(
        category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
        threshold='BLOCK_NONE'
    )
]
```

##### 响应类型

```python
# 生成内容响应
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='你好'
)

# 访问响应属性
print(f"文本内容: {response.text}")
print(f"候选项: {response.candidates}")
print(f"使用元数据: {response.usage_metadata}")
print(f"安全评级: {response.candidates[0].safety_ratings}")

# 检查函数调用
if response.function_calls:
    for call in response.function_calls:
        print(f"函数: {call.name}")
        print(f"参数: {call.args}")
```

##### 文件类型

```python
# 图像类型
image = types.Image.from_file('path/to/image.jpg')
image.show()  # 在notebook中显示
image.save('output.jpg')  # 保存图像

# 视频类型
video = types.Video.from_file('path/to/video.mp4')
video.show()  # 在notebook中显示
video.save('output.mp4')  # 保存视频

# 音频类型
audio = types.Audio.from_file('path/to/audio.mp3')
```

##### HTTP选项

```python
# HTTP配置
http_options = types.HttpOptions(
    api_version='v1',
    client_args={'timeout': 30},
    async_client_args={'timeout': 30}
)

client = genai.Client(
    api_key='your-api-key',
    http_options=http_options
)
```

---

## 实用示例

### 完整的聊天机器人示例

```python
import asyncio
from google import genai
from google.genai import types

class ChatBot:
    def __init__(self, api_key: str, model: str = 'gemini-2.0-flash-001'):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.chat = None

    def start_chat(self, system_instruction: str = None):
        """开始新的对话会话"""
        config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=1000,
            safety_settings=[
                types.SafetySetting(
                    category='HARM_CATEGORY_HARASSMENT',
                    threshold='BLOCK_MEDIUM_AND_ABOVE'
                )
            ]
        )

        if system_instruction:
            config.system_instruction = system_instruction

        self.chat = self.client.chats.create(
            model=self.model,
            config=config
        )

    def send_message(self, message: str) -> str:
        """发送消息并获取回复"""
        if not self.chat:
            self.start_chat()

        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"错误: {str(e)}"

    def send_message_with_image(self, message: str, image_path: str) -> str:
        """发送包含图像的消息"""
        if not self.chat:
            self.start_chat()

        try:
            image = types.Image.from_file(image_path)
            response = self.chat.send_message([message, image])
            return response.text
        except Exception as e:
            return f"错误: {str(e)}"

# 使用示例
bot = ChatBot('your-api-key')
bot.start_chat('你是一个友好的AI助手，请用中文回答问题。')

print(bot.send_message('你好！'))
print(bot.send_message('请介绍一下Python编程语言'))
print(bot.send_message_with_image('这张图片显示了什么？', 'image.jpg'))
```

### 文档分析助手

```python
class DocumentAnalyzer:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def analyze_document(self, file_path: str, questions: list[str]) -> dict:
        """分析文档并回答问题"""
        # 上传文档
        file = self.client.files.upload(
            file=file_path,
            config=types.UploadFileConfig(
                display_name=f'分析文档_{file_path}'
            )
        )

        results = {}

        for question in questions:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.0-flash-001',
                    contents=[question, file],
                    config=types.GenerateContentConfig(
                        temperature=0.1,  # 更准确的回答
                        max_output_tokens=500
                    )
                )
                results[question] = response.text
            except Exception as e:
                results[question] = f"分析失败: {str(e)}"

        # 清理上传的文件
        try:
            self.client.files.delete(name=file.name)
        except:
            pass

        return results

# 使用示例
analyzer = DocumentAnalyzer('your-api-key')
questions = [
    '这个文档的主要内容是什么？',
    '文档中提到了哪些关键点？',
    '有什么重要的结论或建议吗？'
]

results = analyzer.analyze_document('report.pdf', questions)
for question, answer in results.items():
    print(f"问题: {question}")
    print(f"回答: {answer}")
    print("-" * 50)
```

### 批量内容生成器

```python
class ContentGenerator:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_batch_content(self, prompts: list[str], model: str = 'gemini-2.0-flash-001') -> list[str]:
        """批量生成内容"""
        # 准备批处理请求
        batch_requests = [{'contents': prompt} for prompt in prompts]

        # 创建批处理作业
        batch_job = self.client.batches.create(
            model=model,
            src=batch_requests
        )

        # 等待完成
        import time
        while True:
            job = self.client.batches.get(name=batch_job.name)
            if job.state in ['JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED']:
                break
            time.sleep(10)

        if job.state == 'JOB_STATE_SUCCEEDED':
            # 处理结果（实际实现需要根据API返回格式调整）
            return [f"生成的内容 for: {prompt}" for prompt in prompts]
        else:
            raise Exception(f"批处理失败: {job.error}")

    def generate_structured_content(self, topic: str, content_type: str) -> dict:
        """生成结构化内容"""
        from pydantic import BaseModel

        if content_type == 'article':
            class Article(BaseModel):
                title: str
                introduction: str
                main_points: list[str]
                conclusion: str

            schema = Article
            prompt = f"写一篇关于'{topic}'的文章"

        elif content_type == 'recipe':
            class Recipe(BaseModel):
                name: str
                ingredients: list[str]
                instructions: list[str]
                cooking_time: str

            schema = Recipe
            prompt = f"提供一个'{topic}'的食谱"
        else:
            raise ValueError("不支持的内容类型")

        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=schema,
                temperature=0.7
            )
        )

        return schema.model_validate_json(response.text).model_dump()

# 使用示例
generator = ContentGenerator('your-api-key')

# 批量生成
prompts = [
    '写一个关于AI的简短介绍',
    '解释什么是机器学习',
    '描述深度学习的应用'
]
results = generator.generate_batch_content(prompts)

# 生成结构化内容
article = generator.generate_structured_content('人工智能', 'article')
print(f"标题: {article['title']}")
print(f"介绍: {article['introduction']}")
```

### 多模态内容处理器

```python
class MultimodalProcessor:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def process_image_and_text(self, image_path: str, text_query: str) -> str:
        """处理图像和文本组合"""
        image = types.Image.from_file(image_path)

        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=[text_query, image],
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=800
            )
        )

        return response.text

    def generate_image_description(self, image_path: str, style: str = 'detailed') -> str:
        """生成图像描述"""
        prompts = {
            'detailed': '请详细描述这张图片中的所有内容，包括物体、人物、场景、颜色、情感等。',
            'simple': '用简单的语言描述这张图片的主要内容。',
            'creative': '用富有创意和诗意的语言描述这张图片。'
        }

        return self.process_image_and_text(image_path, prompts.get(style, prompts['detailed']))

    def extract_text_from_image(self, image_path: str) -> str:
        """从图像中提取文本"""
        return self.process_image_and_text(
            image_path,
            '请提取并转录这张图片中的所有文本内容。如果没有文本，请说明。'
        )

    def analyze_chart_or_graph(self, image_path: str) -> str:
        """分析图表或图形"""
        return self.process_image_and_text(
            image_path,
            '请分析这个图表或图形，包括数据趋势、关键发现和重要洞察。'
        )

# 使用示例
processor = MultimodalProcessor('your-api-key')

# 生成图像描述
description = processor.generate_image_description('photo.jpg', 'creative')
print(f"创意描述: {description}")

# 提取文本
text = processor.extract_text_from_image('document_scan.jpg')
print(f"提取的文本: {text}")

# 分析图表
analysis = processor.analyze_chart_or_graph('sales_chart.png')
print(f"图表分析: {analysis}")
```

---

## 最佳实践

### 1. 错误处理和重试机制

```python
import time
import random
from typing import Optional

class RobustClient:
    def __init__(self, api_key: str, max_retries: int = 3):
        self.client = genai.Client(api_key=api_key)
        self.max_retries = max_retries

    def generate_with_retry(self, model: str, contents: str, config: Optional[types.GenerateContentConfig] = None) -> str:
        """带重试机制的内容生成"""
        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
                return response.text

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e

                # 指数退避
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"请求失败，{wait_time:.2f}秒后重试... (尝试 {attempt + 1}/{self.max_retries})")
                time.sleep(wait_time)

        raise Exception("所有重试都失败了")

# 使用示例
robust_client = RobustClient('your-api-key')
try:
    result = robust_client.generate_with_retry(
        'gemini-2.0-flash-001',
        '解释量子计算的基本原理'
    )
    print(result)
except Exception as e:
    print(f"最终失败: {e}")
```

### 2. 成本优化策略

```python
class CostOptimizedClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.cache_store = {}  # 简单的内存缓存

    def generate_with_caching(self, model: str, contents: str, cache_key: str = None) -> str:
        """使用缓存优化成本"""
        if cache_key and cache_key in self.cache_store:
            print("使用缓存结果")
            return self.cache_store[cache_key]

        # 使用较小的token限制来控制成本
        config = types.GenerateContentConfig(
            max_output_tokens=500,  # 限制输出长度
            temperature=0.3  # 降低随机性，提高缓存命中率
        )

        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )

        result = response.text

        # 缓存结果
        if cache_key:
            self.cache_store[cache_key] = result

        return result

    def estimate_tokens(self, text: str) -> int:
        """估算文本的token数量"""
        response = self.client.models.count_tokens(
            model='gemini-2.0-flash-001',
            contents=text
        )
        return response.total_tokens

    def optimize_prompt(self, original_prompt: str) -> str:
        """优化提示词以减少token使用"""
        # 移除多余的空格和换行
        optimized = ' '.join(original_prompt.split())

        # 如果太长，尝试压缩
        if self.estimate_tokens(optimized) > 1000:
            compression_prompt = f"请将以下提示词压缩为更简洁的版本，保持核心意思不变：{optimized}"
            compressed = self.generate_with_caching(
                'gemini-2.0-flash-001',
                compression_prompt,
                f"compress_{hash(optimized)}"
            )
            return compressed

        return optimized

# 使用示例
cost_client = CostOptimizedClient('your-api-key')

# 估算成本
prompt = "请详细解释人工智能的发展历史和未来趋势"
token_count = cost_client.estimate_tokens(prompt)
print(f"预估token数量: {token_count}")

# 优化提示词
optimized_prompt = cost_client.optimize_prompt(prompt)
print(f"优化后的提示词: {optimized_prompt}")

# 使用缓存生成
result = cost_client.generate_with_caching(
    'gemini-2.0-flash-001',
    optimized_prompt,
    'ai_history_explanation'
)
```

### 3. 安全和内容过滤

```python
class SafeContentGenerator:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

        # 严格的安全设置
        self.safe_config = types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(
                    category='HARM_CATEGORY_HATE_SPEECH',
                    threshold='BLOCK_LOW_AND_ABOVE'
                ),
                types.SafetySetting(
                    category='HARM_CATEGORY_DANGEROUS_CONTENT',
                    threshold='BLOCK_LOW_AND_ABOVE'
                ),
                types.SafetySetting(
                    category='HARM_CATEGORY_HARASSMENT',
                    threshold='BLOCK_LOW_AND_ABOVE'
                ),
                types.SafetySetting(
                    category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                    threshold='BLOCK_LOW_AND_ABOVE'
                )
            ]
        )

    def generate_safe_content(self, model: str, contents: str) -> dict:
        """生成安全内容并返回安全评级"""
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=self.safe_config
            )

            # 检查安全评级
            safety_ratings = {}
            if response.candidates:
                for rating in response.candidates[0].safety_ratings:
                    safety_ratings[rating.category] = {
                        'probability': rating.probability,
                        'blocked': rating.blocked
                    }

            return {
                'content': response.text,
                'safety_ratings': safety_ratings,
                'finish_reason': response.candidates[0].finish_reason if response.candidates else None
            }

        except Exception as e:
            return {
                'content': None,
                'error': str(e),
                'safety_ratings': {},
                'finish_reason': 'ERROR'
            }

    def validate_input(self, user_input: str) -> bool:
        """验证用户输入是否安全"""
        # 简单的关键词过滤
        forbidden_keywords = ['暴力', '仇恨', '危险']

        for keyword in forbidden_keywords:
            if keyword in user_input:
                return False

        return True

# 使用示例
safe_generator = SafeContentGenerator('your-api-key')

user_input = "请写一个关于友谊的故事"

if safe_generator.validate_input(user_input):
    result = safe_generator.generate_safe_content(
        'gemini-2.0-flash-001',
        user_input
    )

    if result['content']:
        print(f"生成的内容: {result['content']}")
        print(f"安全评级: {result['safety_ratings']}")
    else:
        print(f"内容生成失败: {result['error']}")
else:
    print("输入包含不当内容，请修改后重试")
```

### 4. 性能监控和日志记录

```python
import logging
import time
from datetime import datetime
from typing import Dict, Any

class MonitoredClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.setup_logging()
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_tokens_used': 0,
            'average_response_time': 0
        }
        self.response_times = []

    def setup_logging(self):
        """设置日志记录"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('genai_client.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def generate_content_monitored(self, model: str, contents: str, config: types.GenerateContentConfig = None) -> Dict[str, Any]:
        """监控的内容生成"""
        start_time = time.time()
        request_id = f"req_{int(time.time() * 1000)}"

        self.logger.info(f"[{request_id}] 开始请求 - 模型: {model}")
        self.metrics['total_requests'] += 1

        try:
            # 计算输入token
            input_tokens = self.client.models.count_tokens(
                model=model,
                contents=contents
            ).total_tokens

            # 生成内容
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )

            # 计算响应时间
            response_time = time.time() - start_time
            self.response_times.append(response_time)

            # 更新指标
            self.metrics['successful_requests'] += 1
            if response.usage_metadata:
                self.metrics['total_tokens_used'] += response.usage_metadata.total_token_count

            self.metrics['average_response_time'] = sum(self.response_times) / len(self.response_times)

            self.logger.info(
                f"[{request_id}] 请求成功 - "
                f"响应时间: {response_time:.2f}s, "
                f"输入tokens: {input_tokens}, "
                f"输出tokens: {response.usage_metadata.response_token_count if response.usage_metadata else 'N/A'}"
            )

            return {
                'success': True,
                'content': response.text,
                'response_time': response_time,
                'usage_metadata': response.usage_metadata,
                'request_id': request_id
            }

        except Exception as e:
            response_time = time.time() - start_time
            self.metrics['failed_requests'] += 1

            self.logger.error(
                f"[{request_id}] 请求失败 - "
                f"错误: {str(e)}, "
                f"响应时间: {response_time:.2f}s"
            )

            return {
                'success': False,
                'error': str(e),
                'response_time': response_time,
                'request_id': request_id
            }

    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        success_rate = (self.metrics['successful_requests'] / self.metrics['total_requests'] * 100) if self.metrics['total_requests'] > 0 else 0

        return {
            **self.metrics,
            'success_rate': f"{success_rate:.2f}%",
            'last_updated': datetime.now().isoformat()
        }

    def reset_metrics(self):
        """重置指标"""
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_tokens_used': 0,
            'average_response_time': 0
        }
        self.response_times = []
        self.logger.info("指标已重置")

# 使用示例
monitored_client = MonitoredClient('your-api-key')

# 执行一些请求
for i in range(5):
    result = monitored_client.generate_content_monitored(
        'gemini-2.0-flash-001',
        f'这是第{i+1}个测试请求，请简短回复。'
    )

    if result['success']:
        print(f"请求 {result['request_id']} 成功")
    else:
        print(f"请求 {result['request_id']} 失败: {result['error']}")

# 查看性能指标
metrics = monitored_client.get_metrics()
print("\n性能指标:")
for key, value in metrics.items():
    print(f"{key}: {value}")
```

---

## 错误处理

### 常见错误类型和处理方法

#### 1. API认证错误

```python
from google import genai
from google.genai import types

def handle_auth_errors():
    """处理认证相关错误"""
    try:
        # 错误的API密钥
        client = genai.Client(api_key='invalid-key')
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents='测试'
        )
    except Exception as e:
        if 'authentication' in str(e).lower() or 'api_key' in str(e).lower():
            print("认证错误：请检查API密钥是否正确")
            print("解决方案：")
            print("1. 验证API密钥是否有效")
            print("2. 检查环境变量GOOGLE_API_KEY是否设置正确")
            print("3. 确认API密钥有足够的权限")
        else:
            print(f"其他错误: {e}")

# 正确的认证处理
def safe_client_init(api_key: str = None):
    """安全的客户端初始化"""
    try:
        if api_key:
            client = genai.Client(api_key=api_key)
        else:
            # 尝试从环境变量获取
            import os
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("未找到API密钥，请设置GOOGLE_API_KEY环境变量或直接提供api_key参数")
            client = genai.Client(api_key=api_key)

        # 测试连接
        models = list(client.models.list())
        print(f"客户端初始化成功，可用模型数量: {len(models)}")
        return client

    except Exception as e:
        print(f"客户端初始化失败: {e}")
        return None
```

#### 2. 配额和限制错误

```python
import time
import random

class QuotaAwareClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.request_count = 0
        self.last_request_time = 0

    def generate_with_quota_handling(self, model: str, contents: str, max_retries: int = 3):
        """处理配额限制的内容生成"""
        for attempt in range(max_retries):
            try:
                # 简单的速率限制
                current_time = time.time()
                if current_time - self.last_request_time < 1:  # 最少间隔1秒
                    time.sleep(1 - (current_time - self.last_request_time))

                response = self.client.models.generate_content(
                    model=model,
                    contents=contents
                )

                self.request_count += 1
                self.last_request_time = time.time()
                return response.text

            except Exception as e:
                error_msg = str(e).lower()

                if 'quota' in error_msg or 'rate limit' in error_msg:
                    wait_time = (2 ** attempt) * 60  # 指数退避，以分钟为单位
                    print(f"配额限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)

                elif 'resource exhausted' in error_msg:
                    print("资源耗尽，请稍后重试")
                    time.sleep(300)  # 等待5分钟

                else:
                    # 其他错误，不重试
                    raise e

        raise Exception("达到最大重试次数，请求失败")

# 使用示例
quota_client = QuotaAwareClient('your-api-key')
try:
    result = quota_client.generate_with_quota_handling(
        'gemini-2.0-flash-001',
        '请简要介绍机器学习'
    )
    print(result)
except Exception as e:
    print(f"请求最终失败: {e}")
```

#### 3. 内容安全错误

```python
def handle_safety_errors():
    """处理内容安全相关错误"""
    client = genai.Client(api_key='your-api-key')

    # 可能触发安全过滤的内容
    unsafe_content = "如何制造危险物品"

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=unsafe_content,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category='HARM_CATEGORY_DANGEROUS_CONTENT',
                        threshold='BLOCK_MEDIUM_AND_ABOVE'
                    )
                ]
            )
        )
        print(response.text)

    except Exception as e:
        if 'safety' in str(e).lower() or 'blocked' in str(e).lower():
            print("内容被安全过滤器阻止")
            print("解决方案：")
            print("1. 修改提示词，避免敏感内容")
            print("2. 调整安全设置阈值（如果合适）")
            print("3. 重新表述问题以符合内容政策")

            # 尝试重新表述
            safe_alternative = "请介绍化学实验的安全注意事项"
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash-001',
                    contents=safe_alternative
                )
                print(f"替代内容生成成功: {response.text}")
            except Exception as e2:
                print(f"替代内容也失败: {e2}")
        else:
            print(f"其他错误: {e}")

def check_content_safety(client: genai.Client, content: str) -> dict:
    """检查内容安全性"""
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=content,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category='HARM_CATEGORY_HATE_SPEECH',
                        threshold='BLOCK_LOW_AND_ABOVE'
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_DANGEROUS_CONTENT',
                        threshold='BLOCK_LOW_AND_ABOVE'
                    )
                ]
            )
        )

        safety_info = {}
        if response.candidates:
            candidate = response.candidates[0]
            safety_info['finish_reason'] = candidate.finish_reason
            safety_info['safety_ratings'] = {}

            for rating in candidate.safety_ratings:
                safety_info['safety_ratings'][rating.category] = {
                    'probability': rating.probability,
                    'blocked': rating.blocked
                }

        return {
            'safe': True,
            'content': response.text,
            'safety_info': safety_info
        }

    except Exception as e:
        return {
            'safe': False,
            'error': str(e),
            'safety_info': {}
        }
```

#### 4. 模型和参数错误

```python
def handle_model_errors():
    """处理模型相关错误"""
    client = genai.Client(api_key='your-api-key')

    # 错误的模型名称
    try:
        response = client.models.generate_content(
            model='non-existent-model',
            contents='测试'
        )
    except Exception as e:
        if 'model' in str(e).lower() and 'not found' in str(e).lower():
            print("模型不存在错误")
            print("解决方案：")
            print("1. 检查模型名称是否正确")
            print("2. 列出可用模型")

            # 列出可用模型
            try:
                print("可用模型:")
                for model in client.models.list():
                    print(f"- {model.name}")
            except Exception as list_error:
                print(f"无法列出模型: {list_error}")
        else:
            print(f"其他模型错误: {e}")

def validate_parameters(config: types.GenerateContentConfig) -> list[str]:
    """验证生成配置参数"""
    errors = []

    if config.temperature is not None:
        if not 0 <= config.temperature <= 2:
            errors.append("temperature必须在0-2之间")

    if config.top_p is not None:
        if not 0 <= config.top_p <= 1:
            errors.append("top_p必须在0-1之间")

    if config.top_k is not None:
        if config.top_k < 1:
            errors.append("top_k必须大于0")

    if config.max_output_tokens is not None:
        if config.max_output_tokens < 1:
            errors.append("max_output_tokens必须大于0")

    return errors

# 使用示例
config = types.GenerateContentConfig(
    temperature=2.5,  # 错误：超出范围
    top_p=1.5,       # 错误：超出范围
    max_output_tokens=-100  # 错误：负数
)

validation_errors = validate_parameters(config)
if validation_errors:
    print("参数验证失败:")
    for error in validation_errors:
        print(f"- {error}")
else:
    print("参数验证通过")
```

#### 5. 网络和连接错误

```python
import requests
from urllib3.exceptions import ConnectTimeoutError, ReadTimeoutError

class ResilientClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                client_args={'timeout': 30}  # 30秒超时
            )
        )

    def generate_with_network_handling(self, model: str, contents: str, max_retries: int = 3):
        """处理网络错误的内容生成"""
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents
                )
                return response.text

            except (ConnectTimeoutError, ReadTimeoutError, requests.exceptions.Timeout) as e:
                print(f"网络超时 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    raise Exception("网络连接超时，请检查网络连接")

            except requests.exceptions.ConnectionError as e:
                print(f"连接错误: {e}")
                raise Exception("无法连接到API服务器，请检查网络连接")

            except Exception as e:
                error_msg = str(e).lower()
                if 'network' in error_msg or 'connection' in error_msg:
                    print(f"网络相关错误: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                    else:
                        raise Exception("网络错误，请稍后重试")
                else:
                    # 非网络错误，直接抛出
                    raise e

        raise Exception("达到最大重试次数")

# 网络状态检查
def check_network_connectivity():
    """检查网络连接状态"""
    try:
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            print("网络连接正常")
            return True
    except Exception as e:
        print(f"网络连接异常: {e}")
        return False

# 使用示例
if check_network_connectivity():
    resilient_client = ResilientClient('your-api-key')
    try:
        result = resilient_client.generate_with_network_handling(
            'gemini-2.0-flash-001',
            '请介绍人工智能的应用'
        )
        print(result)
    except Exception as e:
        print(f"请求失败: {e}")
else:
    print("请检查网络连接后重试")
```

### 综合错误处理示例

```python
class ComprehensiveErrorHandler:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def safe_generate_content(self, model: str, contents: str, config: types.GenerateContentConfig = None) -> dict:
        """综合错误处理的内容生成"""
        try:
            # 参数验证
            if config:
                validation_errors = validate_parameters(config)
                if validation_errors:
                    return {
                        'success': False,
                        'error_type': 'VALIDATION_ERROR',
                        'error_message': '; '.join(validation_errors),
                        'content': None
                    }

            # 执行请求
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )

            return {
                'success': True,
                'content': response.text,
                'usage_metadata': response.usage_metadata,
                'safety_ratings': response.candidates[0].safety_ratings if response.candidates else []
            }

        except Exception as e:
            error_msg = str(e).lower()

            # 分类错误类型
            if 'authentication' in error_msg or 'api_key' in error_msg:
                error_type = 'AUTH_ERROR'
                suggestion = "请检查API密钥是否正确"

            elif 'quota' in error_msg or 'rate limit' in error_msg:
                error_type = 'QUOTA_ERROR'
                suggestion = "请稍后重试或检查配额限制"

            elif 'safety' in error_msg or 'blocked' in error_msg:
                error_type = 'SAFETY_ERROR'
                suggestion = "内容被安全过滤器阻止，请修改提示词"

            elif 'model' in error_msg and 'not found' in error_msg:
                error_type = 'MODEL_ERROR'
                suggestion = "请检查模型名称是否正确"

            elif 'timeout' in error_msg or 'connection' in error_msg:
                error_type = 'NETWORK_ERROR'
                suggestion = "网络连接问题，请检查网络状态"

            else:
                error_type = 'UNKNOWN_ERROR'
                suggestion = "未知错误，请查看详细错误信息"

            return {
                'success': False,
                'error_type': error_type,
                'error_message': str(e),
                'suggestion': suggestion,
                'content': None
            }

# 使用示例
handler = ComprehensiveErrorHandler('your-api-key')

# 测试各种情况
test_cases = [
    {
        'model': 'gemini-2.0-flash-001',
        'contents': '请介绍Python编程语言',
        'config': None
    },
    {
        'model': 'non-existent-model',
        'contents': '测试',
        'config': None
    },
    {
        'model': 'gemini-2.0-flash-001',
        'contents': '测试',
        'config': types.GenerateContentConfig(temperature=3.0)  # 无效参数
    }
]

for i, test_case in enumerate(test_cases):
    print(f"\n测试案例 {i + 1}:")
    result = handler.safe_generate_content(**test_case)

    if result['success']:
        print(f"成功: {result['content'][:100]}...")
    else:
        print(f"失败: {result['error_type']}")
        print(f"错误信息: {result['error_message']}")
        print(f"建议: {result['suggestion']}")
```

---

## 总结

本文档详细介绍了Google Generative AI Python SDK的各个模块和功能，包括：

1. **基础设置**: 安装、配置和客户端初始化
2. **核心模块**: 详细的API参考和使用示例
3. **实用示例**: 完整的应用场景演示
4. **最佳实践**: 性能优化、成本控制和安全考虑
5. **错误处理**: 全面的错误类型和处理策略

通过本文档，开发者可以：
- 快速上手Google Generative AI SDK
- 了解各种高级功能的使用方法
- 构建稳定可靠的AI应用
- 优化性能和成本
- 处理各种异常情况

建议开发者根据具体需求选择合适的功能模块，并结合最佳实践来构建生产级的AI应用。
