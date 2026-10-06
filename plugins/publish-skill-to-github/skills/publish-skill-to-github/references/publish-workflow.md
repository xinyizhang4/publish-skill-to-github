# 发布到 GitHub 完整流程

## 1. 打包成插件
- 插件根目录放 `.codex-plugin/plugin.json`（字段：`name`、`version`、`description`、`author`、`skills: "./skills/"`、`interface`）。
- `interface` 里写中文友好的 `displayName`、`shortDescription`、`longDescription`、`category`、`defaultPrompt`。
- skill 本体放在 `skills/<skill-name>/`（`SKILL.md` + 可选 `agents/`、`scripts/`、`references/`）。

## 2. 仓库布局（标准）
```
<repo>/
├── .agents/plugins/marketplace.json   # 他人安装入口
├── plugins/<name>/                    # 插件（含 .codex-plugin/ + skills/）
├── README.md                          # 中英双语
├── LICENSE                            # MIT
└── .gitignore                         # .DS_Store / __pycache__ / *.pyc
```
- `marketplace.json` 根：`name`、`interface.displayName`、`plugins[]`。
- 每个 entry：`name`、`source: {source:"local", path:"./plugins/<name>"}`、`policy: {installation:"AVAILABLE", authentication:"ON_INSTALL"}`、`category`。

## 3. 校验
```bash
python3 <plugin-creator>/scripts/validate_plugin.py <repo>/plugins/<name>
python3 <skill-creator>/scripts/quick_validate.py <repo>/plugins/<name>/skills/<name>
python3 -c "import json; json.load(open('<repo>/.agents/plugins/marketplace.json'))"
```
> 若缺 `yaml`：`python3 -m pip install --target /tmp/pyyaml pyyaml`，运行时 `PYTHONPATH=/tmp/pyyaml`。

## 4. git 初始化与提交
```bash
cd <repo> && git init -b main
git config user.name "你的名字"
git config user.email "你的邮箱"
git add -A && git commit -m "Initial commit: <name> Codex plugin"
```

## 5. GitHub 认证（三选一，推荐 PAT）
- **PAT（推荐）**：github.com → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)；勾 `repo`，有效期 7 天；拿到 `ghp_...`。直达链接 `github.com/settings/tokens/new`。
- **gh 设备码**：`gh auth login --hostname github.com --git-protocol https --web`，复制一次性码到 `github.com/login/device` 授权；弱网下 `/login/oauth/access_token` 易超时。
- **SSH**：`ssh-keygen -t ed25519`，把公钥加到 github.com → Settings → SSH and GPG keys。

## 6. 建仓库 + 推送（弱网需重试）
- 用 PAT 建仓库（`api.github.com` 通常最稳）：
```bash
curl -X POST https://api.github.com/user/repos   -H "Authorization: Bearer $GITHUB_TOKEN" -H "Accept: application/vnd.github+json"   -d '{"name":"<repo>","description":"...","private":false}'
```
- 推送（临时注入 token，不落盘）：
```bash
AUTH=$(printf '<user>:%s' "$GITHUB_TOKEN" | base64)
git -c http.extraheader="AUTHORIZATION: Basic $AUTH" push -u origin main   # 失败就 sleep 5 重试
```
- 设主题标签（利于搜索/star）：
```bash
curl -X PUT https://api.github.com/repos/<user>/<repo>/topics   -H "Authorization: Bearer $GITHUB_TOKEN" -H "Accept: application/vnd.github+json"   -d '{"names":["codex","skill","education","pdf",...]}'
```

## 7. 收尾
- 提醒用户删 PAT：`github.com/settings/tokens` → 找到 token → Delete（classic token 无删除 API）。
- 给出安装命令供他人使用：
```bash
codex plugin marketplace add https://github.com/<user>/<repo>
codex plugin add <repo>@<repo>
```

## 排错
- Homebrew `invalid byte sequence in UTF-8`（PATH 含非 UTF-8）→ 改用 gh releases 直下或 PAT 路线。
- `gh auth login` 卡在 `dial tcp ... i/o timeout` → 换 PAT + api.github.com。
- push `i/o timeout` → 重试循环（本机实测第 1 次就成功）。
- 建仓库返回 `422 name already exists` → 仓库已存在，跳过创建直接 push。
