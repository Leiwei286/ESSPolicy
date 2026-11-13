# -*- coding: utf-8 -*-
"""重算 data/meta.json 的计数与覆盖区间（不碰政策条目本身）

为什么单独一个脚本：
    build_data.py 只在内存里改 meta 再打进 data-bundle.js，并不回写 meta.json，
    所以每轮入库后 meta.json 的 counts 会停留在旧值。这里统一重算。

用法：
    python tools/refresh_meta.py
"""
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def main():
    with open(os.path.join(DATA, "policies.json"), "r", encoding="utf-8") as f:
        items = json.load(f)["policies"]
    mp = os.path.join(DATA, "meta.json")
    with open(mp, "r", encoding="utf-8") as f:
        meta = json.load(f)

    meta["total"] = len(items)
    meta["total_full"] = sum(1 for p in items if p.get("tier") == "full")
    meta["total_index"] = sum(1 for p in items if p.get("tier") == "index")
    meta["counts"] = {
        "by_status": dict(Counter(p["status"] for p in items)),
        "by_category": dict(Counter(p["category"] for p in items)),
        "by_region": dict(Counter(p["region"] for p in items)),
        "by_star": dict(Counter(str(p["star"]) for p in items)),
        "by_impact": dict(Counter(p["impact"] for p in items)),
        "by_channel": dict(Counter(p.get("channel", "bjx") for p in items)),
    }
    meta["coverage_start"] = min(p["publish_date"] for p in items)
    meta["coverage_end"] = max(p["publish_date"] for p in items)
    meta["regions_covered"] = sorted({p["region"] for p in items})

    # 分类清单以实际数据为准，但固定 10 类优先（看板筛选条按它排序）
    base = ["储能装机目标", "储能项目清单", "容量电价政策", "电力现货规则",
            "峰谷电价政策", "新能源配储要求", "辅助服务市场规则", "系统运行费规则",
            "并网与调度规则", "储能补贴政策"]
    present = {p["category"] for p in items}
    meta["categories"] = [c for c in base if c in present] + sorted(present - set(base))

    with open(mp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)

    print("总数 %d（全字段 %d / 索引 %d）" % (meta["total"], meta["total_full"], meta["total_index"]))
    print("区间 %s ~ %s，地区 %d 个" % (meta["coverage_start"], meta["coverage_end"], len(meta["regions_covered"])))
    print("分类：" + "、".join("%s %d" % (k, v) for k, v in
                            sorted(meta["counts"]["by_category"].items(), key=lambda x: -x[1])))
    print("来源渠道：" + "、".join("%s %d" % (k, v) for k, v in meta["counts"]["by_channel"].items()))


if __name__ == "__main__":
    main()
