#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЭкоСознание — меню циклов статей.

На каждой статье, входящей в цикл (например, «Дом по климату»), перед
</main> выводится блок: название цикла, номер части, ссылки «предыдущая /
следующая» и оглавление всего цикла с отмеченной текущей статьёй.
Статьи вне циклов и страницы разделов блока не получают.

Циклы задаются в build/sections.json (ключ series). Блок помечен
ECO:MANAGED:secnav и перезаписывается при каждом запуске; со страниц,
выбывших из цикла, он удаляется.

Запуск из корня сайта:   python3 build/make_secnav.py
"""

import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

META = json.load(open("build/pages.json", encoding="utf-8"))
CONF = json.load(open("build/sections.json", encoding="utf-8"))

ART = "secnav"
OLD = "secmenu"  # прежний блок на страницах разделов — только удаляем


def esc(s):
    return html.escape(s, quote=True)


def title(fn):
    return META[fn]["title"]


def visible(fn):
    m = META.get(fn)
    return bool(m) and not m.get("noindex") and os.path.exists(fn)


series_of = {}
for s in CONF["series"].values():
    items = [f for f in s["items"] if visible(f)]
    for i, f in enumerate(items):
        series_of[f] = (s["title"], items, i)


def block(fn):
    st, items, i = series_of[fn]
    prev_ = items[i - 1] if i > 0 else None
    next_ = items[i + 1] if i + 1 < len(items) else None
    pn = [
        f'<a class="secnav-prev" href="{prev_}"><small>← Предыдущая</small>{esc(title(prev_))}</a>' if prev_
        else '<span class="secnav-prev is-empty"></span>',
        f'<a class="secnav-next" href="{next_}"><small>Следующая →</small>{esc(title(next_))}</a>' if next_
        else '<span class="secnav-next is-empty"></span>',
    ]
    lis = []
    for j, f in enumerate(items, 1):
        if f == fn:
            lis.append(f'<li class="is-current" aria-current="page"><span>{j}. {esc(title(f))}</span></li>')
        else:
            lis.append(f'<li><a href="{f}">{j}. {esc(title(f))}</a></li>')
    return (f"<!-- ECO:MANAGED:{ART} -->\n"
            f'<nav class="secnav" aria-label="Цикл «{esc(st)}»"><div class="secnav-in">'
            f'<div class="secnav-head"><span class="secnav-label">Цикл</span>'
            f'<span class="secnav-title">{esc(st)}</span>'
            f'<span class="secnav-part">часть {i + 1} из {len(items)}</span></div>'
            f'<div class="secnav-series"><div class="secnav-pn">{"".join(pn)}</div>'
            f'<ol class="secnav-series-list">{"".join(lis)}</ol></div>'
            f"</div></nav>\n"
            f"<!-- /ECO:MANAGED:{ART} -->\n")


def strip(s, name):
    return re.sub(rf"<!-- ECO:MANAGED:{name} -->.*?<!-- /ECO:MANAGED:{name} -->\n?", "", s, flags=re.S)


added = removed = 0
for fn in sorted(glob.glob("*.html")):
    s0 = open(fn, encoding="utf-8").read()
    s = strip(strip(s0, ART), OLD)
    if fn in series_of:
        assert s.count("</main>") == 1, fn
        s = s.replace("</main>", block(fn) + "</main>", 1)
        added += 1
    elif s != s0:
        removed += 1
    if s != s0:
        open(fn, "w", encoding="utf-8").write(s)

print(f"secnav: блок цикла на {added} статьях, удалён с {removed} страниц")
