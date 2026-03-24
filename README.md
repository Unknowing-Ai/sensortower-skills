# Sensor Tower Skills

> 让 AI Agent 用自然语言查询游戏/应用市场数据，无需切换窗口，无需记忆 API。

6 modules · 6 tools · Token 认证 · 仅需 requests 一个依赖

---

## 这是什么？

一句话：**你在聊天框里跟 AI 说"帮我查一下 Royal Match 上个月在美国赚了多少钱"，AI 就能自动调用 Sensor Tower API 帮你查出来。**

不需要你打开 Sensor Tower 网页，不需要你记住任何 API 参数，不需要你写代码。

### 它能做什么？

| 你说的话 | AI 做的事 |
|---------|----------|
| 帮我查一下 Royal Match 的数据 | 搜索应用，返回 App ID 和基本信息 |
| 这个游戏上个月收入多少 | 查询下载量和收入估算 |
| 美国游戏收入排行榜前 50 | 查询 Top Charts 排名 |
| 这个游戏日活多少 | 查询 DAU/WAU/MAU |
| Supercell 旗下有哪些游戏 | 查询发行商旗下应用列表 |
| 看看竞品在投什么广告 | 查询广告素材和投放策略 |

---

## 为什么用 Skills，不用 MCP？

**MCP** 像一个**电话总机**——AI 要找 Sensor Tower 拿数据，必须先接通总机，总机再转接。总机要一直开着，接线员也不能下班。

**Skills** 像一叠**写好的便签**——每张便签写着"要查收入，就跑这条命令"。AI 看一眼便签，自己就能动手了。

|  | Skills（本项目） | MCP Server |
|---|---|---|
| **像什么** | 一叠便签，看完就能用 | 一个电话总机，要一直开着 |
| **启动** | git clone 即用 | 需要启动独立进程 + 配置文件 |
| **如果挂了** | 不存在挂了——跑完就结束 | 进程挂了 = 所有工具全挂 |
| **上下文占用** | 按需加载：用到哪个加载哪个 | 全量加载：所有工具一次性塞入 |
| **加新功能** | 加个目录 + 2个文件，自动发现 | 改代码 → 重新部署 → 重启进程 |
| **调试** | 终端直接跑 python3 tool.py --help | 要通过 MCP 协议交互看日志 |
| **依赖** | Python + requests（1个包） | Python + FastMCP + uvicorn + ... |

---

## 5 分钟安装指南

### 第 1 步：下载

    # OpenClaw 用户
    git clone https://github.com/Unknowing-Ai/sensortower-skills.git ~/.openclaw/skills/sensortower

    # Claude Code 用户
    git clone https://github.com/Unknowing-Ai/sensortower-skills.git .claude/skills/sensortower

### 第 2 步：装依赖

    pip install requests

### 第 3 步：拿 Token

1. 登录 app.sensortower.com
2. 右上角头像 → Account Info
3. 找到 API Settings 区域
4. 点 Generate new API key 或 Show API key
5. 复制那串字符

### 第 4 步：配 Token

    cp .env.example .env
    # 编辑 .env，把 your_token_here 换成你的真实 token

### 第 5 步：验证

    python3 -X utf8 app-search/tool.py --term "Royal Match"

看到 JSON 数据 = 安装成功！

---

## 项目结构

| 目录 | 说明 | 文件 |
|------|------|------|
| / 根目录 | 入口和配置 | README.md, SKILL.md, search.py, .env.example, requirements.txt |
| common/ | 共享模块 | api.py（Token 管理 + HTTP 请求 + 工具函数） |
| app-search/ | 搜索应用和发行商 | SKILL.md + tool.py |
| sales-report/ | 下载量和收入查询 | SKILL.md + tool.py |
| top-charts/ | 排行榜 | SKILL.md + tool.py |
| active-users/ | DAU/WAU/MAU | SKILL.md + tool.py |
| publisher-apps/ | 发行商旗下应用 | SKILL.md + tool.py |
| ad-intelligence/ | 广告素材和投放策略 | SKILL.md + tool.py |

每个技能 = **SKILL.md**（告诉 AI 怎么用）+ **tool.py**（实际执行的脚本）

---

## 使用方式

### 方式一：AI 自然语言（推荐）

直接跟 AI Agent 说话：

- 帮我查一下 Royal Match 在美国 3月的收入
- 美国手游收入排行榜前 20
- Supercell 旗下有哪些游戏

### 方式二：命令行

    # 搜索应用
    python3 -X utf8 app-search/tool.py --term "Royal Match"

    # 查收入
    python3 -X utf8 sales-report/tool.py --app-id "1482938460" --os ios --countries US --start 2026-03-01 --end 2026-03-20

    # 排行榜
    python3 -X utf8 top-charts/tool.py --measure revenue --countries US --category 6014 --limit 20

    # 广告素材
    python3 -X utf8 ad-intelligence/tool.py --app-id "1482938460" --action creatives

每个工具都支持 --help 查看完整参数。

---

## 添加新技能

3 步搞定，search.py 会自动发现，不需要改任何已有文件：

1. 建目录：mkdir my-new-skill/
2. 写 SKILL.md（描述用法 + 关键词）
3. 写 tool.py（argparse + api_get + output_json）

---

## API 说明

- Base URL: https://api.sensortower.com
- 认证: 所有请求带 auth_token 参数
- Rate Limit: 6 requests/second
- 收入单位: 美分（tool.py 已自动转美元）

### 已验证的端点

| 端点 | 说明 |
|------|------|
| /v1/{os}/search_entities | 搜索应用/发行商 |
| /v1/{os}/sales_report_estimates | 下载量和收入 |
| /v1/{os}/top_charts | 排行榜 |
| /v1/{os}/active_users | 活跃用户 |
| /v1/{os}/publisher_apps | 发行商旗下应用 |

---

## 常见问题

**Q: 数据准确吗？** Sensor Tower 的数据是估算值，业界广泛用于竞品分析，但不是精确财务数据。

**Q: 能查中国市场吗？** 可以，国家代码用 CN。

**Q: Ad Intelligence 报 403？** 订阅可能不含该模块，联系 ST 销售。

**Q: 和 feishu-skills 冲突吗？** 不冲突，完全独立。

---

## 国家代码速查

| 代码 | 国家 | 代码 | 国家 |
|------|------|------|------|
| WW | 全球 | US | 美国 |
| CN | 中国 | JP | 日本 |
| KR | 韩国 | GB | 英国 |
| DE | 德国 | FR | 法国 |
| BR | 巴西 | IN | 印度 |

## 游戏分类 ID 速查

| ID | 分类 | ID | 分类 |
|----|------|----|------|
| 6014 | Games | 7001 | Action |
| 7009 | Puzzle | 7012 | Role Playing |
| 7015 | Strategy | 7006 | Casino |

---

## 致谢

- [feishu-skills](https://github.com/WenHaoWang1997/feishu-skills) — 架构灵感来源
- [sensortowerR](https://cran.r-project.org/package=sensortowerR) — API 端点参考

## License

MIT
