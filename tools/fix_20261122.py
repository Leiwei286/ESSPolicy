# -*- coding: utf-8 -*-
"""修正 2026-11-22 周更批次的两处规范问题。

1) 星级：库内约定 1—3 星（qa_check 硬校验），本批误用了 4/5 星。统一压回 3 星，
   需要在要点里体现重要性差异已通过 impact/logic/key_points 表达，不靠星级超范围实现。
2) 日期：本批 publish_date 统一取北极星报道日、effective_date 取印发日，
   存在 9 条「生效日早于发布日」。这不是追溯执行，而是报道滞后，需在 note 中说明，
   并让 qa_check 能识别这种情形（与「追溯执行」区分开）。
"""
import io
import json

P = "data/policies.json"
IDS = ["CN-20261113-01", "CN-20261119-01", "NM-20261118-01", "NM-20261119-01",
       "TJ-20261116-01", "JX-20261113-01", "HI-20261113-01", "FJ-20261112-01",
       "SH-20261117-01", "HA-20261117-01", "AH-20261112-01", "SD-20261120-01",
       "SN-20261118-01", "SX-20261120-01", "SD-20260807-01"]

DATE_NOTE = ("【日期口径】publish_date 取北极星/公众号报道日，effective_date 取文件印发（落款）日，"
             "前者晚于后者属报道滞后，非追溯执行。")


def main():
    d = json.load(io.open(P, encoding="utf-8"))
    items = d["policies"]
    fixed_star, fixed_date = [], []

    for p in items:
        if p["id"] not in IDS:
            continue
        # 1) 星级压回上限 3
        if p.get("star") not in (1, 2, 3):
            p["star"] = 3
            fixed_star.append(p["id"])
        # 2) 生效日早于发布日的，补日期口径说明
        ed = p.get("effective_date")
        if ed and ed < p["publish_date"] and "报道日" not in str(p.get("note") or ""):
            p["note"] = (p["note"].rstrip("。") + "。" + DATE_NOTE)
            fixed_date.append(p["id"])

    json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("星级修正 %d 条：%s" % (len(fixed_star), "、".join(fixed_star)))
    print("日期说明补齐 %d 条：%s" % (len(fixed_date), "、".join(fixed_date)))


if __name__ == "__main__":
    main()
