# -*- coding: utf-8 -*-
"""抓取北极星储能网政策频道列表页，解析条目并与库内查重，输出候选清单。

用法: python tools/crawl_list.py 1 25
"""
import io, json, os, re, sys, time, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
ITEM = re.compile(
    r'<li><a href="(https://news\.bjx\.com\.cn/html/\d{8}/\d+\.shtml)"[^>]*?title="([^"]*)"[^>]*>.*?</a><span>(\d{4}-\d{2}-\d{2})</span></li>',
    re.S)


def fetch(page):
    url = "https://chuneng.bjx.com.cn/zc/%d" % page
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(2):
        try:
            return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
        except Exception as e:
            if attempt == 0:
                time.sleep(3)
                continue
            print("  [页%d 抓取失败] %s" % (page, e))
            return ""


def main():
    p0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    p1 = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    items = {}
    for p in range(p0, p1 + 1):
        h = fetch(p)
        if not h:
            continue
        found = ITEM.findall(h)
        dates = []
        for url, title, date in found:
            title = re.sub(r"<[^>]+>", "", title).strip()
            items[url] = {"url": url, "title": title, "date": date, "page": p}
            dates.append(date)
        if dates:
            print("页%-3d %3d 条  %s ~ %s" % (p, len(found), min(dates), max(dates)))
        else:
            print("页%-3d 0 条（结构变化或被拦截）" % p)
        time.sleep(1.0)

    d = json.load(io.open(os.path.join(BASE, "data", "policies.json"), encoding="utf-8"))
    known = {p.get("bjx_url") for p in d["policies"] if p.get("bjx_url")}

    # 累积到 _all_items.json，避免分批抓取互相覆盖
    allp = os.path.join(BASE, "data", "_all_items.json")
    acc = {}
    if os.path.exists(allp):
        acc = json.load(io.open(allp, encoding="utf-8"))
    acc.update(items)
    json.dump(acc, io.open(allp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    cand = [v for v in acc.values() if v["url"] not in known]
    cand.sort(key=lambda x: x["date"], reverse=True)
    out = os.path.join(BASE, "data", "_candidates.json")
    json.dump({"total_scraped": len(acc), "candidates": cand},
              io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print()
    print("累计抓取 %d 条，库内已有 %d 条，候选新增 %d 条 -> %s"
          % (len(acc), len(acc) - len(cand), len(cand), out))
    print("候选日期区间: %s ~ %s" % (cand[-1]["date"], cand[0]["date"]) if cand else "无候选")


if __name__ == "__main__":
    main()
