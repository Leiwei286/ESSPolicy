# -*- coding: utf-8 -*-
"""交付前数据体检：字段完整性、一致性、指标覆盖缺口"""
import io
import json
import os
import re
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

pol = json.load(io.open(os.path.join(DATA, "policies.json"), encoding="utf-8"))["policies"]
meta = json.load(io.open(os.path.join(DATA, "meta.json"), encoding="utf-8"))

FULL_KEYS = ["id", "title", "region", "level", "issuer", "doc_no", "doc_type", "publish_date",
             "effective_date", "status", "superseded_by", "star", "model_flag", "category",
             "sub_tags", "summary", "key_points", "metrics", "impact", "logic",
             "source_url", "source_name", "bjx_url", "tier", "first_seen", "last_checked", "note"]
METRIC_KEYS = ["cap_price", "pv_spread", "storage_ratio", "duration_h",
               "dispatch", "scale_gw", "scale_gwh", "ancillary"]
STATUSES = {"现行有效", "征求意见", "已废止", "被替代", "已失效", "历史索引"}
IMPACTS = {"利多", "利空", "中性"}
CATS = set(meta["categories"])
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

issues = defaultdict(list)
full = [p for p in pol if p.get("tier") == "full"]
index = [p for p in pol if p.get("tier") == "index"]

# 1. 主键与重复
ids = Counter(p["id"] for p in pol)
for k, v in ids.items():
    if v > 1:
        issues["重复ID"].append(k)
urls = Counter(p["bjx_url"] for p in pol if p.get("bjx_url"))
for k, v in urls.items():
    if v > 1:
        issues["重复bjx_url"].append(f"{k} ×{v}")
titles = Counter((p["region"], p["title"]) for p in pol)
for k, v in titles.items():
    if v > 1:
        issues["同地区同标题"].append(f"{k[0]} | {k[1][:40]} ×{v}")

# 2. 字段完整性
for p in full:
    miss = [k for k in FULL_KEYS if k not in p]
    if miss:
        issues["缺字段"].append(f"{p['id']} 缺 {miss}")
    if not p.get("key_points"):
        issues["全字段无要点"].append(p["id"])
    n = len(p.get("key_points") or [])
    if n and not (3 <= n <= 7):
        issues["要点数异常"].append(f"{p['id']} {n}条")
    if not str(p.get("summary", "")).strip():
        issues["summary空"].append(p["id"])
    mk = p.get("metrics") or {}
    lost = [k for k in METRIC_KEYS if k not in mk]
    if lost:
        issues["metrics键缺失"].append(f"{p['id']} 缺 {lost}")
    if not p.get("issuer") or p["issuer"] in ("待核实", "—", ""):
        issues["issuer待核实(全字段)"].append(p["id"])

# 3. 枚举与格式
for p in pol:
    if p["status"] not in STATUSES:
        issues["非法status"].append(f"{p['id']} {p['status']}")
    if p["tier"] == "full":
        if p.get("impact") not in IMPACTS:
            issues["非法impact"].append(f"{p['id']} {p.get('impact')}")
        if p.get("category") not in CATS:
            issues["非法category"].append(f"{p['id']} {p.get('category')}")
        if not isinstance(p.get("star"), int) or not 1 <= p["star"] <= 3:
            issues["非法star"].append(f"{p['id']} {p.get('star')}")
    if not DATE_RE.match(str(p.get("publish_date", ""))):
        issues["非法publish_date"].append(f"{p['id']} {p.get('publish_date')}")

# 4. 日期逻辑（早于发布日多为追溯执行，要求 note 已注明）
for p in full:
    ed = p.get("effective_date")
    if ed and DATE_RE.match(str(ed)):
        if ed < p["publish_date"]:
            _n = str(p.get("note") or "")
            _ok = ("追溯" in _n) or ("报道日" in _n)
            key = "日期差异已注明" if _ok else "生效日早于发布日(未注明)"
            issues[key].append(f"{p['id']} {p['publish_date']} → {ed}")

# 5. 替代关系闭环
by_id = {p["id"]: p for p in pol}
for p in pol:
    sb = p.get("superseded_by")
    if sb:
        if sb not in by_id:
            issues["superseded_by指向不存在"].append(f"{p['id']} → {sb}")
        elif p["status"] not in ("被替代", "已废止"):
            issues["有替代但状态未标"].append(f"{p['id']} status={p['status']}")
    if p["status"] == "被替代" and not sb:
        issues["已替代但无superseded_by"].append(p["id"])

# 6. 指标覆盖
cov = {}
for k in METRIC_KEYS:
    cov[k] = sum(1 for p in full if (p.get("metrics") or {}).get(k) is not None)
print("=" * 62)
print(f"数据体检  |  全库 {len(pol)} 条（全字段 {len(full)} + 索引 {len(index)}）")
print("=" * 62)
print("\n[指标覆盖：全字段条目中有值的条数]")
for k, v in cov.items():
    print(f"  {k:14s} {v:3d}  {v / len(full) * 100:5.1f}%")

# cap_price 省份分布
cap = defaultdict(list)
for p in full:
    v = (p.get("metrics") or {}).get("cap_price")
    if v is not None:
        cap[p["region"]].append((p["publish_date"], v, p["id"]))
print("\n[容量电价结论值：按省份取最新一条]")
for r in sorted(cap, key=lambda x: -max(cap[x])[1]):
    latest = max(cap[r])
    print(f"  {r:6s} {latest[1]:>7} 元/kW·年   {latest[0]}  {latest[2]}  (共{len(cap[r])}条)")

print("\n[问题清单]")
real = {k: v for k, v in issues.items() if "已注明" not in k}
notes = {k: v for k, v in issues.items() if "已注明" in k}
if not real:
    print("  ✅ 无阻断性问题")
for k, v in real.items():
    print(f"  · {k}（{len(v)}）")
    for x in v[:6]:
        print(f"      {x}")
    if len(v) > 6:
        print(f"      …… 另 {len(v) - 6} 条")
if notes:
    print("\n[提示：已核实无需处理]")
    for k, v in notes.items():
        print(f"  · {k}（{len(v)}）：" + "、".join(x.split()[0] for x in v))

# 7. 分类 × 层级 交叉，找稀疏
print("\n[分类分布：全字段 / 其中星级3]")
cat_all = Counter(p["category"] for p in full)
cat_star3 = Counter(p["category"] for p in full if p["star"] == 3)
for c in sorted(cat_all, key=lambda x: -cat_all[x]):
    print(f"  {c:14s} {cat_all[c]:3d} / ★★★{cat_star3[c]:3d}")

print("\n[状态分布]", dict(Counter(p["status"] for p in pol)))
