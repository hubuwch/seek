"""
火山引擎联网搜索API Skill封装脚本
文档来源：https://www.volcengine.com/docs/87772/2272953
"""

import requests
import json
import argparse


def web_search(query: str, count: int = 5, time_range: str = None, sites: str = None):
    """
    Web搜索（返回网页列表）
    :param query: 搜索关键词
    :param count: 返回条数（最大5）
    :param time_range: 时间范围（OneDay/OneWeek/OneMonth/OneYear/YYYY-MM-DD..YYYY-MM-DD）
    :param sites: 指定站点（多站点用|分隔）
    """
    if not query or len(query) > 100:
        return {"success": False, "error": "query不能为空且长度≤100字符", "results": []}

    payload = {
        "Query": query,
        "SearchType": "web",
        "Count": min(count, 5),
        "NeedSummary": True,
        "Filter": {
            "NeedContent": False,
            "NeedUrl": True,
            "site": sites.split("|") if sites else []
        }
    }

    if time_range:
        payload["TimeRange"] = time_range

    try:
        response = requests.post(
            url="https://open.feedcoopapi.com/search_api/web_search",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer amR5BlyrW1pE073zvHRKcJQgXayfc4tx"
            },
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        # 转换为统一输出格式
        return {
            "success": True,
            "query": query,
            "total": len(result.get("data", {}).get("results", [])),
            "results": _normalize_results(result, sites)
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
    """规范化搜索结果格式"""
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
    parser = argparse.ArgumentParser(description="火山引擎联网搜索CLI工具")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--count", "-c", type=int, default=2, help="返回条数（最大5）")
    parser.add_argument("--sites", "-s", type=str, default=None, help="指定站点（多站点用|分隔）")
    parser.add_argument("--time-range", "-t", type=str, default=None, help="时间范围")

    args = parser.parse_args()

    result = web_search(
        query=args.query,
        count=args.count,
        sites=args.sites,
        time_range=args.time_range
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
