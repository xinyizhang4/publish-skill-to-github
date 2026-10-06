# Publish Skill to GitHub

A **Codex skill / plugin** that packages a Codex skill into a standard plugin repo and publishes it to GitHub — bilingual README, MIT license, marketplace manifest, git init & push, with weak-network retries and PAT auth built in.

> 一个 Codex 技能/插件：把做好的 skill 打包成标准插件仓库并发布到 GitHub，自动生成中英 README、MIT 许可、marketplace 清单，git 初始化并推送，内置弱网重试与 PAT 认证。

## What it does · 功能
- Package a skill as a plugin (`.codex-plugin/plugin.json` + `skills/`).
- Generate a publish-ready repo: `plugins/`, `.agents/plugins/marketplace.json`, bilingual README, MIT LICENSE, `.gitignore`.
- Validate plugin + skill + marketplace manifest.
- git init + first commit.
- Create GitHub repo & push with automatic retry; set topic tags.
- Guides GitHub auth (PAT recommended; notes gh device-flow timeouts on weak networks).

## Install · 安装
```bash
codex plugin marketplace add https://github.com/xinyizhang4/publish-skill-to-github
codex plugin add publish-skill-to-github@publish-skill-to-github
```
或作为独立技能：
```bash
cp -R plugins/publish-skill-to-github/skills/publish-skill-to-github ~/.codex/skills/
```

## Usage · 使用
> 帮我把这个 skill 发布到 GitHub。

## Structure · 目录结构
```
.
├── .agents/plugins/marketplace.json
├── plugins/publish-skill-to-github/
│   ├── .codex-plugin/plugin.json
│   └── skills/publish-skill-to-github/
│       ├── SKILL.md
│       ├── references/publish-workflow.md
│       └── scripts/{prepare_repo.py, push_github.sh}
├── README.md
└── LICENSE
```

## License · 许可
[MIT](LICENSE)
