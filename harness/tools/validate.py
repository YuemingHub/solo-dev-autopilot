"""校验安装到 ohmyagent 全局配置目录后的 harness 层结构与 frontmatter。

用法:
  python harness/tools/validate.py [base]
  base 缺省 = %APPDATA%\\com.chaitin.baizhi.monkeycode\\ohmyagent
"""
import glob
import json
import os
import re
import sys

base = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.environ.get('APPDATA', ''),
    'com.chaitin.baizhi.monkeycode', 'ohmyagent')

ok = True

# 1. agents JSON 可解析
for p in glob.glob(os.path.join(base, 'agents', '*.json')):
    raw = open(p, encoding='utf-8-sig').read()
    try:
        d = json.loads(raw)
        print('OK ', os.path.basename(p), '| skills:', d.get('skills'))
    except Exception as e:
        ok = False
        print('FAIL', p, '->', e)

# 2. SKILL.md frontmatter(name/description)
skills = ['env-detect', 'env-setup', 'project-scaffold', 'dev-loop',
          'task-memory', 'harness-guard', 'book-experiments']
for s in skills:
    p = os.path.join(base, 'skills', s, 'SKILL.md')
    if not os.path.exists(p):
        p = os.path.join(base, 'skills', s + '.md')  # 平铺单文件格式
    if not os.path.exists(p):
        ok = False
        print('SKILL MISSING', s)
        continue
    txt = open(p, encoding='utf-8-sig').read()
    m = re.match(r'^---\nname: (.+)\ndescription:', txt, re.S)
    if m:
        print('SKILL OK', m.group(1))
    else:
        ok = False
        print('SKILL BAD FRONTMATTER', s)

# 3. 相对链接可达
for s in skills:
    p = os.path.join(base, 'skills', s, 'SKILL.md')
    if not os.path.exists(p):
        p = os.path.join(base, 'skills', s + '.md')
    if not os.path.exists(p):
        continue
    txt = open(p, encoding='utf-8-sig').read()
    for m in re.finditer(r'\]\(([^)#]+)(#[^)]*)?\)', txt):
        link = m.group(1)
        if link.startswith(('http://', 'https://')) or link.startswith('/'):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(p), link))
        if not os.path.exists(target):
            ok = False
            print('BROKEN LINK', s, '->', link)

print('ALL OK' if ok else 'HAS ISSUES')
sys.exit(0 if ok else 1)
