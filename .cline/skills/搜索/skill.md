---
name: 搜索
description: "完整的搜索流程，包含查询压缩、站点绑定和脚本搜索。接收自然语言问题，自动压缩查询、绑定权威站点、执行搜索并返回结构化结果。当用户提出需要搜索的问题时，请调用此技能。"
---

# 低成本高精度搜索

## 目的

按照「查询压缩 → 站点绑定 → 脚本搜索」三步流程，实现从自然语言问题到结构化搜索结果的一站式低成本高精度检索。

## 使用时机

- 用户提出需要搜索的问题时
- 用户需要获取最新网络信息时
- 需要过滤低质量来源、优先权威站点时
- 查询技术文档、政策法规、行业数据时

## 工作流程

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户问题       │ -> │   查询压缩       │ -> │   站点绑定       │ -> │   搜索执行      │
│ "Python中如何... │    │ "Python 列表排序" │    │ "site:stackoverflow.com" │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Step 1 - 查询压缩

使用 `./scripts/query_compressor.md` 工具：

1. **识别答案类型**：定义/步骤/数据/对比/故障排查/列举
2. **提取核心关键词**：移除疑问词、停用词，保留5-7个关键词
3. **输出JSON**：`compressed_query`、`answer_type`、`token_saved_estimate`

### Step 2 - 站点绑定

使用 `./scripts/site_binder.md` 工具：

1. **检测领域类别**：政策法规/编程技术/学术文献/行业数据/通用百科
2. **应用site约束**：根据领域映射表添加站点限制
3. **输出JSON**：`targeted_query`、`sites`、`domain_category`

### Step 3 - 搜索执行

使用 `../scripts/VolcWebSearch.py` 执行搜索：

```bash
python ../scripts/VolcWebSearch.py "<搜索关键词>" --count 2 --sites "stackoverflow.com|docs.python.org"
```

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索关键词 | 必填 |
| `--count` | 返回条数（最大5） | 2 |
| `--sites` | 指定站点（多站点用 `\|` 分隔） | 空 |

## 输入格式

### 查询压缩输入
```
用户问题：Python中如何对列表进行排序，有没有简单的例子
```

### 站点绑定输入
```json
{
  "compressed_query": "Python 列表 排序 示例",
  "answer_type": "步骤",
  "token_saved_estimate": "45%"
}
```

## 输出格式

### 流水线最终输出
```json
{
  "success": true,
  "query": "Python 列表 排序",
  "domain_category": "编程技术",
  "answer_type": "步骤",
  "total": 3,
  "results": [
    {
      "title": "How do I sort a list of dictionaries by a value of the dictionary?",
      "url": "https://stackoverflow.com/questions/72899/",
      "abstract": "Use the sorted() function with a lambda key...",
      "source": "stackoverflow.com"
    }
  ]
}
```

## 错误处理

### 网络错误
```json
{
  "success": false,
  "error": "网络请求失败，请稍后重试",
  "query": "..."
}
```

### 空结果
```json
{
  "success": true,
  "query": "...",
  "total": 0,
  "results": [],
  "suggestion": "尝试更换关键词或放宽站点限制"
}
```

## 完整示例

### 示例1：编程技术查询

**用户输入：** "Python中如何对列表进行排序，最好有个简单的例子"

**Step 1 - 查询压缩：**
```json
{
  "compressed_query": "Python 列表 排序 示例",
  "answer_type": "步骤",
  "token_saved_estimate": "45%"
}
```

**Step 2 - 站点绑定：**
```json
{
  "targeted_query": "Python 列表 排序 示例",
  "sites": ["stackoverflow.com", "docs.python.org"],
  "domain_category": "编程技术",
  "estimated_precision_boost": "60%"
}
```

**Step 3 - 搜索调用：**
```bash
python ../scripts/VolcWebSearch.py "Python 列表 排序 示例" --count 5 --sites "stackoverflow.com|docs.python.org"
```

**最终结果：**
```json
{
  "success": true,
  "query": "Python 列表 排序 示例",
  "domain_category": "编程技术",
  "answer_type": "步骤",
  "total": 10,
  "results": [
    {
      "title": "How do I sort a list of dictionaries by a value of the dictionary?",
      "url": "https://stackoverflow.com/questions/72899/",
      "abstract": "Use sorted() with key parameter: sorted(list, key=lambda x: x['key'])",
      "source": "stackoverflow.com"
    },
    {
      "title": "Sorting HOW TO",
      "url": "https://docs.python.org/3/howto/sorting.html",
      "abstract": "Python has a built-in sorted() function that returns a new sorted list...",
      "source": "docs.python.org"
    }
  ]
}
```

### 示例2：政策法规查询

**用户输入：** "数据安全法的主要内容是什么"

**Step 1 - 查询压缩：**
```json
{
  "compressed_query": "数据安全法 主要内容",
  "answer_type": "定义",
  "token_saved_estimate": "35%"
}
```

**Step 2 - 站点绑定：**
```json
{
  "targeted_query": "数据安全法 主要内容",
  "sites": ["gov.cn"],
  "domain_category": "政策法规",
  "estimated_precision_boost": "75%"
}
```

**最终结果：** 返回来自gov.cn权威来源的数据安全法相关内容

### 示例3：学术文献查询

**用户输入：** "Transformer架构在NLP中的应用综述"

**Step 1 - 查询压缩：**
```json
{
  "compressed_query": "Transformer NLP 综述",
  "answer_type": "列举",
  "token_saved_estimate": "50%"
}
```

**Step 2 - 站点绑定：**
```json
{
  "targeted_query": "Transformer NLP 综述",
  "sites": ["arxiv.org", "aclweb.org"],
  "domain_category": "学术文献",
  "estimated_precision_boost": "70%"
}
```

### 示例4：故障排查查询

**用户输入：** "Docker容器启动失败，报错permission denied怎么解决"

**Step 1 - 查询压缩：**
```json
{
  "compressed_query": "Docker 容器 启动 失败 permission denied",
  "answer_type": "故障排查",
  "token_saved_estimate": "40%"
}
```

**Step 2 - 站点绑定：**
```json
{
  "targeted_query": "Docker 容器 启动 失败 permission denied",
  "sites": ["stackoverflow.com"],
  "domain_category": "编程技术",
  "estimated_precision_boost": "65%"
}
```

## 领域映射表速查

| 领域 | 主站点 | 适用场景 |
|------|--------|----------|
| 政策法规（国内） | gov.cn | 法律、法规、办法 |
| 政策法规（欧盟） | europa.eu | EU指令、GDPR |
| 编程技术 | stackoverflow.com, docs.python.org | 代码、API、框架 |
| 学术文献（国外） | arxiv.org, aclweb.org | 论文、综述 |
| 学术文献（国内） | ncpssd.cn, pubscholar.cn | 中文学术论文 |
| 行业数据 | gov.cn, marklines.com | 统计数据、市场报告 |
| 通用百科 | wikipedia.org, baike.baidu.com | 概念解释、名词定义 |

## 边界情况处理

| 情况 | 处理方式 |
|------|----------|
| 网络不可用 | 返回友好错误信息，提示检查网络 |
| 查询无结果 | 返回空结果数组，success为true，建议更换关键词 |
| API配额耗尽 | 提示用户稍后重试 |
| 问题太短（<5词） | 保持原查询不做压缩 |
| 包含代码/技术术语 | 原样保留不删除 |
| 无法识别领域 | 默认使用通用百科或stackoverflow.com |

## 性能优化技巧

1. **精准站点选择**：优先使用最相关的单一站点而非多个站点
2. **关键词精简**：压缩后的查询通常3-5个词效果最佳
3. **结果去重**：API自动去重，优先展示权威来源
4. **时间范围**：如需最新信息，可添加 `--time_range "OneMonth"`

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能文档 | `.cline/skills/搜索/skill.md` |
| 查询压缩 | `.cline/skills/搜索/scripts/query_compressor.md` |
| 站点绑定 | `.cline/skills/搜索/scripts/site_binder.md` |
| 搜索脚本 | `.cline/skills/搜索/scripts/VolcWebSearch.py` |
