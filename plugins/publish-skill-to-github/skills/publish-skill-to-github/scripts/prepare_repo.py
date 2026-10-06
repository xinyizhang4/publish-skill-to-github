#!/usr/bin/env python3
"""把 skill/plugin 打包成可发布到 GitHub 的标准仓库布局，并完成 git 首次提交。
用法: prepare_repo.py <repo_dir> <plugin_src> <repo_name> <username>
  repo_dir   目标仓库目录（将创建）
  plugin_src 插件源目录（含 .codex-plugin/plugin.json 与 skills/）
  repo_name  仓库/插件名（小写连字符）
  username   GitHub 用户名（写进 README 安装链接）
"""
import os, sys, json, shutil, subprocess

def main():
    if len(sys.argv) != 5:
        print(__doc__); sys.exit(1)
    repo_dir, plugin_src, repo_name, username = sys.argv[1:5]
    os.makedirs(os.path.join(repo_dir, "plugins"), exist_ok=True)
    os.makedirs(os.path.join(repo_dir, ".agents/plugins"), exist_ok=True)

    dst = os.path.join(repo_dir, "plugins", repo_name)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(plugin_src, dst)

    open(os.path.join(repo_dir, ".gitignore"), "w").write(".DS_Store\n__pycache__/\n*.pyc\n")

    open(os.path.join(repo_dir, "LICENSE"), "w").write(
        "MIT License\n\nCopyright (c) 2026 %s\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE.\n" % username
    )

    marketplace = {
        "name": repo_name,
        "interface": {"displayName": repo_name.replace("-", " ").title()},
        "plugins": [{
            "name": repo_name,
            "source": {"source": "local", "path": "./plugins/" + repo_name},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Education",
        }]
    }
    with open(os.path.join(repo_dir, ".agents/plugins/marketplace.json"), "w") as f:
        json.dump(marketplace, f, ensure_ascii=False, indent=2)

    readme = (
        "# %s\n\n"
        "A **Codex skill / plugin**.\n\n"
        "> 一个 Codex 技能/插件。\n\n"
        "## Install · 安装\n\n"
        "```bash\n"
        "codex plugin marketplace add https://github.com/%s/%s\n"
        "codex plugin add %s@%s\n"
        "```\n\n"
        "## License · 许可\n\n"
        "[MIT](LICENSE)\n"
    ) % (repo_name, username, repo_name, repo_name, repo_name)
    open(os.path.join(repo_dir, "README.md"), "w").write(readme)

    def run(*args):
        return subprocess.run(list(args), cwd=repo_dir, capture_output=True, text=True)

    run("git", "init", "-b", "main")
    name = os.environ.get("GIT_USER_NAME", username)
    email = os.environ.get("GIT_USER_EMAIL", username + "@users.noreply.github.com")
    run("git", "config", "user.name", name)
    run("git", "config", "user.email", email)
    run("git", "add", "-A")
    run("git", "commit", "-m", f"Initial commit: {repo_name} Codex plugin")
    print("repo ready:", repo_dir)

if __name__ == "__main__":
    main()
