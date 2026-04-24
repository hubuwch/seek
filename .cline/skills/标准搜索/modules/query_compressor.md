# 查询压缩器模块

## 概述

查询压缩器模块是标准搜索技能的核心组件之一，负责将自然语言查询压缩为简洁的关键词形式。它整合了现有查询压缩技能的核心逻辑，并提供了更灵活的配置选项。

## 功能特性

### 1. 智能关键词提取
- 自动识别和提取查询中的核心实体
- 支持多语言关键词提取（中文、英文等）
- 保留技术术语和专有名词

### 2. 答案类型识别
- 自动检测用户需要的答案类型
- 支持6种标准答案类型
- 基于关键词和上下文进行类型推断

### 3. 停用词过滤
- 自动移除常见停用词和填充词
- 可配置的停用词列表
- 支持语言特定的停用词处理

### 4. 查询优化
- 控制关键词数量（2-7个）
- 保持查询的语义完整性
- 预估token节省率

## 配置选项

### 基本配置
```yaml
max_keywords: 7          # 最大关键词数量
min_keywords: 2          # 最小关键词数量
remove_stopwords: true   # 是否移除停用词
detect_answer_type: true # 是否检测答案类型
language: "auto"         # 语言设置（auto/zh/en）
```

### 答案类型配置
```yaml
answer_types:
  - "定义"        # 什么是、定义、含义
  - "步骤"        # 如何、怎么、方法
  - "数据"        # 多少、数据、统计
  - "对比"        # 区别、对比、差异
  - "故障排查"    # 错误、失败、问题
  - "列举"        # 哪些、列举、包括
```

### 高级配置
```yaml
token_saving_goal: 40    # token节省目标百分比
fallback_to_original: true # 失败时回退到原始查询
enable_synonym_expansion: false # 是否启用同义词扩展
preserve_numbers: true   # 是否保留数字
preserve_technical_terms: true # 是否保留技术术语
```

## 处理流程

### 步骤1：预处理
1. 清理特殊字符和多余空格
2. 转换为小写（英文）
3. 分词处理（中文需要分词）

### 步骤2：答案类型检测
1. 分析查询中的关键词
2. 匹配答案类型模式
3. 计算类型置信度
4. 选择最可能的答案类型

### 步骤3：关键词提取
1. 移除停用词和填充词
2. 提取名词、动词、形容词
3. 保留数字和专有名词
4. 按重要性排序关键词

### 步骤4：后处理
1. 控制关键词数量
2. 格式化输出
3. 计算性能指标
4. 生成最终结果

## 输入输出

### 输入格式
```json
{
  "query": "自然语言查询",
  "config": {
    "max_keywords": 5,
    "language": "zh"
  }
}
```

### 输出格式
```json
{
  "success": true,
  "original_query": "原始查询",
  "compressed_query": "压缩后的关键词",
  "answer_type": "答案类型",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "metrics": {
    "token_saved": "35%",
    "keywords_count": 3,
    "processing_time_ms": 45
  },
  "confidence": 0.85
}
```

### 错误输出
```json
{
  "success": false,
  "error": "错误描述",
  "error_code": "QUERY_TOO_SHORT",
  "original_query": "原始查询",
  "fallback_used": true
}
```

## 算法细节

### 关键词提取算法
1. **基于规则的方法**：使用预定义规则提取关键词
2. **基于统计的方法**：使用TF-IDF等统计方法
3. **基于深度学习的方法**：使用BERT等模型（可选）

### 答案类型检测算法
1. **关键词匹配**：匹配预定义的关键词模式
2. **模式识别**：识别查询的句式结构
3. **机器学习分类**：使用分类模型（可选）

### 停用词处理
- **中文停用词**：的、了、吗、呢、啊等
- **英文停用词**：the, a, an, and, or, but等
- **技术停用词**：请、请问、帮忙、帮助等

## 性能优化

### 缓存策略
- 查询结果缓存
- 配置缓存
- 停用词列表缓存

### 并行处理
- 多查询并行处理
- 流水线优化
- 内存使用优化

### 资源管理
- 内存使用限制
- 处理时间限制
- 错误恢复机制

## 扩展接口

### 自定义停用词列表
```yaml
custom_stopwords:
  zh: ["自定义词1", "自定义词2"]
  en: ["custom1", "custom2"]
```

### 自定义答案类型
```yaml
custom_answer_types:
  - name: "价格查询"
    keywords: ["价格", "多少钱", "售价"]
    priority: 1
```

### 插件系统
```yaml
plugins:
  - name: "同义词扩展"
    class: "SynonymExpander"
    enabled: false
  - name: "实体识别"
    class: "EntityRecognizer"
    enabled: true
```

## 使用示例

### 示例1：中文查询
```json
输入: {
  "query": "Python中如何对列表进行排序"
}

输出: {
  "success": true,
  "original_query": "Python中如何对列表进行排序",
  "compressed_query": "Python 列表 排序",
  "answer_type": "步骤",
  "keywords": ["Python", "列表", "排序"],
  "metrics": {
    "token_saved": "40%",
    "keywords_count": 3,
    "processing_time_ms": 32
  }
}
```

### 示例2：英文查询
```json
输入: {
  "query": "How to install Docker on Ubuntu",
  "config": {
    "language": "en"
  }
}

输出: {
  "success": true,
  "original_query": "How to install Docker on Ubuntu",
  "compressed_query": "install Docker Ubuntu",
  "answer_type": "步骤",
  "keywords": ["install", "Docker", "Ubuntu"],
  "metrics": {
    "token_saved": "45%",
    "keywords_count": 3,
    "processing_time_ms": 28
  }
}
```

## 错误处理

### 常见错误
- `QUERY_TOO_SHORT`：查询过短（少于2个词）
- `LANGUAGE_NOT_SUPPORTED`：不支持的语言
- `NO_KEYWORDS_FOUND`：未找到有效关键词
- `CONFIG_ERROR`：配置错误

### 错误恢复策略
1. 尝试使用默认配置
2. 回退到原始查询
3. 提供部分处理结果
4. 记录错误日志

## 测试用例

### 单元测试
```python
# 测试中文查询压缩
test_query = "什么是人工智能"
expected = {
  "compressed_query": "人工智能",
  "answer_type": "定义"
}

# 测试英文查询压缩  
test_query = "How to create a REST API"
expected = {
  "compressed_query": "create REST API",
  "answer_type": "步骤"
}
```

### 性能测试
- 平均处理时间：<50ms
- 内存使用：<10MB
- 并发处理能力：100 QPS

## 相关模块

- [站点绑定器](../modules/site_binder.md) - 下一阶段处理
- [配置加载器](../modules/config_loader.md) - 配置管理
- [缓存管理器](../modules/cache.md) - 结果缓存

## 版本历史

- v1.0.0 (2025-04-20) - 初始版本
  - 整合现有查询压缩逻辑
  - 添加可配置选项
  - 实现模块化接口