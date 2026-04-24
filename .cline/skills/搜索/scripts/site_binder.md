# 站点绑定工具

## 目的
通过自动添加 `site:` 操作符将搜索范围限制在可信域名内，避免用户手动筛选新闻聚合站或垃圾博客等低质量来源。

## 指令

### 第一步：检测领域类别
分析压缩后的查询和答案类型，确定合适的领域类别：

**政策法规**
- 关键词：数据出境、安全评估、AI法案、法规、办法、条例
- 答案类型：定义、列举
- 站点：`gov.cn`、`europa.eu`

**编程技术**
- 关键词：Python、JavaScript、Docker、Nginx、API、代码
- 答案类型：步骤、故障排查
- 站点：`stackoverflow.com`、`docs.python.org`、`developer.mozilla.org`

**学术文献**
- 关键词：Transformer、LLM、幻觉检测、论文、综述
- 答案类型：定义、对比
- 站点：`arxiv.org`、`aclweb.org`

**行业数据**
- 关键词：销量、市场份额、半导体、新能源、数据
- 答案类型：数据、对比
- 站点：`gov.cn`、`stats.gov.cn`

### 第二步：应用站点约束
约束后格式如下：
```json
{
  "targeted_query": "<关键词> site:<域名>",
  "sites": ["<域名>"],
  "domain_category": "<类别>",
  "estimated_precision_boost": "XX%"
}
```

如果有多个域名：将所有域名添加到 `sites` 数组中。
如果只有一个最佳域名：只使用该域名

### 第三步：输出
返回绑定结果（JSON格式）

## 领域映射表

| 类别 | 主站点 | 次站点 |
|------|--------|--------|
| 政策法规（国内） | site:gov.cn | site:pkulaw.com |
| 政策法规（欧盟） | site:europa.eu | - |
| 编程技术 | site:stackoverflow.com | site:docs.python.org |
| 学术文献(国外) | site:arxiv.org | site:aclweb.org |
| 学术文献(国内) | site:ncpssd.cn | site:pubscholar.cn |site:nstl.gov.cn|
| 行业数据 | site:gov.cn | site:marklines.com |
| 通用百科 | site:wikipedia.org | site:baike.baidu.com |
| Linux/服务器 | site:wiki.archlinux.org | site:nginx.org |

## 输出格式
```json
{
  "targeted_query": "<关键词>",
  "sites": ["<域名>"],
  "domain_category": "<类别>",
  "estimated_precision_boost": "XX%"
}
```