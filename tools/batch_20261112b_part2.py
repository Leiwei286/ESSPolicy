# -*- coding: utf-8 -*-
"""第2批 part2（2025-09 ~ 2026-04）：江苏/浙江/新疆/河南/四川/福建/山东/陕西/山西/云南/海南/天津/黑龙江/湖南/安徽/上海/贵州 共 32 条"""

TODAY = "2026-11-12"
M = dict(cap_price=None, pv_spread=None, storage_ratio=None, duration_h=None,
         dispatch=None, scale_gw=None, scale_gwh=None, ancillary=None, note=None)


def m(**kw):
    d = dict(M)
    d.update(kw)
    return d


BATCH = [
    # ---------------- 江苏 ----------------
    {
        "id": "JS-20251104-01",
        "title": "江苏调频辅助服务市场规则调整：独立储能可申报0.1-15元/MW",
        "region": "江苏", "level": "省级",
        "issuer": "国家能源局江苏监管办公室",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2025-11-04", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["调频", "申报区间", "独立储能"],
        "summary": "江苏调频里程申报价 0.1-15 元/MW，独立储能纳入申报主体",
        "key_points": [
            "调频里程申报价格区间 0.1~15 元/MW",
            "独立储能可参与调频申报",
            "分摊主体与考核规则待原文确认"
        ],
        "metrics": m(ancillary=15, note="申报区间0.1~15元/MW"),
        "impact": "中性",
        "logic": "申报下限 0.1 元/MW 意味着价格战可以打到几乎为零，实际结算价大概率贴近下限而非上限",
        "source_url": None, "source_name": "国家能源局江苏监管办公室",
        "bjx_url": "https://news.bjx.com.cn/html/20251104/1468164.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },
    {
        "id": "JS-20251010-01",
        "title": "江苏电力辅助服务管理实施细则、江苏电力并网运行管理实施细则",
        "region": "江苏", "level": "省级",
        "issuer": "国家能源局江苏监管办公室",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2025-10-10", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["一次调频无补偿", "AVC", "孤岛检测"],
        "summary": "江苏两个细则：储能须具备孤岛检测、AVC 与无功调节能力，一次调频无补偿",
        "key_points": [
            "储能应具备孤岛检测、AVC 和无功调节能力，属并网硬性技术门槛",
            "一次调频不给予补偿——基本辅助服务部分没有收入",
            "考核扣减规则与执行起始日待原文确认"
        ],
        "metrics": m(note="一次调频无补偿"),
        "impact": "中性",
        "logic": "一次调频白干、AVC 强制配置，等于在设备端增加成本却不增加收入，对江苏项目 IRR 是隐性扣分",
        "source_url": None, "source_name": "国家能源局江苏监管办公室",
        "bjx_url": "https://news.bjx.com.cn/html/20251010/1464205.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息；与 2025-12-31 江苏两个细则正式印发形成前后关系"
    },
    {
        "id": "JS-20251231-01",
        "title": "江苏电力辅助服务管理实施细则、江苏电力并网运行管理实施细则（正式印发）",
        "region": "江苏", "level": "省级",
        "issuer": "国家能源局江苏监管办公室",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2025-12-31", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["AVC要求", "并网考核", "储能"],
        "summary": "江苏两个细则正式印发，明确储能电站应具备 AVC 功能",
        "key_points": [
            "储能电站应具备 AVC（自动电压控制）功能",
            "并网运行考核与辅助服务补偿同步执行",
            "具体补偿标准与考核阈值待原文确认"
        ],
        "metrics": m(note="无量化补偿标准"),
        "impact": "中性",
        "logic": "正式稿落地意味着并网考核开始实际执行，江苏存量项目的可用率与考核成本需重新测算",
        "source_url": None, "source_name": "国家能源局江苏监管办公室",
        "bjx_url": "https://news.bjx.com.cn/html/20251231/1477540.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },
    {
        "id": "JS-20251224-01",
        "title": "江苏首批100个虚拟电厂项目公布，总投资12.73亿元",
        "region": "江苏", "level": "省级",
        "issuer": "江苏省发展和改革委员会",
        "doc_no": "—", "doc_type": "清单",
        "publish_date": "2025-12-24", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 1, "model_flag": "装机规模",
        "category": "储能项目清单",
        "sub_tags": ["虚拟电厂", "用户侧储能", "聚合"],
        "summary": "江苏首批 100 个虚拟电厂项目公布，总投资 12.73 亿元",
        "key_points": [
            "首批 100 个虚拟电厂项目，总投资 12.73 亿元",
            "用户侧储能可通过虚拟电厂聚合参与市场，获得间接收益通道",
            "单个项目调节能力与补贴标准待原文确认"
        ],
        "metrics": m(note="100个项目，总投资12.73亿元"),
        "impact": "利多",
        "logic": "虚拟电厂是用户侧储能目前唯一可规模化变现的聚合通道，100 个项目落地等于打开江苏用户侧储能的收益出口",
        "source_url": None, "source_name": "江苏省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20251224/1476300.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 浙江 ----------------
    {
        "id": "ZJ-20251031-01",
        "title": "浙江各地公示电网侧新型储能容量补偿项目清单",
        "region": "浙江", "level": "省级",
        "issuer": "浙江省各设区市发展和改革委员会",
        "doc_no": "浙发改能源〔2024〕111号",
        "doc_type": "清单",
        "publish_date": "2025-10-31", "effective_date": "2025-10-31",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "容量电价",
        "category": "容量电价政策",
        "sub_tags": ["容量补偿", "电网侧储能", "分年退坡"],
        "summary": "浙江公示 16 个项目 1064MW 获容量补偿，首年 200 元/kW·年",
        "key_points": [
            "7 个城市共 16 个项目纳入容量补偿清单，总规模 1064MW",
            "补偿标准按年退坡：2024 年 200 元/kW·年、2025 年 180 元、2026 年 170 元",
            "资金来源为历年电力直接交易结余资金，总额约 7.15 亿元；补偿对象为 2024-06-30 前完成并网试验的项目",
            "杭州 205MW、绍兴 156MW、金华 300MW、湖州 150MW、温州 150MW，另有嘉兴与余姚各 1 个项目"
        ],
        "metrics": m(cap_price=200, scale_gw=1.064, note="2024/2025/2026年分别为200/180/170元/kW·年"),
        "impact": "利多",
        "logic": "浙江是「存量一次性补偿+逐年退坡」模式，与辽宁、甘肃的长期容量电价不同，项目 IRR 需按三年退坡现金流重算",
        "source_url": None, "source_name": "浙江省各设区市发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20251103/1467926.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "补偿资金为一次性结余资金，2026 年后无接续安排"
    },
    {
        "id": "ZJ-20251128-01",
        "title": "浙江调频市场：火电15元/MW、储能无报价限制，储能电站申报容量不低于80%",
        "region": "浙江", "level": "省级",
        "issuer": "国家能源局浙江监管办公室",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2025-11-28", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["调频", "无报价限制", "申报容量门槛"],
        "summary": "浙江调频储能无报价限制，但申报容量不得低于 80%",
        "key_points": [
            "火电调频报价上限 15 元/MW；储能不设报价限制——理论上可报更高价",
            "储能电站申报容量不得低于其额定容量的 80%，等于强制预留大部分容量参与调频",
            "考核与结算细则待原文确认"
        ],
        "metrics": m(ancillary=15, note="储能无报价限制；申报容量≥80%"),
        "impact": "中性",
        "logic": "不设报价上限是少见的价格红利，但 80% 申报容量门槛把储能锁死在调频市场，机会成本可能高于收益",
        "source_url": None, "source_name": "国家能源局浙江监管办公室",
        "bjx_url": "https://news.bjx.com.cn/html/20251128/1472269.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },
    {
        "id": "ZJ-20251015-01",
        "title": "浙江拟优化分时电价：夏冬高峰时段收缩",
        "region": "浙江", "level": "省级",
        "issuer": "浙江省发展和改革委员会",
        "doc_no": "—", "doc_type": "征求意见稿",
        "publish_date": "2025-10-15", "effective_date": "待核实",
        "status": "征求意见", "superseded_by": None,
        "star": 3, "model_flag": "价差",
        "category": "峰谷电价政策",
        "sub_tags": ["高峰时段收缩", "峰谷价差", "用户侧储能"],
        "summary": "浙江拟收缩夏冬高峰时段，储能可放电的高价窗口变短",
        "key_points": [
            "拟优化分时电价，夏冬两季高峰时段收缩",
            "高峰时段缩短直接减少储能单日可放电小时数，影响套利电量",
            "调整后的浮动比例与执行起始日待正式文件确认"
        ],
        "metrics": m(note="浮动比例待补"),
        "impact": "利空",
        "logic": "高峰时段是被压缩的一端，储能可卖的高价电量减少，用户侧项目收益下修",
        "source_url": None, "source_name": "浙江省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20251015/1465105.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },
    {
        "id": "ZJ-20260104-01",
        "title": "浙江拟发放新型储能容量补偿：17个项目首年获2.3亿元",
        "region": "浙江", "level": "省级",
        "issuer": "浙江省发展和改革委员会",
        "doc_no": "—", "doc_type": "清单",
        "publish_date": "2026-01-04", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "容量电价",
        "category": "容量电价政策",
        "sub_tags": ["容量补偿", "资金发放"],
        "summary": "浙江 17 个储能项目首年获容量补偿 2.3 亿元",
        "key_points": [
            "17 个项目首年合计获得容量补偿 2.3 亿元",
            "按 200 元/kW·年 反推，对应补偿容量约 1.15GW，与前批清单规模基本吻合",
            "分年度发放节奏与 2026 年后安排待确认"
        ],
        "metrics": m(cap_price=200, note="首年2.3亿元/17个项目"),
        "impact": "利多",
        "logic": "资金真正到账是政策可信度的关键验证，2.3 亿元落地说明浙江补偿机制在真实执行",
        "source_url": None, "source_name": "浙江省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260104/1477793.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 新疆 ----------------
    {
        "id": "XJ-20260119-01",
        "title": "新疆新能源就近消纳：鼓励通过合理配置储能、深挖负荷灵活调节潜力",
        "region": "新疆", "level": "省级",
        "issuer": "新疆维吾尔自治区发展和改革委员会",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2026-01-19", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 1, "model_flag": "配储比例",
        "category": "新能源配储要求",
        "sub_tags": ["就近消纳", "自愿配储"],
        "summary": "新疆鼓励就近消纳项目合理配置储能，未设强制比例",
        "key_points": [
            "对新能源就近消纳项目，鼓励通过合理配置储能、深挖负荷灵活调节潜力提升消纳",
            "属鼓励性表述，未设强制配储比例",
            "配套电价与考核机制待原文确认"
        ],
        "metrics": m(note="无强制比例"),
        "impact": "中性",
        "logic": "鼓励而非强制，短期不改变新疆装机节奏，属于方向性文件",
        "source_url": None, "source_name": "新疆维吾尔自治区发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260119/1480115.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 河南 ----------------
    {
        "id": "HA-20251020-01",
        "title": "推动河南省新型储能高质量发展的若干措施（征求意见稿）",
        "region": "河南", "level": "省级",
        "issuer": "河南省发展和改革委员会",
        "doc_no": "—", "doc_type": "征求意见稿",
        "publish_date": "2025-10-20", "effective_date": "待核实",
        "status": "征求意见", "superseded_by": None,
        "star": 3, "model_flag": "调用与结算",
        "category": "容量电价政策",
        "sub_tags": ["兜底收益", "容量租赁", "调用次数", "2030年15GW"],
        "summary": "河南给独立储能 0.383 元/kWh 兜底收益、年调用不低于 350 次，租赁储能减免 30% 辅助服务费",
        "key_points": [
            "独立储能因现货运行导致收益减少时，以系统循环效率 75% 为基准按上网电量 0.383 元/kWh 兜底；效率低于 75% 时按实际效率/75% 折减",
            "独立储能向电网送电时，充电电量执行工商业峰谷电价差，不承担输配电价、系统运行费与政府性基金及附加，不执行功率因数考核",
            "租赁储能容量的新能源场站，分摊辅助服务费用时给予 30% 减免；调度优先调用储能配比高、时长长的项目",
            "未参与配储且未签租赁协议的电网侧独立储能，按满功率连续放电时长÷前一年最长净负荷高峰时长×当地煤电容量电价获得可靠容量补偿",
            "独立储能每年完全充放电次数原则上不低于 350 次；新规划项目原则上不低于 20 万千瓦时；2030 年装机目标 15GW"
        ],
        "metrics": m(dispatch=350, cap_price=None, note="兜底0.383元/kWh；年调用≥350次；单项目≥200MWh"),
        "impact": "利多",
        "logic": "兜底收益+350 次调用+租赁费减免三件套，把河南独立储能的收益下限锁得比多数省份都实，属于收益确定性最高的省份之一",
        "source_url": None, "source_name": "河南省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20251022/1466060.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "征求意见稿；与 2026-03-25 河南重磅文件形成组合，需核对其最终定稿口径"
    },
    {
        "id": "HA-20260120-01",
        "title": "关于调整我省工商业分时电价峰谷浮动基数的通知（征求意见稿）",
        "region": "河南", "level": "省级",
        "issuer": "河南省发展和改革委员会",
        "doc_no": "—", "doc_type": "征求意见稿",
        "publish_date": "2026-01-20", "effective_date": "待核实",
        "status": "征求意见", "superseded_by": None,
        "star": 3, "model_flag": "价差",
        "category": "峰谷电价政策",
        "sub_tags": ["输配电价不浮动", "价差收缩", "代理购电"],
        "summary": "河南拟让输配电价不参与峰谷浮动，尖峰-低谷价差或收缩 33%",
        "key_points": [
            "直接参与市场交易的用户不再执行工商业分时电价；代理购电用户执行分时电价的，输配电价不再参与峰谷浮动",
            "峰谷时段与浮动比例仍按豫发改价管〔2024〕283 号执行：高峰:平段:低谷=1.72:1:0.45，尖峰为高峰的 1.2 倍",
            "据测算，单一制 10kV 以下用户尖峰-低谷价差将由 0.8195 元/kWh 降至 0.5484 元/kWh，降幅 33%",
            "高峰-低谷价差由 0.6449 元/kWh 降至 0.4315 元/kWh"
        ],
        "metrics": m(note="尖峰0.8195→0.5484元/kWh；高峰0.6449→0.4315元/kWh"),
        "impact": "利空",
        "logic": "价差一次性收缩三分之一，用户侧储能套利收入几乎等比例下降，河南工商业储能 IRR 需整体下修",
        "source_url": None, "source_name": "河南省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260121/1480566.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "征求意见稿；价差数值为北极星测算口径，非官方公布"
    },
    {
        "id": "HA-20260325-01",
        "title": "河南储能重磅：容量电价补偿、不收输配电价、给予50MW新能源配额",
        "region": "河南", "level": "省级",
        "issuer": "河南省发展和改革委员会",
        "doc_no": "—", "doc_type": "政策措施",
        "publish_date": "2026-03-25", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "容量电价",
        "category": "容量电价政策",
        "sub_tags": ["容量电价", "新能源配额", "中央预算支持"],
        "summary": "河南把容量电价补偿、免输配电价与 50MW 新能源配额打包给储能",
        "key_points": [
            "对储能给予容量电价补偿，充电电量不收输配电价",
            "给予 50MW 新能源配额作为配套激励",
            "争取中央预算内资金支持；具体补偿标准与配额兑现方式待原文确认"
        ],
        "metrics": m(note="无具体元/kW·年数值；配额50MW"),
        "impact": "利多",
        "logic": "「容量电价+免输配电价+新能源配额」是三合一的实质性激励，配额尤其稀缺，会显著抬升河南项目抢装意愿",
        "source_url": None, "source_name": "河南省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260325/1489222.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息，容量补偿具体标准待补"
    },

    # ---------------- 四川 ----------------
    {
        "id": "SC-20260214-01",
        "title": "四川省电力辅助服务管理实施细则（征求意见稿）、四川省电力并网运行管理实施细则（征求意见稿）",
        "region": "四川", "level": "省级",
        "issuer": "国家能源局四川监管办公室",
        "doc_no": "—", "doc_type": "征求意见稿",
        "publish_date": "2026-02-14", "effective_date": "待核实",
        "status": "征求意见", "superseded_by": None,
        "star": 3, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["调峰补偿", "按充电量补偿", "可用率考核", "一次调频"],
        "summary": "四川独立储能调峰按充电量补偿 400 元/MWh，配建储能 80-160 元/MWh",
        "key_points": [
            "独立储能调峰按其充电电量补偿 400 元/MWh；配建储能按月度累计充电电量分档：<30h 不补、30-60h 补 80 元/MWh、≥60h 补 160 元/MWh",
            "纳入两个细则的独立储能容量门槛 10MW/20MWh；一次调频补偿小扰动 200 元/MWh、大扰动 1000 元/MWh",
            "AGC 补偿 6 元/MW，APC 按实际调节里程 6 元/MW，爬坡补偿 40 元/MW，转动惯量 100 元/Mvar",
            "可用率考核：功率或能量可用率低于额定值 70% 时，按储能额定容量×5 小时/月考核，月度考核电量不超过全场站上网电量 2%"
        ],
        "metrics": m(ancillary=400, note="独立储能调峰400元/MWh（按充电量）；配建80~160元/MWh"),
        "impact": "利多",
        "logic": "按充电量补偿是罕见的「充电也给钱」设计，直接降低度电成本；400 元/MWh 相当于 0.4 元/kWh，接近多数省份峰谷价差的一半",
        "source_url": None, "source_name": "国家能源局四川监管办公室",
        "bjx_url": "https://news.bjx.com.cn/html/20260224/1484542.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "征求意见稿；正式稿补偿标准可能下调"
    },
    {
        "id": "SC-20251010-01",
        "title": "四川省深化新能源上网电价市场化改革实施方案",
        "region": "四川", "level": "省级",
        "issuer": "四川省发展和改革委员会",
        "doc_no": "—", "doc_type": "方案",
        "publish_date": "2025-10-10", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "配储比例",
        "category": "新能源配储要求",
        "sub_tags": ["取消强制配储", "机制电价", "增量竞价"],
        "summary": "四川取消强制配储，存量机制电价 0.4012 元/kWh，增量竞价 0.2-0.4012",
        "key_points": [
            "明确取消强制配储",
            "存量项目机制电价 0.4012 元/kWh，增量项目竞价区间 0.2~0.4012 元/kWh",
            "配储退出后储能的收益来源转向调峰补偿（400 元/MWh）等市场机制"
        ],
        "metrics": m(note="存量0.4012元/kWh"),
        "impact": "中性",
        "logic": "强制配储退出会削掉一部分「被动装机」，但四川 400 元/MWh 的充电补偿能补上主动装机的动机",
        "source_url": None, "source_name": "四川省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20251010/1464164.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 福建 ----------------
    {
        "id": "FJ-20260306-01",
        "title": "福建省电力辅助服务管理实施细则、福建省电力并网运行管理实施细则",
        "region": "福建", "level": "省级",
        "issuer": "国网福建电力调控中心（转发）",
        "doc_no": "调计〔2026〕29号", "doc_type": "实施细则",
        "publish_date": "2026-03-06", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["一次调频", "转动惯量", "黑启动", "AGC考核"],
        "summary": "福建有偿一次调频 600 元/MWh，独立储能可参与 6 类辅助服务",
        "key_points": [
            "有偿一次调频：实际动作积分电量超理论值 70% 的，补偿 600 元/MWh",
            "低频调节（频率低于 49.933Hz 时 1 分钟内增发超理论积分电量 80%）补偿 800 元/MWh；有偿调峰最高 10 万元/台次",
            "独立储能旋转备用 10 元/MWh（参与现货主体 50 元/MWh），转动惯量 0.1 元/MWh，爬坡最高 120 元/MW·天，黑启动动作 2000 元/MW·次",
            "AGC 考核：未按规定时间具备 AGC 功能或联调不达标，每月每万千瓦考核 1 万元"
        ],
        "metrics": m(ancillary=600, note="一次调频600元/MWh；低频调节800元/MWh"),
        "impact": "利多",
        "logic": "600 元/MWh 的一次调频补偿是全国最高档，福建独立储能的辅助服务收入占比会明显高于其他省份",
        "source_url": None, "source_name": "国网福建电力调控中心",
        "bjx_url": "https://news.bjx.com.cn/html/20260310/1486818.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "调计〔2026〕29号"
    },

    # ---------------- 山东 ----------------
    {
        "id": "SD-20251129-01",
        "title": "山东2026年工商业分时电价政策",
        "region": "山东", "level": "省级",
        "issuer": "国网山东省电力公司",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2025-11-29", "effective_date": "2026-01-01",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "价差",
        "category": "峰谷电价政策",
        "sub_tags": ["尖峰上浮100%", "深谷下浮90%", "午间谷段"],
        "summary": "山东 2026 分时电价：高峰上浮 70%、尖峰上浮 100%、深谷下浮 90%",
        "key_points": [
            "浮动比例：高峰上浮 70%、低谷下浮 70%、尖峰上浮 100%、深谷下浮 90%——深谷幅度全国最深",
            "1-2 月及 12 月谷段含 10:00-15:00（深谷 11:00-14:00），峰段 7:00-9:00、16:00-21:00（尖峰 16:00-19:00）",
            "3-5 月与 9-11 月谷段 10:00-15:00（深谷 11:00-14:00），支持午间充电+晚峰放电的两充两放",
            "6-8 月谷段移至夜间 1:00-6:00（7-8 月），午间无深谷，夏季套利窗口结构与其他月份不同",
            "容量补偿电价、上网环节线损费用、系统运行费用及代理购电价格执行分时；各类分摊损益不执行"
        ],
        "metrics": m(note="峰+70%/谷-70%/尖峰+100%/深谷-90%"),
        "impact": "利多",
        "logic": "深谷下浮 90% 加上稳定的午间谷段，是用户侧储能最友好的价差结构之一；但 6-8 月夏季结构变化需分月建模",
        "source_url": None, "source_name": "国网山东省电力公司",
        "bjx_url": "https://news.bjx.com.cn/html/20251205/1473188.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "2026 年时段沿用 2025 年，仅浮动比例执行"
    },
    {
        "id": "SD-20260305-01",
        "title": "关于做好2026年第二季度全省电力市场建设有关工作的通知",
        "region": "山东", "level": "省级",
        "issuer": "山东省发展和改革委员会等",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2026-03-05", "effective_date": "2026-06-01",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "调用与结算",
        "category": "系统运行费规则",
        "sub_tags": ["分布式储能", "免输配电费", "报量报价"],
        "summary": "山东分布式储能向电网送电，当月等量充电量不承担输配电费",
        "key_points": [
            "自 2026-06-01 起，未参与市场的分布式储能上网电量暂按所在市级行政区域发电侧节点实时市场算术平均电价结算",
            "鼓励分布式储能以独立或聚合方式报量报价参与市场，其向电网送电当月等量充电量不承担输配电费",
            "调频辅助服务改为按小时调整容量与速率需求、分时出清，增加参与灵活性",
            "双边协商交易电量上限由当月中长期签约比例下限的 40% 调整为 50%"
        ],
        "metrics": m(note="免输配电费按当月等量充电量计算"),
        "impact": "利多",
        "logic": "免掉输配电费等于直接压低充电成本约 0.1 元/kWh 量级，分布式储能的度电套利空间被结构性打开",
        "source_url": None, "source_name": "山东省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260309/1486618.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "2026-06-01 起执行"
    },
    {
        "id": "SD-20260319-01",
        "title": "山东2026年集中式光伏项目申报：鼓励自愿配储，不得将配置储能作为前置条件",
        "region": "山东", "level": "省级",
        "issuer": "山东省能源局",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2026-03-19", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "配储比例",
        "category": "新能源配储要求",
        "sub_tags": ["自愿配储", "配储脱钩"],
        "summary": "山东集中式光伏申报明确不得将配储作为前置条件，改为鼓励自愿配储",
        "key_points": [
            "鼓励新能源项目自愿配置储能",
            "明确不得将配置储能作为项目申报的前置条件",
            "配储与项目排序、并网优先级的挂钩方式待原文确认"
        ],
        "metrics": m(note="无强制比例"),
        "impact": "中性",
        "logic": "配储从门槛变成加分项，短期削弱被动装机需求，但把选择权交给项目方后，只有真正算得过账的储能才会建",
        "source_url": None, "source_name": "山东省能源局",
        "bjx_url": "https://news.bjx.com.cn/html/20260319/1488414.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 陕西 ----------------
    {
        "id": "SN-20251210-01",
        "title": "关于2026年陕西电力市场交易相关重要事项的提示",
        "region": "陕西", "level": "省级",
        "issuer": "陕西电力交易中心",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2025-12-10", "effective_date": "2026-01-01",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "价差",
        "category": "峰谷电价政策",
        "sub_tags": ["取消峰谷浮动", "市场化定价", "用户侧储能"],
        "summary": "陕西 2026 年起市场化用户不再执行峰谷浮动，峰谷价差政策退场",
        "key_points": [
            "2026 年市场化用户（批发、零售）分时价格不再执行峰谷浮动政策",
            "售电公司代理用户电价主要由市场内批发均价传导形成，最低电价将主要出现在中午光伏大发时段",
            "新能源电价改革与煤电容量电价相关费用纳入系统运行费，由全体工商业用户分摊，市场外度电分摊费用较 2025 年上涨"
        ],
        "metrics": m(note="取消统一浮动比例"),
        "impact": "利空",
        "logic": "政府定价的峰谷价差消失后，用户侧储能只能靠现货午间低价与晚峰高价套利，价差方向与幅度都不再由政策保证",
        "source_url": None, "source_name": "陕西电力交易中心",
        "bjx_url": "https://news.bjx.com.cn/html/20251215/1474607.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "与 2025-12-26 国家《电力中长期市场基本规则》方向一致"
    },
    {
        "id": "SN-20260104-01",
        "title": "陕西调频辅助服务市场：补偿上限15元/MW，独立储能与虚拟电厂参与分摊",
        "region": "陕西", "level": "省级",
        "issuer": "国家能源局西北监管局",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2026-01-04", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["调频", "费用分摊", "虚拟电厂"],
        "summary": "陕西调频补偿上限 15 元/MW，独立储能与虚拟电厂均参与分摊",
        "key_points": [
            "调频里程补偿上限 15 元/MW",
            "独立储能、虚拟电厂参与调频费用分摊",
            "申报区间与考核规则待原文确认"
        ],
        "metrics": m(ancillary=15, note="上限15元/MW"),
        "impact": "中性",
        "logic": "既要分摊又受 15 元/MW 上限约束，陕西调频对储能是「净支出项」，除非 K 值足够高能拿到足额补偿",
        "source_url": None, "source_name": "国家能源局西北监管局",
        "bjx_url": "https://news.bjx.com.cn/html/20260104/1477611.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 山西 ----------------
    {
        "id": "SX-20260120-01",
        "title": "山西：不再人为规定分时电价水平和时段，根据现货市场优化峰谷价格浮动比例",
        "region": "山西", "level": "省级",
        "issuer": "山西省发展和改革委员会",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2026-01-20", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "价差",
        "category": "峰谷电价政策",
        "sub_tags": ["取消政府定价", "现货引导", "浮动比例"],
        "summary": "山西不再人为规定分时电价，峰谷浮动比例改由现货价格优化",
        "key_points": [
            "不再人为规定分时电价水平和时段",
            "根据现货市场运行情况优化峰谷价格浮动比例",
            "过渡期如何衔接原 2026 年 3 月起的节假日 2h 深谷时段，待原文确认"
        ],
        "metrics": m(note="无统一浮动比例"),
        "impact": "中性",
        "logic": "现货驱动的价差波动更大，山西储能套利的收益方差上升，需要按月度现货价格分布而非年度均价建模",
        "source_url": None, "source_name": "山西省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260120/1480347.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "与本库 2026-03-03 山西「节假日 2h 深谷」条目存在政策衔接关系"
    },

    # ---------------- 云南 ----------------
    {
        "id": "YN-20251231-01",
        "title": "云南省新型储能高质量发展专项行动方案（2025—2027年）",
        "region": "云南", "level": "省级",
        "issuer": "云南省发展和改革委员会、云南省能源局",
        "doc_no": "—", "doc_type": "方案",
        "publish_date": "2025-12-31", "effective_date": "2025-12-31",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "装机规模",
        "category": "储能装机目标",
        "sub_tags": ["2027年8GW", "长时储能", "构网型", "开工时限"],
        "summary": "云南 2027 年新型储能 8GW，清单 8.955GW/20.36GWh，另布局 4.45GW 长时储能",
        "key_points": [
            "2027 年全省新型储能装机达 800 万千瓦以上；下发清单合计 8.955GW/20.36GWh（已投产 5.455GW/11.11GWh、在建 2.05GW/5.75GWh）",
            "另在 17 个区域优先布局长时储能，总规模 4.45GW；技术路线含全钒液流约 1GW/3GWh、压缩空气 550MW/2.55GWh",
            "新建新型共享电化学储能项目原则上须采用构网型储能技术，并通过涉网试验验证",
            "开工时限：电化学储能不超过 1 年；磷酸铁锂开工后 8 个月内投产（最长 1 年）、全钒液流 1.5 年内（最长 2 年）",
            "各州市不得将配置储能作为新建新能源项目核准、并网、上网的前置条件；未纳入推送清单的项目不享受容量租赁与容量电价"
        ],
        "metrics": m(scale_gw=8.955, scale_gwh=20.36, note="2027年目标8GW；长时储能另4.45GW"),
        "impact": "利多",
        "logic": "8GW 目标+明确开工投产时限，是西南地区最具约束力的装机规划；构网型强制要求会改变设备端竞争格局",
        "source_url": None, "source_name": "云南省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260104/1477780.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "清单规模 8.955GW 与目标 8GW 的差额需按滚动调整口径理解"
    },
    {
        "id": "YN-20251126-01",
        "title": "云南省新型共享储能项目（电化学储能）投产并网时间认定清单",
        "region": "云南", "level": "省级",
        "issuer": "云南省能源局",
        "doc_no": "—", "doc_type": "清单",
        "publish_date": "2025-11-26", "effective_date": "2025-11-26",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "装机规模",
        "category": "储能项目清单",
        "sub_tags": ["并网时间认定", "共享储能", "清算"],
        "summary": "云南 23 个共享储能 4.355GW/8.71GWh 通过投产并网时间认定",
        "key_points": [
            "23 个项目通过并网时间认定，总规模 4.355GW/8.71GWh",
            "分三类认定：2025-04-30 前投产 7 个 1.3GW/2.6GWh；2025-05-31 前投产 13 个 2.62GW/5.24GWh；其他 3 个 0.435GW/0.87GWh",
            "2 个独立储能项目并网时间未通过认定，合计 235MW/470MWh，将影响其电价与补偿清算"
        ],
        "metrics": m(scale_gw=4.355, scale_gwh=8.71, note="23个项目；未通过认定235MW/470MWh"),
        "impact": "中性",
        "logic": "并网时间直接决定适用哪一档电价与补偿，认定未通过的项目收益会明显低于预期，是云南项目的关键风险点",
        "source_url": None, "source_name": "云南省能源局",
        "bjx_url": "https://news.bjx.com.cn/html/20251127/1471895.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "认定分类依据云能源科技〔2024〕98号与〔2025〕1号"
    },
    {
        "id": "YN-20260228-01",
        "title": "云南促进绿电消纳措施：新建共享储能需采用构网型储能",
        "region": "云南", "level": "省级",
        "issuer": "云南省能源局",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2026-02-28", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "配储比例",
        "category": "新能源配储要求",
        "sub_tags": ["构网型", "共享储能", "技术门槛"],
        "summary": "云南要求新建共享储能采用构网型，技术门槛实质抬高",
        "key_points": [
            "新建共享储能项目需采用构网型储能技术",
            "构网型设备成本高于跟网型，单位 kW 投资上升",
            "与 2025-12-31 专项行动方案表述一致，属执行层面加严"
        ],
        "metrics": m(note="无量化比例，属技术路线强制"),
        "impact": "中性",
        "logic": "强制构网型会抬高单位投资 10-20%，但同时抬高了准入门槛、减少低价竞争，对头部设备商有利",
        "source_url": None, "source_name": "云南省能源局",
        "bjx_url": "https://news.bjx.com.cn/html/20260228/1485490.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 海南 ----------------
    {
        "id": "HI-20251217-01",
        "title": "海南独立储能参与电力市场规则：日均循环2次、SOC 5%~95%",
        "region": "海南", "level": "省级",
        "issuer": "海南省发展和改革委员会",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2025-12-17", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "调用与结算",
        "category": "电力现货规则",
        "sub_tags": ["循环次数", "SOC区间", "独立储能"],
        "summary": "海南独立储能参与市场日均循环 2 次、SOC 5%~95%",
        "key_points": [
            "日均循环次数上限 2 次",
            "荷电状态区间 5%~95%，可用容量约 90%",
            "结算价格形成方式与分摊规则待原文确认"
        ],
        "metrics": m(dispatch=2, note="SOC 5%~95%"),
        "impact": "中性",
        "logic": "日均 2 次循环是较宽松的上限，SOC 5-95% 也留足了可用容量，海南对储能的运行约束比蒙西友好",
        "source_url": None, "source_name": "海南省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20251217/1475046.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 天津 ----------------
    {
        "id": "TJ-20251215-01",
        "title": "天津独立储能电力交易只能签订高峰/尖峰合同",
        "region": "天津", "level": "省级",
        "issuer": "天津市工业和信息化局",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2025-12-15", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "价差",
        "category": "电力现货规则",
        "sub_tags": ["合同类型限制", "价格上限", "独立储能"],
        "summary": "天津独立储能只能签订高峰/尖峰合同，价格上限 0.7/0.84 元/kWh",
        "key_points": [
            "独立储能电力交易只能签订高峰或尖峰时段合同",
            "高峰合同价格不超过 0.7 元/kWh，尖峰不超过 0.84 元/kWh",
            "充电侧如何签约与结算待原文确认"
        ],
        "metrics": m(note="高峰≤0.7元/kWh、尖峰≤0.84元/kWh"),
        "impact": "中性",
        "logic": "只能卖高峰/尖峰等于锁定高价时段，但 0.7/0.84 的价格上限同时封死了套利上限，收益结构明确但天花板不高",
        "source_url": None, "source_name": "天津市工业和信息化局",
        "bjx_url": "https://news.bjx.com.cn/html/20251215/1474570.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 黑龙江 ----------------
    {
        "id": "HLJ-20260214-01",
        "title": "黑龙江1.7GW/6.1GWh独立储能项目清单公布，纳入容量电价机制",
        "region": "黑龙江", "level": "省级",
        "issuer": "黑龙江省发展和改革委员会",
        "doc_no": "—", "doc_type": "清单",
        "publish_date": "2026-02-14", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "装机规模",
        "category": "储能项目清单",
        "sub_tags": ["容量电价", "独立储能", "清单"],
        "summary": "黑龙江 1.7GW/6.1GWh 独立储能清单纳入容量电价机制",
        "key_points": [
            "清单规模 1.7GW/6.1GWh，折合平均时长约 3.6h",
            "纳入容量电价机制，享受容量补偿",
            "容量电价具体标准与执行起始日待原文确认"
        ],
        "metrics": m(scale_gw=1.7, scale_gwh=6.1, note="平均时长约3.6h"),
        "impact": "利多",
        "logic": "东北首个明确「清单+容量电价」绑定的省份，3.6h 平均时长在折算公式下接近满档，收益结构优于 2h 项目",
        "source_url": None, "source_name": "黑龙江省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260214/1484499.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 湖南 ----------------
    {
        "id": "HN-20251208-01",
        "title": "湖南两个细则：独立储能门槛2MW/1h，明确构网能力补偿标准",
        "region": "湖南", "level": "省级",
        "issuer": "国家能源局湖南监管办公室",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2025-12-08", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "调用与结算",
        "category": "辅助服务市场规则",
        "sub_tags": ["构网型", "调峰补偿", "准入门槛"],
        "summary": "湖南独立储能准入门槛降至 2MW/1h，并明确构网能力补偿标准",
        "key_points": [
            "独立储能参与辅助服务的准入门槛为 2MW/1h，为全国最低档之一",
            "明确构网能力补偿标准，调峰充电补偿有专门口径（报道口径为 300 元/MWh 量级，单位存在歧义需核对原文）",
            "考核规则与执行起始日待原文确认"
        ],
        "metrics": m(duration_h=1, note="门槛2MW/1h；构网补偿标准单位待核实"),
        "impact": "利多",
        "logic": "2MW/1h 的门槛让分布式与小型储能也能进入辅助服务市场，构网补偿则为技术溢价定价",
        "source_url": None, "source_name": "国家能源局湖南监管办公室",
        "bjx_url": "https://news.bjx.com.cn/html/20251208/1473388.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "标题中「300元/Wh」疑为笔误，需核对原文单位"
    },

    # ---------------- 安徽 ----------------
    {
        "id": "AH-20260131-01",
        "title": "安徽电力现货电能量市场交易实施细则（结算试运行第6.1版）",
        "region": "安徽", "level": "省级",
        "issuer": "安徽电力交易中心",
        "doc_no": "—", "doc_type": "实施细则",
        "publish_date": "2026-01-31", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 3, "model_flag": "价差",
        "category": "电力现货规则",
        "sub_tags": ["现货限价", "报量保价", "调频与现货选择"],
        "summary": "安徽现货限价 0-1.1 元/kWh，独立储能可自选现货/调频出清方式",
        "key_points": [
            "电能量市场申报价格与出清价格上下限均为 0~1.1 元/kWh",
            "独立储能可在申报时选择：仅参与现货出清、仅参与调频出清、现货未中标则参加次日调频出清（默认第一种）",
            "参与现货的独立储能须具备接受出清指令条件，充电功率不低于 5MW、持续充电时间不低于 1h",
            "申报的放电价格须大于充电价格"
        ],
        "metrics": m(dispatch=None, note="现货限价0~1.1元/kWh；充电功率≥5MW、≥1h"),
        "impact": "利多",
        "logic": "「现货未中标转调频」的选择权给了储能收益兜底，避免单日空转；1.1 元/kWh 上限也高于多数省份",
        "source_url": None, "source_name": "安徽电力交易中心",
        "bjx_url": "https://news.bjx.com.cn/html/20260203/1482480.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "结算试运行第6.1版"
    },
    {
        "id": "AH-20260320-01",
        "title": "安徽公布78个电网侧储能推荐站点，优先支持新能源租赁项目",
        "region": "安徽", "level": "省级",
        "issuer": "安徽省能源局",
        "doc_no": "—", "doc_type": "清单",
        "publish_date": "2026-03-20", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "装机规模",
        "category": "储能项目清单",
        "sub_tags": ["推荐站点", "容量租赁", "电网侧"],
        "summary": "安徽公布 78 个电网侧储能推荐站点，优先支持新能源租赁项目",
        "key_points": [
            "共 78 个电网侧储能推荐站点",
            "优先支持新能源租赁项目，租赁成为安徽独立储能的主要收益来源之一",
            "站点总容量与并网时限待原文确认"
        ],
        "metrics": m(note="78个推荐站点，总规模待补"),
        "impact": "利多",
        "logic": "推荐站点制把选址前置，缩短项目前期周期；优先租赁则把新能源的配储义务转化为独立储能的收入",
        "source_url": None, "source_name": "安徽省能源局",
        "bjx_url": "https://news.bjx.com.cn/html/20260320/1488657.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 上海 ----------------
    {
        "id": "SH-20260212-01",
        "title": "上海明确现货市场申报价 0-1.4 元/kWh，参考工商业尖峰电价",
        "region": "上海", "level": "省级",
        "issuer": "上海市发展和改革委员会",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2026-02-12", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "价差",
        "category": "电力现货规则",
        "sub_tags": ["现货限价", "尖峰电价", "套利上限"],
        "summary": "上海现货申报价上限 1.4 元/kWh，以工商业尖峰电价为参考",
        "key_points": [
            "现货市场申报价格区间 0~1.4 元/kWh",
            "上限参考工商业尖峰电价设定，是全国省级现货限价中较高档",
            "结算与考核细则待原文确认"
        ],
        "metrics": m(note="现货限价0~1.4元/kWh"),
        "impact": "利多",
        "logic": "1.4 元/kWh 的上限把储能套利天花板抬到多数省份之上，对上海用户侧与独立储能都是实质利好",
        "source_url": None, "source_name": "上海市发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260212/1484036.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },

    # ---------------- 贵州 ----------------
    {
        "id": "GZ-20260126-01",
        "title": "贵州补充完善峰谷分时电价：输配电价、系统运行费用、政府性基金及附加不参与浮动",
        "region": "贵州", "level": "省级",
        "issuer": "贵州省发展和改革委员会",
        "doc_no": "—", "doc_type": "通知",
        "publish_date": "2026-01-26", "effective_date": "待核实",
        "status": "现行有效", "superseded_by": None,
        "star": 2, "model_flag": "价差",
        "category": "峰谷电价政策",
        "sub_tags": ["浮动基数收窄", "价差压缩"],
        "summary": "贵州把输配电价、系统运行费、基金附加剔除出浮动基数，峰谷价差实质收窄",
        "key_points": [
            "输配电价、系统运行费用、政府性基金及附加不参与峰谷浮动",
            "浮动基数收窄后，实际峰谷价差小于名义浮动比例",
            "新的浮动比例与执行起始日待原文确认"
        ],
        "metrics": m(note="浮动比例待补"),
        "impact": "利空",
        "logic": "与河南、云南、冀北同属「缩小浮动基数」路径，名义比例不变但实际价差下降，用户侧储能收益被系统性削减",
        "source_url": None, "source_name": "贵州省发展和改革委员会",
        "bjx_url": "https://news.bjx.com.cn/html/20260126/1481189.shtml",
        "tier": "full", "first_seen": "2026-11-12", "last_checked": "2026-11-12",
        "note": "仅标题级信息"
    },
]
