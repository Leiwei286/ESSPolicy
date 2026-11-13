# -*- coding: utf-8 -*-
"""
青海容量电价 165 vs 185 口径判定补丁（2026-11-12）

判定结论（依据官方原文）：
1. 2026-02-25《关于建立青海省发电侧容量电价机制的通知(征求意见稿)》
   → 165 元/(kW·年)，高峰持续 4h，供需系数 1.04（2023-2025 需求 22102.96MW / 可靠容量 21167.93MW）
2. 2026-04-21《青海省发电侧可靠容量补偿机制(征求意见稿)》二次征求意见
   → 改为 185 元、高峰 8h、系数 0.92（2020-2025 需求 20920MW / 可靠容量 22788MW）
3. 2026-07-07 正式印发《青海省发电侧可靠容量补偿机制》(青发改价格规〔2026〕365号)
   → 185 元、8h、0.92，有效期 2026-07-07 至 2031-07-06
4. 2026-07-29《关于公布青海省发电侧容量补偿机制项目清单的通知》(青发改价格〔2026〕406号)
   → 月度标准 15.4 元/kW·月（=185/12），2026-08-01 起执行，废止青发改价格〔2023〕950号煤电容量电价

结论：165 为征求意见稿历史参数，已被 185 取代，不存在并列口径。新入库 406 号文（清单+月度+起始日）。
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

# ---------- 1. 征求意见稿（165）标记为被替代 ----------
draft = by_id["QH-20260225-01"]
draft["status"] = "被替代"
draft["superseded_by"] = "QH-20260707-01"
draft["summary"] = (
    "【已被正式稿替代，165 元作废】征求意见稿原定 2026 年统一容量补偿 165 元/(kW·年)，"
    "高峰按 4h、供需系数 1.04 折算"
)
draft["logic"] = (
    "本文件为 2026-02-25 首版征求意见稿，三项参数均与正式稿不同（标准 165→185、高峰 4h→8h、"
    "系数 1.04→0.92），不可用于测算；现行取值见 QH-20260707-01"
)
draft["metrics"]["note"] = (
    "历史版本参数：165 元/kW·年、高峰 4h、系数 1.04（2023-2025 需求 22102.96MW/可靠容量 21167.93MW）；"
    "测算禁用，改取正式稿 185 元"
)
draft["last_checked"] = TODAY
draft["note"] = (
    "保留用于制度沿革对照。正式稿 QH-20260707-01 将名称由「容量电价机制」改为「可靠容量补偿机制」，"
    "并重新统计 2020-2025 六年数据"
)

# ---------- 2. 正式稿（185）补文号、修正 note、补折算示例 ----------
final = by_id["QH-20260707-01"]
final["doc_no"] = "青发改价格规〔2026〕365号"
final["metrics"]["note"] = (
    "年度 185 元/kW；月度 15.4 元/kW（=185/12，见 QH-20260729-02）；厂用电率 10.39%；"
    "供需系数 0.92；高峰折算基准 8h"
)
final["key_points"].append(
    "折算强度全国最严之一：可靠容量系数=(1-10.39%)×Min(时长÷8,100%)，2h 储能仅 22.4%、"
    "4h 为 44.8%、8h 及以上为 89.6%；按额定功率折算的等效补偿约 38/83/152 元/(kW·年)"
)
final["key_points"].append(
    "首批清单仅纳入 1 个储能项目（格尔木宏储源 100MW/2h，核定可靠容量 22.4MW，年容量电费约 381 万元）"
)
final["logic"] = (
    "185 元/kW·年叠加 5 年有效期给出长期确定性，但青海按 8h 高峰折算，短时长储能折价极重："
    "2h 项目按额定功率计的实际补偿强度仅约 38 元/(kW·年)，与名义 185 元相差近 5 倍"
)
final["last_checked"] = TODAY
final["note"] = "机械、细节条款完整，可直接用于 IRR 测算；原始发文页待补。165 元版本见 QH-20260225-01（已替代）"

# ---------- 3. 新增 406 号文：项目清单 + 月度标准 + 执行起始日 ----------
new = {
    "id": "QH-20260729-02",
    "title": "关于公布青海省发电侧容量补偿机制项目清单的通知",
    "region": "青海",
    "level": "省级",
    "issuer": "青海省发展和改革委员会、青海省能源局",
    "doc_no": "青发改价格〔2026〕406号",
    "doc_type": "正式文件",
    "publish_date": "2026-07-29",
    "effective_date": "2026-08-01",
    "status": "现行有效",
    "superseded_by": None,
    "star": 3,
    "model_flag": "容量电价",
    "category": "容量电价政策",
    "sub_tags": ["项目清单", "月度折算", "执行起始日", "煤电容量电价废止"],
    "summary": "青海容量补偿首批清单 14 个项目，2026 年月度标准 15.4 元/kW，8 月 1 日起执行，储能仅 1 项",
    "key_points": [
        "2026 年月度统一容量补偿标准按 15.4 元/千瓦执行（年度标准 185 元/千瓦按月折算，15.4×12=184.8）",
        "本通知自 2026 年 8 月 1 日起执行，青发改价格〔2023〕950 号煤电容量电价机制废止，"
        "格尔木燃气电站容量电价条款一并废止",
        "首批清单 14 个项目：燃煤 4、燃气 1、光热 8、电网侧独立储能 1（格尔木宏储源 100MW/2h，核定可靠容量 22.4MW）",
        "2027 年度考核周期确定为 2026 年 8 月至 12 月，即 2026 年实际只执行 5 个月（15.4×5=77 元/千瓦）",
        "新增机组全容量并网后可申请纳入清单，补偿自并网投运次月起执行；退役项目自无法足额完成核定可靠容量的月份起停发",
        "项目业主主动退出可持续发展价格结算机制等其他保障政策的容量，不再纳入容量补偿范围",
    ],
    "metrics": {
        "cap_price": 185,
        "pv_spread": None,
        "storage_ratio": None,
        "duration_h": 8,
        "dispatch": None,
        "scale_gw": 0.1,
        "scale_gwh": 0.2,
        "ancillary": None,
        "note": "月度 15.4 元/kW（=185/12）；2026 年仅执行 8-12 月共 5 个月，当年实得 77 元/kW；"
                "储能清单仅 100MW/2h 一个项目",
    },
    "impact": "利多",
    "logic": (
        "机制本体之外最关键的一条执行细则：2026 年容量收入只能按 5 个月计（77 元/kW 而非 185 元/kW），"
        "按 185 元全额测算 2026 年收入会高估 2.4 倍；2027 年起才是完整年度"
    ),
    "source_url": "http://fgw.qinghai.gov.cn/zfxxgk/sdzdgknr/fgwwj_1247/202607/t20260731_92326.html",
    "source_name": "青海省发展和改革委员会",
    "bjx_url": None,
    "tier": "full",
    "first_seen": TODAY,
    "last_checked": TODAY,
    "note": "执行细则类文件，卡住 2026 年青海容量收入的时间口径；官方原文页已确认",
}

if "QH-20260729-02" not in by_id:
    pol.append(new)
    print("新增 QH-20260729-02")
else:
    pol[pol.index(by_id["QH-20260729-02"])] = new
    print("覆盖已有 QH-20260729-02")

doc["generated_at"] = "2026-11-12T19:40:00+08:00"
json.dump(doc, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("policies.json 写入完成，共", len(pol), "条")

# ---------- 4. 同步 meta 计数 ----------
mp = os.path.join(DATA, "meta.json")
meta = json.load(io.open(mp, encoding="utf-8"))
full = [p for p in pol if p.get("tier") == "full"]

cat, reg, star, imp, sta = {}, {}, {}, {}, {}
for p in pol:
    sta[p["status"]] = sta.get(p["status"], 0) + 1
for p in full:
    cat[p["category"]] = cat.get(p["category"], 0) + 1
    star[str(p["star"])] = star.get(str(p["star"]), 0) + 1
    imp[p["impact"]] = imp.get(p["impact"], 0) + 1
for p in pol:
    reg[p["region"]] = reg.get(p["region"], 0) + 1

meta["total"] = len(pol)
meta["counts"]["by_category"] = dict(sorted(cat.items(), key=lambda kv: -kv[1]))
meta["counts"]["by_region"] = dict(sorted(reg.items(), key=lambda kv: -kv[1]))
meta["counts"]["by_star"] = dict(sorted(star.items()))
meta["counts"]["by_impact"] = dict(sorted(imp.items(), key=lambda kv: -kv[1]))
meta["counts"]["by_status"] = dict(sorted(sta.items(), key=lambda kv: -kv[1]))
meta["coverage_start"] = min(p["publish_date"] for p in pol)
meta["coverage_end"] = max(p["publish_date"] for p in pol)
meta["phase"] = "第3b批已入库 + 青海容量电价口径判定（全字段 207 条 + 索引 846 条）"
meta["last_update_note"] = (
    "青海容量电价专项核对：165 与 185 元/kW·年判定为征求意见稿→正式稿替代关系，"
    "165 标记被替代；新增 406 号清单通知 1 条。全库 1053 条（全字段 207 + 索引 846）"
)
meta["known_gaps"] = [g for g in meta.get("known_gaps", []) if "青海" not in g]
meta["known_gaps"].insert(
    0,
    "青海 2027 年度容量补偿标准、容量供需系数、高峰持续时长待 2026 年底公布，届时须替换 2026 年参数",
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
    "summary": "青海容量电价 165 vs 185 元/kW·年 判定完成：征求意见稿→正式稿替代，新增 406 号清单通知",
    "added": 1,
    "updated": 2,
    "deprecated": 1,
    "detail": [
        "判定依据：2026-02-25 首版征求意见稿（165 元、高峰 4h、系数 1.04）；2026-04-21 二次征求意见改为 185 元、8h、0.92；2026-07-07 正式稿（青发改价格规〔2026〕365号）沿用 185 元、8h、0.92",
        "结论：165 为历史版本参数，已被正式稿取代，不存在并列口径；QH-20260225-01 状态改为「被替代」，superseded_by 指向 QH-20260707-01",
        "更正 QH-20260707-01 的 metrics.note：原写「实际到账约名义值 82%」易误导，82% 仅对应 8h 及以上时长项目；2h 仅 20.6%、4h 约 41%",
        "新增 QH-20260729-02《关于公布青海省发电侧容量补偿机制项目清单的通知》（青发改价格〔2026〕406号）",
        "该通知明确 2026 年月度标准 15.4 元/千瓦、2026-08-01 起执行、首批清单 14 个项目（储能仅格尔木宏储源 100MW/2h）",
        "重要执行口径：2027 年度考核周期为 2026 年 8-12 月，2026 年实际仅 5 个月，实得 77 元/千瓦，按 185 元全额测算会高估 2.4 倍",
    ],
})
json.dump(cl, io.open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("changelog.json 追加完成，共", len(cl["logs"]), "条日志")
