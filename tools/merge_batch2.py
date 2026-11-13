# -*- coding: utf-8 -*-
"""合并第2批（2025-09 ~ 2026-04）新增政策，校验后写入 policies.json"""
import io, json, os, sys, importlib.util

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BATCH


new = load("batch_20261112b_part1") + load("batch_20261112b_part2")
print("待入库条数:", len(new))

path = os.path.join(BASE, "data", "policies.json")
d = json.load(io.open(path, encoding="utf-8"))
old = d["policies"]
old_ids = {p["id"] for p in old}
old_urls = {p["bjx_url"] for p in old if p.get("bjx_url")}

REGIONS = {"全国", "内蒙古", "新疆", "河北", "广东", "宁夏", "青海", "甘肃", "江苏", "浙江",
           "辽宁", "陕西", "海南", "山东", "安徽", "湖南", "山西", "河南", "吉林", "四川",
           "云南", "贵州", "江西", "湖北", "福建", "广西", "重庆", "天津", "上海", "北京",
           "黑龙江", "西藏", "其他"}
CATS = {"储能装机目标", "储能项目清单", "容量电价政策", "电力现货规则", "峰谷电价政策",
        "系统运行费规则", "辅助服务市场规则", "新能源配储要求", "储能补贴政策", "并网与调度规则"}
MKEYS = {"cap_price", "pv_spread", "storage_ratio", "duration_h", "dispatch",
         "scale_gw", "scale_gwh", "ancillary", "note"}

errs = []
seen_id, seen_url = set(), set()
for p in new:
    if p["id"] in old_ids or p["id"] in seen_id:
        errs.append("ID重复: " + p["id"])
    seen_id.add(p["id"])
    u = p.get("bjx_url")
    if u and (u in old_urls or u in seen_url):
        errs.append("URL重复: " + u)
    if u:
        seen_url.add(u)
    if not u:
        errs.append("缺bjx_url: " + p["id"])
    if p.get("region") not in REGIONS:
        errs.append("region非法: %s -> %s" % (p["id"], p.get("region")))
    if p.get("category") not in CATS:
        errs.append("category非法: %s -> %s" % (p["id"], p.get("category")))
    if p.get("level") not in {"国家", "省级", "市级"}:
        errs.append("level非法: " + p["id"])
    if p.get("status") not in {"现行有效", "征求意见", "已废止", "被替代", "已失效"}:
        errs.append("status非法: %s -> %s" % (p["id"], p.get("status")))
    if p.get("impact") not in {"利多", "利空", "中性"}:
        errs.append("impact非法: " + p["id"])
    if p.get("tier") not in {"full", "index"}:
        errs.append("tier非法: " + p["id"])
    if set(p.get("metrics", {}).keys()) != MKEYS:
        errs.append("metrics键不一致: " + p["id"])
    if not (1 <= len(p.get("key_points", [])) <= 6):
        errs.append("key_points数量异常: " + p["id"])
    if len(p.get("summary", "")) > 60:
        errs.append("summary过长(%d字): %s" % (len(p["summary"]), p["id"]))

if errs:
    print("校验失败:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

merged = old + new
merged.sort(key=lambda p: (p["publish_date"], -p["star"]), reverse=True)
d["policies"] = merged
d["generated_at"] = "2026-11-12T18:30:00+08:00"

with io.open(path, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

print("写入完成，总条数:", len(merged))
print("新增区间:", min(p["publish_date"] for p in new), "~", max(p["publish_date"] for p in new))
