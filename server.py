"""
竞品搜索 MCP Server
====================
把竞品分析项目的搜索功能封装为 MCP Server。
Claude Code、Cursor 等任何支持 MCP 的 AI 工具都能直接调用。

使用真实 DuckDuckGo 搜索（无需 API Key）。
"""

from fastmcp import FastMCP

mcp = FastMCP("竞品搜索服务 🔍")


def search_web(query: str) -> str:
    """真实 DuckDuckGo 搜索"""
    try:
        from ddgs import DDGS
        results = DDGS().text(query, max_results=5)
        if not results:
            return f"关于「{query}」未找到结果"
        return "\n\n".join(
            f"{i+1}. {r['title']}\n   {r['body']}\n   {r['href']}"
            for i, r in enumerate(results)
        )
    except ImportError:
        return "错误：请先安装 duckduckgo-search（py -m pip install duckduckgo-search）"
    except Exception as e:
        return f"搜索失败：{e}"


@mcp.tool()
def search(query: str) -> str:
    """
    搜索指定主题的最新市场信息。
    用于竞品分析、行业研究、市场调查。

    参数:
        query: str — 搜索关键词，如"特斯拉 2026 销量"、"比亚迪 海外市场"
    """
    return search_web(query)


@mcp.tool()
def multi_search(queries: str) -> str:
    """
    同时搜索多个关键词（用逗号分隔）。
    用于一次性获取多个竞品的对比信息。

    参数:
        queries: str — 逗号分隔的关键词，如"特斯拉,比亚迪,新能源市场"
    """
    keywords = [q.strip() for q in queries.split(",") if q.strip()]
    results = []
    for kw in keywords:
        r = search_web(kw)
        results.append(f"【{kw}】\n{r}")
    return "\n\n---\n\n".join(results)


@mcp.tool()
def analyze(data: str) -> str:
    """
    分析文本，提取关键数字和洞察。
    用于对搜索结果做量化分析。

    参数:
        data: str — 要分析的文本
    """
    import re
    numbers = re.findall(r'\d+[\.,\d]*\s*(?:万|亿|%|辆|美元|元|kW|kWh)?', data)
    keywords = ["特斯拉", "比亚迪", "销量", "交付", "营收", "利润", "市场", "增长"]
    found_kw = [kw for kw in keywords if kw in data]

    summary = []
    if numbers:
        summary.append(f"📊 关键数字：{', '.join(numbers[:10])}")
    if found_kw:
        summary.append(f"🏷️ 关键词：{', '.join(found_kw)}")
    if not summary:
        return "未提取到量化数据。建议补充具体数值信息。"
    return "\n".join(summary)


@mcp.resource("industry://automotive/2026")
def auto_industry_overview() -> str:
    """
    2026 年汽车行业概况（实时搜索 + 汇总）
    """
    data = multi_search("2026年新能源汽车市场,特斯拉2026销量,比亚迪2026销量")
    return f"## 2026 年新能源汽车行业概况（实时数据）\n\n{data}"


if __name__ == "__main__":
    print("=" * 50)
    print("🔍 竞品搜索服务 — MCP Server")
    print("=" * 50)
    print("工具：search | multi_search | analyze")
    print("资源：industry://automotive/2026")
    print()
    mcp.run()
