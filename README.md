# 竞品搜索 MCP Server

> 把竞品分析项目的搜索功能封装为 MCP Server，任何支持 MCP 的 AI 工具都能直接调用。

## 安装

```bash
py -m pip install -r requirements.txt
```

## 工具列表

| 工具 | 说明 |
|------|------|
| `search` | 搜索指定主题（DuckDuckGo 真实搜索） |
| `multi_search` | 同时搜索多个关键词 |
| `analyze` | 分析文本，提取关键数字 |

## 资源

| URI | 说明 |
|------|------|
| `industry://automotive/2026` | 2026 年汽车行业概况 |

## 测试

```bash
# 启动测试界面
fastmcp dev inspector server.py

# 或直接 HTTP 模式启动
fastmcp run server.py --transport http --port 8000
```

## Claude Code 配置

在 Claude Code 的 MCP 设置中添加：

```json
{
  "mcpServers": {
    "search": {
      "command": "py",
      "args": ["D:/mcp-search-server/server.py"]
    }
  }
}
```

配置后，Claude Code 就能直接调用你的搜索服务。
