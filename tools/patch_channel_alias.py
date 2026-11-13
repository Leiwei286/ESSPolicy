# -*- coding: utf-8 -*-
"""一次性补丁：加 channel 字段 + 归一分类型别名

1. 所有既有条目补 channel="bjx"（北极星抓取入库），手动收集源入库时为 "ima"
2. category 别名 "辅助服务市场" → "辅助服务市场规则"（老索引批次写法，会分裂筛选器）
3. doc_type 别名 "工作方案" → "方案"
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "policies.json")

with open(P, "r", encoding="utf-8") as f:
    pol = json.load(f)
items = pol["policies"]

n_channel = n_cat = n_dt = 0
for p in items:
    if "channel" not in p:
        p["channel"] = "bjx"
        n_channel += 1
    if p.get("category") == "辅助服务市场":
        p["category"] = "辅助服务市场规则"
        n_cat += 1
    if p.get("doc_type") == "工作方案":
        p["doc_type"] = "方案"
        n_dt += 1

shutil.copy2(P, os.path.join(ROOT, "data", "policies.backup-字段补丁.json"))
with open(P, "w", encoding="utf-8") as f:
    json.dump(pol, f, ensure_ascii=False, indent=1)

print("channel 补齐 %d 条" % n_channel)
print("category 归一 %d 条" % n_cat)
print("doc_type 归一 %d 条" % n_dt)
print("全库 %d 条" % len(items))
