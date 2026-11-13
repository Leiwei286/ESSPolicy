# -*- coding: utf-8 -*-
"""更新 meta.json 与 changelog.json（第1批 35 条入库后）"""
import io, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

# ---- meta ----
mp = os.path.join(DATA, "meta.json")
meta = json.load(io.open(mp, encoding="utf-8"))
pol = json.load(io.open(os.path.join(DATA, "policies.json"), encoding="utf-8"))["policies"]

counts = {}
for p in pol:
    counts[p["status"]] = counts.get(p["status"], 0) + 1
for k in ["现行有效", "征求意见", "已废止", "被替代", "已失效"]:
    counts.setdefault(k, 0)

meta["coverage_start"] = min(p["publish_date"] for p in pol)
meta["coverage_end"] = max(p["publish_date"] for p in pol)
meta["phase"] = "第1批已入库（2026-04-20 至 2026-11-12，60 条）"
meta["total"] = len(pol)
meta["counts"] = counts
meta["regions_covered"] = sorted({p["region"] for p in pol})
meta["last_update"] = "2026-11-12"
meta["last_update_note"] = (
    "第1批补录：新增 35 条，覆盖 2026-04-20 至 2026-08-13；"
    "全库 60 条、20 个省级行政区 + 全国，10 个分类均有条目"
)
meta["known_gaps"] = [
    "2026-08-13 之后至 2026-08-19 仍有少量条目未入库，下批补齐",
    "甘肃仍缺省级容量电价或项目清单类核心文件，需专项排查是否出台",
    "pv_spread（峰谷价差绝对值）仍普遍缺失，多条政策仅有浮动比例，需用代购电价折算",
    "source_url 多为北极星转载页，政府官网原文链接按新规则不再逐条追溯"
]

with io.open(mp, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

# ---- changelog ----
cp = os.path.join(DATA, "changelog.json")
cl = json.load(io.open(cp, encoding="utf-8"))
cl["logs"].append({
    "date": "2026-11-12",
    "type": "增量",
    "operator": "Aaron",
    "summary": "第1批补录：新增 35 条，时间前推至 2026-04-20",
    "added": 35,
    "updated": 0,
    "deprecated": 0,
    "detail": [
        "覆盖区间 2026-04-20 至 2026-08-13，全国 + 18 个省级行政区",
        "容量电价 6 条：新疆165/6h、吉林330/8h、青海185/8h、陕西165/6h、辽宁政策包、海南清单门槛",
        "峰谷与现货 3 条：浙江2.05:1.85:1:0.4:0.2、广东征求意见、山东市场规则",
        "辅助服务 6 条：宁夏、湖南、安徽、江苏、河北南网、山东两个细则",
        "项目清单 7 条：内蒙古2批、山西库调整、云南液流清单、陕西首批、银川、广东重点项目",
        "装机目标 4 条：新型电力系统十五五140GW、新型能源体系十五五300GW、可再生能源十五五、山西800万千瓦",
        "系统运行费 4 条：河北/辽宁第四监管周期输配电价、五省放电退减、湖南充电免输配电价",
        "配储与并网 4 条：青海配储脱钩、煤电加装储能、质量监督大纲、广东绿电直连",
        "入库判定按既定规则执行，已剔除环评公示、企业申报、矿端、充电桩等非政策条目"
    ]
})
with io.open(cp, "w", encoding="utf-8") as f:
    json.dump(cl, f, ensure_ascii=False, indent=2)

print("meta 已更新: total=%d, 区间 %s ~ %s" % (meta["total"], meta["coverage_start"], meta["coverage_end"]))
print("地区数:", len(meta["regions_covered"]))
print("状态分布:", json.dumps(counts, ensure_ascii=False))
print("changelog 条数:", len(cl["logs"]))
