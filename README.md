# Sensor Tower Skills

> 让 AI Agent 用自然语言查询游戏/应用市场数据，无需切换窗口，无需记忆 API。

6 modules · 6 tools · Token 认证 · 仅需 `requests` 一个依赖

---

## 这是什么？

一句话：**你在聊天框里跟 AI 说"帮我查一下 Royal Match 上个月在美国赚了多少钱"，AI 就能自动调用 Sensor Tower API 帮你查出来。**

不需要你打开 Sensor Tower 网页，不需要你记住任何 API 参数，不需要你写代码。

### 它能做什么？

| 你说的话 | AI 做的事 |
|---------|----------|
| "帮我查一下 Royal Match 的数据" | 搜索应用，返回 App ID 和基本信息 |
| "这个游戏上个月收入多少" | 查询下载量和收入估算 |
| "美国游戏收入排行榜前 50" | 查询 Top Charts 排名 |
| "这个游戏日活多少" | 查询 DAU/WAU/MAU |
| "Supercell 旗下有哪些游戏" | 查询发行商旗下应用列表 |
| "看看竞品在投什么广告" | 查询广告素材和投放策略 |

---

## 为什么用 Skills，不用 MCP？

Sensor Tower 有 MCP Server，为什么还要做 Skills？

### 大白话版

**MCP** 像一个**电话总机**——AI 要找 Sensor Tower 拿数据，必须先接通总机，总机再转接。总机要一直开着（常驻进程），接线员（协议层）也不能下班。

**Skills** 像一叠**写好的便签**——每张便签写着"要查收入，就跑这条命令"。AI 看一眼便签，自己就能动手了。不需要总机，不需要接线员。

### 对比表

|  | Skills（本项目） | MCP Server |
|---|---|---|
| **像什么** | 一叠便签，看完就能用 | 一个电话总机，要一直开着 |
| **启动** | `git clone` 即用，零配置 | 需要启动独立进程 + 配置文件 |
| **如果挂了** | 不存在"挂了"——跑完就结束 | 进程挂了 = 所有工具全挂 |
| **上下文占用** | 按需加载：用到哪个加载哪个 | 全量加载：所有工具一次性塞入 |
| **加新功能** | 加个目录 + 2个文件，自动发现 | 改代码 → 重新部署 → 重启进程 |
| **调试** | 终端直接跑 `python3 tool.py --help` | 要通过 MCP 协议交互看日志 |
| **依赖** | Python + `requests`（1个包） | Python + FastMCP + uvicorn + ... |
| **多人协作** | 各目录独立，互不影响 | 集中式代码，改动易冲突 |

**什么时候该用 MCP？** 同一套工具要同时对接多个 AI 客户端（Claude Desktop、Cursor 等）。

**什么时候该用 Skills？** 你的 AI Agent 已经支持通过 `exec` 执行命令（Claude Code、OpenClaw 等），Skills 更简单、更稳、更省上下文。

---

## 5 分钟安装指南

### 前提条件

- Python 3.9+
- 一个 [Sensor Tower](https://sensortower.com) 付费账号（需含 API/Connect 权限）
- 一个支持 `exec` 的 AI Agent（如 [OpenClaw](https://github.com)、Claude Code）

### 第 1 步：下载
```bash
# OpenClaw 用户
git clone https://github.com/Unknowing-Ai/sensortower-skills.git ~/.openclaw/skills/sensortower

# Claude Code 用户
git clone https://github.com/Unknowing-Ai/sensortower-skills.git .claude/skills/sensortower

# 先试试玩
git clone https://github.com/Unknowing-Ai/sensortower-skills.git ~/sensortower-skills
```

### 第 2 步：装依赖
```bash
pip install requests
```

就这一个包，没别的了。

### 第 3 步：拿 Token

1. 登录 [app.sensortower.com](https://app.sensortower.com)
2. 右上角**头像** → **Account Info**（或直接访问 `sensortower.com/users/edit`）
3. 找到 **API Settings** 区域
4. 点 **Generate new API key**（首次）或 **Show API key**（已有）
5. 复制那串字符

### 第 4 步：配 Token
```bash
cp .env.example .env
```

编辑 `.env`，把 `your_token_here` 换成你的真实 token：SENSORTOWER_AUTH_TOKEN=你复制的那串字符
### 第 5 步：验证
```bash
python3 -X utf8 app-search/tool.py --term "Royal Match"
```

看到 JSON 数据 = 安装成功！

**常见报错**：
- `SENSORTOWER_AUTH_TOKEN not found` → .env 文件没配好
- `401 Unauthorized` → Token 不对，重新复制
- `403 Forbidden` → 订阅不含 API 权限，联系 ST 销售

---

## 使用方式

### 方式一：AI 自然语言（推荐）

直接跟 AI Agent 说话就行：
"帮我查一下 Royal Match 在美国 3月的收入"
"美国手游收入排行榜前 20"
"Supercell 旗下有哪些游戏"
"看看 Monopoly GO 在投什么广告"
AI 会自动调用对应工具，整理好数据后回复你。

### 方式二：命令行直接用
```bash
# 搜索应用
python3 -X utf8 app-search/tool.py --term "Royal Match"

# 查收入（需要 iOS 数字 ID，先用上面搜索拿到）
python3 -X utf8 sales-report/tool.py --app-id "1482938460" --os ios --countries US --start 2026-03-01 --end 2026-03-20 --granularity daily

# 排行榜
python3 -X utf8 top-charts/tool.py --measure revenue --countries US --category 6014 --limit 20

# 活跃用户
python3 -X utf8 active-users/tool.py --app-id "1482938460" --metric DAU --countries US --start 2026-03-01 --end 2026-03-20

# 发行商旗下应用
python3 -X utf8 publisher-apps/tool.py --publisher-id "发行商ID"

# 广告素材
python3 -X utf8 ad-intelligence/tool.py --app-id "1482938460" --action creatives --limit 10
```

每个工具都支持 `--help`：
```bash
python3 sales-report/tool.py --help
```

---

## 项目结构

sensortower-skills/
├── README.md              ← 你正在看的这个文件
├── SKILL.md               ← AI 最先读的入口文件
├── search.py              ← 关键词搜索，按需发现子技能
├── .env.example           ← Token 配置模板
├── .env                   ← 你的 Token（不会上传 Git）
├── requirements.txt       ← Python 依赖（只有 requests）
│
├── common/
│   └── api.py             ← 共享：Token 管理 + HTTP 请求 + 工具函数
│
├── app-search/            ← 🔍 搜索应用和发行商
│   ├── SKILL.md
│   └── tool.py
│
├── sales-report/          ← 💰 下载量和收入查询
│   ├── SKILL.md
│   └── tool.py
│
├── top-charts/            ← 📊 排行榜
│   ├── SKILL.md
│   └── tool.py
│
├── active-users/          ← 👥 DAU/WAU/MAU
│   ├── SKILL.md
│   └── tool.py
│
├── publisher-apps/        ← 🏢 发行商旗下应用
│   ├── SKILL.md
│   └── tool.py
│
└── ad-intelligence/       ← 📺 广告素材和投放策略
├── SKILL.md
└── tool.py

每个技能 = **SKILL.md**（告诉 AI 怎么用）+ **tool.py**（实际执行的脚本）

---

## 架构：关键词搜索
AI 加载根 SKILL.md → 知道有哪些技能
用户说"查一下 Royal Match 收入"
AI 调用 search.py + 关键词 → 返回匹配的技能路径
AI 读匹配的 SKILL.md → 知道具体怎么调用
AI 执行 tool.py → 拿到数据 → 整理后回复用户

示例：
```bash
$ python3 search.py revenue
[
  {
    "path": "sales-report/SKILL.md",
    "description": "Query app downloads and revenue estimates."
  }
]
```

---

## 添加新技能

3 步搞定，`search.py` 会自动发现，不需要改任何已有文件：

**1. 建目录**
```bash
mkdir my-new-skill/
```

**2. 写 SKILL.md**
```markdown
---
description: "一句话描述做什么"
keywords: "关键词1 关键词2"
---
# 技能名称
调用方式和参数说明
```

**3. 写 tool.py**
```python
#!/usr/bin/env python3
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.api import api_get, output_json

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--my-param", required=True)
    a = p.parse_args()
    data = api_get("/v1/ios/your_endpoint", {"param": a.my_param})
    output_json(data)

if __name__ == "__main__": main()
```

---

## API 说明

- **Base URL**: `https://api.sensortower.com`
- **认证**: 所有请求带 `auth_token` 参数
- **Rate Limit**: 6 requests/second
- **收入单位**: 美分（cents），tool.py 已自动 ÷100 转美元
- **端点文档**: 登录后访问 `app.sensortower.com/api/docs`

### 已验证的端点

| 端点 | 说明 |
|------|------|
| `/v1/{os}/search_entities` | 搜索应用/发行商 |
| `/v1/{os}/sales_report_estimates` | 下载量和收入 |
| `/v1/{os}/top_charts` | 排行榜 |
| `/v1/{os}/active_users` | 活跃用户 |
| `/v1/{os}/publisher_apps` | 发行商旗下应用 |

其中 `{os}` = `ios` 或 `android`（部分端点支持 `unified`）。

---

## 常见问题

**Q: 数据准确吗？**
Sensor Tower 的数据是估算值，基于面板和模型推算。业界广泛用于竞品分析，但不是精确财务数据。

**Q: 能查中国市场吗？**
可以，国家代码用 `CN`。但中国 Android 市场覆盖度不如 iOS。

**Q: Ad Intelligence 报 403？**
订阅可能不含该模块，联系 ST 销售。

**Q: 和 feishu-skills 冲突吗？**
不冲突。两个技能集各自独立，共享 Python 环境。

---

## 国家代码速查

| 代码 | 国家 | 代码 | 国家 |
|------|------|------|------|
| WW | 全球 | US | 美国 |
| CN | 中国 | JP | 日本 |
| KR | 韩国 | GB | 英国 |
| DE | 德国 | FR | 法国 |
| BR | 巴西 | IN | 印度 |
| ID | 印尼 | TW | 台湾 |
| TH | 泰国 | VN | 越南 |
| SA | 沙特 | TR | 土耳其 |

## 游戏分类 ID 速查

| ID | 分类 | ID | 分类 |
|----|------|----|------|
| 6014 | Games（全部） | 7001 | Action |
| 7002 | Adventure | 7003 | Arcade |
| 7005 | Card | 7006 | Casino |
| 7009 | Puzzle | 7012 | Role Playing |
| 7014 | Sports | 7015 | Strategy |

---

## 致谢

- [feishu-skills](https://github.com/WenHaoWang1997/feishu-skills) — 本项目的架构灵感来源
- [sensortowerR](https://cran.r-project.org/package=sensortowerR) — API 端点逆向参考

## License

MIT
