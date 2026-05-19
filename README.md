# ЭкоСознание — проектная документация

Русскоязычный ресурс об экологически осознанном образе жизни. Тезис: экологический кризис — это в первую очередь кризис восприятия.

**Манифест:** «Экология — это не тема для обсуждения. Это способ смотреть на реальность, видеть взаимосвязи там, где другие видят разрозненные объекты».

---

## Дизайн-система

**Шрифты:** Cormorant Garamond (заголовки, эссе) + Jost (интерфейс, описания)

**Цветовые переменные:**
```css
--ink: #1c2b1e; --ink-light: #3d5240; --moss: #4a7c59; --fern: #6ea87e;
--sage: #a8c5a0; --mist: #d4e6d0; --cream: #f3ede3; --warm: #ece5d6;
--paper: #faf6ef; --gold: #b8924a; --clay: #c4956a; --rust: #7a4f2e;
```

**SVG-логотип:** круг с разрывом (метафора гиперобъекта Мортона) + точка-центр #4a7c59.

---

## Файлы проекта (25 файлов)

| Файл | Описание | Статус |
|------|----------|--------|
| `ecolife-landing.html` | Главная · 11 разделов · блок «Свежее» 8 материалов | ✅ |
| `about.html` | О проекте · SVG-логотип · манифест редакции | ✅ |
| `glossary.html` | Глоссарий 28 терминов с поиском | ✅ |
| `section-icons-library.html` | Библиотека 12 SVG-знаков разделов | ✅ |
| `section-philosophy.html` | Философия 01/12 | ✅ |
| `section-psychology.html` | Психология 02/12 | ✅ |
| `section-lifestyle.html` | Стиль жизни 03/12 | ✅ |
| `section-technologies.html` | Технологии 04/12 | ✅ |
| `section-food.html` | Питание 05/12 | ✅ |
| `section-architecture.html` | Архитектура 06/12 | ✅ |
| `section-economy.html` | Экономика 07/12 | ✅ |
| `section-education.html` | Образование 09/12 | ✅ |
| `section-community.html` | Сообщество 10/12 | ✅ |
| `section-travel.html` | Путешествия 11/12 | ✅ |
| `section-health.html` | Здоровье 12/12 | ✅ |
| `essay-truth-and-climate.html` | Манифест Философии (~14 мин) | ✅ |
| `essay-passive-design.html` | Эссе Архитектуры — пассивный дизайн (~16 мин) | ✅ |
| `essay-solastalgia.html` | Эссе Психологии — соластальгия (~14 мин) | ✅ |
| `essay-community-survives.html` | Эссе Сообщества — что нужно общине (~15 мин) | ✅ |
| `essay-bread.html` | Эссе Питания — хлеб (~13 мин) | ✅ |
| `essay-morning-light.html` | Эссе Здоровья — утренний свет (~14 мин) | ✅ |
| `essay-moneyless-year.html` | Эссе Стиля жизни — год без денег (~15 мин) | ✅ |
| `lab-heidegger-plastic.html` | Лаборатория №01 — Алетейя пластика (~9 мин) | ✅ |
| `lab-hyperobject-room.html` | Лаборатория №02 — Гиперобъект в комнате (~10 мин) | ✅ |
| `README.md` | Эта документация | ✅ |

---

## Featured-блоки разделов → эссе

| Раздел | Эссе |
|--------|------|
| section-philosophy.html | essay-truth-and-climate.html |
| section-psychology.html | essay-solastalgia.html |
| section-architecture.html | essay-passive-design.html |
| section-food.html | essay-bread.html |
| section-community.html | essay-community-survives.html |
| section-health.html | essay-morning-light.html |
| section-lifestyle.html | essay-moneyless-year.html |

---

## SVG hero-mark-svg CSS

```css
.hero-mark-svg {
  position: absolute; right: 4rem; top: 11rem;
  width: 90px; height: 90px;
  color: rgba(74,124,89,0.18); pointer-events: none;
}
.hero-mark-svg svg { width: 100%; height: 100%; display: block; }
@media (max-width:800px) {
  .hero-mark-svg { right:1.5rem; top:9rem; width:60px; height:60px; }
}
```

---

## Редакционная политика

- Тон не учительский — исследуем вместе
- Честный взгляд — каждый раздел завершается критикой своей темы
- Связь с экологией структурная — не навязанная
- Цифры с источниками — мета-анализы, а не «учёные говорят»
- Эстетика не противоположна содержанию
- Русский язык как собственная мысль

---

## Backlog

- [x] Главная страница
- [x] Глоссарий и О проекте
- [x] 11 разделов из 12
- [x] 7 эссе
- [x] 2 лаборатории
- [x] SVG-иконография: логотип, hero-знаки, знаки рубрик, заставки эссе
- [ ] Раздел «Искусство» 08/12 — концепция: русскоязычная эко-эстетика как незанятая ниша
- [ ] Новые лаборатории (Бейтсон vs ChatGPT · Биография куртки · День в 15-мин городе)
- [ ] Рубрика «Разговор» — интервью или диалог
- [ ] Визуальная карта связей между разделами

---

*Последнее обновление: Май 2026*
