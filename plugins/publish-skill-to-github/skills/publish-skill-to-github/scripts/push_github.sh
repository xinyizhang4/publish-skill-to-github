#!/usr/bin/env bash
# 建 GitHub 公开仓库并推送（弱网自动重试）。token 用环境变量 GITHUB_TOKEN 传入，不写进任何文件。
# 用法: GITHUB_TOKEN=ghp_xxx push_github.sh <username> <repo_name> [repo_dir]
set -euo pipefail

USER="${1:?用法: push_github.sh <username> <repo_name> [repo_dir]}"
REPO="${2:?缺少 repo_name}"
DIR="${3:-.}"
TOKEN="${GITHUB_TOKEN:?缺少 GITHUB_TOKEN 环境变量}"

cd "$DIR"
PY="${PYTHON:-python3}"

# 1) 建仓库（已存在则跳过）
echo "==> 创建仓库 $USER/$REPO"
RESP=$(curl -s -X POST "https://api.github.com/user/repos"   -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json"   -d "{\"name\":\"$REPO\",\"private\":false}")
if ! echo "$RESP" | grep -q '"html_url"'; then
  if echo "$RESP" | grep -q 'already exists'; then
    echo "    仓库已存在，跳过创建"
  else
    echo "    创建失败: $(echo "$RESP" | head -c 300)"; exit 1
  fi
fi

# 2) 推送（重试）
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$USER/$REPO.git"
AUTH=$(printf '%s:%s' "$USER" "$TOKEN" | base64)
for i in 1 2 3 4 5 6; do
  echo "==> push attempt $i"
  if git -c http.extraheader="AUTHORIZATION: Basic $AUTH" push -u origin main 2>&1; then
    echo "==> PUSH OK"; break
  fi
  sleep 5
done

# 3) 设主题标签
curl -s -X PUT "https://api.github.com/repos/$USER/$REPO/topics"   -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json"   -d '{"names":["codex","skill","plugin","education","pdf","organizer"]}' >/dev/null
echo "==> 完成: https://github.com/$USER/$REPO"
echo "==> 提醒用户到 github.com/settings/tokens 删除 PAT"
