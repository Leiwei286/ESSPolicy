# -*- coding: utf-8 -*-
"""从 _all_items.json 筛出第3批候选：非重点省 × 政策类 × 2025-01 起。

输出 data/_batch3_candidates.txt（供人工判断）+ 统计
"""
import io, json, os, re
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KEY_PROV = ["内蒙古", "新疆", "河北", "广东", "宁夏", "青海", "甘肃", "江苏", "浙江"]

# 省份识别：长名优先，避免 山西/陕西、河南/湖南/海南 混淆
PROV_PATTERNS = [
    ("黑龙江", ["黑龙江"]), ("内蒙古", ["内蒙古", "蒙西", "蒙东"]),
    ("北京", ["北京"]), ("天津", ["天津"]), ("上海", ["上海"]), ("重庆", ["重庆"]),
    ("河北", ["河北", "冀北", "冀南"]), ("山西", ["山西", "晋北"]), ("陕西", ["陕西"]),
    ("辽宁", ["辽宁"]), ("吉林", ["吉林"]), ("山东", ["山东"]), ("河南", ["河南"]),
    ("湖北", ["湖北"]), ("湖南", ["湖南"]), ("安徽", ["安徽"]), ("江苏", ["江苏"]),
    ("浙江", ["浙江"]), ("江西", ["江西"]), ("福建", ["福建"]), ("广东", ["广东", "南方区域", "南网"]),
    ("广西", ["广西"]), ("海南", ["海南"]), ("四川", ["四川"]), ("贵州", ["贵州"]),
    ("云南", ["云南"]), ("西藏", ["西藏"]), ("甘肃", ["甘肃"]), ("青海", ["青海"]),
    ("宁夏", ["宁夏"]), ("新疆", ["新疆"]),
]

# 政策正文类：命中即视为规范性/清单类文件
HIT = ["办法", "细则", "方案", "规划", "通知", "清单", "征求意见", "批复", "规则",
       "指引", "计划", "实施意见", "若干政策", "若干措施", "管理规定", "行动计划",
       "公示", "目录", "试点", "印发", "发布", "出台", "明确", "调整", "完善",
       "工作要点", "实施方案", "管理办法", "指导文件", "政策"]

# 噪音类：命中即排除（优先级高于 HIT）
DROP = ["环评", "环境影响", "招聘", "中标", "招标", "开标", "签约", "开工", "并网发电",
        "投产", "封顶", "交付", "订单", "融资", "IPO", "股价", "涨停", "业绩", "财报",
        "会议", "论坛", "峰会", "沙龙", "培训", "调研", "专访", "演讲", "致辞",
        "锂", "钴", "镍", "正极", "负极", "隔膜", "电解液", "碳酸锂", "材料",
        "回收", "拆解", "专利", "白皮书", "蓝皮书", "研报", "报告", "排名", "榜单",
        "充电桩", "充电站", "新能源车", "电动车", "汽车", "光伏组件", "风机", "逆变器",
        "火灾", "事故", "爆炸", "起火", "召回", "人事", "任免", "挂牌", "成立",
        "用地", "土地", "规划许可", "施工许可", "竣工验收", "安全评价",
        "虚拟电厂运营商", "售电公司", "公示名单（企业）"]


def prov_of(t):
    for name, keys in PROV_PATTERNS:
        for k in keys:
            if k in t:
                return name
    return None


def main():
    acc = json.load(io.open(os.path.join(BASE, "data", "_all_items.json"), encoding="utf-8"))
    rows = []
    for url, v in acc.items():
        t = v["title"]
        if v["date"] < "2025-01-01":
            continue
        p = prov_of(t)
        if p in KEY_PROV:
            continue
        dropped = any(k in t for k in DROP)
        hit = any(k in t for k in HIT)
        rows.append({
            "date": v["date"], "prov": p or "?", "title": t, "url": url,
            "hit": hit, "drop": dropped,
        })
    rows.sort(key=lambda r: (r["date"]), reverse=True)

    keep = [r for r in rows if r["hit"] and not r["drop"]]
    maybe = [r for r in rows if r["hit"] and r["drop"]]
    noprov = [r for r in keep if r["prov"] == "?"]

    lines = []
    lines.append("=" * 70)
    lines.append("第3批候选：非重点省 × 政策类 × 2025-01 起")
    lines.append("区间 %s ~ %s" % (min(r["date"] for r in rows), max(r["date"] for r in rows)))
    lines.append("总条目(2025后非重点省) %d | 建议收 %d | 疑似噪音 %d | 省份未识别 %d"
                 % (len(rows), len(keep), len(maybe), len(noprov)))
    lines.append("")
    lines.append("--- 按省份（建议收）---")
    for p, n in Counter(r["prov"] for r in keep).most_common():
        lines.append("  %-4s %d" % (p, n))
    lines.append("")
    lines.append("=" * 70)
    lines.append("【建议收】按省份分组明细")
    lines.append("=" * 70)
    byp = {}
    for r in keep:
        byp.setdefault(r["prov"], []).append(r)
    for p in sorted(byp, key=lambda x: -len(byp[x])):
        lines.append("")
        lines.append("### %s (%d 条)" % (p, len(byp[p])))
        for r in byp[p]:
            lines.append("%s | %s" % (r["date"], r["title"]))
            lines.append("       %s" % r["url"])

    lines.append("")
    lines.append("=" * 70)
    lines.append("【疑似噪音，供快速扫一眼纠错】")
    lines.append("=" * 70)
    for r in maybe:
        lines.append("%s | %s" % (r["date"], r["title"]))

    out = os.path.join(BASE, "data", "_batch3_candidates.txt")
    io.open(out, "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(lines[:40]))
    print("...")
    print("完整清单 ->", out)


if __name__ == "__main__":
    main()
