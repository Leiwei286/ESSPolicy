# -*- coding: utf-8 -*-
"""
交付前数据规范化（2026-11-12）

修复三类问题：
1. superseded_by 语义反转 6 条 —— 字段定义是「本条目被谁替代」，但原文填的是「本文件废止/替代了谁」，
   在看板上会显示成"本文件已被旧文件替代"，属实质性误导，全部清空并改写为 note。
2. metrics 结构不齐 17 条 —— 早期批次只写了有值的键，补齐 8 个固定键为 null，统一结构。
3. 生效日早于发布日 3 条 —— 属追溯执行，不是错误，在 note 注明即可。
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

METRIC_KEYS = ["cap_price", "pv_spread", "storage_ratio", "duration_h",
               "dispatch", "scale_gw", "scale_gwh", "ancillary"]

# ---------- 1. superseded_by 语义纠正 ----------
FIX_SB = {
    "GS-20251231-01": "本文件同步废止甘发改价格〔2024〕14 号煤电容量电价文件（本条目本身现行有效，未被替代）",
    "ZJ-20260528-01": "本文件废止浙发改价格〔2024〕21 号（本条目本身现行有效，未被替代）",
    "AH-20260920-01": "本文件替代皖发改能源〔2025〕568 号中的特定场景调度运行结算补偿标准（本条目本身现行有效，未被替代）",
    "HE-20261010-01": "本正式文件替代 2026-09-17《河北独立储能：共用工程建设费用、运行费用分摊方法（征求意见稿）》"
                     "（本条目本身现行有效，未被替代）",
    "CN-20261019-01": "国家级征求意见稿，拟替代发改能源规〔2023〕1217 号试行规则，尚未定稿（本条目尚未生效）",
    "GD-20261105-01": "本清单替代 2025 年 2 月版《广州市新型储能电站项目推荐布局清单》（本条目本身现行有效，未被替代）",
}
n_sb = 0
for pid, text in FIX_SB.items():
    p = by_id[pid]
    old = p.get("superseded_by")
    p["superseded_by"] = None
    base_note = str(p.get("note") or "").strip()
    if text not in base_note:
        p["note"] = (text + "；" + base_note).strip("；") if base_note else text
    p["last_checked"] = TODAY
    n_sb += 1
    print(f"[superseded_by 纠正] {pid} 原值：{old}")

# ---------- 2. metrics 结构补齐 ----------
n_m = 0
for p in pol:
    if p.get("tier") != "full":
        continue
    ms = p.setdefault("metrics", {})
    added = []
    for k in METRIC_KEYS:
        if k not in ms:
            ms[k] = None
            added.append(k)
    if added:
        n_m += 1
        print(f"[metrics 补齐] {p['id']} +{len(added)} 键")
print(f"metrics 结构补齐 {n_m} 条")

# ---------- 3. 追溯执行标注 ----------
RETRO = {
    "CN-20250113-01": "生效日 2025-01-01 早于发文日，属追溯执行",
    "NM-20250318-01": "生效日 2025-01-01 早于发文日，属追溯执行",
    "QH-20260225-01": "生效日 2026-01-01 早于发文日，属追溯执行（本条目已被正式稿替代）",
}
for pid, text in RETRO.items():
    p = by_id[pid]
    base_note = str(p.get("note") or "").strip()
    if text not in base_note:
        p["note"] = (base_note + "；" + text) if base_note else text
    print(f"[追溯执行标注] {pid}")

doc["generated_at"] = "2026-11-12T19:55:00+08:00"
json.dump(doc, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\npolicies.json 写入完成，共 {len(pol)} 条")

# ---------- 4. changelog ----------
cp = os.path.join(DATA, "changelog.json")
cl = json.load(io.open(cp, encoding="utf-8"))
cl["logs"].append({
    "date": TODAY,
    "type": "数据规范化",
    "operator": "Aaron",
    "summary": "交付前体检：修正 superseded_by 语义反转 6 条、补齐 metrics 结构 17 条、标注追溯执行 3 条",
    "added": 0,
    "updated": 26,
    "deprecated": 0,
    "detail": [
        "superseded_by 字段定义为「本条目被谁替代」，但 6 条填的是「本文件废止/替代了谁」，方向相反，看板会显示成旧文件替代新文件；已全部清空并改写进 note",
        "涉及 GS-20251231-01、ZJ-20260528-01、AH-20260920-01、HE-20261010-01、CN-20261019-01、GD-20261105-01",
        "17 条早期批次的 metrics 只写了有值的键，已补齐 cap_price/pv_spread/storage_ratio/duration_h/dispatch/scale_gw/scale_gwh/ancillary 8 个固定键（缺省 null），看板渲染逻辑不受影响",
        "3 条生效日早于发文日（CN-20250113-01、NM-20250318-01、QH-20260225-01）确认为追溯执行，非数据错误，已注明",
        "体检脚本固化于 tools/qa_check.py，可随时重跑",
    ],
})
json.dump(cl, io.open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("changelog 追加完成")
