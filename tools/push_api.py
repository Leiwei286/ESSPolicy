# -*- coding: utf-8 -*-
"""在没有可用代理（github.com 不可达）时，用 GitHub Git Data API 推送本地提交。

背景：本机网络环境下 github.com 直连超时、系统代理对 github.com 返回 502，
但 api.github.com 直连正常。因此 `git push` 会失败，只能用 REST API 逐文件建 blob、
建 tree、建 commit，最后更新 ref。

用法（token 由 GCM 缓存提供，不要写进文件）：
    python tools/push_api.py --owner Leiwei286 --repo ESSPolicy --branch main --message "..." [--dry-run]

只推送 HEAD 提交里相对远端分支变动的文件。
"""
import argparse
import base64
import json
import os
import ssl
import subprocess
import sys
import urllib.request

API = "https://api.github.com"


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout.strip()


def get_token():
    """从 Git 凭据管理器取 token，仅驻留内存。"""
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    r = subprocess.run(["git", "credential", "fill"],
                       input="protocol=https\nhost=github.com\n\n",
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    for line in (r.stdout or "").splitlines():
        if line.startswith("password="):
            return line[len("password="):]
    raise SystemExit("未取到 GitHub 凭据，请先在本机执行一次 git push 并完成登录")


def req(method, path, token, payload=None):
    url = API + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", "Bearer " + token)
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data:
        r.add_header("Content-Type", "application/json")
    # api.github.com 直连即可，绕过本机系统代理（代理对 github 域名返回 502）
    ctx = ssl.create_default_context()
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx))
    try:
        with opener.open(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        raise SystemExit("%s %s 失败：HTTP %s\n%s" % (method, path, e.code, body[:800]))


def changed_files(base_sha):
    """本地 HEAD 相对远端 base_sha 变动的文件（含新增、修改，不含删除的简化处理）。"""
    out = sh("git -c core.quotepath=false diff --name-status %s HEAD" % base_sha)
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        if status.startswith("D"):
            print("  跳过删除文件（本脚本不处理删除）：%s" % path)
            continue
        if os.path.exists(path):
            files.append(path)
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", default="Leiwei286")
    ap.add_argument("--repo", default="ESSPolicy")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--message", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = get_token()
    base = "/repos/%s/%s" % (args.owner, args.repo)

    ref = req("GET", base + "/git/ref/heads/" + args.branch, token)
    parent_sha = ref["object"]["sha"]
    parent = req("GET", base + "/git/commits/" + parent_sha, token)
    base_tree = parent["tree"]["sha"]
    print("远端 HEAD：%s" % parent_sha[:10])

    # 基线：API 建出的提交在本机不存在，因此用「上次推送时对应的本地提交」作 diff 基线，
    # 记录在 .git/last_pushed_local_sha，避免每次都依赖远端 sha 是否存在于本地。
    marker = os.path.join(".git", "last_pushed_local_sha")
    diff_base = parent_sha
    if os.path.exists(marker):
        cand = open(marker).read().strip()
        if cand and subprocess.run(["git", "cat-file", "-e", cand + "^{commit}"],
                                   capture_output=True).returncode == 0:
            diff_base = cand
            print("基线（本地上次推送提交）：%s" % cand[:10])
        else:
            print("基线（远端提交，本地无此对象）：%s" % parent_sha[:10])

    files = changed_files(diff_base)
    if not files:
        print("无差异，退出")
        return
    print("待推送 %d 个文件：" % len(files))

    tree = []
    for path in files:
        raw = open(path, "rb").read()
        print("  %-40s %8.1f KB" % (path, len(raw) / 1024))
        if args.dry_run:
            continue
        blob = req("POST", base + "/git/blobs", token, {
            "content": base64.b64encode(raw).decode("ascii"),
            "encoding": "base64",
        })
        tree.append({"path": path.replace(os.sep, "/"), "mode": "100644",
                     "type": "blob", "sha": blob["sha"]})

    if args.dry_run:
        print("[dry-run] 未写入")
        return

    new_tree = req("POST", base + "/git/trees", token, {"base_tree": base_tree, "tree": tree})
    commit = req("POST", base + "/git/commits", token, {
        "message": args.message,
        "tree": new_tree["sha"],
        "parents": [parent_sha],
    })
    req("PATCH", base + "/git/refs/heads/" + args.branch, token, {"sha": commit["sha"]})
    print("已推送提交：%s" % commit["sha"][:10])
    # 本地同步远端引用，并记录本次推送对应的本地提交，供下次 diff 使用
    sh("git update-ref refs/remotes/origin/%s %s" % (args.branch, commit["sha"]))
    head = sh("git rev-parse HEAD")
    open(os.path.join(".git", "last_pushed_local_sha"), "w").write(head)
    print("远端 %s 已更新（基线已记录为本地 %s）" % (args.branch, head[:10]))


if __name__ == "__main__":
    main()
