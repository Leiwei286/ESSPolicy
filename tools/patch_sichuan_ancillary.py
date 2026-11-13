# -*- coding: utf-8 -*-
"""
四川调峰 350 vs 400 元/MWh 口径判定补丁（2026-11-12）

判定结论：
1. 400 元/MWh = 2026-02-14《四川省电力辅助服务管理实施细则(征求意见稿)》的独立储能调峰补偿标准
   → 已被 2026-04-13 正式稿下调至 350 元/MWh，作废
2. 350 元/MWh 有两个不同出处，含义不同，不可混用：
   a) 2025-12-12《四川电力辅助服务市场交易实施细则》(川监能市场〔2025〕126号)
      —— 低谷调峰市场「申报价格上限」初设 350 元/MWh，属竞价上限，非补偿标准；
         且现货市场结算（试）运行期间该市场不再运行
   b) 2026-04-13《四川省电力辅助服务管理实施细则》正式稿
      —— 独立储能调峰「补偿标准」350 元/MWh，按充电电量补偿，2026-05-01 起实施
3. 因此不是"两个版本打对不平"，而是三类口径：竞价上限 / 固定补偿 / 已作废的征求意见值
"""
import io
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
P = os.path.join(DATA, "policies.json")

doc = json.load(io.open(P, encoding="utf-8"))
pol = doc["policies"]
by_id = {p["id"]: p for p in pol}
TODAY = "2026-11-12"

# ---------- 1. 126 号文：澄清 350 的性质 ----------
mkt = by_id["SC-20251223-01"]
mkt["summary"] = (
    "四川低谷调峰市场独立储能申报价格上限350元/MWh（竞价上限，非补偿标准）、调频5元/MW，独立储能须≥5MW/1h"
)
mkt["key_points"][0] = (
    "低谷调峰市场：独立储能、虚拟电厂申报价格上限初设 350 元/MWh，报价不分成、按报价由低到高出清；"
    "燃煤机组同为 350 元/MWh、燃气机组 80 元/MWh"
)
mkt["logic"] = (
    "这是市场竞价的价格天花板，不是到手补偿：实际补偿由出清价决定，且现货市场结算（试）运行期间"
    "低谷调峰市场直接停运，所以不能把 350 元/MWh 当成储能稳定收益项"
)
mkt["metrics"]["note"] = (
    "350 元/MWh 为低谷调峰市场申报价格上限（初设值），非补偿标准；现货结算（试）运行期间该市场不再运行"
)
mkt["note"] = (
    "文件落款 2025-12-12，四川电力交易中心 12-19 转发，北极星 12-23 报道。"
    "此处 350 元/MWh 与正式稿《四川省电力辅助服务管理实施细则》(SC-20260413-01) 的调峰补偿 350 元/MWh "
    "分属两套机制（一为竞价上限、一为按充电量固定补偿），数值相同但不可混用"
)
mkt["last_checked"] = TODAY

# ---------- 2. 征求意见稿（400）标记被替代 ----------
draft = by_id["SC-20260214-01"]
draft["status"] = "被替代"
draft["superseded_by"] = "SC-20260413-01"
draft["star"] = 1
draft["summary"] = (
    "【已被正式稿替代，400 元作废】征求意见稿拟按充电量补偿独立储能 400 元/MWh，"
    "配建储能分 80/160 元两档"
)
draft["metrics"]["note"] = (
    "历史版本参数：400 元/MWh；正式稿（SC-20260413-01）下调至 350 元，配建由 80/160 两档降为 40 元"
)
draft["logic"] = (
    "征求意见稿三项标准均高于正式稿（400→350、配建 80/160→40、取消中间档），"
    "仅用于观察监管取向变化，测算不可取 400"
)
draft["note"] = "征求意见稿，2026-04-13 正式印发版本显著下调，测算禁用；正式稿见 SC-20260413-01"
draft["last_checked"] = TODAY

# ---------- 3. 新增正式稿 ----------
new = {
    "id": "SC-20260413-01",
    "title": "四川省电力辅助服务管理实施细则",
    "region": "四川",
    "level": "省级",
    "issuer": "国家能源局四川监管办公室",
    "doc_no": "待核实",
    "doc_type": "正式文件",
    "publish_date": "2026-04-13",
    "effective_date": "2026-05-01",
    "status": "现行有效",
    "superseded_by": None,
    "star": 3,
    "model_flag": "调用与结算",
    "category": "辅助服务市场规则",
    "sub_tags": ["调峰补偿", "按充电量补偿", "两个细则", "配储调峰", "一次调频"],
    "summary": "四川独立储能调峰按充电量补 350 元/MWh（较征求意见降 50 元），配建储能降至 40 元/MWh 并设补偿电量上限",
    "key_points": [
        "独立新型储能调峰补偿：因系统调峰需求下达调度计划（含调度指令）要求进入充电状态时，"
        "对其充电电量补偿 350 元/MWh（征求意见稿为 400 元，正式稿下调 50 元）",
        "新能源配建储能调峰补偿大幅收紧：月度累计充电量 > 额定容量×30h 才予补偿，标准 40 元/MWh，"
        "补偿电量上限为额定容量×60（征求意见稿为 80/160 元两档，无电量上限）",
        "纳入本细则的独立新型储能容量门槛 10MW/20MWh，压缩空气、飞轮等独立新型储能参照执行",
        "一次调频补偿小扰动 200 元/MWh、大扰动 1000 元/MWh；AGC 6 元/MW、APC 按实际调节里程 6 元/MW、"
        "爬坡 40 元/MW、转动惯量 100 元/Mvar、有偿无功 50 元/Mvarh",
        "自 2026 年 5 月 1 日起实施；辅助服务补偿费用由发电侧并网主体、新型储能按上网电量比例分摊",
    ],
    "metrics": {
        "cap_price": None,
        "pv_spread": None,
        "storage_ratio": None,
        "duration_h": None,
        "dispatch": None,
        "scale_gw": None,
        "scale_gwh": None,
        "ancillary": 350,
        "note": "独立储能按充电电量 350 元/MWh；配建 40 元/MWh（充电量>额定容量×30h，补偿电量上限×60）；"
                "门槛 10MW/20MWh",
    },
    "impact": "利多",
    "logic": (
        "350 元/MWh 折 0.35 元/kWh，相当于给充电侧成本打掉约三分之一到一半，是四川独立储能收益的重要一项；"
        "但只在调度指令要求充电时才算，且配建储能几乎被削平（40 元 + 电量上限），政策明确向独立储能倾斜"
    ),
    "source_url": None,
    "source_name": "国家能源局四川监管办公室",
    "bjx_url": "https://news.bjx.com.cn/html/20260414/1491892.shtml",
    "tier": "full",
    "first_seen": TODAY,
    "last_checked": TODAY,
    "note": "正式稿将征求意见稿 400 元下调至 350 元；与川监能市场〔2025〕126号的低谷调峰市场 350 元"
            "（申报价格上限）是两套机制，数值巧合不可混用",
}

if "SC-20260413-01" not in by_id:
    pol.append(new)
    print("新增 SC-20260413-01")
else:
    pol[pol.index(by_id["SC-20260413-01"])] = new
    print("覆盖已有 SC-20260413-01")

doc["generated_at"] = "2026-11-12T19:50:00+08:00"
json.dump(doc, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("policies.json 写入完成，共", len(pol), "条")

# ---------- 4. meta 计数 ----------
mp = os.path.join(DATA, "meta.json")
meta = json.load(io.open(mp, encoding="utf-8"))
full = [p for p in pol if p.get("tier") == "full"]
cat, reg, star, imp, sta = {}, {}, {}, {}, {}
for p in pol:
    sta[p["status"]] = sta.get(p["status"], 0) + 1
    reg[p["region"]] = reg.get(p["region"], 0) + 1
for p in full:
    cat[p["category"]] = cat.get(p["category"], 0) + 1
    star[str(p["star"])] = star.get(str(p["star"]), 0) + 1
    imp[p["impact"]] = imp.get(p["impact"], 0) + 1

meta["total"] = len(pol)
meta["counts"]["by_category"] = dict(sorted(cat.items(), key=lambda kv: -kv[1]))
meta["counts"]["by_region"] = dict(sorted(reg.items(), key=lambda kv: -kv[1]))
meta["counts"]["by_star"] = dict(sorted(star.items()))
meta["counts"]["by_impact"] = dict(sorted(imp.items(), key=lambda kv: -kv[1]))
meta["counts"]["by_status"] = dict(sorted(sta.items(), key=lambda kv: -kv[1]))
meta["coverage_start"] = min(p["publish_date"] for p in pol)
meta["coverage_end"] = max(p["publish_date"] for p in pol)
meta["phase"] = "第3b批已入库 + 青海/四川两项口径判定（全字段 208 条 + 索引 846 条）"
meta["last_update_note"] = (
    "四川调峰口径判定：400 元为征求意见稿已作废，正式稿 350 元按充电量补偿（2026-05-01 实施）；"
    "与 126 号文低谷调峰市场 350 元竞价上限分属两套机制。全库 1054 条（全字段 208 + 索引 846）"
)
json.dump(meta, io.open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("meta.json 更新完成：total", meta["total"], "| 全字段", len(full))

# ---------- 5. changelog ----------
cp = os.path.join(DATA, "changelog.json")
cl = json.load(io.open(cp, encoding="utf-8"))
cl["logs"].append({
    "date": TODAY,
    "type": "口径修正",
    "operator": "Aaron",
    "summary": "四川调峰 350 vs 400 元/MWh 判定完成：400 为征求意见稿已作废，正式稿 350 元；新增正式稿条目",
    "added": 1,
    "updated": 2,
    "deprecated": 1,
    "detail": [
        "400 元/MWh 出自 2026-02-14《四川省电力辅助服务管理实施细则(征求意见稿)》，已被 2026-04-13 正式稿下调至 350 元，SC-20260214-01 状态改为「被替代」",
        "350 元/MWh 有两个出处且含义不同：川监能市场〔2025〕126号为低谷调峰市场「申报价格上限」；2026-04-13 正式稿为「按充电量补偿标准」，2026-05-01 起实施",
        "新增 SC-20260413-01《四川省电力辅助服务管理实施细则》正式稿：独立储能 350 元/MWh、配建储能 40 元/MWh（充电量>额定容量×30h，补偿电量上限×60）、门槛 10MW/20MWh",
        "正式稿对配建储能削减幅度大于独立储能：配建由 80/160 两档降至 40 元且加设电量上限，政策明确向独立储能倾斜",
        "修正 SC-20251223-01 的 summary/note：原把市场竞价上限当作调峰补偿写入，易与正式稿 350 元混淆；补注「现货结算（试）运行期间低谷调峰市场不再运行」",
        "全库 1054 条（全字段 208 + 索引 846）",
    ],
})
json.dump(cl, io.open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("changelog.json 追加完成，共", len(cl["logs"]), "条日志")
