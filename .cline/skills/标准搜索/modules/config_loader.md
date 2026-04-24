# 配置加载器模块

## 概述

配置加载器模块是标准搜索技能的基础组件，负责加载、管理和验证所有配置文件。它提供了统一的配置管理接口，支持热重载、缓存和配置验证功能。

## 功能特性

### 1. 统一配置管理
- 集中管理所有配置文件
- 提供统一的配置访问接口
- 支持配置分层和覆盖

### 2. 热重载支持
- 配置文件修改后自动重载
- 不影响正在进行的处理
- 支持配置版本管理

### 3. 配置验证
- 自动验证配置文件格式
- 检查配置项的有效性
- 提供详细的错误信息

### 4. 缓存优化
- 配置文件缓存加速访问
- 智能缓存失效策略
- 内存使用优化

## 配置选项

### 基本配置
```yaml
config_path: "./config"      # 配置文件路径
cache_configs: true          # 是否缓存配置
cache_ttl_seconds: 300       # 缓存存活时间（秒）
hot_reload: true             # 是否启用热重载
```

### 验证配置
```yaml
validation_strict: false     # 严格验证模式
fallback_to_defaults: true   # 失败时回退到默认配置
log_config_changes: true     # 记录配置变更日志
validate_on_load: true       # 加载时验证配置
```

### 高级配置
```yaml
watch_interval_seconds: 5    # 文件监控间隔（秒）
max_config_size_mb: 10       # 最大配置文件大小（MB）
backup_configs: true         # 是否备份配置
backup_count: 5              # 备份文件数量
```

## 处理流程

### 步骤1：初始化
1. 检查配置文件目录
2. 加载默认配置
3. 初始化缓存系统
4. 启动文件监控（如果启用）

### 步骤2：配置加载
1. 扫描配置文件目录
2. 按优先级加载配置文件
3. 解析配置文件格式（YAML/JSON）
4. 合并配置层次

### 步骤3：配置验证
1. 验证配置文件格式
2. 检查必需配置项
3. 验证配置值有效性
4. 生成验证报告

### 步骤4：配置提供
1. 缓存配置数据
2. 提供配置访问接口
3. 处理配置更新
4. 维护配置状态

## 配置文件结构

### 配置文件目录
```
config/
├── domains.yaml     # 领域映射配置
├── sites.json       # 站点配置
├── modules.yaml     # 模块配置
├── cache.yaml       # 缓存配置（可选）
└── logging.yaml     # 日志配置（可选）
```

### 配置层次结构
1. **默认配置** - 内置的硬编码配置
2. **文件配置** - 配置文件中的配置
3. **环境配置** - 环境变量覆盖
4. **运行时配置** - 程序运行时传入的配置

### 配置合并规则
- 后加载的配置覆盖先加载的配置
- 环境变量优先级最高
- 数组配置可以合并或替换
- 支持配置继承和扩展

## 输入输出

### 输入格式
```json
{
  "action": "get_config",
  "config_name": "domains",
  "options": {
    "force_reload": false,
    "validate": true
  }
}
```

### 输出格式（成功）
```json
{
  "success": true,
  "config_name": "domains",
  "config_data": {
    "domains": {
      "programming": {
        "name": "编程技术",
        "keywords": ["Python", "JavaScript"]
      }
    }
  },
  "metadata": {
    "loaded_from": "file",
    "load_time_ms": 45,
    "cache_hit": true,
    "version": "1.0.0"
  }
}
```

### 输出格式（错误）
```json
{
  "success": false,
  "error": "配置文件格式错误",
  "error_code": "CONFIG_PARSE_ERROR",
  "config_name": "domains",
  "details": {
    "file": "config/domains.yaml",
    "line": 25,
    "message": "无效的YAML语法"
  },
  "fallback_used": true
}
```

## 配置验证

### 验证规则
1. **格式验证** - 检查配置文件格式是否正确
2. **结构验证** - 检查配置结构是否符合预期
3. **值验证** - 检查配置值是否在有效范围内
4. **依赖验证** - 检查配置项之间的依赖关系

### 验证示例
```yaml
# 领域配置验证规则
domains:
  type: object
  required: true
  properties:
    programming:
      type: object
      required: true
      properties:
        name:
          type: string
          required: true
        keywords:
          type: array
          min_items: 1
        enabled:
          type: boolean
          default: true
```

### 验证错误处理
1. **警告** - 非关键错误，继续使用配置
2. **错误** - 关键错误，使用默认配置
3. **致命错误** - 无法恢复，停止加载

## 缓存机制

### 缓存策略
- **内存缓存** - 配置数据内存缓存
- **文件缓存** - 解析后的配置文件缓存
- **查询缓存** - 频繁访问的配置项缓存

### 缓存失效
1. **时间失效** - 基于TTL自动失效
2. **文件变更** - 配置文件修改时失效
3. **手动失效** - 程序主动清除缓存
4. **内存压力** - 内存不足时自动清理

### 缓存配置
```yaml
cache:
  enabled: true
  strategy: "lru"
  max_size_mb: 50
  ttl_seconds: 300
  cleanup_interval_seconds: 60
```

## 热重载机制

### 文件监控
- 监控配置文件目录变化
- 支持文件创建、修改、删除事件
- 防抖处理避免频繁重载

### 重载流程
1. 检测到文件变化
2. 验证新配置文件
3. 合并配置变更
4. 通知相关模块
5. 更新缓存

### 重载配置
```yaml
hot_reload:
  enabled: true
  watch_interval_seconds: 5
  debounce_ms: 1000
  notify_modules: true
  backup_before_reload: true
```

## 扩展接口

### 自定义配置格式
```yaml
custom_formats:
  - name: "toml"
    parser: "toml_parser"
    enabled: false
  - name: "xml"
    parser: "xml_parser"
    enabled: false
```

### 配置转换器
```yaml
transformers:
  - name: "env_var_expander"
    enabled: true
    config:
      prefix: "SEARCH_"
  - name: "template_processor"
    enabled: false
    config:
      variables:
        version: "1.0.0"
```

### 插件系统
```yaml
plugins:
  - name: "配置加密"
    class: "ConfigEncryptor"
    enabled: false
    config:
      algorithm: "aes-256"
  - name: "远程配置"
    class: "RemoteConfigLoader"
    enabled: false
    config:
      endpoint: "https://config.example.com"
```

## 使用示例

### 示例1：获取配置
```json
请求: {
  "action": "get_config",
  "config_name": "sites",
  "options": {
    "force_reload": false
  }
}

响应: {
  "success": true,
  "config_name": "sites",
  "config_data": {
    "sites": {
      "stackoverflow.com": {
        "name": "Stack Overflow",
        "authority_score": 95
      }
    }
  },
  "metadata": {
    "loaded_from": "cache",
    "load_time_ms": 12,
    "cache_hit": true
  }
}
```

### 示例2：更新配置
```json
请求: {
  "action": "update_config",
  "config_name": "domains",
  "config_data": {
    "new_domain": {
      "name": "医疗健康",
      "keywords": ["疾病", "治疗"]
    }
  },
  "options": {
    "persist": true
  }
}

响应: {
  "success": true,
  "config_name": "domains",
  "action": "updated",
  "changes": {
    "added": ["new_domain"],
    "modified": [],
    "removed": []
  },
  "metadata": {
    "persisted": true,
    "backup_created": true
  }
}
```

## 错误处理

### 常见错误
- `CONFIG_NOT_FOUND` - 配置文件未找到
- `CONFIG_PARSE_ERROR` - 配置文件解析错误
- `CONFIG_VALIDATION_ERROR` - 配置验证失败
- `CONFIG_PERMISSION_ERROR` - 配置文件权限错误
- `CACHE_ERROR` - 缓存操作错误

### 错误恢复策略
1. **使用默认配置** - 加载失败时使用内置默认配置
2. **使用缓存配置** - 使用缓存的旧版本配置
3. **部分加载** - 加载有效的配置部分
4. **降级模式** - 使用最小功能集配置

## 性能优化

### 加载优化
- 并行加载多个配置文件
- 延迟加载不常用的配置
- 配置文件预解析

### 缓存优化
- 分层缓存策略
- 智能缓存预加载
- 缓存压缩

### 内存优化
- 配置数据共享
- 内存使用监控
- 自动垃圾回收

## 测试用例

### 单元测试
```python
# 测试配置加载
test_config = {
  "action": "get_config",
  "config_name": "domains"
}
expected_keys = ["programming", "policy"]

# 测试配置验证
invalid_config = "invalid: yaml: syntax"
expected_error = "CONFIG_PARSE_ERROR"
```

### 性能测试
- 配置加载时间：<100ms（冷启动）
- 配置访问时间：<5ms（缓存命中）
- 内存使用：<20MB（100个配置文件）
- 并发访问：200 QPS

## 相关模块

- [查询压缩器](../modules/query_compressor.md) - 使用配置的模块
- [站点绑定器](../modules/site_binder.md) - 使用配置的模块
- [缓存管理器](../modules/cache.md) - 缓存协作模块

## 版本历史

- v1.0.0 (2025-04-20) - 初始版本
  - 统一配置管理接口
  - 支持热重载和缓存
  - 实现配置验证
  - 提供扩展接口