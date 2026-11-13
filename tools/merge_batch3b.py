# -*- coding: utf-8 -*-
"""合并第 3b 批（其他省长尾 17 条）。"""
import io, json, os, shutil, importlib.util

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP = os.path.join(BASE, 'data', 'policies.json')

spec = importlib.util.spec_from_file_location('b3b', os.path.join(BASE, 'tools', 'batch_20261112f_3b.py'))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
NEW = mod.NEW

shutil.copy(MP, os.path.join(BASE, 'data', 'policies.backup-batch3b.json'))

d = json.load(io.open(MP, encoding='utf-8'))
exist_id = {p['id'] for p in d['policies']}
exist_url = {p.get('bjx_url') for p in d['policies'] if p.get('bjx_url')}

add = []
for p in NEW:
    if p['bjx_url'] in exist_url:
        print('跳过重复链接:', p['id'], p['title'][:30])
        continue
    if p['id'] in exist_id:
        raise SystemExit('ID 冲突: ' + p['id'])
    exist_id.add(p['id'])
    exist_url.add(p['bjx_url'])
    add.append(p)

print('待入库:', len(add))
if not add:
    raise SystemExit('无新增')

d['policies'].extend(add)
d['policies'].sort(key=lambda x: (x['publish_date'], x['id']))

REQ = ['id', 'title', 'region', 'level', 'issuer', 'publish_date', 'status', 'category',
       'summary', 'impact', 'logic', 'bjx_url', 'tier']
bad = [(p['id'], k) for p in d['policies'] for k in REQ if not p.get(k)]
# 索引层不要求要点
bad += [(p['id'], 'key_points') for p in d['policies']
        if p.get('tier') != 'index' and not p.get('key_points')]
ids = [p['id'] for p in d['policies']]
dup = len(ids) - len(set(ids))
print('总条数:', len(d['policies']), '| 字段缺失:', len(bad), '| 重复ID:', dup)
if bad:
    print('前5项:', bad[:5])
    raise SystemExit('校验失败')
if dup:
    raise SystemExit('ID 重复')

d['generated_at'] = '2026-11-12T21:05:00+08:00'
json.dump(d, io.open(MP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('已写入')
