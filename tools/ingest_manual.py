# -*- coding: utf-8 -*-
"""
手动收集政策入库器（ima / 手工整理 → policies.json）

背景
----
用户会把自己手动收集的政策放到 ima 的
「太和致远实习/储能/储能政策汇总/储能政策手动收集」，
或直接丢进本项目 manual/inbox/。这些内容与北极星抓取的内容必然大量重叠，
所以入库前必须先做去重与口径冲突检测，否则看板会出现一稿多条、
以及同一指标两个数字并存（青海 165/185、四川 350/400 就是这么来的）。

用法
----
    python tools/ingest_manual.py                 # 只看报告，不写盘（默认）
    python tools/ingest_manual.py --apply         # 去重后合并 + 更新 meta/changelog + 归档
    python tools/ingest_manual.py --apply --no-build   # 合并但不重新打包 data-bundle.js

输入
----
manual/ready/*.json，每个文件可以是：
    - 一个条目对象 {...}
    - 条目数组 [{...}, {...}]
    - {"items": [{...}]}
字段名与 data/policies.json 完全一致（见 docs/看板说明 字段字典）。
必填：title / region / level / issuer / publish_date / category
未填的字段按默认值补齐，metrics 会补全 8 个固定键。

去重命中顺序
----
1. bjx_url 完全相同
2. source_url 完全相同
3. 归一化标题完全相同（去书名号、标点、「关于…的通知」外壳）
4. region + doc_no 相同（doc_no 非空且非「—/待核实」）
命中即判重复，不重复入库，只把新链接/新要点并入旧条目 note。

冲突检测
----
对「疑似同一政策」的两条（去重命中 或 同省同分类且标题相似度≥0.75），
逐项比对 cap_price / duration_h / ancillary / storage_ratio / dispatch：
    - 两边都有值且不同 → 口径冲突（需人工判定哪个是现行有效值）
    - 一边有一边空     → 信息补全建议（默认只提示、不写入，确认单位口径后加 --fill）
另外对 cap_price 做量级体检：数值 < 10 一律视为元/kWh（按充放电量）口径而非元/kW·年，
直接报冲突——内蒙古 0.35 元/kWh 与 165 元/kW·年混用会让测算差一个量级。
这一条是硬要求：宁可报告冲突，也不要静默覆盖。
"""
import argparse
import datetime as dt
import difflib
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
MANUAL = os.path.join(ROOT, "manual")
READY = os.path.join(MANUAL, "ready")
ARCHIVE = os.path.join(MANUAL, "archive")
REPORTS = os.path.join(MANUAL, "reports")

METRIC_KEYS = ["cap_price", "pv_spread", "storage_ratio", "duration_h",
               "dispatch", "scale_gw", "scale_gwh", "ancillary", "note"]
COMPARE_KEYS = ["cap_price", "duration_h", "ancillary", "storage_ratio", "dispatch"]
METRIC_LABEL = {"cap_price": "容量电价(元/kW·年)", "duration_h": "时长(h)",
                "ancillary": "辅助服务补偿", "storage_ratio": "配储比例(%)",
                "dispatch": "调用/结算"}

STATUS_SET = {"现行有效", "征求意见", "已废止", "被替代", "已失效", "历史索引"}
CATEGORY_SET = {"储能项目清单", "容量电价政策", "辅助服务市场规则", "峰谷电价政策",
                "新能源配储要求", "电力现货规则", "储能装机目标", "系统运行费规则",
                "并网与调度规则", "储能补贴政策", "其他"}
IMPACT_SET = {"利多", "利空", "中性"}
LEVEL_SET = {"国家", "省级", "市级"}
MODEL_SET = {"无", "容量电价", "价差", "调用与结算", "配储比例", "装机规模"}
# 来源渠道：bjx=北极星主源 / ima=用户手动收集文件夹 / wx_espm=公众号「储能与电力市场」/ official=官网直取
CHANNEL_SET = {"bjx", "ima", "wx_espm", "official"}
CHANNEL_LABEL = {"bjx": "北极星储能网", "ima": "ima 手动收集", "wx_espm": "公众号：储能与电力市场",
                 "official": "官网直取"}
# 历史数据里出现过的非标准分类别名 → 标准值
CATEGORY_ALIAS = {"辅助服务市场": "辅助服务市场规则"}
DOC_TYPE_ALIAS = {"工作方案": "方案"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PUNCT = re.compile(r"[《》〈〉「」『』（）()【】\[\]{}·、，,。.：:；;！!？?—－\-_/\\|\"'“”‘’\s\u3000]")
SHELL_PREFIX = ("关于", "印发", "转发", "公布", "发布", "关于印发")
SHELL_SUFFIX = ("的通知", "的函", "的公告", "的意见", "的批复", "的公告的通知")


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def norm_title(t):
    """标题归一化：只用于比对，不用于展示。

    顺序很重要：必须先去标点（含书名号），再剥「关于…」外壳。
    否则「《关于XX的公示》」里的「关于」会被书名号挡住，与「关于XX的公示」判成不同标题。
    """
    if not t:
        return ""
    s = PUNCT.sub("", str(t))
    for p in SHELL_PREFIX:
        if s.startswith(p):
            s = s[len(p):]
            break
    for suf in SHELL_SUFFIX:
        if s.endswith(suf):
            s = s[: -len(suf)]
            break
    # 去掉年份变体与「（试行/征求意见稿）」等版本后缀，避免同一文件不同版本被判同一条
    s = re.sub(r"^\d{4}年?", "", s)
    return s


def similar(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def region_code_map(items):
    """从既有数据里学出 region → 2~3 位 id 前缀。"""
    from collections import Counter
    bucket = {}
    for p in items:
        code = str(p["id"]).split("-")[0]
        bucket.setdefault(p["region"], Counter())[code] += 1
    m = {r: c.most_common(1)[0][0] for r, c in bucket.items()}
    m.setdefault("全国", "CN")
    # 常见补充，避免新省份无前缀
    m.update({"北京": "BJ", "天津": "TJ", "上海": "SH", "重庆": "CQ", "河北": "HE",
              "山西": "SX", "内蒙古": "NM", "辽宁": "LN", "吉林": "JL", "黑龙江": "HL",
              "江苏": "JS", "浙江": "ZJ", "安徽": "AH", "福建": "FJ", "江西": "JX",
              "山东": "SD", "河南": "HA", "湖北": "HUB", "湖南": "HN", "广东": "GD",
              "广西": "GX", "海南": "HI", "四川": "SC", "贵州": "GZ", "云南": "YN",
              "西藏": "XZ", "陕西": "SN", "甘肃": "GS", "青海": "QH", "宁夏": "NX",
              "新疆": "XJ"})
    return m


def normalize(item, code_map, today, default_channel="ima"):
    """补默认值 + 别名归一 + 类型清洗。返回 (item, errors)。"""
    errors = []
    it = dict(item or {})
    it.setdefault("doc_no", "—")
    it.setdefault("doc_type", "正式文件")
    it.setdefault("effective_date", "待核实")
    it.setdefault("status", "现行有效")
    it.setdefault("superseded_by", "")
    it.setdefault("star", 2)
    it.setdefault("model_flag", "无")
    it.setdefault("sub_tags", [])
    it.setdefault("key_points", [])
    it.setdefault("impact", "中性")
    it.setdefault("logic", "")
    it.setdefault("source_url", "")
    it.setdefault("source_name", "")
    it.setdefault("bjx_url", "")
    it.setdefault("tier", "full")
    it.setdefault("first_seen", today)
    it.setdefault("last_checked", today)
    it.setdefault("note", "")
    it.setdefault("channel", default_channel)
    it.setdefault("summary", "")

    for k in ("title", "region", "level", "issuer", "publish_date", "category"):
        if not str(it.get(k) or "").strip():
            errors.append("缺少必填字段 %s" % k)

    # 别名归一
    it["category"] = CATEGORY_ALIAS.get(it["category"], it["category"])
    it["doc_type"] = DOC_TYPE_ALIAS.get(it["doc_type"], it["doc_type"])
    if it["doc_no"] in ("", None):
        it["doc_no"] = "—"
    if it["superseded_by"] is None:
        it["superseded_by"] = ""

    # 枚举校验
    if it["status"] not in STATUS_SET:
        errors.append("status 非法值：%s" % it["status"])
    if it["category"] not in CATEGORY_SET:
        errors.append("category 非法值：%s" % it["category"])
    if it["impact"] not in IMPACT_SET:
        errors.append("impact 非法值：%s" % it["impact"])
    if it["level"] not in LEVEL_SET:
        errors.append("level 非法值：%s" % it["level"])
    if it["model_flag"] not in MODEL_SET:
        errors.append("model_flag 非法值：%s" % it["model_flag"])
    if it["tier"] not in ("full", "index"):
        errors.append("tier 非法值：%s" % it["tier"])
    if it["channel"] not in CHANNEL_SET:
        errors.append("channel 非法值：%s（可选：%s）" % (it["channel"], "、".join(sorted(CHANNEL_SET))))
    if not DATE_RE.match(str(it["publish_date"])):
        errors.append("publish_date 不是 YYYY-MM-DD：%s" % it["publish_date"])
    ed = str(it.get("effective_date") or "")
    if ed and ed != "待核实" and not DATE_RE.match(ed):
        errors.append("effective_date 既不是 YYYY-MM-DD 也不是「待核实」：%s" % ed)

    # 星级
    try:
        it["star"] = int(it["star"])
    except Exception:
        errors.append("star 不是整数：%r" % it.get("star"))
        it["star"] = 2
    if it["star"] not in (1, 2, 3):
        errors.append("star 超出 1-3：%s" % it["star"])
    if it["tier"] == "index" and it["star"] > 2:
        errors.append("索引层条目星级不得为 3")

    # 列表字段
    if isinstance(it["sub_tags"], str):
        it["sub_tags"] = [x.strip() for x in re.split(r"[、,，/]", it["sub_tags"]) if x.strip()]
    if isinstance(it["key_points"], str):
        it["key_points"] = [x.strip() for x in str(it["key_points"]).split("\n") if x.strip()]
    if not isinstance(it["key_points"], list) or not isinstance(it["sub_tags"], list):
        errors.append("key_points / sub_tags 必须是数组或换行/顿号分隔的字符串")

    # metrics 补齐 8 键
    mk = dict(it.get("metrics") or {})
    for k in mk:
        if k not in METRIC_KEYS:
            errors.append("metrics 出现未定义键：%s（固定键见字段字典）" % k)
    clean = {}
    for k in METRIC_KEYS:
        v = mk.get(k)
        if v in ("", "None"):
            v = None
        if k != "note" and isinstance(v, str):
            try:
                v = float(v) if "." in v else int(v)
            except ValueError:
                errors.append("metrics.%s 不是数值：%r" % (k, v))
                v = None
        clean[k] = v
    it["metrics"] = clean

    # 全字段条目底线：summary 与 key_points 不能都空
    if it["tier"] == "full" and not str(it["summary"]).strip() and not it["key_points"]:
        errors.append("全字段条目 summary 与 key_points 同时为空（要么补内容，要么置 tier=index）")

    it["_norm_title"] = norm_title(it["title"])
    it["_code"] = code_map.get(it["region"], "CN")
    return it, errors


def build_index(items):
    by_bjx, by_src, by_title, by_docno = {}, {}, {}, {}
    for p in items:
        pid = p["id"]
        if p.get("bjx_url"):
            by_bjx.setdefault(p["bjx_url"].strip(), []).append(pid)
        if p.get("source_url"):
            by_src.setdefault(p["source_url"].strip(), []).append(pid)
        nt = norm_title(p["title"])
        if nt:
            by_title.setdefault(nt, []).append(pid)
        dn = str(p.get("doc_no") or "").strip()
        if dn and dn not in ("—", "待核实"):
            by_docno.setdefault((p["region"], dn), []).append(pid)
    return by_bjx, by_src, by_title, by_docno


def find_dup(it, items, idx):
    by_bjx, by_src, by_title, by_docno = idx
    by_id = {p["id"]: p for p in items}
    checks = []
    if it.get("bjx_url"):
        checks.append(("bjx_url 相同", by_bjx.get(it["bjx_url"].strip(), [])))
    if it.get("source_url"):
        checks.append(("source_url 相同", by_src.get(it["source_url"].strip(), [])))
    if it["_norm_title"]:
        checks.append(("标题归一一致", by_title.get(it["_norm_title"], [])))
    dn = str(it.get("doc_no") or "").strip()
    if dn and dn not in ("—", "待核实"):
        checks.append(("同省同文号", by_docno.get((it["region"], dn), [])))
    for reason, ids in checks:
        ids = [i for i in ids if i in by_id]
        if ids:
            return reason, by_id[ids[0]]
    return None, None


def find_similar(it, items, threshold=0.75):
    """同省同分类、标题相似的条目（用于冲突比对，即使未命中硬去重）。"""
    out = []
    for p in items:
        if p["region"] != it["region"] or p["category"] != it["category"]:
            continue
        r = similar(it["_norm_title"], norm_title(p["title"]))
        if r >= threshold:
            out.append((r, p))
    out.sort(key=lambda x: -x[0])
    return out[:3]


def compare_metrics(new, old):
    """返回 (冲突列表, 补全列表)。

    注意：cap_price 的补全建议要过单位体检。内蒙古 0.35 元/kWh（按放电量）
    与 165 元/kW·年（按额定功率）是两种口径，混填会让测算差一个量级。
    """
    conflicts, fills = [], []
    nm, om = new.get("metrics") or {}, old.get("metrics") or {}
    for k in COMPARE_KEYS:
        a, b = nm.get(k), om.get(k)
        if a is None and b is None:
            continue
        if k == "cap_price" and a is not None:
            try:
                if 0 < float(a) < 10:
                    conflicts.append("cap_price 新值 %s 量级异常，疑为元/kWh（按充放电量）口径，"
                                     "元/kW·年正常在 100-400 区间，先确认单位再入库" % a)
                    continue
            except (TypeError, ValueError):
                pass
        if a is not None and b is None:
            fills.append("%s：旧条目空 → 新值 %s" % (METRIC_LABEL[k], a))
        elif a is not None and b is not None and str(a) != str(b):
            conflicts.append("%s：库里 %s vs 手动源 %s" % (METRIC_LABEL[k], b, a))
    return conflicts, fills


def merge_note(old, new, source_label, allow_fill=False):
    """把新来源与新增要点并入旧条目。

    默认不覆盖也不自动补指标：数值写入必须人工确认（--fill）。
    链接、文号、生效日、要点属于事实性补充，可以直接并入。
    """
    old_note = str(old.get("note") or "").strip()
    add = []
    if new.get("bjx_url") and not old.get("bjx_url"):
        old["bjx_url"] = new["bjx_url"]
    if new.get("source_url") and not old.get("source_url"):
        old["source_url"] = new["source_url"]
    if new.get("doc_no") not in (None, "", "—") and old.get("doc_no") in (None, "", "—"):
        old["doc_no"] = new["doc_no"]
    if new.get("effective_date") not in (None, "", "待核实") and old.get("effective_date") in (None, "", "待核实"):
        old["effective_date"] = new["effective_date"]
    # 指标只补空，不覆盖，且默认需 --fill 才写
    if allow_fill:
        for k in COMPARE_KEYS:
            if old["metrics"].get(k) is None and new["metrics"].get(k) is not None:
                old["metrics"][k] = new["metrics"][k]
        if new.get("metrics", {}).get("note") and not old["metrics"].get("note"):
            old["metrics"]["note"] = new["metrics"]["note"]
    # 要点取并集（去重）
    for kp in new.get("key_points") or []:
        if kp and kp not in (old.get("key_points") or []):
            if len(old.setdefault("key_points", [])) < 8:
                old["key_points"].append(kp)
                add.append(kp)
    if source_label not in old_note:
        old["note"] = (old_note + "；" if old_note else "") + "手动源补充核对（%s）" % source_label
    old["last_checked"] = dt.date.today().isoformat()
    return old


def next_id(it, items, code_map):
    """生成不冲突的 id。"""
    base = "%s-%s" % (it["_code"], str(it["publish_date"]).replace("-", ""))
    used = {p["id"] for p in items}
    n = 1
    while True:
        cand = "%s-%02d" % (base, n)
        if cand not in used:
            return cand
        n += 1


def read_ready():
    files = sorted(glob.glob(os.path.join(READY, "*.json")))
    raw, bad = [], []
    for fp in files:
        d = load_json(fp, None)
        if d is None:
            bad.append((os.path.basename(fp), "JSON 解析失败"))
            continue
        if isinstance(d, dict) and "items" in d:
            d = d["items"]
        rows = d if isinstance(d, list) else [d]
        for i, r in enumerate(rows):
            if not isinstance(r, dict):
                bad.append((os.path.basename(fp), "第 %d 项不是对象" % (i + 1)))
                continue
            r["_src_file"] = os.path.basename(fp)
            raw.append(r)
    return files, raw, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正写盘（默认只出报告）")
    ap.add_argument("--no-build", action="store_true", help="不重新打包 data-bundle.js")
    ap.add_argument("--channel", default="ima", choices=sorted(CHANNEL_SET),
                    help="来源渠道标记，写进条目的 channel 字段（默认 ima）")
    ap.add_argument("--fill", action="store_true",
                    help="允许把「旧条目为空」的指标补进旧条目（默认只提示不写，防口径混用）")
    args = ap.parse_args()

    os.makedirs(READY, exist_ok=True)
    os.makedirs(ARCHIVE, exist_ok=True)
    os.makedirs(REPORTS, exist_ok=True)

    today = dt.date.today().isoformat()
    pol = load_json(os.path.join(DATA, "policies.json"))
    items = pol["policies"]
    code_map = region_code_map(items)
    idx = build_index(items)

    files, raw, bad = read_ready()
    print("=" * 72)
    print("手动源入库自检  %s   （%s 模式）" % (today, "落盘" if args.apply else "试运行"))
    print("=" * 72)
    print("待处理文件 %d 个，条目 %d 条，来源渠道：%s" % (
        len(files), len(raw), CHANNEL_LABEL.get(args.channel, args.channel)))
    if not files:
        print("\nmanual/ready/ 为空。把整理好的 JSON 放进去再跑，")
        print("或把原始文件放到 manual/inbox/ 后由助手提取成 ready JSON。")
        return

    accepted, dups, errs, conflicts, fills, need_check = [], [], [], [], [], []

    for r in raw:
        it, e = normalize(r, code_map, today, args.channel)
        label = "%s ｜ %s" % (it.get("region", "?"), str(it.get("title", "?"))[:40])
        if e:
            errs.append((label, e))
            continue
        reason, old = find_dup(it, items, idx)
        if old:
            c, f = compare_metrics(it, old)
            dups.append((label, reason, old["id"], old["title"][:34]))
            if c:
                conflicts.append((label, old["id"], c))
            if f:
                fills.append((label, old["id"], f))
            it["_dup_of"] = old["id"]
            accepted.append(it)          # 仍需并入 note / 补空
            continue
        # 未命中硬去重，但可能同省同分类高度相似 → 提冲突（不合并）
        sim = find_similar(it, items)
        for ratio, p in sim:
            c, f = compare_metrics(it, p)
            if c:
                conflicts.append((label, p["id"], c + ["标题相似度 %.2f，疑似同一政策的不同版本" % ratio]))
                need_check.append((label, p["id"], ratio))
        accepted.append(it)

    newly = [x for x in accepted if not x.get("_dup_of")]

    # ---------- 报告 ----------
    print("\n[1] 格式校验")
    if errs:
        for label, e in errs:
            print("  ✗ %s" % label)
            for x in e:
                print("      - %s" % x)
    else:
        print("  通过")

    print("\n[2] 重复判定：%d 条命中既有库" % len(dups))
    for label, reason, oid, otitle in dups:
        print("  = %s" % label)
        print("      命中方式：%s → %s（%s）" % (reason, oid, otitle))

    print("\n[3] 真正新增：%d 条" % len(newly))
    for x in newly:
        print("  + %s ｜ %s ｜ %s ｜ %s" % (x["publish_date"], x["region"], x["category"], x["title"][:46]))

    print("\n[4] 口径冲突（需人工判定，脚本不会自动选值）：%d 项" % len(conflicts))
    for label, oid, c in conflicts:
        print("  ! %s  → %s" % (label, oid))
        for x in c:
            print("      %s" % x)

    print("\n[5] 指标补全建议：%d 项%s" % (len(fills), "" if args.fill else "（默认不写，确认口径后加 --fill）"))
    for label, oid, f in fills:
        print("  ~ %s → %s" % (label, oid))
        for x in f:
            print("      %s" % x)

    if bad:
        print("\n[6] 读取失败文件")
        for f, why in bad:
            print("  ✗ %s：%s" % (f, why))

    # ---------- 写盘 ----------
    if not args.apply:
        print("\n" + "-" * 72)
        print("试运行结束，未改动任何数据。确认无误后加 --apply 落盘。")
        return

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(DATA, "policies.backup-manual-%s.json" % stamp)
    shutil.copy2(os.path.join(DATA, "policies.json"), backup)
    print("\n[落盘] 备份 → %s" % os.path.basename(backup))

    added_ids = []
    merged = 0
    for it in accepted:
        if it.get("_dup_of"):
            old = next(p for p in items if p["id"] == it["_dup_of"])
            merge_note(old, it, it["_src_file"], allow_fill=args.fill)
            merged += 1
            continue
        it["id"] = it.get("id") or next_id(it, items, code_map)
        if any(p["id"] == it["id"] for p in items):
            it["id"] = next_id(it, items, code_map)
        for k in ("_norm_title", "_code", "_src_file", "_dup_of"):
            it.pop(k, None)
        items.append(it)
        added_ids.append(it["id"])
        # 同批内后续条目也要能被这批新条目去重
        idx = build_index(items)

    items.sort(key=lambda p: (p["publish_date"], p["id"]))
    pol["generated_at"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_json(os.path.join(DATA, "policies.json"), pol)
    print("[落盘] 新增 %d 条，合并补充 %d 条，全库 %d 条" % (len(added_ids), merged, len(items)))

    # meta：计数与区间统一交给 refresh_meta.py，这里只写「本次更新了什么」
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "refresh_meta.py")], check=True)
    mp = os.path.join(DATA, "meta.json")
    meta = load_json(mp, {})
    meta["last_update"] = today
    meta["last_update_note"] = "手动源增量：新增 %d 条、合并补充 %d 条（全库 %d 条）" % (
        len(added_ids), merged, len(items))
    save_json(mp, meta)

    # changelog
    cp = os.path.join(DATA, "changelog.json")
    cl = load_json(cp, {"logs": []})
    cl.setdefault("logs", []).append({
        "date": today,
        "type": "手动源增量",
        "operator": "Aaron",
        "summary": "手动收集源入库：新增 %d 条、合并 %d 条" % (len(added_ids), merged),
        "added": len(added_ids),
        "updated": merged,
        "deprecated": 0,
        "detail": ["新增 id：%s" % "、".join(added_ids)] if added_ids else ["无新增，仅合并补充"],
    })
    save_json(cp, cl)

    # 报告留档
    rep = os.path.join(REPORTS, "ingest-%s.txt" % stamp)
    with open(rep, "w", encoding="utf-8") as f:
        f.write("新增 %d 条 / 合并 %d 条 / 冲突 %d 项\n" % (len(added_ids), merged, len(conflicts)))
        for x in newly:
            f.write("+ %s %s %s\n" % (x["publish_date"], x["region"], x["title"]))
        for label, oid, c in conflicts:
            f.write("! %s → %s :: %s\n" % (label, oid, "；".join(c)))

    # 归档
    for fp in files:
        dst = os.path.join(ARCHIVE, "%s__%s" % (stamp, os.path.basename(fp)))
        shutil.move(fp, dst)
    print("[落盘] 已处理文件归档 %d 个，报告 → %s" % (len(files), os.path.basename(rep)))

    if not args.no_build:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_data.py")],
                           capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            print(r.stderr.strip())
            sys.exit(1)


if __name__ == "__main__":
    main()
