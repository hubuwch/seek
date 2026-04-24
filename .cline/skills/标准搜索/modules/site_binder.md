# 站点绑定器模块

## 概述

站点绑定器模块是标准搜索技能的核心组件之一，负责为压缩后的查询添加site约束，将搜索范围限制在权威域名内。它整合了现有站点绑定技能的核心逻辑，并提供了更灵活的配置和扩展选项。

## 功能特性

### 1. 智能领域检测
- 自动识别查询所属的领域类别
- 支持多领域交叉匹配
- 基于关键词和答案类型进行领域推断

### 2. 权威站点选择
- 根据领域类别选择最相关的站点
- 考虑站点权威性评分
- 支持多站点组合

### 3. 站点约束生成
- 自动生成site:操作符查询
- 支持OR操作符组合多个站点
- 优化查询语法

### 4. 性能预估
- 预估查询精度提升率
- 计算站点匹配置信度
- 提供优化建议

## 配置选项

### 基本配置
```yaml
use_domain_detection: true   # 是否使用领域检测
max_sites_per_query: 3       # 每个查询最大站点数
min_authority_score: 80      # 最小权威性评分
combine_operator: "OR"       # 站点组合操作符
```

### 站点选择配置
```yaml
include_backup_sites: true   # 是否包含备用站点
prefer_local_sites: true     # 是否优先本地站点
language_preference: ["zh", "en"] # 语言偏好
fallback_to_general: true    # 是否回退到通用站点
```

### 高级配置
```yaml
estimate_precision_boost: true # 是否预估精度提升
enable_site_validation: true  # 是否启用站点验证
cache_site_selection: true    # 是否缓存站点选择结果
dynamic_site_ranking: true    # 是否动态调整站点排名
```

## 处理流程

### 步骤1：领域检测
1. 分析压缩查询的关键词
2. 匹配领域类别关键词
3. 考虑答案类型的影响
4. 计算领域置信度

### 步骤2：站点选择
1. 获取领域对应的站点列表
2. 过滤不符合条件的站点
3. 按权威性评分排序
4. 选择前N个站点

### 步骤3：查询构建
1. 生成site:操作符查询片段
2. 组合多个站点（使用OR）
3. 将站点约束添加到原始查询
4. 优化查询语法

### 步骤4：结果生成
1. 计算性能指标
2. 生成最终输出
3. 记录处理日志
4. 更新缓存

## 输入输出

### 输入格式
```json
{
  "compressed_query": "压缩后的关键词",
  "answer_type": "答案类型",
  "keywords": ["关键词1", "关键词2"],
  "config": {
    "max_sites": 3,
    "prefer_language": "zh"
  }
}
```

### 输出格式
```json
{
  "success": true,
  "original_query": "原始查询",
  "compressed_query": "压缩后的关键词",
  "targeted_query": "带site约束的查询",
  "domain_category": "领域类别",
  "selected_sites": [
    {
      "domain": "stackoverflow.com",
      "name": "Stack Overflow",
      "authority_score": 95,
      "reason": "编程技术领域首选站点"
    }
  ],
  "metrics": {
    "precision_boost": "60%",
    "sites_count": 2,
    "processing_time_ms": 28
  },
  "confidence": 0.88
}
```

### 错误输出
```json
{
  "success": false,
  "error": "错误描述",
  "error_code": "NO_VALID_SITES",
  "original_query": "原始查询",
  "fallback_used": true,
  "fallback_query": "回退查询"
}
```

## 算法细节

### 领域检测算法
1. **关键词匹配**：匹配领域关键词列表
2. **答案类型加权**：根据答案类型调整领域权重
3. **多领域融合**：支持查询属于多个领域
4. **置信度计算**：计算领域检测的置信度

### 站点选择算法
1. **权威性排序**：按权威性评分排序站点
2. **语言偏好**：优先选择偏好语言的站点
3. **地域偏好**：优先选择本地站点
4. **内容类型匹配**：匹配查询的内容类型需求

### 查询构建算法
1. **语法优化**：确保查询语法正确
2. **长度控制**：避免查询过长
3. **操作符优化**：合理使用OR/AND操作符
4. **特殊字符处理**：正确处理特殊字符

## 站点权威性评分

### 评分维度
1. **内容质量** (0-25分)：内容的准确性、完整性
2. **更新频率** (0-20分)：内容的更新及时性
3. **专业性** (0-20分)：领域的专业程度
4. **用户评价** (0-15分)：用户反馈和评价
5. **权威认证** (0-10分)：官方认证和背书
6. **可访问性** (0-10分)：访问速度和稳定性

### 评分等级
- **90-100分**：非常权威（官方文档、政府网站）
- **80-89分**：高度权威（知名技术社区、学术站点）
- **70-79分**：中等权威（专业博客、行业网站）
- **60-69分**：一般权威（普通资讯站点）
- **<60分**：低权威（不建议使用）

## 扩展接口

### 自定义领域映射
```yaml
custom_domains:
  - name: "医疗健康"
    keywords: ["疾病", "症状", "治疗", "医院"]
    sites: ["nih.gov", "who.int"]
    priority: 1
```

### 自定义站点配置
```yaml
custom_sites:
  - domain: "custom-site.com"
    name: "自定义站点"
    authority_score: 85
    domain_categories: ["general"]
    language: "zh"
```

### 插件系统
```yaml
plugins:
  - name: "站点验证器"
    class: "SiteValidator"
    enabled: true
    config:
      check_availability: true
      timeout_seconds: 5
  - name: "站点排名器"
    class: "SiteRanker"
    enabled: false
    config:
      use_machine_learning: false
```

## 使用示例

### 示例1：编程技术查询
```json
输入: {
  "compressed_query": "Python 列表 排序",
  "answer_type": "步骤",
  "keywords": ["Python", "列表", "排序"]
}

输出: {
  "success": true,
  "original_query": "Python中如何对列表进行排序",
  "compressed_query": "Python 列表 排序",
  "targeted_query": "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org",
  "domain_category": "编程技术",
  "selected_sites": [
    {
      "domain": "stackoverflow.com",
      "name": "Stack Overflow",
      "authority_score": 95,
      "reason": "编程问答首选社区"
    },
    {
      "domain": "docs.python.org",
      "name": "Python官方文档",
      "authority_score": 98,
      "reason": "官方文档最权威"
    }
  ],
  "metrics": {
    "precision_boost": "65%",
    "sites_count": 2,
    "processing_time_ms": 35
  }
}
```

### 示例2：政策法规查询
```json
输入: {
  "compressed_query": "数据安全法 主要内容",
  "answer_type": "定义",
  "keywords": ["数据安全法", "主要内容"]
}

输出: {
  "success": true,
  "original_query": "数据安全法的主要内容是什么",
  "compressed_query": "数据安全法 主要内容",
  "targeted_query": "数据安全法 主要内容 site:gov.cn",
  "domain_category": "政策法规",
  "selected_sites": [
    {
      "domain": "gov.cn",
      "name": "中国政府网",
      "authority_score": 99,
      "reason": "政策法规最权威来源"
    }
  ],
  "metrics": {
    "precision_boost": "75%",
    "sites_count": 1,
    "processing_time_ms": 25
  }
}
```

## 错误处理

### 常见错误
- `NO_VALID_SITES`：未找到有效站点
- `DOMAIN_UNKNOWN`：未知领域类别
- `CONFIG_ERROR`：配置错误
- `SITE_VALIDATION_FAILED`：站点验证失败

### 错误恢复策略
1. **降级处理**：使用通用站点
2. **放宽条件**：降低权威性要求
3. **多领域尝试**：尝试相关领域
4. **原始查询**：返回不带site约束的查询

## 性能优化

### 缓存策略
- 站点选择结果缓存
- 领域检测结果缓存
- 站点权威性数据缓存

### 预加载机制
- 配置文件预加载
- 站点数据预加载
- 领域映射预加载

### 异步处理
- 站点验证异步执行
- 数据更新异步执行
- 日志记录异步执行

## 测试用例

### 单元测试
```python
# 测试编程技术领域站点选择
test_input = {
  "compressed_query": "Python 列表 排序",
  "answer_type": "步骤"
}
expected_sites = ["stackoverflow.com", "docs.python.org"]

# 测试政策法规领域站点选择
test_input = {
  "compressed_query": "数据安全法 主要内容",
  "answer_type": "定义"
}
expected_sites = ["gov.cn"]
```

### 性能测试
- 平均处理时间：<40ms
- 内存使用：<15MB
- 并发处理能力：80 QPS
- 缓存命中率：>70%

## 相关模块

- [查询压缩器](../modules/query_compressor.md) - 前一阶段处理
- [配置加载器](../modules/config_loader.md) - 配置管理
- [缓存管理器](../modules/cache.md) - 结果缓存

## 版本历史

- v1.0.0 (2025-04-20) - 初始版本
  - 整合现有站点绑定逻辑
  - 添加可配置选项
  - 实现模块化接口
  - 支持自定义领域和站点