---
name: 检索流水线
description: "完整的搜索流水线，串联查询压缩、站点绑定和MiniMax web_search搜索。接收自然语言问题，自动压缩查询、绑定权威站点、执行搜索并返回结构化结果。"
---

# 低成本高精度搜索流水线

## 目的

按正确顺序编排所有技能，串联查询压缩 → 站点绑定 → MiniMax搜索，实现从自然语言问题到结构化搜索结果的一站式检索。

## 使用时机

- 用户提出需要搜索的问题时
- 用户需要获取网页搜索结果时
- 需要过滤低质量来源、优先权威站点时
- 需要自动化整个检索流程时

## 前置条件

### MCP服务器配置

确保已安装并启用 `minimax-web-search` MCP服务器：
- MCP服务器名称：`minimax-web-search`
- 工具名称：`cGuKep0mcp0web_search`
- 环境变量：`MINIMAX_API_KEY` 已配置

## 完整工作流程

```
用户自然语言输入
        ↓
┌─────────────────┐
│   第一步：查询压缩   │  → 提取核心关键词，识别答案类型
│   (查询压缩技能)    │
└─────────────────┘
        ↓
┌─────────────────┐
│   第二步：站点绑定   │  → 根据领域类别添加site约束
│   (站点绑定技能)    │
└─────────────────┘
        ↓
┌─────────────────┐
│   第三步：搜索调用   │  → 调用MiniMax web_search MCP工具，执行搜索，按site约束过滤结果
│  (cGuKep0mcp0...) │
└─────────────────┘
        ↓
返回结构化JSON结果
```

## 使用方式

### 直接调用MCP工具

```json
{
  "tool": "cGuKep0mcp0web_search",
  "parameters": {
    "query": "压缩后的查询关键词"
  }
}
```

### 流水线调用示例

```
用户输入："Python中如何对列表进行排序"

Step 1 - 查询压缩：
{
  "compressed_query": "Python 列表 排序",
  "answer_type": "步骤"
}

Step 2 - 站点绑定：
{
  "targeted_query": "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org",
  "domain_category": "编程技术"
}

Step 3 - MiniMax搜索调用：
{
  "tool": "cGuKep0mcp0web_search",
  "parameters": {
    "query": "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org"
  }
}
```

## 输入格式

### 查询压缩输入
用户问题：<自然语言问题>

### 站点绑定输入
压缩后的查询结果（JSON）

### MiniMax搜索输入
```json
{
  "query": "关键词 site:域名"
}
```

## 输出格式

### MiniMax web_search 返回格式
```json
{
  "results": [
    {
      "title": "搜索结果标题",
      "url": "https://example.com/page",
      "content": "摘要内容..."
    }
  ]
}
```

### 流水线最终输出
```json
{
  "success": true,
  "query": "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org",
  "domain_category": "编程技术",
  "answer_type": "步骤",
  "total": 10,
  "results": [
    {
      "title": "How do I sort a list of dictionaries by a value of the dictionary?",
      "url": "https://stackoverflow.com/questions/72899/...",
      "abstract": "This is a code-only answer...",
      "source": "stackoverflow.com"
    }
  ]
}
```

## 错误处理

### API未配置
```json
{
  "success": false,
  "error": "MiniMax web_search MCP未配置或未连接",
  "query": "...",
  "results": []
}
```

### 网络错误
```json
{
  "success": false,
  "error": "网络请求失败，请稍后重试",
  "query": "...",
  "results": []
}
```

### 空结果
```json
{
  "success": true,
  "query": "...",
  "total": 0,
  "results": []
}
```

## 完整示例

### 示例1：编程技术查询

**用户输入：** "Python中如何对列表进行排序"

**Step 1 - 查询压缩：**
```json
{
  "compressed_query": "Python 列表 排序",
  "answer_type": "步骤",
  "token_saved_estimate": "40%"
}
```

**Step 2 - 站点绑定：**
```json
{
  "targeted_query": "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org",
  "domain_category": "编程技术",
  "estimated_precision_boost": "60%"
}
```

**Step 3 - MiniMax搜索调用：**
```
使用 cGuKep0mcp0web_search 工具，query="Python 列表 排序 site:stackoverflow.com OR site:docs.python.org"
```

**最终结果：**
```json
{
  "success": true,
  "query": "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org",
  "domain_category": "编程技术",
  "answer_type": "步骤",
  "total": 10,
  "results": [
    {
      "title": "How do I sort a list of dictionaries by a value of the dictionary?",
      "url": "https://stackoverflow.com/questions/72899/...",
      "abstract": "This is a code-only answer...",
      "source": "stackoverflow.com"
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
  "targeted_query": "数据安全法 主要内容 site:gov.cn",
  "domain_category": "政策法规",
  "estimated_precision_boost": "75%"
}
```

**最终结果：** 返回来自gov.cn权威来源的数据安全法相关内容

## 边界情况

1. **MCP未连接**：返回错误提示，指导用户检查MCP服务器状态
2. **网络不可用**：捕获异常并返回友好的错误信息
3. **查询无结果**：返回空结果数组，success仍为true
4. **API配额耗尽**：根据返回的错误信息提示用户
5. **特殊字符处理**：MiniMax API会自动处理URL编码

## 性能优化

- 使用MiniMax MCP工具直接调用，无需安装额外依赖
- 搜索结果自动去重和排序
- 支持site:约束过滤低质量来源
- 错误响应包含调试信息

## 文件位置

- **技能文档**：`.cline/skills/检索流水线/skill.md`

## 相关技能

- [查询压缩](./../查询压缩/skill.md) - 第一步：压缩查询
- [站点绑定](./../站点绑定/skill.md) - 第二步：绑定站点

## 搜索工具

- **MCP工具**：`cGuKep0mcp0web_search`
- **用途**：MiniMax提供的web搜索服务
- **参数**：`query` - 搜索关键词（建议已绑定site约束）
