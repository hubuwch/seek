# -*- coding: utf-8 -*-
"""
火山引擎联网搜索API Skill封装脚本
文档来源：https://www.volcengine.com/docs/87772/2272953
"""

import requests
import json
import argparse
import sys
import os

# 设置 UTF-8 编码支持（解决 Windows 命令行中文编码问题）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # 设置标准错误输出编码
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'


def _load_config():
    """从配置文件加载 API Key"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('api_key', '')
    except (FileNotFoundError, json.JSONDecodeError):
        return ''


def web_search(query: str, count: int = 3, time_range: str = None, sites: str = None):
    """
    Web搜索（返回网页列表）
    :param query: 搜索关键词
    :param count: 返回条数（最大3）
    :param time_range: 时间范围（OneDay/OneWeek/OneMonth/OneYear/YYYY-MM-DD..YYYY-MM-DD）
    :param sites: 指定站点（多站点用|分隔）
    """
    if not query or len(query) > 100:
        return {"success": False, "error": "query不能为空且长度≤100字符", "results": []}

    payload = {
        "Query": query,
        "SearchType": "web",
        "Count": min(count, 3),
        "NeedSummary": True,
        "Filter": {
            "NeedContent": False,
            "NeedUrl": True,
            "site": sites.split("|") if sites else []
        }
    }

    if time_range:
        payload["TimeRange"] = time_range

    api_key = _load_config()
    if not api_key:
        return {"success": False, "error": "未配置 API Key，请检查 config.json", "query": query, "results": []}

    try:
        response = requests.post(
            url="https://open.feedcoopapi.com/search_api/web_search",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        # 修复：API返回结构是 Result.WebResults，不是 data.results
        result_data = result.get("Result", {})
        web_results = result_data.get("WebResults", [])

        # 转换为统一输出格式
        return {
            "success": True,
            "query": query,
            "total": len(web_results),
            "results": _normalize_results_webresults(web_results)
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "网络请求超时，请稍后重试", "query": query, "results": []}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "网络连接失败，请检查网络", "query": query, "results": []}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP错误: {e}", "query": query, "results": []}
    except Exception as e:
        return {"success": False, "error": f"请求失败：{str(e)}", "query": query, "results": []}


def _normalize_results(raw_result: dict, sites: str = None) -> list:
    """规范化搜索结果格式（旧接口，兼容使用）"""
    results = []
    raw_items = raw_result.get("data", {}).get("results", [])

    for item in raw_items:
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "abstract": item.get("summary", item.get("abstract", "")),
            "source": _extract_domain(item.get("url", ""))
        })

    return results


def _normalize_results_webresults(web_results: list) -> list:
    """规范化火山引擎API返回的WebResults格式"""
    results = []
    for item in web_results:
        url = item.get("Url", "") or item.get("url", "")
        results.append({
            "title": item.get("Title", "") or item.get("title", ""),
            "url": url,
            "abstract": item.get("Snippet", "") or item.get("snippet", ""),
            "source": _extract_domain(url)
        })

    return results


def _extract_domain(url: str) -> str:
    """从URL中提取域名"""
    if not url:
        return ""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return url.split("/")[2] if "/" in url else url


if __name__ == "__main__":
    # Windows 下修复命令行参数编码问题
    if sys.platform == 'win32':
        import locale
        # 获取系统默认编码
        encoding = locale.getpreferredencoding() or 'utf-8'
        # 修复 argv 中的中文字符编码
        if sys.version_info[0] >= 3:
            # Python 3 下确保使用正确的编码解码命令行参数
            sys.argv = [arg.encode(encoding, errors='replace').decode(encoding, errors='replace') for arg in sys.argv]
    
    parser = argparse.ArgumentParser(description="火山引擎联网搜索CLI工具")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--count", "-c", type=int, default=2, help="返回条数（最大3）")
    parser.add_argument("--sites", "-s", type=str, default=None, help="指定站点（多站点用|分隔）")
    parser.add_argument("--time-range", "-t", type=str, default=None, help="时间范围")

    args = parser.parse_args()

    result = web_search(
        query=args.query,
        count=args.count,
        sites=args.sites,
        time_range=args.time_range
    )

    # 将结果写入文件，确保中文正确保存
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'search_output.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 同时打印到标准输出
    print(json.dumps(result, ensure_ascii=False, indent=2))
