# 基础使用示例

## 概述

本文档提供标准搜索技能的基础使用示例，展示如何从自然语言查询获取精准搜索结果。

## 快速开始

### 示例1：编程技术查询

**用户输入：** "Python中如何对列表进行排序"

**处理流程：**

1. **查询压缩**
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

2. **站点绑定**
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

3. **最终结果**
   ```json
   {
     "success": true,
     "original_query": "Python中如何对列表进行排序",
     "compressed_query": "Python 列表 排序",
     "answer_type": "步骤",
     "targeted_query": "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org",
     "domain_category": "编程技术",
     "config_source": "默认配置",
     "estimated_improvements": {
       "token_saved": "40%",
       "precision_boost": "65%"
     },
     "search_ready": true,
     "timestamp": "2025-04-20T14:30:00Z"
   }
   ```

### 示例2：政策法规查询

**用户输入：** "数据安全法的主要内容是什么"

**处理流程：**

1. **查询压缩**
   ```json
   输出: {
     "success": true,
     "original_query": "数据安全法的主要内容是什么",
     "compressed_query": "数据安全法 主要内容",
     "answer_type": "定义",
     "keywords": ["数据安全法", "主要内容"],
     "metrics": {
       "token_saved": "35%",
       "keywords_count": 2,
       "processing_time_ms": 28
     }
   }
   ```

2. **站点绑定**
   ```json
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

3. **最终结果**
   ```json
   {
     "success": true,
     "original_query": "数据安全法的主要内容是什么",
     "compressed_query": "数据安全法 主要内容",
     "answer_type": "定义",
     "targeted_query": "数据安全法 主要内容 site:gov.cn",
     "domain_category": "政策法规",
     "config_source": "默认配置",
     "estimated_improvements": {
       "token_saved": "35%",
       "precision_boost": "75%"
     },
     "search_ready": true,
     "timestamp": "2025-04-20T14:32:00Z"
   }
   ```

## 完整工作流程

### 步骤1：初始化配置
```python
# 初始化标准搜索技能
from standard_search import StandardSearch

search = StandardSearch(
    config_path="./config",
    cache_enabled=True,
    hot_reload=True
)

# 等待配置加载完成
search.initialize()
```

### 步骤2：处理查询
```python
# 处理自然语言查询
query = "Ubuntu系统如何安装Docker"
result = search.process(query)

print(f"原始查询: {result['original_query']}")
print(f"压缩查询: {result['compressed_query']}")
print(f"目标查询: {result['targeted_query']}")
print(f"领域类别: {result['domain_category']}")
print(f"答案类型: {result['answer_type']}")
```

### 步骤3：执行搜索
```python
# 使用目标查询执行搜索
if result['search_ready']:
    search_results = search.execute_search(result['targeted_query'])
    
    print(f"找到 {len(search_results)} 个结果:")
    for i, item in enumerate(search_results[:3], 1):
        print(f"{i}. {item['title']}")
        print(f"   来源: {item['source']}")
        print(f"   摘要: {item['abstract'][:100]}...")
```

### 步骤4：处理结果
```python
# 分析搜索结果
analysis = search.analyze_results(search_results, result)

print(f"搜索结果分析:")
print(f"- 平均相关性: {analysis['avg_relevance']:.2f}")
print(f"- 权威站点占比: {analysis['authority_ratio']:.1%}")
print(f"- 建议操作: {analysis['suggested_action']}")
```

## 配置检查

### 检查当前配置
```python
# 获取当前配置状态
config_status = search.get_config_status()

print("配置状态:")
print(f"- 领域配置: {config_status['domains']['status']}")
print(f"- 站点配置: {config_status['sites']['status']}")
print(f"- 模块配置: {config_status['modules']['status']}")
print(f"- 缓存状态: {config_status['cache']['hit_rate']:.1%} 命中率")
```

### 验证配置
```python
# 验证配置文件
validation_report = search.validate_configs()

if validation_report['valid']:
    print("所有配置文件验证通过")
else:
    print("配置验证发现问题:")
    for error in validation_report['errors']:
        print(f"- {error['config']}: {error['message']}")
```

## 错误处理示例

### 示例1：查询过短
```python
query = "Python"
try:
    result = search.process(query)
except QueryTooShortError as e:
    print(f"错误: {e.message}")
    print(f"建议: 请提供更详细的问题描述")
    
    # 使用原始查询继续
    result = {
        'original_query': query,
        'compressed_query': query,
        'targeted_query': query,
        'search_ready': True,
        'warning': '查询过短，未进行优化'
    }
```

### 示例2：未知领域
```python
query = "外星人是否存在"
try:
    result = search.process(query)
except UnknownDomainError as e:
    print(f"错误: 无法识别查询领域")
    print(f"使用的领域: {e.fallback_domain}")
    
    # 使用通用领域继续
    result = search.process_with_domain(query, 'general')
```

### 示例3：配置错误
```python
try:
    search = StandardSearch(config_path="./invalid_config")
    search.initialize()
except ConfigError as e:
    print(f"配置错误: {e.message}")
    print(f"使用默认配置继续...")
    
    # 使用默认配置
    search = StandardSearch(use_default_config=True)
    search.initialize()
```

## 性能监控

### 监控搜索性能
```python
# 获取性能指标
metrics = search.get_performance_metrics()

print("性能指标:")
print(f"- 平均查询处理时间: {metrics['avg_processing_time_ms']}ms")
print(f"- 平均token节省率: {metrics['avg_token_saved']:.1%}")
print(f"- 平均精度提升率: {metrics['avg_precision_boost']:.1%}")
print(f"- 缓存命中率: {metrics['cache_hit_rate']:.1%}")
print(f"- 错误率: {metrics['error_rate']:.2%}")
```

### 性能优化建议
```python
# 获取优化建议
suggestions = search.get_optimization_suggestions()

if suggestions:
    print("优化建议:")
    for suggestion in suggestions:
        print(f"- {suggestion['description']}")
        print(f"  预计提升: {suggestion['estimated_improvement']}")
        print(f"  实施难度: {suggestion['difficulty']}")
```

## 批量处理示例

### 批量查询处理
```python
queries = [
    "Python列表排序方法",
    "Docker安装教程",
    "数据安全法解读",
    "机器学习入门指南"
]

results = []
for query in queries:
    try:
        result = search.process(query)
        results.append(result)
        print(f"✓ 处理完成: {query}")
    except Exception as e:
        print(f"✗ 处理失败: {query} - {str(e)}")
        results.append({
            'original_query': query,
            'error': str(e),
            'search_ready': False
        })

# 统计处理结果
success_count = sum(1 for r in results if r.get('search_ready', False))
print(f"\n批量处理完成: {success_count}/{len(queries)} 成功")
```

### 批量搜索执行
```python
# 执行批量搜索
search_tasks = []
for result in results:
    if result.get('search_ready', False):
        search_tasks.append({
            'query': result['targeted_query'],
            'domain': result['domain_category'],
            'max_results': 5
        })

# 并行执行搜索
search_results = search.execute_batch_search(search_tasks, parallel=True)

print(f"批量搜索完成，获取 {len(search_results)} 组结果")
```

## 集成示例

### 与现有系统集成
```python
class MySearchSystem:
    def __init__(self):
        self.standard_search = StandardSearch()
        self.standard_search.initialize()
    
    def search(self, user_query, options=None):
        # 使用标准搜索处理查询
        processed = self.standard_search.process(user_query)
        
        if not processed['search_ready']:
            return self.fallback_search(user_query)
        
        # 执行搜索
        results = self.standard_search.execute_search(
            processed['targeted_query'],
            max_results=options.get('max_results', 10) if options else 10
        )
        
        # 格式化结果
        formatted = self.format_results(results, processed)
        
        return {
            'query': user_query,
            'processed_query': processed,
            'results': formatted,
            'metadata': {
                'domain': processed['domain_category'],
                'answer_type': processed['answer_type'],
                'estimated_improvements': processed['estimated_improvements']
            }
        }
    
    def fallback_search(self, query):
        # 回退搜索逻辑
        pass
    
    def format_results(self, results, processed):
        # 格式化搜索结果
        formatted = []
        for result in results:
            formatted.append({
                'title': result['title'],
                'url': result['url'],
                'summary': result['abstract'],
                'source': result.get('source', 'unknown'),
                'relevance_score': self.calculate_relevance(result, processed)
            })
        return formatted
    
    def calculate_relevance(self, result, processed):
        # 计算相关性分数
        return 0.85  # 示例值
```

## 最佳实践

### 1. 配置管理
- 定期备份配置文件
- 使用版本控制管理配置变更
- 在生产环境前测试配置更改

### 2. 错误处理
- 始终检查`success`字段
- 实现适当的回退机制
- 记录错误日志以便调试

### 3. 性能优化
- 启用缓存以提高性能
- 监控关键性能指标
- 定期清理缓存和日志

### 4. 安全考虑
- 不要暴露敏感配置信息
- 验证用户输入以防止注入攻击
- 限制API访问频率

## 下一步

- 查看 [自定义配置示例](./custom_config.md) 了解如何定制配置
- 查看 [高级扩展示例](./advanced_extensions.md) 了解扩展功能
- 参考 [API文档](../skill.md) 获取完整API参考