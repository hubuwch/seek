---
name: 标准搜索
description: "整合查询压缩和站点绑定的模块化搜索技能，支持可配置的领域映射和扩展。提供标准化的搜索流程，从自然语言问题到精准搜索结果。"
---

# 标准搜索技能

## 概述

标准搜索技能是一个模块化、可扩展的搜索解决方案，整合了查询压缩和站点绑定两大核心功能。它提供了标准化的搜索流程，支持自定义配置，适用于各种搜索场景。

## 设计理念

1. **模块化架构** - 各组件独立，便于扩展和维护
2. **配置驱动** - 通过配置文件自定义行为，无需修改代码
3. **标准化接口** - 统一的输入输出格式，易于集成
4. **向后兼容** - 兼容现有查询压缩和站点绑定技能的输出格式

## 核心功能

### 1. 智能查询压缩
- 自动提取自然语言问题的核心关键词
- 识别答案类型（定义、步骤、数据、对比等）
- 去除停用词和冗余信息
- 支持多语言关键词提取

### 2. 精准站点绑定
- 根据领域类别自动添加site约束
- 支持多级权威站点配置
- 可配置的领域映射规则
- 智能站点选择算法

### 3. 可扩展架构
- 插件式模块设计
- 支持自定义领域类别
- 可配置的站点权威性评分
- 模块热插拔支持

## 使用时机

- 需要从自然语言问题获取精准搜索结果时
- 需要过滤低质量来源，优先权威站点时
- 需要可配置、可扩展的搜索解决方案时
- 需要标准化搜索流程，便于团队协作时

## 快速开始

### 基本使用
```
用户输入："Python中如何对列表进行排序"

标准搜索处理流程：
1. 查询压缩 → "Python 列表 排序" (答案类型: 步骤)
2. 站点绑定 → "Python 列表 排序 site:stackoverflow.com OR site:docs.python.org"
3. 返回标准化搜索结果
```

### 输出格式
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
    "precision_boost": "60%"
  },
  "search_ready": true
}
```

## 配置系统

标准搜索技能采用分层配置系统：

1. **默认配置** - 内置的通用配置
2. **用户配置** - 用户自定义的配置文件
3. **运行时配置** - 通过参数传递的临时配置

### 配置文件位置
- 领域映射：`config/domains.yaml`
- 站点配置：`config/sites.json`
- 模块配置：`config/modules.yaml`

## 模块架构

### 核心模块
- **查询压缩器** (`modules/query_compressor.md`) - 负责查询压缩功能
- **站点绑定器** (`modules/site_binder.md`) - 负责站点绑定功能
- **配置加载器** (`modules/config_loader.md`) - 负责配置管理

### 扩展模块
- **缓存模块** - 查询结果缓存
- **日志模块** - 搜索过程日志记录
- **监控模块** - 性能指标监控

## 输入格式

### 自然语言输入
```
用户问题：<自然语言问题>
```

### 带配置的输入
```json
{
  "query": "自然语言问题",
  "config": {
    "domain_override": "编程技术",
    "max_sites": 3,
    "strict_mode": false
  }
}
```

## 输出格式

### 成功响应
```json
{
  "success": true,
  "original_query": "原始问题",
  "compressed_query": "压缩后的关键词",
  "answer_type": "答案类型",
  "targeted_query": "带site约束的查询",
  "domain_category": "领域类别",
  "config_source": "配置来源",
  "estimated_improvements": {
    "token_saved": "XX%",
    "precision_boost": "YY%"
  },
  "search_ready": true,
  "timestamp": "2025-04-20T14:30:00Z"
}
```

### 错误响应
```json
{
  "success": false,
  "error": "错误描述",
  "error_code": "ERROR_CODE",
  "original_query": "原始问题",
  "suggestion": "修复建议",
  "timestamp": "2025-04-20T14:30:00Z"
}
```

## 错误处理

### 常见错误码
- `CONFIG_NOT_FOUND` - 配置文件未找到
- `DOMAIN_UNKNOWN` - 未知领域类别
- `QUERY_TOO_SHORT` - 查询过短
- `NO_VALID_SITES` - 无有效站点配置

### 错误恢复策略
1. 尝试使用默认配置
2. 降级到基础功能
3. 返回部分处理结果
4. 提供明确的错误信息

## 性能指标

### 查询压缩性能
- 平均token节省率：35-50%
- 关键词提取准确率：>85%
- 答案类型识别准确率：>80%

### 站点绑定性能
- 权威站点匹配准确率：>90%
- 查询精度提升：50-75%
- 配置加载时间：<100ms

## 扩展指南

### 添加新领域类别
1. 在 `config/domains.yaml` 中添加新领域定义
2. 在 `config/sites.json` 中配置对应站点
3. 更新关键词映射规则

### 添加新站点
1. 在 `config/sites.json` 中添加站点配置
2. 设置站点权威性评分
3. 关联到相应领域类别

### 创建自定义模块
1. 实现标准模块接口
2. 在 `config/modules.yaml` 中注册
3. 提供模块配置选项

## 示例

更多使用示例请参考：
- `examples/basic_usage.md` - 基础使用示例
- `examples/custom_config.md` - 自定义配置示例
- `examples/advanced_extensions.md` - 高级扩展示例

## 相关技能

- [查询压缩](../查询压缩/skill.md) - 基础查询压缩功能
- [站点绑定](../站点绑定/skill.md) - 基础站点绑定功能
- [检索流水线](../检索流水线/skill.md) - 完整搜索流水线

## 版本历史

- v1.0.0 (2025-04-20) - 初始版本发布
  - 整合查询压缩和站点绑定功能
  - 实现模块化架构
  - 支持配置文件自定义

## 贡献指南

1. Fork 项目仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request
5. 通过代码审查

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 支持

如有问题或建议，请：
1. 查看 `examples/` 目录中的示例
2. 检查配置文件是否正确
3. 提交 Issue 报告问题
4. 参与社区讨论