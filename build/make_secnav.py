#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЭкоСознание — внутренние меню разделов.

1. На каждой статье перед </main> — блок «Раздел»: темы раздела со всеми
   материалами (текущий отмечен), а для статей из цикла — навигация
   «предыдущая / следующая» и оглавление цикла.
2. На странице раздела сразу после полосы оглавления (или после hero) —
   блок «Материалы раздела по темам» с якорем #secmenu.

Темы и циклы задаются в build/sections.json. Материалы раздела, не
попавшие в темы, уходят в группу «Другое» — так новая статья не потеряется.
Блоки помечены ECO:MANAGED и перезаписываются при каждом запуске.

Запуск из корня сайта:   python3 build/make_secnav.py
"""

import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

META = json.load(open("build/pages.json", encoding="utf-8"))
CONF = json.load(open("build/sections.json", encoding="utf-8"))

SECTION_PAGE = {
    "Философия": "section-philosophy.html", "Психология": "section-psychology.html",
    "Стиль жизни": "section-lifestyle.html", "Технологии": "section-technologies.html",
    "Питание": "section-food.html", "Компост": "section-compost.html",
    "Архитектура": "section-architecture.html", "Строительство": "section-construction.html",
    "Экономика": "section-economy.html", "Образование": "section-education.html",
    "Сообщество": "section-community.html", "Путешествия": "section-travel.html",
    "Здоровье": "section-health.html", "Наука": "section-science.html",
    "Ревизия": "revisions.html",
}

ART = "secnav"
SEC = "secmenu"


def esc(s):
    return html.escape(s, quote=True)


def title(fn):
    return META[fn]["title"]


def visible(fn):
    m = META.get(fn)
    return m and m.get("kind") == "article" and not m.get("noindex") and os.path.exists(fn)


# материалы по разделам (по дате, затем по имени)
by_section = {}
for fn, m in META.items():
    if visible(fn) and m.get("section_title"):
        by_section.setdefault(m["section_title"], []).append(fn)
for k in by_section:
    by_section[k].sort(key=lambda f: (META[f].get("date", ""), f))


def groups_for(section):
    conf = CONF["sections"].get(section, [])
    members = set(by_section.get(section, []))
    used, out = set(), []
    for g in conf:
        items = [f for f in g["items"] if f in members and f not in used]
        used.update(items)
        if items:
            out.append((g["title"], items))
    rest = [f for f in by_section.get(section, []) if f not in used]
    if rest:
        out.append(("Другое" if out else "Материалы раздела", rest))
    return out


series_of = {}
for key, s in CONF["series"].items():
    items = [f for f in s["items"] if visible(f)]
    for i, f in enumerate(items):
        series_of[f] = (s["title"], items, i)


def group_html(groups, current=None):
    cols = []
    for gt, items in groups:
        lis = []
        for f in items:
            if f == current:
                lis.append(f'<li class="is-current" aria-current="page"><span>{esc(title(f))}</span></li>')
            else:
                lis.append(f'<li><a href="{f}">{esc(title(f))}</a></li>')
        cols.append(f'<div class="secnav-group"><div class="secnav-gtitle">{esc(gt)}</div><ul>{"".join(lis)}</ul></div>')
    return '<div class="secnav-groups">' + "".join(cols) + "</div>"


def series_html(fn):
    st, items, i = series_of[fn]
    prev_ = items[i - 1] if i > 0 else None
    next_ = items[i + 1] if i + 1 < len(items) else None
    pn = []
    pn.append(f'<a class="secnav-prev" href="{prev_}"><small>← Предыдущая</small>{esc(title(prev_))}</a>' if prev_ else '<span class="secnav-prev is-empty"></span>')
    pn.append(f'<a class="secnav-next" href="{next_}"><small>Следующая →</small>{esc(title(next_))}</a>' if next_ else '<span class="secnav-next is-empty"></span>')
    lis = []
    for j, f in enumerate(items, 1):
        if f == fn:
            lis.append(f'<li class="is-current" aria-current="page"><span>{j}. {esc(title(f))}</span></li>')
        else:
            lis.append(f'<li><a href="{f}">{j}. {esc(title(f))}</a></li>')
    return (f'<div class="secnav-series"><div class="secnav-series-label">Цикл «{esc(st)}» · часть {i + 1} из {len(items)}</div>'
            f'<div class="secnav-pn">{"".join(pn)}</div><ol class="secnav-series-list">{"".join(lis)}</ol></div>')


def article_block(fn):
    sec = META[fn]["section_title"]
    page = SECTION_PAGE.get(sec)
    head_link = f'<a class="secnav-title" href="{page}">{esc(sec)}</a>' if page else f'<span class="secnav-title">{esc(sec)}</span>'
    all_link = f'<a class="secnav-all" href="{page}#{SEC}">Все материалы раздела →</a>' if page and page.startswith("section-") else (
        f'<a class="secnav-all" href="{page}">Все материалы раздела →</a>' if page else "")
    parts = [f'<div class="secnav-head"><span class="secnav-label">Раздел</span>{head_link}{all_link}</div>']
    if fn in series_of:
        parts.append(series_html(fn))
    parts.append(group_html(groups_for(sec), fn))
    return (f"<!-- ECO:MANAGED:{ART} -->\n"
            f'<nav class="secnav" aria-label="Материалы раздела «{esc(sec)}»"><div class="secnav-in">{"".join(parts)}</div></nav>\n'
            f"<!-- /ECO:MANAGED:{ART} -->\n")


def section_block(sec):
    groups = groups_for(sec)
    n = sum(len(i) for _, i in groups)
    return (f"<!-- ECO:MANAGED:{SEC} -->\n"
            f'<nav class="secnav secnav-top" id="{SEC}" aria-label="Материалы раздела по темам"><div class="secnav-in">'
            f'<div class="secnav-head"><span class="secnav-label">В разделе</span><span class="secnav-title">{n} материалов по темам</span></div>'
            f"{group_html(groups)}</div></nav>\n"
            f"<!-- /ECO:MANAGED:{SEC} -->\n")


def strip(s, name):
    return re.sub(rf"<!-- ECO:MANAGED:{name} -->.*?<!-- /ECO:MANAGED:{name} -->\n?", "", s, flags=re.S)


done_a = done_s = 0
for sec, files in by_section.items():
    for fn in files:
        s = open(fn, encoding="utf-8").read()
        s = strip(s, ART)
        assert s.count("</main>") == 1, fn
        s = s.replace("</main>", article_block(fn) + "</main>", 1)
        open(fn, "w", encoding="utf-8").write(s)
        done_a += 1
    page = SECTION_PAGE.get(sec)
    if page and page.startswith("section-") and os.path.exists(page):
        s = strip(open(page, encoding="utf-8").read(), SEC)
        blk = section_block(sec)
        m = re.search(r'<div class="toc-bar">.*?</div>\n', s, flags=re.S)
        if m:
            s = s[:m.end()] + "\n" + blk + s[m.end():]
        else:
            m = re.search(r'<section class="hero".*?</section>\n', s, flags=re.S)
            s = s[:m.end()] + "\n" + blk + s[m.end():]
        open(page, "w", encoding="utf-8").write(s)
        done_s += 1

print(f"secnav: {done_a} статей, {done_s} страниц разделов")
