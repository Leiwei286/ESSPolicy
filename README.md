# 储能政策跟踪看板（ESSPolicy）

面向储能行业研究的政策跟踪看板。覆盖 2022-01 至 2026-11 全国及 31 个省级行政区的储能相关政策，用于评估政策对项目经济性与装机需求的影响。

在线看板：`https://leiwei286.github.io/ESSPolicy/`

## 仓库结构

```
├── index.html                  看板本体（三视图：列表 / 矩阵 / 时间轴 + 详情抽屉）
├── .nojekyll                   关闭 Jekyll 处理，保证静态资源按原样发布
├── data/
│   ├── data-bundle.js          打包产物，index.html 通过 <script src> 加载（Pages 实际读取的文件）
│   ├── policies.json           唯一主数据（1104 条）
│   ├── meta.json               计数与覆盖区间
│   ├── changelog.json          变更日志（追加式）
│   ├── source_watchlist.json   固定信息源清单
│   └── provincial-storage-targets.json  分省装机目标
├── docs/看板设计说明.md          字段字典 + 更新 SOP + 口径判定记录 + 已知缺口
├── tools/
│   ├── build_data.py           JSON → data-bundle.js 打包 + 字段校验
│   ├── qa_check.py             数据体检（阻断性问题 / 指标覆盖率 / 省级容量电价汇总）
│   ├── refresh_meta.py         重算 meta 计数与覆盖区间
│   ├── ingest_manual.py        手动来源入库（去重 / 合并 / 口径保护）
│   ├── crawl_list.py           北极星列表页抓取
│   └── patch_*.py              历史口径修正与批次补丁（保留备查）
└── manual/README.md            手动来源的三条通道与 JSON 样例
```

## 数据规模

| 项 | 值 |
|---|---|
| 条目总数 | 1104（全字段 258 + 历史索引层 846） |
| 时间覆盖 | 2022-01-04 ~ 2026-11-20 |
| 区域覆盖 | 全国 + 31 个省级行政区 |
| 政策分类 | 10 类（装机目标、容量电价、辅助服务、峰谷电价、项目清单、配储、并网、现货、补贴、系统运行费等） |
| 指标字段 | 8 个固定键：`cap_price` / `pv_spread` / `storage_ratio` / `duration_h` / `dispatch` / `scale_gw` / `scale_gwh` / `ancillary` |

## 本地打开

直接双击 `index.html` 即可，无需启动服务器。因为浏览器在 `file://` 下会拦截 `fetch` 读取 JSON，所以数据以 `data-bundle.js` 形式通过 `<script>` 加载。

## 更新流程

```bash
python tools/build_data.py       # 主数据改动后必须执行，重新生成 data-bundle.js
python tools/refresh_meta.py     # 重算 meta 计数
python tools/qa_check.py         # 数据体检，确认无阻断性问题
```

顺序不可颠倒。手动来源入库：

```bash
python tools/ingest_manual.py --channel ima            # 只出报告
python tools/ingest_manual.py --channel ima --apply     # 落盘
```

## 口径提醒（重要）

库内存在多组**不可相加**的数值，跨条目汇总前必读 `docs/看板设计说明.md`：

- **内蒙古容量电价**原为放电量补偿（2025 年度 0.35 元/kWh，**2026 年度已降至 0.28**），2027-01-01 起改为容量电价×折算比例（蒙西 4h/蒙东 5h 为分母，2h 项目约拿一半）。与各省「元/kW·年」口径不同，`cap_price` 故意留空。**2027 年及以后测算不可再沿用 0.35**
- **浙江 30GW** 是「抽蓄 + 新型储能」合计，扣除抽蓄约 10GW 后新型储能为 15–20GW；湖北 17GW 同口径
- **广东 5GW** 是「十五五」新增量，非累计
- **四川** 13GW/26GWh（三年目标）与 7.16GW/16.745GWh（已入清单）是目标与子集关系，不可相加
- **全国汇总 280GW** 已被官方口径取代：2030 年全国为 **300GW、平均 3 小时**（见 `CN-20261113-01`），280GW 仅作省际对照，不可再作装机预测
- **青海** 10GW 总量、独立储能 600 万千瓦、抽蓄 820 万千瓦分属三个口径
- **辽宁** 5GW（2027 目标）与 3.15GW（第一批遴选结果）不可相加

## 信息源

| 源 | 标识 | 说明 |
|---|---|---|
| 北极星储能网政策频道 | `bjx` | 主源 |
| ima 知识库手动收集 | `ima` | 用户手工收集的公众号文章与官网链接 |
| 公众号「储能与电力市场」 | `wx_espm` | 线索源与口径旁证，非原文源 |
| 官网直取 | `official` | 政府网站原文 |

## 部署

仓库启用 GitHub Pages（分支 `main`，目录 `/`）。改动数据后：

```bash
python tools/build_data.py
git add -A && git commit -m "数据更新：xxx"
git push
```

Pages 会在 1–2 分钟内重新构建。若页面未更新，检查 `data/data-bundle.js` 是否已随提交推送（缓存可用 `Ctrl+F5` 强刷）。
