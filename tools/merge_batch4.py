# -*- coding: utf-8 -*-
"""第4批：把索引层条目合并进 policies.json。"""
import io, json, os, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP = os.path.join(BASE, 'data', 'policies.json')
IP = os.path.join(BASE, 'data', '_index_batch4.json')

shutil.copy(MP, os.path.join(BASE, 'data', 'policies.backup-batch4.json'))

d = json.load(io.open(MP, encoding='utf-8'))
idx = json.load(io.open(IP, encoding='utf-8'))['policies']

exist_id = {p['id'] for p in d['policies']}
exist_url = {p.get('bjx_url') for p in d['policies'] if p.get('bjx_url')}

new = []
for p in idx:
    if p['bjx_url'] in exist_url:
        continue
    i = p['id']
    if i in exist_id:
        # 同日同省序号冲突时顺延
        k = 90
        while '%s-%02d' % (i.rsplit('-', 1)[0], k) in exist_id:
            k += 1
        p['id'] = '%s-%02d' % (i.rsplit('-', 1)[0], k)
    exist_id.add(p['id'])
    exist_url.add(p['bjx_url'])
    new.append(p)

print('待入库:', len(new))
if not new:
    raise SystemExit('无新增')

d['policies'].extend(new)
d['policies'].sort(key=lambda x: (x['publish_date'], x['id']))

# 校验
bad = [p['id'] for p in d['policies'] if not p.get('title') or not p.get('region')
       or not p.get('publish_date') or not p.get('category')]
ids = [p['id'] for p in d['policies']]
dup = len(ids) - len(set(ids))
print('总条数:', len(d['policies']), '| 字段缺失:', len(bad), '| 重复ID:', dup)
if bad or dup:
    raise SystemExit('校验失败')

d['generated_at'] = '2026-11-12T20:10:00+08:00'
json.dump(d, io.open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('已写入', MP)
