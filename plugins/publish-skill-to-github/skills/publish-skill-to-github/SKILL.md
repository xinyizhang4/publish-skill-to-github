---
name: publish-skill-to-github
description: 把 Codex 技能/插件打包并发布到 GitHub 公开仓库（生成中英 README、LICENSE、marketplace.json，git 初始化并推送，处理 GitHub 认证与弱网重试）。当用户要把做好的 skill/plugin 开源到 GitHub、想获得 star 或写进简历时使用。不用于创建 skill 本身，也不用于普通代码仓库的通用 git 操作。
---

# 发布 Codex Skill 到 GitHub

把已做好的 skill/plugin 打包成标准 Codex 插件仓库，推送到 GitHub 公开仓库（他人可安装、可写进简历）。

## 工作流（按序）
1. **确认来源**：找到要发布的 skill/plugin 目录（含 `SKILL.md` 或 `.codex-plugin/plugin.json`）。
2. **打包成插件**：插件根放 `.codex-plugin/plugin.json` + `skills/<skill-name>/`（若源是纯 skill，则补齐 plugin.json）。
3. **准备仓库布局**：`plugins/<name>/` + `.agents/plugins/marketplace.json` + `README.md`(中英双语) + `LICENSE`(MIT) + `.gitignore`，用 `scripts/prepare_repo.py` 一键生成并完成 git 首次提交。
4. **校验**：`validate_plugin.py` + `quick_validate.py` + 确认 marketplace.json 合法。
5. **GitHub 认证**：三种方式见 `references/publish-workflow.md`（**优先 PAT**，最稳）。
6. **建仓库并推送**：`scripts/push_github.sh`（自动重试）。
7. **设主题标签 + 提醒撤销 token**。

## 关键坑（务必遵守）
- **认证优先用 PAT**：`gh auth login --web`（设备码）在弱网下常在 `/login/oauth/access_token` 超时；PAT + `api.github.com` 最稳。
- **`gh` 可能装不上**：Homebrew 遇 PATH 含非 UTF-8 会崩；可直接从 GitHub releases 下载 `gh_<版本>_macOS_arm64.zip` 解压。
- **推送会断连**：用 `git -c http.extraheader="AUTHORIZATION: Basic <base64(user:token)>"` 临时注入 token（不写进 `.git/config`），并套重试循环。
- **仓库级市场布局**：`plugins/<name>/` + `.agents/plugins/marketplace.json`，entry 的 `source.path` = `./plugins/<name>`，且必须带 `policy.installation` / `policy.authentication` / `category`。
- **安全**：推送完立即提醒用户到 `github.com/settings/tokens` 删除 PAT（classic token 无法用 API 删除）。

## 脚本与参考
- `scripts/prepare_repo.py <repo_dir> <plugin_src> <repo_name> <username>`：生成仓库布局 + git init + 首次提交。
- `scripts/push_github.sh <username> <repo_name> [repo_dir]`（token 用环境变量 `GITHUB_TOKEN` 传入）：建仓库 + 推送 + 设主题标签。
- `references/publish-workflow.md`：完整步骤、认证三选一、排错清单。
