# -*- coding: utf-8 -*-
"""把四川《全省电网侧独立新型储能项目清单》从 SC-20261103-01 中拆出，单列为「储能项目清单」条目。

背景：该清单是川发改能源〔2026〕478号 的附件，2026-11-13 由 ima 手动源补入时被标题归一判为
同一文件，走了合并（清单数据压进 key_points）。用户要求它单列在「储能项目清单」栏目下，
故拆为 SC-20261103-02，并把主条里的清单要点改成交叉引用，避免同一事实出现两遍。
"""
import io
import json
import os

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
P = os.path.join(DATA, "policies.json")

d = json.load(io.open(P, encoding="utf-8"))
items = d["policies"]

# ---------- 1. 主条：去掉清单正文要点，改交叉引用 ----------
main = [p for p in items if p["id"] == "SC-20261103-01"][0]
LIST_KP = "同步印发《全省电网侧独立新型储能项目清单》（截至2026-09-30），共66个项目、7.16GW/16.745GWh，分建成投产/开工在建/加快前期/谋划储备四类"
NEW_KP = "同步印发《全省电网侧独立新型储能项目清单》（截至2026-09-30，66个项目、7.16GW/16.745GWh），清单本身另立条目 SC-20261103-02 记入「储能项目清单」"
if LIST_KP in main["key_points"]:
    i = main["key_points"].index(LIST_KP)
    main["key_points"][i] = NEW_KP
    print("[主条] 清单要点改为交叉引用")
else:
    print("[主条] 未找到原清单要点，跳过")
main["note"] = main["note"].replace(
    "手动源补充核对（2026-11-13-ima-项目清单.json）",
    "手动源补充核对（2026-11-13-ima-项目清单.json）；清单部分已拆为 SC-20261103-02，本条只保留 13GW/26GWh 装机目标口径")

# ---------- 2. 拆出清单条目 ----------
if any(p["id"] == "SC-20261103-02" for p in items):
    print("[清单条] 已存在，更新内容")
    new = [p for p in items if p["id"] == "SC-20261103-02"][0]
else:
    new = {"id": "SC-20261103-02"}
    items.append(new)
    print("[清单条] 新建 SC-20261103-02")

new.update({
    "title": "全省电网侧独立新型储能项目清单（截至2026-09-30）",
    "region": "四川",
    "level": "省级",
    "issuer": "四川省发展和改革委员会、四川省能源局",
    "doc_no": "川发改能源〔2026〕478号附件",
    "doc_type": "清单",
    "publish_date": "2026-11-03",
    "effective_date": "2026-11-03",
    "status": "现行有效",
    "superseded_by": "",
    "star": 3,
    "model_flag": "装机规模",
    "category": "储能项目清单",
    "sub_tags": ["电网侧独立储能", "滚动清单管理"],
    "summary": "四川随三年行动方案同步印发电网侧独立储能项目清单，66个项目、7.16GW/16.745GWh，分四类进度",
    "key_points": [
        "清单共 66 个电网侧独立新型储能项目，合计 7.16GW/16.745GWh，统计截至 2026-09-30",
        "按进度分四类：建成投产、开工在建、加快前期、谋划储备，构成四川 13GW 目标的逐年落地盘子",
        "7.16GW 已达三年新增目标 13GW 的 55%，剩余约 5.8GW 尚未落到具体项目",
        "清单附主要投资方名单，可自下而上校验装机预测，也是容量电价机制「滚动清单管理」的对象",
    ],
    "metrics": {
        "cap_price": None,
        "pv_spread": None,
        "storage_ratio": None,
        "duration_h": 2.3,
        "dispatch": None,
        "scale_gw": 7.16,
        "scale_gwh": 16.745,
        "ancillary": None,
        "note": "66个项目合计；16.745/7.16 折算平均时长约2.3小时；13GW/26GWh 三年目标见 SC-20261103-01，勿与本条相加",
    },
    "impact": "利多",
    "logic": "清单把 13GW 目标落到具体项目与业主，装机预测可自下而上校验；但已入库量仅 7.16GW，且容量电价仍处「加快建立」阶段，清单转化为开工还需电价机制配合",
    "source_url": "",
    "source_name": "四川省发展和改革委员会",
    "bjx_url": "",
    "tier": "full",
    "first_seen": "2026-11-13",
    "last_checked": "2026-11-13",
    "channel": "ima",
    "note": "478号文附件，公众号 2026-11-04 披露；与主条 SC-20261103-01（方案本体、13GW/26GWh 目标）分列，统计装机时按清单口径取本条、按目标口径取主条，不可相加",
})

# ---------- 3. 按日期重排 ----------
items.sort(key=lambda x: (x["publish_date"], x["id"]))
d["policies"] = items
json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("[完成] 全库 %d 条；四川清单类 %d 条" % (
    len(items), sum(1 for p in items if p["region"] == "四川" and p["category"] == "储能项目清单")))
