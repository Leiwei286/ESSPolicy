# -*- coding: utf-8 -*-
"""补齐手动源入库后体检发现的两类问题

1. 4 条要点只有 2 条（规则要求 3-7 条），补 1 条折算类要点
2. SC-20261103-01 合并后 8 条要点超上限，把两条清单要点合并为一条
"""
import io
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "policies.json")

with io.open(P, encoding="utf-8") as f:
    pol = json.load(f)
items = {p["id"]: p for p in pol["policies"]}

ADD = {
    "HI-20260126-01": "7个项目合计6.8GWh，按项目数折算单体约0.97GWh，属重大项目层级但单体偏小",
    "GZ-20260301-01": "6.1GW/12.5GWh 按容量除以功率折算，平均时长约2.05小时",
    "HUB-20260317-01": "595MWh÷498MW 折算配储时长约1.2小时，以短时配储为主",
    "CQ-20260407-01": "储能未单列项目清单，散见于风光储一体化项目，需回溯通知附表才能取数",
}
ADD2 = {
    "CQ-20260407-01": "由市政府办公厅以渝府办发〔2026〕16号印发，属市级重点项目年度实施安排，含要素保障与进度考核要求",
}

for pid, txt in ADD.items():
    p = items[pid]
    if txt not in p["key_points"]:
        p["key_points"].append(txt)
for pid, txt in ADD2.items():
    p = items[pid]
    if txt not in p["key_points"]:
        p["key_points"].append(txt)

# 四川：两条清单要点合并为一条，压回 7 条
sc = items["SC-20261103-01"]
merged_kp = ("同步印发《全省电网侧独立新型储能项目清单》（截至2026-09-30），"
             "共66个项目、7.16GW/16.745GWh，分建成投产/开工在建/加快前期/谋划储备四类")
new_kps = []
for k in sc["key_points"]:
    if k.startswith("同步印发《全省电网侧独立新型储能项目清单》") or k.startswith("清单涵盖建成投产"):
        if merged_kp not in new_kps:
            new_kps.append(merged_kp)
    else:
        new_kps.append(k)
sc["key_points"] = new_kps

shutil.copy2(P, os.path.join(ROOT, "data", "policies.backup-要点补齐.json"))
with io.open(P, "w", encoding="utf-8") as f:
    json.dump(pol, f, ensure_ascii=False, indent=1)

for pid in ["HI-20260126-01", "GZ-20260301-01", "HUB-20260317-01", "CQ-20260407-01", "SC-20261103-01"]:
    print(pid, "→", len(items[pid]["key_points"]), "条")
