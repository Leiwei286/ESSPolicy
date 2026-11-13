# -*- coding: utf-8 -*-
"""
把 data/*.json 打包成 data/data-bundle.js。

为什么需要这一步：
    浏览器在 file:// 协议下会拦截 fetch 读取本地 JSON（CORS 限制），
    但允许通过 <script src="..."> 加载同目录 JS。因此把 JSON 包一层
    赋值语句，看板即可双击直接打开，无需起本地服务器。

用法：
    python tools/build_data.py

每周更新流程：
    1. 修改 data/policies.json（或由增量脚本写入）
    2. 运行本脚本
    3. 刷新 index.html
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "data-bundle.js")


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        sys.exit("[ERR] 缺少文件: %s" % path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    policies = load("policies.json")
    meta = load("meta.json")

    items = policies.get("policies", [])

    # 一致性校验：id 唯一、必填字段齐全
    seen = set()
    problems = []
    required = ["id", "title", "region", "level", "issuer", "publish_date",
                "status", "category", "impact", "star", "tier"]
    for p in items:
        pid = p.get("id")
        if pid in seen:
            problems.append("重复 id: %s" % pid)
        seen.add(pid)
        for k in required:
            if k not in p or p[k] in (None, ""):
                problems.append("%s 缺少必填字段 %s" % (pid, k))

    # 计数以实际数据为准，避免 meta 与实际脱节
    counts = {}
    for p in items:
        counts[p["status"]] = counts.get(p["status"], 0) + 1
    meta["total"] = len(items)
    meta["counts"] = counts
    regions = sorted({p["region"] for p in items})
    meta["regions_covered"] = regions

    payload = (
        "window.POLICY_DATA = %s;\n"
        "window.POLICY_META = %s;\n"
    ) % (
        json.dumps(policies, ensure_ascii=False, indent=1),
        json.dumps(meta, ensure_ascii=False, indent=1),
    )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(payload)

    print("[OK] 打包完成: %s" % OUT)
    print("     政策条数: %d" % len(items))
    print("     覆盖地区: %s" % "、".join(regions))
    print("     状态分布: %s" % json.dumps(counts, ensure_ascii=False))
    if problems:
        print("[WARN] 校验问题 %d 项:" % len(problems))
        for x in problems:
            print("       - " + x)
    else:
        print("     字段校验: 通过")


if __name__ == "__main__":
    main()
