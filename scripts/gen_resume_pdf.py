#!/usr/bin/env python3
"""
生成 PDF 简历
用法：python3 scripts/gen_resume_pdf.py
输出：马汉新_简历.pdf（项目根目录）

依赖安装：
  pip3 install weasyprint pyyaml
"""

import sys

# 检查依赖，缺失时给出明确提示
missing = []
try:
    import yaml
except ImportError:
    missing.append("pyyaml")
try:
    from weasyprint import HTML
except ImportError:
    missing.append("weasyprint")

if missing:
    print(f"[错误] 缺少依赖包：{', '.join(missing)}")
    print(f"请先执行：pip3 install {' '.join(missing)}")
    sys.exit(1)

from pathlib import Path

# ── 路径 ──────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
OUT  = ROOT / "马汉新_简历.pdf"

HOMEPAGE_URL = "https://mahanxin.github.io/my-homepage/"

# ── 读取数据 ──────────────────────────────────────────────
def load(name):
    with open(DATA / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)

profile    = load("profile")
experience = load("experience")["items"]
projects   = load("projects")["items"]
education  = load("education")["items"]

contacts = {c["label"]: c for c in profile.get("contacts", [])}
email  = next((c["label"] for c in profile["contacts"] if "mail" in c["href"]), "")
phone  = next((c["label"] for c in profile["contacts"] if "tel"  in c["href"]), "")

# ── HTML 模板 ─────────────────────────────────────────────
def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def render_highlights(highlights):
    if not highlights:
        return ""
    items = []
    for h in highlights:
        if isinstance(h, dict):
            sub_html = ""
            if h.get("sub"):
                sub_items = "".join(f"<li>{esc(s)}</li>" for s in h["sub"])
                sub_html = f'<ul class="sub">{sub_items}</ul>'
            items.append(f'<li>{esc(h["text"])}{sub_html}</li>')
        else:
            items.append(f'<li>{esc(h)}</li>')
    return f'<ul class="highlights">{"".join(items)}</ul>'

def render_tags(tags):
    if not tags:
        return ""
    spans = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)
    return f'<div class="tags">{spans}</div>'

# ── 工作经历 ──────────────────────────────────────────────
exp_html = ""
for e in experience:
    exp_html += f"""
<div class="block">
  <div class="row-between">
    <span class="org">{esc(e['company'])}</span>
    <span class="period">{esc(e['period'])}</span>
  </div>
  <div class="subtitle">{esc(e['position'])}</div>
  {render_highlights(e.get('highlights', []))}
  {render_tags(e.get('tags', []))}
</div>"""

# ── 项目经历 ──────────────────────────────────────────────
proj_html = ""
for p in projects:
    achs = "".join(f"<li>{esc(a)}</li>" for a in (p.get("achievements") or []))
    ach_block = f'<ul class="highlights">{achs}</ul>' if achs else ""
    proj_html += f"""
<div class="block">
  <div class="row-between">
    <span class="org">{esc(p['name'])}</span>
    <span class="period">{esc(p['period'])}</span>
  </div>
  <div class="proj-desc">{esc(p['desc'])}</div>
  {ach_block}
  {render_tags(p.get('tags', []))}
</div>"""

# ── 教育背景 ──────────────────────────────────────────────
edu_html = ""
for e in education:
    desc = f'<div class="proj-desc">{esc(e["desc"])}</div>' if e.get("desc") else ""
    edu_html += f"""
<div class="block">
  <div class="row-between">
    <span class="org">{esc(e['school'])}</span>
    <span class="period">{esc(e['period'])}</span>
  </div>
  <div class="subtitle">{esc(e['degree'])}</div>
  {desc}
</div>"""

# ── 完整 HTML ─────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
@page {{
  size: A4;
  margin: 18mm 20mm 16mm 20mm;
}}
body {{
  font-family: "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC",
               "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
  font-size: 9.5pt;
  color: #1e293b;
  line-height: 1.6;
}}
/* ── Header ── */
.header {{ text-align: center; margin-bottom: 14pt; }}
.header h1 {{ font-size: 22pt; font-weight: 700; letter-spacing: 4px; margin-bottom: 4pt; }}
.header .title {{ font-size: 11pt; color: #2563eb; margin-bottom: 5pt; }}
.contact-line {{ font-size: 8.5pt; color: #475569; margin-bottom: 3pt; }}
.contact-line a {{ color: #2563eb; text-decoration: none; }}
.bio {{ font-size: 9pt; color: #475569; margin-top: 5pt; }}
/* ── Section ── */
.section-title {{
  font-size: 11pt; font-weight: 700; color: #2563eb;
  border-bottom: 1.5pt solid #2563eb;
  padding-bottom: 2pt; margin: 12pt 0 7pt 0;
}}
/* ── Block ── */
.block {{ margin-bottom: 8pt; }}
.row-between {{
  display: flex; justify-content: space-between; align-items: baseline;
}}
.org {{ font-weight: 700; font-size: 10pt; }}
.period {{ font-size: 8pt; color: #64748b; white-space: nowrap; }}
.subtitle {{ font-size: 9pt; color: #2563eb; margin: 1pt 0 3pt 0; }}
.proj-desc {{ font-size: 8.5pt; color: #64748b; margin: 2pt 0 3pt 0; }}
/* ── Lists ── */
ul.highlights {{
  padding-left: 12pt; margin: 2pt 0 3pt 0;
}}
ul.highlights > li {{ margin-bottom: 2pt; font-size: 9pt; }}
ul.sub {{
  padding-left: 12pt; margin: 2pt 0 1pt 0;
  list-style-type: circle;
}}
ul.sub li {{ font-size: 8.5pt; color: #334155; margin-bottom: 1pt; }}
/* ── Tags ── */
.tags {{ display: flex; flex-wrap: wrap; gap: 3pt; margin-top: 3pt; }}
.tag {{
  background: #eff6ff; color: #2563eb;
  padding: 1pt 5pt; border-radius: 3pt;
  font-size: 7.5pt; font-weight: 500;
}}
/* ── Homepage link ── */
.homepage-link {{
  text-align: center; margin-top: 6pt;
  font-size: 8.5pt; color: #64748b;
}}
.homepage-link a {{ color: #2563eb; }}
</style>
</head>
<body>

<div class="header">
  <h1>{esc(profile['name'])}</h1>
  <div class="title">{esc(profile['title'])}</div>
  <div class="contact-line">
    {esc(profile.get('age',''))} 岁 &nbsp;·&nbsp;
    {esc(profile.get('gender',''))} &nbsp;·&nbsp;
    {esc(profile.get('location',''))} &nbsp;·&nbsp;
    ✉ {esc(email)} &nbsp;·&nbsp;
    📱 {esc(phone)}
  </div>
  <div class="contact-line">
    🌐 <a href="{HOMEPAGE_URL}">{HOMEPAGE_URL}</a>
  </div>
  <div class="bio">{esc(profile['bio'])}</div>
</div>

<div class="section-title">工作经历</div>
{exp_html}

<div class="section-title">项目经历</div>
{proj_html}

<div class="section-title">教育背景</div>
{edu_html}

</body>
</html>"""

# ── 渲染 PDF ──────────────────────────────────────────────
print("正在生成 PDF…")
HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
print(f"已生成：{OUT}")
