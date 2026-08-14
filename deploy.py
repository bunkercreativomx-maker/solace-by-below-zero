#!/usr/bin/env python3
"""Push del portal de Solace by Below Zero a GitHub Pages (repo bunkercreativomx-maker/solace-by-below-zero).
Usa GITHUB_TOKEN del .env como x-access-token (patrón probado en empire/solace).
"""
import os, re, subprocess, sys

BASE = '/opt/data/solace-by-below-zero'
REPO = 'https://github.com/bunkercreativomx-maker/solace-by-below-zero.git'

def run(cmd, cwd=BASE):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'ERR: {cmd}\n{r.stderr[:800]}')
    return r

# token
txt = open('/opt/data/.env').read()
m = re.search(r'^GITHUB_TOKEN=(.+)$', txt, re.M)
if not m:
    sys.exit('GITHUB_TOKEN no encontrado')
tok = m.group(1).strip()
remote = f'https://x-access-token:{tok}@github.com/bunkercreativomx-maker/solace-by-below-zero.git'

# init si falta
if not os.path.isdir(os.path.join(BASE, '.git')):
    run('git init -b main')
run('git remote remove origin 2>/dev/null || true')
run(f'git remote add origin "{remote}"')

# .gitignore para no subir scripts de build ni contact sheets
open(os.path.join(BASE, '.gitignore'), 'w').write(
    'build_portal.py\ngenerate_batch.py\nqa_batch.py\nmake_contact_sheets.py\n'
    'contact_sheet_30.png\ncontact_g*.png\nimages/pilot_*\n*.tmp.png\n')

run('git add -A')
r = run('git -c user.email=hermes@bunkercreative.mx -c user.name="Bunker Creative MX" commit -m "Solace by Below Zero — 30-day FB calendar + Meta Ads approval portal"')
run('git push -u origin main --force')
print('push listo')
