# 🔍 Search Skill - 智能搜索技能

> 低成本高精度检索：查询压缩 → 站点绑定 →执行搜索 →返回结构化搜索结果

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 📖 目录
- [项目简介](#-项目简介)
- [运行环境](#-运行环境)
- [特性](#-特性)
- [快速开始](#-快速开始)
- [工作流程](#-工作流程)
- [使用指南](#-使用指南)
- [完整示例](#-完整示例)
- [API参考](#-api参考)
- [文件结构](#-文件结构)
- [常见问题](#-常见问题)

---

## 📝 项目简介

本项目是一个面向大模型（LLM）Agent 的**智能网络搜索技能**，旨在为 AI 助手提供低成本、高精度的联网检索能力。

### 核心问题

传统搜索方式直接使用用户原始问题进行检索，存在以下问题：
- **查询冗长**：自然语言问题包含大量停用词，浪费 token 额度
- **站点泛化**：未针对特定领域绑定权威站点，引入大量低质量结果
- **结果混乱**：返回非结构化文本，难以被程序处理和利用

### 解决方案

本技能通过三步流程实现高效检索：

| 步骤 | 功能 | 效果 |
|------|------|------|
| 查询压缩 | 将长句压缩为 5-7 个关键词 | 减少 token 消耗约 40-60% |
| 站点绑定 | 根据领域自动添加 `site:` 约束 | 过滤低质量来源，提升精度 |
| 执行搜索 | 调用搜索API执行检索 | 获取权威、相关结果 |
| 结构化搜索结果 | 返回标准 JSON 格式 | 便于程序解析和后处理 |

### 技术特点

- **兼容性**：纯 Python 实现，仅依赖 `requests` 库
- **可扩展**：站点映射表和压缩规则支持自定义配置
- **易集成**：支持命令行和 Python API 两种调用方式
- **可观测**：返回详细元数据，支持结果追溯

### 适用场景

- AI 助手/Agent 的联网问答需求
- 需要结构化搜索结果的自动化流程
- 特定领域的精准信息检索（如编程技术、政策法规、学术文献等）

---

## 🖥️ 运行环境

本技能在以下环境开发和运行：

| 组件 | 版本/名称 | 说明 |
|------|-----------|------|
| **IDE** | VSCode | Visual Studio Code 编辑器 |
| **插件** | Cline | AI 代码助手插件 |
| **大模型** | minimax-M2.7 | 支持长上下文的高性能大模型 |
| **搜索API** | 豆包联网搜索 | 字节跳动提供的网络检索服务 |


### 技术栈

```
┌─────────────────────────────────────────────────────────┐
│                     用户问题                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Cline 插件 (VSCode)                                    │
│  ├── minimax-M2.7 大模型                               │
│  └── 技能执行引擎                                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  搜索技能                                               │
│  ├── query_compressor.md (查询压缩)                    │
│  ├── site_binder.md (站点绑定)                         │
│  └── VolcWebSearch.py (搜索执行)                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  豆包联网搜索 API                                       │
│  └── https://open.feedcoopapi.com/search_api/web_search│
└─────────────────────────────────────────────────────────┘
```

---

## ✨ 特性

- **🔄 查询压缩** - 自动将自然语言问题压缩为精准关键词
- **🎯 站点绑定** - 智能识别领域，自动绑定权威站点
- **📊 结构化输出** - 返回标准JSON格式，便于程序处理
- **⚡ 高精度低开销** - 过滤低质量来源，提升搜索效率

## 🚀 快速开始
依赖python3.8+版本，
在vscode 的cline插件中配置minimax-M2.7大模型
申请豆包联网搜索API密钥，地址：https://console.volcengine.com/search-infinity/web-search, 并将其配置到 ./scripts/config.json 中。

```json
{
  "api_key": "你的API密钥"
}
```

### 安装依赖

```bash
pip install requests
```

### skill使用
在vscode中打开项目目录，点击安装插件Cline，打开搜索技能，然后直接输入搜索问题，即可使用。

### 搜索脚本基本使用

```bash
# 简单搜索
python scripts/VolcWebSearch.py "Python 列表排序"

# 指定站点和数量
python scripts/VolcWebSearch.py "Docker 部署" --count 3 --sites "stackoverflow.com|docs.docker.com"

# 添加时间范围
python scripts/VolcWebSearch.py "AI 大模型" --time-range "OneMonth"
```

## 📋 工作流程

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户问题       │ → │   查询压缩       │ → │   站点绑定       │ → │   搜索执行      │
│                 │    │                 │    │                 │    │                 │
│ "Python中如何对  │    │ "Python 列表排序" │    │ "site:stackoverflow│    │ 返回结构化结果  │
│  列表进行排序？" │    │                 │    │   .com"          │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Step 1: 查询压缩

将冗长的自然语言问题转换为简洁的关键词：

```json
// 输入
"Python中如何对列表进行排序，有没有简单的例子"

// 输出
{
  "compressed_query": "Python 列表 排序 示例",
  "answer_type": "步骤",
  "token_saved_estimate": "45%"
}
```

### Step 2: 站点绑定

根据问题领域自动添加站点约束：

| 领域 | 主站点 | 适用场景 |
|------|--------|----------|
| 编程技术 | stackoverflow.com | 代码、API、框架 |
| 政策法规 | gov.cn | 法律、法规 |
| 学术文献 | arxiv.org | 论文、综述 |
| 通用百科 | wikipedia.org | 概念解释 |

### Step 3: 搜索执行

调用火山引擎搜索API获取结果：

```bash
python scripts/VolcWebSearch.py "Python 列表 排序" --sites "stackoverflow.com"
```

## 📖 使用指南

### 查询压缩工具

**文件位置**: `scripts/query_compressor.md`

#### 答案类型识别

| 类型 | 触发关键词 | 说明 |
|------|-----------|------|
| `定义` | 什么是、定义、含义 | 概念解释类问题 |
| `步骤` | 如何、怎么、方法 | 操作指南类问题 |
| `数据` | 多少、数据、统计 | 数值查询类问题 |
| `对比` | 区别、vs、差异 | 比较分析类问题 |
| `故障排查` | 错误、失败、报错 | 问题解决类问题 |
| `列举` | 哪些、包括、分类 | 列表查询类问题 |

#### 压缩规则

1. 移除疑问词（如何、为什么、请问）
2. 移除停用词（的、了、吗、呢）
3. 保留名词、动词、数字、专有名词
4. 最终保留 5-7 个关键词

### 站点绑定工具

**文件位置**: `scripts/site_binder.md`

#### 领域映射表

| 类别 | 主站点 | 次站点 |
|------|--------|--------|
| 政策法规（国内） | site:gov.cn | site:pkulaw.com |
| 政策法规（欧盟） | site:europa.eu | - |
| 编程技术 | site:stackoverflow.com | site:docs.python.org |
| 学术文献(国外) | site:arxiv.org | site:aclweb.org |
| 学术文献(国内) | site:ncpssd.cn | site:pubscholar.cn |
| 行业数据 | site:gov.cn | site:marklines.com |
| 通用百科 | site:wikipedia.org | site:baike.baidu.com |
| Linux/服务器 | site:wiki.archlinux.org | site:nginx.org |

## 💡 完整示例
以下示例，在vscode中打开项目目录，点击安装插件Cline，打开搜索技能，然后直接输入搜索问题，即可使用。

### 示例 1: 编程技术查询

```bash
# 用户问题
"Python中如何对列表进行排序，最好有个简单的例子"

# Step 1: 查询压缩
python scripts/query_compressor.md
# {"compressed_query": "Python 列表 排序 示例", "answer_type": "步骤"}

# Step 2: 站点绑定
python scripts/site_binder.md
# {"sites": ["stackoverflow.com", "docs.python.org"], "domain_category": "编程技术"}

# Step 3: 搜索执行
python scripts/VolcWebSearch.py "Python 列表 排序 示例" \
  --count 2 \
  --sites "stackoverflow.com|docs.python.org"
```

**返回结果:**
```json
{
  "success": true,
  "query": "Python 列表 排序 示例",
  "domain_category": "编程技术",
  "total": 2,
  "results": [
    {
      "title": "How do I sort a list of dictionaries?",
      "url": "https://stackoverflow.com/questions/72899/",
      "abstract": "Use sorted() with key parameter",
      "source": "stackoverflow.com"
    },
    {
      "title": "Sorting HOW TO",
      "url": "https://docs.python.org/3/howto/sorting.html",
      "abstract": "Python has a built-in sorted() function",
      "source": "docs.python.org"
    }
  ]
}
```

### 示例 2: 政策法规查询

```bash
# 用户问题
"数据安全法的主要内容包括哪些？"

# Step 1: 查询压缩
python scripts/query_compressor.md
# {"compressed_query": "数据安全法 主要内容", "answer_type": "列举"}

# Step 2: 站点绑定
python scripts/site_binder.md
# {"sites": ["gov.cn"], "domain_category": "政策法规（国内）"}

# Step 3: 搜索执行
python scripts/VolcWebSearch.py "数据安全法 主要内容" \
  --count 3 \
  --sites "gov.cn"
```

**返回结果:**
```json
{
  "success": true,
  "query": "数据安全法 主要内容",
  "total": 3,
  "results": [
    {
      "title": "中华人民共和国数据安全法-黄河新闻网",
      "url": "https://www.sxgov.cn/content/2025-09/12/content_13503101.htm",
      "abstract": "中华人民共和国数据安全法中华人民共和国数据安全法（2021年6月10日第十三届全国人民代表大会常务委员会第二十九次会议通过）目录第一章 总则第二章 数据安全与发展第三章 数据安全制度第四章 数据安全保护义\n务第五章 政务数据安全与开放第六章 法律责任第七章 附则第一章 总则第一条 为了规范数据处理活动，保障数据安全，促进数据开发利用，保护个人、组织的合法权益，维护国家主权、安全和发展利益，制定本法。第二条 ",
      "source": "www.sxgov.cn"
    },
    {
      "title": "中华人民共和国数据安全法(全文)",
      "url": "http://www.tjcma.edu.cn/Print.aspx?id=5999",
      "abstract": "中华人民共和国数据安全法（全文）\n中华人民共和国数据安全法\n（2021年6月10日第十三届全国人民代表大会常务委员会第二十九次会议通过）\n目录\n第一章 总则\n第二章 数据安全与发展\n第三章 数据安全制度\n\n第四章 数据安全保护义务\n第五章 政务数据安全与开放\n第六章 法律责任\n第七章 附则\n第一章 总则\n第一条为了规范数据处理活动，保障数据安全，促进数据开发利用，保护个人、组织的合法权益，维护国家主权、安全",
      "source": "www.tjcma.edu.cn"
    },
    {
      "title": "中华人民共和国数据安全法(全文)",
      "url": "https://dsj.guizhou.gov.cn/zwgk/zdlyxx/sjzytg/202106/t20210615_86419664.html?isMobile=false",
      "abstract": "中华人民共和国数据安全法（全文）\n2021年6月10日，十三届全国人大常委会第二十九次会议表决通过《中华人民共和国数据安全法》，将于2021年9月1日起施行。\n中华人民共和国数据安全法\n目录\n第一章 总则\n\n第二章 数据安全与发展\n第三章 数据安全制度\n第四章 数据安全保护义务\n第五章 政务数据安全与开放\n第六章 法律责任\n第七章 附则\n第一章 总则\n第一条 为了规范数据处理活动，保障数据安全，促进数据开发",
      "source": "dsj.guizhou.gov.cn"
    }
  ]
}
```

### 示例 3: 故障排查

```bash
# 用户问题
"Docker启动失败提示permission denied怎么解决？"

# Step 1: 查询压缩
python scripts/query_compressor.md
# {"compressed_query": "Docker 启动失败 permission denied", "answer_type": "故障排查"}

# Step 2: 站点绑定
python scripts/site_binder.md
# {"sites": ["stackoverflow.com"], "domain_category": "编程技术"}

# Step 3: 搜索执行
python scripts/VolcWebSearch.py "Docker 启动失败 permission denied" \
  --count 2 \
  --sites "stackoverflow.com"
```

**返回结果:**
```json
{
  "success": true,
  "query": "Docker 启动失败 permission denied",
  "domain_category": "编程技术",
  "total": 2,
  "results": [
    {
      "title": "Docker: permission denied while trying to connect to the Docker daemon socket",
      "url": "https://stackoverflow.com/questions/...",
      "abstract": "Add user to docker group: sudo usermod -aG docker $USER",
      "source": "stackoverflow.com"
    },
    {
      "title": "Docker permission denied solutions",
      "url": "https://stackoverflow.com/questions/...",
      "abstract": "Check socket permissions and restart docker service",
      "source": "stackoverflow.com"
    }
  ]
}
```

## 🔌 API参考

### 命令行参数

```bash
python scripts/VolcWebSearch.py <query> [options]
```

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `query` | - | 搜索关键词 | 必填 |
| `--count` | `-c` | 返回条数（最大3） | 2 |
| `--sites` | `-s` | 指定站点（多站点用 `\|` 分隔） | 空 |
| `--time-range` | `-t` | 时间范围 | 空 |

### 时间范围选项

| 值 | 说明 |
|----|------|
| `OneDay` | 最近一天 |
| `OneWeek` | 最近一周 |
| `OneMonth` | 最近一月 |
| `OneYear` | 最近一年 |
| `YYYY-MM-DD..YYYY-MM-DD` | 自定义范围 |

### Python API

```python
from scripts.VolcWebSearch import web_search

result = web_search(
    query="Python 列表排序",
    count=5,
    sites="stackoverflow.com|docs.python.org",
    time_range="OneMonth"
)

if result["success"]:
    for item in result["results"]:
        print(f"📄 {item['title']}")
        print(f"🔗 {item['url']}")
        print(f"📝 {item['abstract']}")
        print()
```

### 返回格式

```json
{
  "success": true,
  "query": "搜索关键词",
  "total": 3,
  "results": [
    {
      "title": "页面标题",
      "url": "https://example.com",
      "abstract": "内容摘要",
      "source": "example.com"
    }
  ]
}
```

### 错误处理

```json
// 网络错误
{"success": false, "error": "网络请求失败，请稍后重试"}

// 空结果
{"success": true, "total": 0, "results": [], "suggestion": "尝试更换关键词"}
```

## 📁 文件结构

```
.cline/skills/搜索/
├── README.md                      # 项目文档
├── skill.md                       # 技能配置
├── scripts/
│   ├── VolcWebSearch.py          # 搜索执行脚本
│   ├── query_compressor.md       # 查询压缩工具
│   └── site_binder.md            # 站点绑定工具
└── references/                    # 参考资料
```

## ❓ 常见问题

**Q: 如何处理搜索无结果的情况？**

A: 返回空结果数组并提供建议，尝试更换关键词或放宽站点限制。

**Q: 问题太短是否需要压缩？**

A: 问题少于5个词时保持原查询不做压缩。

**Q: 包含代码的查询如何处理？**

A: 代码和技术术语原样保留，不进行删除或修改。

**Q: 无法识别问题领域时怎么办？**

A: 默认使用通用百科（wikipedia.org）或stackoverflow.com。

**Q: 如何提升搜索精度？**

A: 
1. 优先使用单一相关站点而非多个
2. 关键词精简到3-5个效果最佳
3. 需要最新信息时添加时间范围

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../../LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
