# 自定义配置示例

## 概述

本文档展示如何自定义标准搜索技能的配置，包括添加新领域类别、配置新站点、调整模块参数等。

## 配置文件结构

### 默认配置文件位置
```
.cline/skills/标准搜索/config/
├── domains.yaml     # 领域映射配置
├── sites.json       # 站点配置
├── modules.yaml     # 模块配置
└── (可选) custom/   # 自定义配置目录
```

## 添加新领域类别

### 示例：添加"医疗健康"领域

**修改 `config/domains.yaml`：**

```yaml
# 在domains部分添加新领域
domains:
  # ... 现有领域配置 ...
  
  # 新增医疗健康领域
  healthcare:
    name: "医疗健康"
    description: "疾病、症状、治疗、药物等医疗健康信息"
    keywords:
      - "疾病"
      - "症状"
      - "治疗"
      - "药物"
      - "医院"
      - "医生"
      - "健康"
      - "医疗"
      - "诊断"
      - "预防"
    answer_types:
      - "定义"
      - "步骤"
      - "列举"
    priority: 7
    enabled: true
```

### 验证新领域配置
```python
from standard_search import StandardSearch

search = StandardSearch(config_path="./config")
search.initialize()

# 检查新领域是否加载成功
config = search.get_config('domains')
if 'healthcare' in config['domains']:
    print("✓ 医疗健康领域加载成功")
    print(f"  名称: {config['domains']['healthcare']['name']}")
    print(f"  关键词数量: {len(config['domains']['healthcare']['keywords'])}")
```

## 配置新站点

### 示例：为医疗健康领域添加权威站点

**修改 `config/sites.json`：**

```json
{
  "sites": {
    // ... 现有站点配置 ...
    
    // 新增医疗健康站点
    "nih.gov": {
      "name": "美国国立卫生研究院",
      "description": "美国国立卫生研究院官方网站",
      "domain_categories": ["healthcare"],
      "authority_score": 97,
      "language": "en",
      "region": "us",
      "content_type": "Official",
      "trust_level": "very_high",
      "enabled": true,
      "priority": 1,
      "max_results": 5,
      "site_operator": "site:nih.gov"
    },
    
    "who.int": {
      "name": "世界卫生组织",
      "description": "世界卫生组织官方网站",
      "domain_categories": ["healthcare"],
      "authority_score": 98,
      "language": ["en", "zh"],
      "region": "global",
      "content_type": "Official",
      "trust_level": "very_high",
      "enabled": true,
      "priority": 1,
      "max_results": 5,
      "site_operator": "site:who.int"
    },
    
    "cdc.gov": {
      "name": "美国疾病控制与预防中心",
      "description": "CDC官方网站",
      "domain_categories": ["healthcare"],
      "authority_score": 96,
      "language": "en",
      "region": "us",
      "content_type": "Official",
      "trust_level": "very_high",
      "enabled": true,
      "priority": 2,
      "max_results": 3,
      "site_operator": "site:cdc.gov"
    }
  },
  
  "domain_mappings": {
    // ... 现有映射 ...
    "healthcare": ["nih.gov", "who.int", "cdc.gov"]
  }
}
```

### 测试新站点配置
```python
# 测试医疗健康查询
query = "糖尿病有哪些症状"
result = search.process(query)

print(f"查询: {query}")
print(f"领域类别: {result['domain_category']}")
print(f"目标查询: {result['targeted_query']}")

# 检查是否使用了新配置的站点
if 'nih.gov' in result['targeted_query'] or 'who.int' in result['targeted_query']:
    print("✓ 成功使用医疗健康领域站点")
```

## 自定义模块配置

### 示例：调整查询压缩器参数

**修改 `config/modules.yaml`：**

```yaml
modules:
  query_compressor:
    # ... 现有配置 ...
    config:
      max_keywords: 10          # 增加最大关键词数量
      min_keywords: 1           # 降低最小关键词数量
      remove_stopwords: true
      detect_answer_type: true
      answer_types:
        - "定义"
        - "步骤"
        - "数据"
        - "对比"
        - "故障排查"
        - "列举"
        - "价格"               # 添加自定义答案类型
      language: "auto"
      token_saving_goal: 30     # 降低token节省目标
      fallback_to_original: true
      enable_synonym_expansion: true  # 启用同义词扩展
      preserve_numbers: true
      preserve_technical_terms: true
      custom_stopwords:         # 添加自定义停用词
        zh: ["请问", "帮忙", "帮助", "一下"]
        en: ["please", "help", "thanks"]
```

### 示例：调整站点绑定器参数

```yaml
modules:
  site_binder:
    # ... 现有配置 ...
    config:
      use_domain_detection: true
      max_sites_per_query: 5    # 增加最大站点数
      min_authority_score: 70   # 降低权威性要求
      combine_operator: "OR"
      include_backup_sites: true
      prefer_local_sites: true
      language_preference: ["zh", "en", "ja"]  # 添加日语偏好
      fallback_to_general: true
      estimate_precision_boost: true
      enable_site_validation: false  # 禁用站点验证（提高性能）
      cache_site_selection: true
      dynamic_site_ranking: true
      custom_domains:           # 添加自定义领域映射
        - name: "电商购物"
          keywords: ["价格", "购买", "商品", "优惠"]
          sites: ["amazon.com", "taobao.com"]
          priority: 1
```

## 高级配置示例

### 1. 多语言支持配置

**创建 `config/languages.yaml`：**

```yaml
# 多语言配置
languages:
  zh:
    name: "中文"
    stopwords:
      - "的"
      - "了"
      - "吗"
      - "呢"
      - "啊"
      - "请问"
      - "帮忙"
    tokenizer: "jieba"  # 使用结巴分词
    enabled: true
    
  en:
    name: "English"
    stopwords:
      - "the"
      - "a"
      - "an"
      - "and"
      - "or"
      - "but"
      - "please"
      - "help"
    tokenizer: "nltk"   # 使用NLTK分词
    enabled: true
    
  ja:
    name: "日本語"
    stopwords:
      - "です"
      - "ます"
      - "の"
      - "は"
      - "が"
    tokenizer: "mecab"  # 使用MeCab分词
    enabled: false      # 暂时禁用
    
# 语言检测配置
detection:
  default_language: "zh"
  fallback_language: "en"
  confidence_threshold: 0.6
  enable_auto_detection: true
```

### 2. 缓存配置优化

**创建 `config/cache.yaml`：**

```yaml
# 缓存配置
cache:
  enabled: true
  strategy: "lru"
  
  # 内存缓存配置
  memory:
    max_size_mb: 100
    ttl_seconds: 3600
    cleanup_interval_seconds: 300
    
  # 查询缓存配置
  query:
    enabled: true
    max_entries: 1000
    ttl_seconds: 1800
    
  # 结果缓存配置
  results:
    enabled: true
    max_entries: 500
    ttl_seconds: 900
    
  # 配置缓存配置
  config:
    enabled: true
    ttl_seconds: 600
    
  # 磁盘缓存配置（可选）
  disk:
    enabled: false
    path: "./cache"
    max_size_mb: 1024
    compression: true
```

### 3. 性能监控配置

**创建 `config/monitoring.yaml`：**

```yaml
# 性能监控配置
monitoring:
  enabled: true
  
  # 指标收集
  metrics:
    collection_interval_seconds: 60
    retention_days: 30
    
    # 查询处理指标
    query_processing:
      enabled: true
      include_details: true
      
    # 站点选择指标
    site_selection:
      enabled: true
      include_details: false
      
    # 缓存性能指标
    cache_performance:
      enabled: true
      include_details: true
      
  # 告警配置
  alerts:
    enabled: true
    channels:
      - type: "log"
        level: "error"
      - type: "email"
        enabled: false
        recipients: ["admin@example.com"]
        
    thresholds:
      error_rate_percent: 5.0
      avg_response_time_ms: 1000
      cache_hit_rate: 60.0
      
  # 报告配置
  reporting:
    daily_report: true
    weekly_report: true
    monthly_report: true
```

## 配置继承和覆盖

### 使用配置继承

**创建 `config/custom/domains_override.yaml`：**

```yaml
# 自定义领域配置（继承并覆盖默认配置）
extends: "../domains.yaml"

# 覆盖编程技术领域配置
domains:
  programming:
    # 继承原有配置，只修改部分字段
    keywords:
      - "Python"
      - "JavaScript"
      - "Java"
      - "C++"
      - "Go"          # 新增
      - "Rust"        # 新增
      - "Docker"
      - "Kubernetes"
      - "云原生"       # 新增中文关键词
    priority: 1       # 提高优先级
    
  # 添加新领域（不修改原有领域）
  ai_ml:
    name: "人工智能与机器学习"
    description: "人工智能、机器学习、深度学习相关技术"
    keywords:
      - "AI"
      - "人工智能"
      - "机器学习"
      - "深度学习"
      - "神经网络"
      - "大模型"
      - "Transformer"
      - "LLM"
    answer_types:
      - "定义"
      - "步骤"
      - "对比"
    priority: 2
    enabled: true
```

### 配置加载顺序
```python
from standard_search import StandardSearch

# 指定多个配置目录，后面的覆盖前面的
search = StandardSearch(
    config_path=["./config", "./config/custom", "./config/local"],
    merge_strategy="deep_merge"  # 深度合并配置
)
```

## 环境特定配置

### 开发环境配置
**创建 `config/env/development.yaml`：**

```yaml
# 开发环境配置
environment: "development"

modules:
  query_compressor:
    config:
      debug: true
      log_level: "debug"
      
  site_binder:
    config:
      debug: true
      enable_site_validation: false  # 开发环境禁用站点验证
      
cache:
  enabled: false  # 开发环境禁用缓存
  
logging:
  level: "debug"
  to_file: true
  file_path: "./logs/development.log"
```

### 生产环境配置
**创建 `config/env/production.yaml`：**

```yaml
# 生产环境配置
environment: "production"

modules:
  query_compressor:
    config:
      debug: false
      log_level: "info"
      
  site_binder:
    config:
      debug: false
      enable_site_validation: true  # 生产环境启用站点验证
      
cache:
  enabled: true
  memory:
    max_size_mb: 500
    
logging:
  level: "info"
  to_file: true
  file_path: "/var/log/standard_search.log"
  max_file_size_mb: 100
  backup_count: 10
  
security:
  rate_limit:
    enabled: true
    requests_per_minute: 100
    burst_size: 20
```

## 动态配置更新

### 通过API更新配置
```python
# 动态更新配置示例
from standard_search import StandardSearch

search = StandardSearch()
search.initialize()

# 添加新站点
new_site = {
    "custom-site.com": {
        "name": "自定义技术博客",
        "description": "个人技术博客",
        "domain_categories": ["programming"],
        "authority_score": 75,
        "language": "zh",
        "region": "cn",
        "content_type": "Blog",
        "trust_level": "medium",
        "enabled": true,
        "priority": 3,
        "max_results": 2,
        "site_operator": "site:custom-site.com"
    }
}

# 更新配置
update_result = search.update_config(
    config_name="sites",
    config_data=new_site,
    options={
        "persist": True,      # 持久化到文件
        "backup": True,       # 创建备份
        "notify": True        # 通知相关模块
    }
)

if update_result['success']:
    print("配置更新成功")
    print(f"变更: {update_result['changes']}")
    
    # 立即生效（热重载）
    search.reload_config("sites")
```

### 配置版本管理
```python
# 配置版本管理示例
config_history = search.get_config_history("sites")

print("配置版本历史:")
for version in config_history[:5]:  # 显示最近5个版本
    print(f"版本 {version['version']}:")
    print(f"  时间: {version['timestamp']}")
    print(f"  变更: {version['changes']}")
    print(f"  作者: {version['author']}")

# 回滚到特定版本
rollback_result = search.rollback_config("sites", version="20250420_143000")
if rollback_result['success']:
    print(f"已回滚到版本 {rollback_result['rolled_back_to']}")
```

## 配置验证和测试

### 配置验证脚本
```python
#!/usr/bin/env python3
# config_validator.py

import yaml
import json
import sys
from pathlib import Path

def validate_domains_config(config_path):
    """验证领域配置"""
    with open(config_path / "domains.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    errors = []
    
    # 检查必需字段
    required_fields = ['name', 'keywords', 'answer_types', 'priority', 'enabled']
    for domain_id, domain_config in config.get('domains', {}).items():
        for field in required_fields:
            if field not in domain_config:
                errors.append(f"领域 '{domain_id}' 缺少必需字段 '{field}'")
    
    # 检查关键词数量
    for domain_id, domain_config in config.get('domains', {}).items():
        keywords = domain_config.get('keywords', [])
        if len(keywords) < 3:
            errors.append(f"领域 '{domain_id}' 关键词数量不足（至少需要3个）")
    
    return errors

def validate_sites_config(config_path):
    """验证站点配置"""
    with open(config_path / "sites.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    errors = []
    
    # 检查站点配置
    for site_domain, site_config in config.get('sites', {}).items():
        # 检查权威性评分范围
        score = site_config.get('authority_score', 0)
        if not 0 <= score <= 100:
            errors.append(f"站点 '{site_domain}' 权威性评分超出范围: {score}")
    
    return errors

def main():
    config_path = Path("./config")
    
    print("开始验证配置文件...")
    
    # 验证各个配置文件
    domains_errors = validate_domains_config(config_path)
    sites_errors = validate_sites_config(config_path)
    
    all_errors = domains_errors + sites_errors
    
    if not all_errors:
        print("✓ 所有配置文件验证通过")
        return 0
    else:
        print("✗ 发现配置错误:")
        for error in all_errors:
            print(f"  - {error}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 配置测试用例
```python
# test_configurations.py
import unittest
from standard_search import StandardSearch

class TestConfigurations(unittest.TestCase):
    def setUp(self):
        self.search = StandardSearch(config_path="./config")
        self.search.initialize()
    
    def test_domains_config(self):
        """测试领域配置"""
        config = self.search.get_config('domains')
        
        # 检查必需领域是否存在
        self.assertIn('programming', config['domains'])
        self.assertIn('policy', config['domains'])
        self.assertIn('general', config['domains'])
        
        # 检查领域配置完整性
        for domain_id, domain_config in config['domains'].items():
            self.assertIn('name', domain_config)
            self.assertIn('keywords', domain_config)
            self.assertIn('enabled', domain_config)
            self.assertIsInstance(domain_config['enabled'], bool)
    
    def test_sites_config(self):
        """测试站点配置"""
        config = self.search.get_config('sites