# AGENTS.md — Futebol com Python ⚽🐍

Instructions for AI coding agents (Claude Code, Codex, Cursor, etc.) working on this repository. Read this whole file before creating or changing anything.

## 1. What this project is

A series of Google Colab notebooks that teach an **8-year-old Brazilian boy who is gifted in math (GT)** Python, statistics, math and logic through **soccer**. Each notebook asks a question a young fan already cares about ("Who is the best young scorer in Europe?", "How many packs do I need to fill the sticker album?") and answers it with code.

The kid stays motivated through a **reward system**: aura points, meme reactions (sigma, 67, Lamine Yamal dance, "farmando aura"), and **mini-games that unlock** when he answers. Rewards, mini-games, media links and fun facts all live in this GitHub repo and are downloaded into Colab by the first cell of every notebook.

## 2. The learner

- Age 8, strong at math, still a slow typist. **Reading level matters more than math level.**
- Usually works with a parent nearby, on a laptop or tablet; sometimes the parent tests on a phone. Everything must work with touch (no hover-only or keyboard-only controls in games).
- Short attention bursts: one mission takes 3–5 minutes, one notebook sitting about 15–25 minutes.

## 3. Language rules (strict)

- **All Markdown cells and all code comments are in Brazilian Portuguese (pt-BR).** No English in anything the kid reads, including printed messages, chart titles, axis labels, widget labels, error messages and game text.
- Use Brazilian football vocabulary: *futebol, gol, chute, goleiro, zagueiro, meio-campo, atacante, escalação, campeonato, pênalti, embaixadinha, figurinha, olheiro, joia (prospect), base (youth categories)*.
- Kid-facing variables and helper functions use Portuguese names without accents: `gols`, `jogos`, `minutos`, `nascido`, `valor_milhoes`, `checar()`, `comemorar()`. Python keywords and library methods (`print`, `sort_values`, `len`) stay as they are, and each one is explained in Portuguese the first time it appears.
- Data columns are renamed to Portuguese in the setup cell: `nome, clube, liga, posicao, pais, nascido, jogos, minutos, gols, assistencias, valor_milhoes`.
- Short sentences. Use "você". No sarcasm the kid could misread. Explain every symbol the first time (`=` guarda, `==` pergunta, `>=` maior ou igual).
- Internal (non-kid-facing) library code may have English identifiers, but its docstrings and comments are also in pt-BR.

## 4. Repository layout

```
FutebolComPython/
├── AGENTS.md
├── README.md                    # pt-BR, for parents: how to open in Colab (desktop and phone)
├── notebooks/
│   ├── nivel1_sub9/             # one folder per level, files numbered globally
│   ├── nivel2_sub11/
│   ├── nivel3_sub13/
│   └── nivel4_sub15/
├── vestiario/                   # Python package imported by every notebook ("locker room")
│   ├── __init__.py              # iniciar(), checar(), chute(), comemorar(), etc.
│   ├── aura.py                  # aura points, streaks, levels, the 67 easter egg
│   ├── reacoes.py               # shows GIFs/emoji reactions from midia/reacoes.json
│   ├── jogos.py                 # unlocks and launches mini-games
│   ├── curiosidades.py          # fun facts + Wikipedia links (section 9)
│   ├── progresso.py             # save/load progress (Drive or secret code)
│   └── dados.py                 # loads the data snapshot (section 10)
├── jogos/                       # self-contained HTML/JS mini-games
├── midia/
│   ├── reacoes.json             # links to reaction GIFs (never the GIF files themselves)
│   └── sons/                    # short original or CC0 sound effects only
├── dados/
│   ├── jogadores_2025_26.csv.gz # snapshot built by scripts/preparar_dados.py
│   ├── clubes.csv
│   └── curiosidades.json        # curated, sourced fun facts
├── scripts/
│   ├── preparar_dados.py
│   ├── verificar_curiosidades.py
│   └── testar_notebooks.py
└── tests/
```

The GitHub repo URL is set in one place, `vestiario/config.py` (and the bootstrap cell). The repo is `https://github.com/brunicardoso/FutebolComPython`.

## 5. Curriculum: four levels, increasing difficulty

Levels are named after Brazilian youth categories. **It is not only statistics:** each notebook mixes Python, math or logic, and soccer. A notebook only uses concepts introduced in earlier notebooks.

| # | Notebook | Python | Math / stats / logic |
|---|---|---|---|
| **Nível 1 — Sub-9 (fundamentos)** ||||
| 01 | Python é uma calculadora (placar e saldo de gols) | `print`, variables, `+ - * /` | negative numbers, goal difference |
| 02 | Olheiro de Joias | tables, `head`, `sort_values`, filters | guess-and-check, percent error, totals vs. rates |
| 03 | Monte sua escalação | lists, `len`, indexes, `append` | counting, formations (4-3-3 adds up to 10 + goalkeeper) |
| 04 | Cara ou coroa e pênaltis | `random`, simple loops | chance, fractions, "fair" games |
| **Nível 2 — Sub-11 (lógica)** ||||
| 05 | O VAR decide | `if / elif / else`, booleans | logic, `and` / `or` |
| 06 | Tabela do campeonato | `for` loops, accumulators | points system (3/1/0), sorting with tiebreakers |
| 07 | Gols por 90 minutos | new columns, division | rates, fairness, the small-sample trap |
| 08 | Média ou mediana? | `mean`, `median`, `max`, `min` | outliers (one superstar's market value) |
| **Nível 3 — Sub-13 (geometria e simulação)** ||||
| 09 | Desenhe o campo | `matplotlib`, coordinates | x/y plane, rectangle area, perimeter, scale |
| 10 | Distância e ângulo do chute | functions with `def`, `math` | Pythagoras, angles, why wide shots are harder |
| 11 | 10.000 disputas de pênaltis | loops + `random`, counters | Monte Carlo, law of large numbers |
| 12 | O álbum de figurinhas | dictionaries, `while` | coupon collector problem: how many packs to finish? |
| **Nível 4 — Sub-15 (construindo coisas)** ||||
| 13 | Sua carta de jogador | functions, f-strings, dictionaries | weighted average (overall rating) |
| 14 | Idade e gols andam juntos? | scatter plots | correlation is not causation |
| 15 | Simulador de campeonato | functions + loops + `random` | probability, expected value, simple ratings |
| 16 | Projeto final: seu jogo de futebol | everything | the kid designs the rules |

Difficulty rules:

- **Nível 1:** kid types at most 1–2 short lines per mission; fill-in-the-blank allowed (`gols = ___`).
- **Nível 2:** up to 3–4 lines; first blank-cell challenges.
- **Nível 3:** writes small functions; reads error messages (with a pt-BR "como ler um erro" guide).
- **Nível 4:** writes most code; notebooks give goals, not code.
- Every notebook ends with a **Desafio do Técnico** (2 challenges; the second is ⭐ hard) with hidden answers in a collapsed `#@title 🔑 Respostas` form cell.

## 6. Notebook template (every notebook follows this order)

1. **Bootstrap cell** (hidden Colab form; the only thing the kid presses first):

   ```python
   #@title ⚽ Preparar o vestiário (aperte o play)
   REPO = "https://github.com/brunicardoso/FutebolComPython"
   import os, sys
   if not os.path.exists("/content/futebol"):
       !git clone -q --depth 1 {REPO} /content/futebol
   else:
       !git -C /content/futebol pull -q
   sys.path.insert(0, "/content/futebol")
   from vestiario import *
   iniciar(nivel=1, notebook="02_olheiro")
   ```

   `iniciar()` loads data, restores progress, shows the aura counter and a welcome reaction. It must finish in under 60 s on Colab.

2. Title, **a pergunta grande**, and a small table "O que você vai aprender" (🐍 Python / 📊 Matemática).
3. Collapsed `<details>` block **"Para os pais"**: goals, pace, data source, how to open on a phone.
4. **Aquecimento** (warm-up, 1 minute, guaranteed win to start with a reward).
5. **Missões 1…N**, each following: *palpite* (guess) → kid's code → `checar()` / `chute()` → reaction → short "🤔 Pense:" question → "✏️ Tente:" variation.
6. **Curiosidades** appear after results that name players or clubs (section 9).
7. **Desafio do Técnico** + hidden answers.
8. **Jogo do vestiário** (bonus game) and **Resumo**: what was learned, total aura, the progress code, and a teaser for the next notebook.

Technical rules for notebooks:

- Setup and helper code go in `#@title` form cells with `"cellView": "form"` metadata so the code is hidden.
- Kid-facing cells stay short and must run in under 5 s after setup.
- Use `random.seed()` wherever an answer must be checkable; leave it unseeded where variety is the point (simulations).
- Notebooks are committed **without outputs** (`nbstripout`).
- Target Colab's current runtime (Python 3.12+, pandas 2.x). Use only libraries preinstalled on Colab plus `ipywidgets`. No `pip install` in kid-facing cells.

## 7. Reward system ("farmando aura")

The goal is fast, funny, varied feedback that keeps an 8-year-old going, while the learning stays the main event.

### Aura points

- Correct answer: **+100 aura**; first try: **+50 bonus**; hard ⭐ challenge: **+500**.
- **Sequência (streak):** 3 correct in a row shows "🔥 Sequência de 3!"; 5 in a row triggers a rare reaction.
- Aura is **never subtracted**. Wrong answers keep the streak count but break it.
- Levels by total aura, shown as a progress bar: Reserva → Titular → Craque → Lenda → Sigma Supremo.
- Every aura change prints a big line like `✨ +100 de aura! Você está farmando aura: 1.350 ✨`.

### Reactions (meme mapping)

Reactions come from `midia/reacoes.json`. Each category has several options picked at random (variable rewards feel better than the same GIF every time). Every entry needs an emoji/ASCII fallback for when the link fails or the device is offline.

| Moment | Category | Example text (pt-BR) |
|---|---|---|
| Correct answer | `sigma`, `aura` | "Resposta sigma. 🗿" / "+100 de aura ✨" |
| Hard challenge, 5-streak, finishing a notebook | `yamal_danca` (rare) | "Isso merece a dancinha do Lamine Yamal! 💃⚽" |
| Any result, guess or aura total equal to 67 (or 670, 6.700) | `seis_sete` | "SIX SEVEN! 🤲 67!" |
| Wrong answer | `beta` | "Modo beta 🔧: versão de teste! Todo craque treina. Dica: …" |
| Very close guess (within 10%) | `quase` | "Na trave! 🥅" |

**The "beta" rule:** wrong answers use *beta* as in a **beta version of software** (still being tested, about to be upgraded), **never** as a label for the kid. No reaction may mock, call him names, or imply he is bad at something. The joke is always about the situation, and every wrong-answer reaction comes with a hint and a retry.

**The 67 easter egg:** `aura.py` checks every number passed through `checar()` and `chute()`, every aura total, and the kid's own guesses. Rate-limit it to at most once per mission so it stays special.

### Media links and copyright (strict)

- **Never commit third-party GIFs, video clips, player photos, club crests or copyrighted sounds to this repo.** That includes Lamine Yamal dance clips and meme GIFs.
- `midia/reacoes.json` stores only **links** from platforms that provide share/embed links (e.g. GIPHY, Tenor), plus the fallback text:

  ```json
  {
    "yamal_danca": [
      {"url": "https://media.giphy.com/media/EXEMPLO/giphy.gif",
       "fallback": "💃⚽💃⚽💃", "texto": "Dancinha do Lamine Yamal!"}
    ],
    "seis_sete": [
      {"url": "...", "fallback": "🤲 6️⃣7️⃣ 🤲", "texto": "SIX SEVEN!"}
    ]
  }
  ```

- The parent chooses and adds the links. Agents may add placeholder entries and **must not invent URLs**: an entry with an unverified URL must have `"url": null` so the fallback is used.
- Reactions are displayed with `IPython.display` (HTML `<img>` with a fixed max width of 300px), never downloaded and re-hosted.
- Agents do not generate images or drawings of real people. Original drawings (a cartoon ball, a trophy, a generic player silhouette) are fine.
- Sounds: only original or CC0 files, under 1 s, muted by default with a 🔊 toggle.

## 8. Mini-games (unlocked on right **and** wrong answers)

Mini-games are short HTML/JS files in `jogos/`, displayed inline in Colab through `IPython.display.HTML`.

| Trigger | What unlocks | Purpose |
|---|---|---|
| Correct answer on a mission marked `desbloqueia=True` | A new **jogo de campeão** added permanently to the kid's *vestiário* (collection) | Reward |
| Wrong answer | A 20–30 s **treino rápido** (quick drill) that ends by showing the hint, then asks to retry | Turns a miss into play instead of frustration |
| Finishing a notebook | The notebook's **jogo do vestiário** | Big reward |

Game ideas, roughly in unlock order: *Pênalti* (tap where to shoot; the goalkeeper dives randomly), *Embaixadinhas* (tap to keep the ball up), *Goleiro reflexo* (tap the ball before it crosses the line), *Falta com barreira* (pick an angle and power; ties into notebook 10's geometry), *Álbum relâmpago* (open packs; ties into notebook 12), *Tabela maluca* (sort teams by points as fast as possible).

Rules for games:

- **One self-contained HTML file each**: inline CSS and JS, no external libraries or network requests (except links from `reacoes.json`), under 200 KB.
- Touch-first: big tap targets (at least 48px), works at 360px wide, no keyboard required.
- All text in pt-BR. Rounds last 30–60 s and end with a clear "Fim de jogo!" and a replay button.
- A wrong answer must never pay more than a right one: treino games give no aura, and champion games give at most +50 aura per play (reported back via `google.colab.kernel.invokeFunction` when available; otherwise no aura).
- `vestiario()` shows the kid's collection: unlocked games as playable cards, locked ones as "🔒 ???".
- Original art only (shapes, emoji, CSS); no club crests, real kits or player likenesses.

## 9. Curiosidades and Wikipedia links

Whenever an output names players or clubs (top-10 tables, Scout Mode, card battles), show **up to 3 fun facts** below it, each with a link to the subject's **Portuguese Wikipedia** page.

Display format (Markdown/HTML in the output):

> 💡 **Curiosidade:** Lamine Yamal estreou no time principal do Barcelona com apenas 15 anos.
> 📖 [Leia mais na Wikipédia](https://pt.wikipedia.org/wiki/Lamine_Yamal)

### Sources, in priority order

1. **`dados/curiosidades.json` (curated, preferred).** Keyed by Transfermarkt `player_id` / `club_id`:

   ```json
   {
     "jogadores": {
       "ID_TRANSFERMARKT_DO_JOGADOR": {
         "nome": "Lamine Yamal",
         "wikipedia_pt": "https://pt.wikipedia.org/wiki/Lamine_Yamal",
         "curiosidades": [
           {"texto": "…", "fonte": "https://…", "verificado_em": "2026-10-31"}
         ]
       }
     },
     "clubes": { "…": { "nome": "…", "wikipedia_pt": "…", "curiosidades": [ … ] } }
   }
   ```

2. **Wikidata mapping (to build and maintain the links).** Wikidata stores Transfermarkt IDs for players and clubs, so `scripts/verificar_curiosidades.py` can map a Transfermarkt ID → Wikidata item → `ptwiki` sitelink exactly, with no guessing by name. Look up and verify the correct Wikidata property IDs before using them. Fall back to `enwiki` only when no pt-BR page exists, and label that link "(em inglês)".
3. **Live summary (optional, runtime).** For players with no curated facts, `curiosidades.py` may fetch the first sentence from the pt Wikipedia REST summary endpoint (`/api/rest_v1/page/summary/{title}`) for a page already mapped in step 2. Send a descriptive `User-Agent` as Wikimedia requires, cache results per session, time out after 3 s, and show nothing if it fails. Never pick a page by name search alone.

### Rules for fun facts

- **Every curated fact must be true and sourced** (`fonte` + `verificado_em`). Do not write facts from memory: an agent adding facts must verify each one against Wikipedia or another reliable source and include the URL. Unverifiable facts are left out.
- Kid-friendly, in short pt-BR sentences: debuts, records, nicknames, hometown, club founding year, stadium size, titles, fun numbers (good hooks for math, such as record attendances).
- **Football and public career only.** No family drama, injuries described graphically, legal issues, salaries of minors, betting, or rumors.
- **Players under 18:** only on-pitch, public football facts; no photos; no birthplace details beyond country.
- Facts with numbers can become bonus questions, using the verified number from the fact (e.g. "Se o estádio tem N lugares, quantos a mais que 67.000?").
- Wikipedia photos are not shown by default. If enabled later, use only Commons images with their license and author credited, and never for players under 18.

## 10. Data

- Source: [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets) (license **CC0 1.0**). Its updates paused in July 2026, so the snapshot covers the **complete 2025–26 season**. Say this in each notebook's parent section.
- `scripts/preparar_dados.py` downloads the raw tables (with a browser `User-Agent`, since the server returns 403 to Python's default; Kaggle `davidcariboo/player-scores` as fallback), filters to the five big leagues (`GB1, ES1, L1, IT1, FR1`) and league games of 2025-07-01 to 2026-06-30, aggregates per player, renames columns to Portuguese, shortens club names, and writes `dados/jogadores_2025_26.csv.gz`. Keep `player_id` and `club_id` so curiosidades can be joined.
- Notebooks load **the repo snapshot**, not the raw source: faster, works offline from the clone, and avoids the 403 problem.
- Credit the source in the README and in each notebook's parent section.
- Simulation notebooks (04, 11, 12, 15) need no external data.

## 11. `vestiario` API (kid-facing functions)

Keep the signatures simple; the kid calls these directly.

```python
iniciar(nivel, notebook)            # setup, progress, welcome reaction
checar(resposta, missao="m1")       # compares with the stored answer; triggers aura, reactions, games
chute(palpite, real)                # guess game: shows percent error, "na trave" if within 10%
comemorar(tipo="aura")              # manual celebration (for the parent to trigger)
dica(missao="m1")                   # shows the hint for a mission
curiosidades(tabela, n=3)           # fun facts + Wikipedia links for players/clubs in a table
vestiario()                         # shows unlocked games and aura level
jogar(nome)                         # launches an unlocked game
salvar_progresso() / carregar_progresso(codigo)
```

- `checar()` normalizes text answers (case, accents, extra spaces) and accepts numbers within a stated tolerance. Expected answers that depend on data are **computed from the snapshot**, not hard-coded.
- Correct: reaction + aura + maybe unlock. Wrong: beta reaction + hint + treino game + "tente de novo". After 3 misses, show the answer with an explanation (no aura), so he never gets stuck.
- **Progress:** Colab forgets everything when the session ends. `salvar_progresso()` offers (a) saving to Google Drive (optional, asks permission via `drive.mount`), or (b) a short **código secreto** like `AURA-1350-J3-7F2` encoding aura, unlocked games and completed notebooks with a checksum, which the kid types into the next notebook. Option (b) always works and is the default.
- No personal data is collected or sent anywhere. The only network calls are: git clone, the reaction links, and the optional Wikipedia summary.

## 12. Wellbeing guardrails

- Rewards follow effort and correct thinking; the explanation ("🤔 Pense:") always comes right after the reaction, never skipped.
- After about 20 minutes of activity in a session, `iniciar()`'s timer shows a friendly **"⏸️ Intervalo!"** suggestion (stretch, drink water, go kick a real ball). It is a suggestion, not a lock.
- Games are capped per notebook (the jogo do vestiário can be replayed; treino games show up only after wrong answers).
- No ads, purchases, external chat, social links, or links outside Wikipedia and the approved reaction platforms.

## 13. Testing and definition of done

Before considering a change done:

1. `python scripts/testar_notebooks.py` runs every notebook headless (nbclient) against the snapshot, with kid cells filled from the hidden answers, and finishes with no errors.
2. `pytest tests/` passes: answer checking (accents, tolerance), aura math, the 67 easter egg, progress code round-trip, reaction fallbacks when a URL is `null` or unreachable, curiosidades lookup by ID.
3. A language check finds **no English** in Markdown cells, comments, printed strings, chart labels or game text (allow-list: Python keywords, library names, column codes).
4. Every game in `jogos/` opens in a 360px-wide browser, works by touch, and makes no network requests.
5. Every curated fact has `fonte` and `verificado_em`; every Wikipedia link resolves (checked by `scripts/verificar_curiosidades.py`).
6. No copyrighted media files were added (`git diff --stat` shows no `.gif`, `.mp4` or player images).
7. Notebooks are committed without outputs, and each opens in Colab from GitHub with the bootstrap cell working first try.

## 14. Use pixi for local building and test