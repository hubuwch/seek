#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度千帆平台搜索API调用脚本

使用方法:
    python baidu_search_api.py --query "搜索关键词" [--num 10]

环境变量:
    QIANFAN_ACCESS_KEY: 百度千帆平台的Access Key
    QIANFAN_SECRET_KEY: 百度千帆平台的Secret Key
"""

import os
import sys
import json
import argparse
import requests
import hashlib
import hmac
import base64
from datetime import datetime, timezone
from urllib.parse import quote, urlparse
from typing import List, Dict, Optional


class QianfanSearchAPI:
    """百度千帆平台搜索API客户端"""
    
    BASE_URL = "https://qianfan.baidubce.com"
    SEARCH_ENDPOINT = "/v2/search"
    
    def __init__(self, access_key: Optional[str] = None, secret_key: Optional[str] = None):
        """
        初始化搜索API客户端
        
        Args:
            access_key: 百度千帆平台Access Key，默认从环境变量读取
            secret_key: 百度千帆平台Secret Key，默认从环境变量读取
        """
        self.access_key = access_key or os.getenv("QIANFAN_ACCESS_KEY")
        self.secret_key = secret_key or os.getenv("QIANFAN_SECRET_KEY")
        
        if not self.access_key or not self.secret_key:
            raise ValueError(
                "Missing API credentials. Please set QIANFAN_ACCESS_KEY and QIANFAN_SECRET_KEY "
                "environment variables or pass them as arguments."
            )
    
    def _get_timestamp(self) -> str:
        """生成ISO 8601格式的时间戳"""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def _sign_request(self, method: str, path: str, timestamp: str, body: str = "") -> str:
        """
        使用AK/SK方式签名请求
        
        Args:
            method: HTTP方法
            path: API路径
            timestamp: 时间戳
            body: 请求体
        
        Returns:
            签名字符串
        """
        # 构建签名字符串
        string_to_sign = f"{method}\n{path}\n\n{body}\n{timestamp}"
        
        # 使用HMAC-SHA256签名
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256
        ).digest()
        
        # Base64编码
        return base64.b64encode(signature).decode("utf-8")
    
    def search(self, query: str, num_results: int = 10, **kwargs) -> Dict:
        """
        执行搜索请求
        
        Args:
            query: 搜索关键词（已绑定站点约束）
            num_results: 返回结果数量，默认10
            **kwargs: 其他搜索参数
        
        Returns:
            包含搜索结果的JSON对象
        """
        timestamp = self._get_timestamp()
        path = self.SEARCH_ENDPOINT
        
        # 构建请求体
        payload = {
            "query": query,
            "num": min(num_results, 20),  # 最多20条
            **kwargs
        }
        body = json.dumps(payload, ensure_ascii=False)
        
        # 生成签名
        signature = self._sign_request("POST", path, timestamp, body)
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bce-auth-v1/{self.access_key}/{timestamp}/{signature}",
            "x-bce-date": timestamp
        }
        
        # 发送请求
        url = f"{self.BASE_URL}{path}"
        try:
            response = requests.post(
                url,
                headers=headers,
                data=body.encode("utf-8"),
                timeout=30
            )
            response.raise_for_status()
            return self._parse_response(response.json(), query)
            
        except requests.exceptions.Timeout:
            return self._error_response(query, "请求超时，请稍后重试")
        except requests.exceptions.ConnectionError:
            return self._error_response(query, "网络连接错误，请检查网络")
        except requests.exceptions.HTTPError as e:
            return self._error_response(query, f"HTTP错误: {e.response.status_code}")
        except Exception as e:
            return self._error_response(query, f"未知错误: {str(e)}")
    
    def _parse_response(self, api_response: Dict, query: str) -> Dict:
        """
        解析API响应并统一输出格式
        
        Args:
            api_response: 百度API原始响应
            query: 原始查询
        
        Returns:
            统一格式的搜索结果
        """
        results = []
        
        # 解析百度API返回的结果
        if "results" in api_response:
            for item in api_response["results"]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "abstract": item.get("abstract", ""),
                    "source": item.get("site", "unknown")
                })
        
        return {
            "success": True,
            "query": query,
            "total": len(results),
            "results": results,
            "raw_response": api_response  # 保留原始响应用于调试
        }
    
    def _error_response(self, query: str, error_msg: str) -> Dict:
        """生成错误响应"""
        return {
            "success": False,
            "query": query,
            "error": error_msg,
            "results": [],
            "total": 0
        }


def parse_site_constraint(query: str) -> tuple:
    """
    解析查询中的site约束，提取域名信息
    
    Args:
        query: 带有site约束的查询字符串
    
    Returns:
        (clean_query, domain_category) 元组
    """
    # 简单的域名映射
    domain_mapping = {
        "gov.cn": "政策法规",
        "stackoverflow.com": "编程技术",
        "docs.python.org": "编程技术",
        "developer.mozilla.org": "编程技术",
        "arxiv.org": "学术文献",
        "aclweb.org": "学术文献",
        "wikipedia.org": "通用百科",
        "baike.baidu.com": "通用百科",
    }
    
    # 提取site约束
    import re
    site_matches = re.findall(r'site:(\S+)', query)
    
    # 确定领域类别
    category = "通用"
    for site in site_matches:
        for domain, cat in domain_mapping.items():
            if domain in site:
                category = cat
                break
    
    return category


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="百度千帆平台搜索API调用脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
    QIANFAN_ACCESS_KEY    百度千帆平台Access Key
    QIANFAN_SECRET_KEY    百度千帆平台Secret Key

示例:
    python search_api.py --query "Python 教程 site:docs.python.org"
    python search_api.py --query "数据安全法 site:gov.cn" --num 5
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        required=True,
        help="搜索关键词（建议已绑定site约束）"
    )
    
    parser.add_argument(
        "--num", "-n",
        type=int,
        default=10,
        help="返回结果数量（默认10，最多20）"
    )
    
    parser.add_argument(
        "--access-key",
        help="百度千帆Access Key（默认从环境变量读取）"
    )
    
    parser.add_argument(
        "--secret-key",
        help="百度千帆Secret Key（默认从环境变量读取）"
    )
    
    args = parser.parse_args()
    
    # 初始化API客户端
    try:
        client = QianfanSearchAPI(
            access_key=args.access_key,
            secret_key=args.secret_key
        )
    except ValueError as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "query": args.query,
            "results": []
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 执行搜索
    result = client.search(args.query, num_results=args.num)
    
    # 添加领域信息
    domain = parse_site_constraint(args.query)
    result["domain_category"] = domain
    
    # 输出JSON结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()