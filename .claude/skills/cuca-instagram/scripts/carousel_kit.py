"""Kit de carrosséis do Cuca Pensante.

Monta a prévia (moldura de Instagram, arrastável) com slides na identidade da
marca. Cada slide é um <section class="slide"> que o export.py fotografa.

Uso típico:

    import sys; sys.path.insert(0, ".claude/skills/cuca-instagram/scripts")
    from carousel_kit import *

    c = Carousel(game="tramela")              # ou game=None para o estúdio
    c.add(f'<div class="h1">Você acha o culpado?</div>', variant="glow", tag="DESAFIO")
    c.add(phone("instagram/prints/tramela/01.png"), variant="dark")
    c.write("instagram/posts/2026-10-06-tramela-desafio/preview.html",
            caption="Texto da legenda…")

Sempre gere o HTML por Python (nunca heredoc de shell): base64 e "$" quebram.
"""
from __future__ import annotations

import base64
import html as _html
import json
import mimetypes
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # raiz do repositório cucapensante
ASSETS = ROOT / "assets"

HANDLE = "cucapensante.jogos"

GAMES = {
    "blueprint": {"name": "Blueprint Mansion", "color": "#00E5FF", "icon": "blueprint-icon.png", "kind": "Roguelike tático"},
    "nodyx":     {"name": "Nodyx",             "color": "#7C7FF5", "icon": "nodyx-icon.png",     "kind": "Puzzles casuais"},
    "tramela":   {"name": "Tramela",           "color": "#38BDF8", "icon": "tramela-icon.png",   "kind": "Dedução espacial"},
    "encaixe":   {"name": "Encaixe",           "color": "#F2B632", "icon": "encaixe-icon.png",   "kind": "Cruzadinha diária"},
}
STUDIO_COLOR = "#00E5FF"

# Proporção: 3:4 (1080×1440) é o padrão atual do feed; 4:5 (1080×1350) também serve.
# 9:16 (1080×1920) é story: cada slide vira um quadro, sem barra de progresso nem seta.
FORMATS = {"3:4": (420, 560), "4:5": (420, 525), "9:16": (420, 746.667)}


# ---------------------------------------------------------------- utilidades

def esc(text: str) -> str:
    return _html.escape(str(text), quote=True)


def data_uri(path: str | Path) -> str:
    """Embute uma imagem como data: URI, detectando o formato real do arquivo."""
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    head = p.read_bytes()[:12]
    if head.startswith(b"\x89PNG"):
        mime = "image/png"
    elif head[:3] == b"\xff\xd8\xff":
        mime = "image/jpeg"
    elif head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        mime = "image/webp"
    else:
        mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def shrink(path: str | Path, max_side: int = 1400) -> Path:
    """Reduz prints enormes (ex.: 1290×2796) para não pesar a prévia. Usa sips (macOS)."""
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    out = Path("/tmp") / f"cuca-shrink-{p.stem}-{max_side}{p.suffix}"
    if not out.exists():
        subprocess.run(["sips", "-Z", str(max_side), str(p), "--out", str(out)],
                       check=True, capture_output=True)
    return out


def mark_svg(size: int = 28, mono: bool = False) -> str:
    """Símbolo do Cuca Pensante inline. mono=True usa currentColor (para fundos coloridos)."""
    svg = (ASSETS / "brand" / ("cuca-mark-mono.svg" if mono else "cuca-mark.svg")).read_text().strip()
    return svg.replace('width="68" height="68"', f'width="{size}" height="{size}" aria-hidden="true"', 1)


def game_icon(game: str, size: int = 56) -> str:
    g = GAMES[game]
    return (f'<img class="gicon" src="{data_uri(ASSETS / g["icon"])}" '
            f'style="width:{size}px;height:{size}px;--gc:{g["color"]}" alt="{esc(g["name"])}">')


# ---------------------------------------------------------------- componentes

def phone(img: str | Path, width: int = 190, tilt: float = 0, glow: bool = True) -> str:
    """Print de tela dentro de um celular desenhado. Use prints na vertical."""
    src = data_uri(shrink(img))
    style = f"width:{width}px;transform:rotate({tilt}deg)"
    return f'<div class="phone{" glow" if glow else ""}" style="{style}"><img src="{src}" alt=""></div>'


def phones(*imgs: str | Path, width: int = 160) -> str:
    """Dois ou três celulares em leque."""
    tilts = {1: [0], 2: [-6, 6], 3: [-9, 0, 9]}[len(imgs)]
    inner = "".join(phone(i, width=width, tilt=t) for i, t in zip(imgs, tilts))
    return f'<div class="phones n{len(imgs)}">{inner}</div>'


def chips(*items: str) -> str:
    return '<div class="chips">' + "".join(f"<span>{esc(i)}</span>" for i in items) + "</div>"


def clue(label: str, text: str) -> str:
    """Cartão de pista (Tramela: BIOMETRIA, CÂMERA, SENSOR, CONDICIONAL…)."""
    return f'<div class="clue"><b>{esc(label)}</b><p>{esc(text)}</p></div>'


def steps(*items: tuple[str, str]) -> str:
    """Lista ordenada de passos (título, descrição). Só para sequências reais."""
    out = []
    for i, (t, d) in enumerate(items, 1):
        out.append(f'<div class="step"><span>{i:02d}</span><div><b>{esc(t)}</b><p>{esc(d)}</p></div></div>')
    return '<div class="steps">' + "".join(out) + "</div>"


def crossword(grid: list[str], words: list[dict], reveal: bool = False, cell: int = 52) -> str:
    """Grade do Encaixe. grid: linhas com letras e '#' para casa preta."""
    nums = {(w["row"], w["col"]): w["number"] for w in words}
    n = len(grid)
    cells = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                cells.append('<i class="blk"></i>')
                continue
            num = f"<sup>{nums[(r, c)]}</sup>" if (r, c) in nums else ""
            letter = f"<em>{esc(ch)}</em>" if reveal else ""
            cells.append(f"<i>{num}{letter}</i>")
    return (f'<div class="cw" style="--n:{n};--cell:{cell}px">' + "".join(cells) + "</div>")


def crossword_clues(words: list[dict], direction: str) -> str:
    title = "Horizontais" if direction == "across" else "Verticais"
    items = "".join(f"<li><b>{w['number']}</b>{esc(w['clue'])}</li>"
                    for w in words if w["direction"] == direction)
    return f'<div class="cw-clues"><h4>{title}</h4><ol>{items}</ol></div>'


def _palavra_cores(guess: str, answer: str) -> list[str]:
    """certa / presente / ausente, com a regra usual de letras repetidas."""
    guess, answer = guess.upper(), answer.upper()
    res = ["ausente"] * len(guess)
    sobra: dict[str, int] = {}
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            res[i] = "certa"
        else:
            sobra[a] = sobra.get(a, 0) + 1
    for i, g in enumerate(guess):
        if res[i] != "certa" and sobra.get(g, 0) > 0:
            res[i] = "presente"
            sobra[g] -= 1
    return res


def palavra(guesses: list[str], answer: str, rows: int = 6, cell: int = 40) -> str:
    """Tabuleiro da Palavra do dia do Encaixe (5 letras, 6 tentativas), nas cores do jogo.
    Use respostas de dias passados ou a palavra de exemplo do app ("santa")."""
    out = []
    for r in range(rows):
        if r < len(guesses):
            g = guesses[r].upper()
            out += [f'<i class="{c}"><em>{esc(ch)}</em></i>' for ch, c in zip(g, _palavra_cores(g, answer))]
        else:
            out += ["<i></i>"] * len(answer)
    return f'<div class="pw" style="--cell:{cell}px">' + "".join(out) + "</div>"


def palavra_compartilhar(guesses: list[str], answer: str, numero: int | None = None) -> str:
    """Resultado compartilhado sem letras: quadradinhos por tentativa.
    Só passe `numero` quando for a palavra real daquele número."""
    linhas = "".join(
        "<div>" + "".join(f'<i class="{c}"></i>' for c in _palavra_cores(g, answer)) + "</div>"
        for g in guesses)
    return (f'<div class="pw-share"><b>Encaixe Palavra{f" nº {numero}" if numero else ""} · {len(guesses)}/6</b>'
            f'{linhas}<span>jogoencaixe.com.br/?palavra</span></div>')


def load_encaixe(date: str) -> dict:
    """Carrega a grade do Encaixe de uma data (AAAA-MM-DD) já passada."""
    import datetime
    if date >= datetime.date.today().isoformat():
        raise ValueError(f"A grade de {date} ainda não saiu (ou é a de hoje). Use uma data passada para não dar spoiler.")
    p = ROOT.parent / "encaixe" / "conteudo" / "grades" / f"{date}.json"
    return json.loads(p.read_text())


# ---------------------------------------------------------------- carrossel

class Carousel:
    def __init__(self, game: str | None = None, fmt: str = "3:4", handle: str = HANDLE):
        self.game = game
        self.accent = GAMES[game]["color"] if game else STUDIO_COLOR
        self.fmt = fmt
        self.w, self.h = FORMATS[fmt]
        self.handle = handle
        self.slides: list[tuple[str, str, str, str, str | None]] = []

    def add(self, body: str, variant: str = "dark", tag: str = "", align: str = "center",
            accent: str | None = None) -> None:
        """variant: dark (padrão) | glow (brilho na cor de destaque) | accent (fundo na cor do jogo).
        align: center | end (conteúdo embaixo) | start.
        accent: troca a cor de destaque só neste slide (ex.: um jogo por slide no post do estúdio)."""
        self.slides.append((body, variant, tag, align, accent))

    # chrome que aparece em todos os slides e sai na imagem exportada
    def _chrome(self, i: int, total: int, tag: str, variant: str) -> str:
        pct = (i + 1) / total * 100
        top = (f'<div class="top"><span class="brand">{mark_svg(20, mono=variant == "accent")}cuca pensante</span>'
               f'<span class="tag">{esc(tag)}</span></div>')
        if self.fmt == "9:16":
            return top  # o Instagram já mostra o progresso dos stories
        bar = (f'<div class="bar"><div class="track"><div style="width:{pct:.1f}%"></div></div>'
               f'<span>{i + 1}/{total}</span></div>')
        arrow = "" if i == total - 1 else (
            '<div class="arrow"><svg width="22" height="22" viewBox="0 0 24 24" fill="none">'
            '<path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" '
            'stroke-linejoin="round"/></svg></div>')
        return top + bar + arrow

    def write(self, path: str | Path, caption: str = "") -> Path:
        out = Path(path)
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        total = len(self.slides)
        slides_html = []
        for i, (body, variant, tag, align, accent) in enumerate(self.slides):
            acc = f' style="--c:{accent}"' if accent else ""
            slides_html.append(
                f'<section class="slide v-{variant} a-{align}{" story" if self.fmt == "9:16" else ""}"{acc}>'
                f'<div class="content">{body}</div>{self._chrome(i, total, tag, variant)}</section>')
        dots = "".join("<i></i>" for _ in range(total))
        page = (TEMPLATE
                .replace("__W__", str(self.w)).replace("__H__", str(self.h))
                .replace("__ACCENT__", self.accent)
                .replace("__MARK__", mark_svg(18))
                .replace("__HANDLE__", esc(self.handle))
                .replace("__CAPTION__", esc(caption).replace("\n", "<br>"))
                .replace("__DOTS__", dots)
                .replace("__SLIDES__", "\n".join(slides_html)))
        out.write_text(page, encoding="utf-8")
        if caption:
            out.with_name("legenda.txt").write_text(caption + "\n", encoding="utf-8")
        return out


TEMPLATE = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prévia do carrossel</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;900&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
:root{
  --W:__W__px;--H:__H__px;--c:__ACCENT__;
  --bg:#070B14;--bg2:#0C1322;--text:#F3F6FB;--muted:#8E9AB1;--dim:#5B6780;--line:rgba(255,255,255,.09);
  --gold:#F2B632;
  --display:'Unbounded',system-ui,sans-serif;--body:'Instrument Sans',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1B1F2A;font-family:var(--body);color:var(--text);min-height:100vh;display:flex;justify-content:center;align-items:flex-start;padding:32px 16px;-webkit-font-smoothing:antialiased}

/* ---------- moldura de Instagram (só prévia; some no export) ---------- */
.ig-frame{width:var(--W);background:#000;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.ig-header{display:flex;align-items:center;gap:10px;padding:10px 12px}
.ig-header .av{width:32px;height:32px;border-radius:50%;background:var(--bg);display:grid;place-items:center;outline:1.5px solid var(--c);outline-offset:1.5px}
.ig-header b{font-size:13px}.ig-header small{display:block;font-size:11px;color:#a8a8a8}
.carousel-viewport{width:var(--W);height:var(--H);overflow:hidden;position:relative;cursor:grab;touch-action:pan-y}
.carousel-track{display:flex;height:100%;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.ig-dots{display:flex;justify-content:center;gap:4px;padding:10px 0 4px}
.ig-dots i{width:6px;height:6px;border-radius:50%;background:#555}.ig-dots i.on{background:#3897f0}
.ig-actions{display:flex;gap:14px;padding:6px 12px;color:#fff}
.ig-actions svg{width:24px;height:24px}.ig-actions .sp{flex:1}
.ig-caption{padding:4px 12px 14px;font-size:13px;line-height:1.45;color:#eee}
.ig-caption b{margin-right:6px}
.nav-btn{position:absolute;top:50%;transform:translateY(-50%);z-index:20;width:30px;height:30px;border-radius:50%;border:0;background:rgba(255,255,255,.85);color:#000;font-size:16px;cursor:pointer}
.nav-btn.prev{left:8px}.nav-btn.next{right:8px}

/* ---------- slide ---------- */
.slide{flex:none;width:var(--W);height:var(--H);position:relative;overflow:hidden;background:var(--bg);color:var(--text)}
.slide::before{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);
  background-size:28px 28px;-webkit-mask-image:radial-gradient(ellipse at 50% 30%,#000 25%,transparent 80%);mask-image:radial-gradient(ellipse at 50% 30%,#000 25%,transparent 80%)}
.slide.v-glow{background:radial-gradient(420px 320px at 15% 0%,color-mix(in srgb,var(--c) 26%,transparent),transparent 70%),radial-gradient(380px 300px at 100% 100%,color-mix(in srgb,var(--c) 14%,transparent),transparent 70%),var(--bg)}
.slide.v-accent{background:var(--c);color:#061019}
.slide.v-accent::before{background-image:linear-gradient(rgba(0,0,0,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.06) 1px,transparent 1px)}
.content{position:absolute;inset:58px 36px 56px 28px;display:flex;flex-direction:column;gap:14px;z-index:2}
/* story: topo e base ficam cobertos pela interface do Instagram (~14% de cada lado) */
.story .content{inset:130px 28px 120px 28px}
.story .top{top:62px}
.a-center .content{justify-content:center}.a-end .content{justify-content:flex-end}.a-start .content{justify-content:flex-start}

.top{position:absolute;top:0;left:0;right:0;padding:20px 28px 0;display:flex;justify-content:space-between;align-items:center;z-index:5}
.brand{display:flex;align-items:center;gap:7px;font-family:var(--display);font-weight:900;font-size:11.5px;letter-spacing:-.01em}
.tag{font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--c)}
.v-accent .tag{color:#061019;opacity:.7}
.bar{position:absolute;left:0;right:0;bottom:0;padding:0 28px 18px;display:flex;align-items:center;gap:10px;z-index:5}
.bar .track{flex:1;height:3px;border-radius:2px;background:rgba(255,255,255,.12);overflow:hidden}
.bar .track div{height:100%;background:var(--c);border-radius:2px}
.bar span{font-family:var(--mono);font-size:10px;color:rgba(255,255,255,.45)}
.v-accent .bar .track{background:rgba(0,0,0,.15)}.v-accent .bar .track div{background:#061019}.v-accent .bar span{color:rgba(0,0,0,.5)}
.arrow{position:absolute;right:0;top:0;bottom:0;width:40px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,.35);
  background:linear-gradient(to right,transparent,rgba(255,255,255,.05));z-index:4}
.v-accent .arrow{color:rgba(0,0,0,.35);background:linear-gradient(to right,transparent,rgba(0,0,0,.06))}

/* ---------- tipografia ---------- */
.label{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--c);display:flex;align-items:center;gap:8px}
.label::before{content:"";width:20px;height:1px;background:currentColor;opacity:.6}
.v-accent .label{color:#061019}
.h1{font-family:var(--display);font-weight:900;font-size:34px;line-height:1.02;letter-spacing:-.02em;text-wrap:balance}
.h2{font-family:var(--display);font-weight:700;font-size:24px;line-height:1.08;letter-spacing:-.01em;text-wrap:balance}
.hl{color:var(--c)}
.grad{background:linear-gradient(90deg,#00E5FF,#7C7FF5 70%);-webkit-background-clip:text;background-clip:text;color:transparent}
.body{font-size:15px;line-height:1.5;color:var(--muted);max-width:32ch}
.v-accent .body{color:rgba(6,16,25,.75)}
.big-num{font-family:var(--display);font-weight:900;font-size:72px;line-height:.9;color:var(--c)}
.center{text-align:center;align-items:center}
.row{display:flex;gap:14px;align-items:center}
.stack{display:flex;flex-direction:column;gap:10px}

/* ---------- componentes ---------- */
.gicon{border-radius:22%;display:block;box-shadow:0 8px 24px -8px var(--gc,var(--c))}
.phone{border-radius:26px;padding:5px;background:#0E1424;border:1px solid rgba(255,255,255,.14);flex:none}
.phone img{display:block;width:100%;border-radius:21px}
.phone.glow{box-shadow:0 24px 50px -18px color-mix(in srgb,var(--c) 70%,transparent),0 20px 40px -20px #000}
.phones{display:flex;justify-content:center;align-items:center}
.phones.n2 .phone+.phone{margin-left:-28px;margin-top:40px}
.phones.n3 .phone{margin-left:-34px}.phones.n3 .phone:first-child{margin-left:0}.phones.n3 .phone:nth-child(2){z-index:2;margin-top:-30px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips span{font-family:var(--mono);font-size:10px;letter-spacing:.04em;padding:5px 10px;border-radius:999px;border:1px solid color-mix(in srgb,var(--c) 45%,transparent);background:color-mix(in srgb,var(--c) 10%,transparent)}
.v-accent .chips span{border-color:rgba(0,0,0,.25);background:rgba(0,0,0,.06)}
.clue{padding:12px 14px;border-radius:12px;border:1px solid var(--line);background:rgba(255,255,255,.04)}
.clue b{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;color:var(--c)}
.clue p{font-size:13.5px;line-height:1.45;color:var(--text);margin-top:4px}
.steps{display:flex;flex-direction:column}
.step{display:flex;gap:14px;padding:11px 0;border-bottom:1px solid var(--line)}
.step span{font-family:var(--mono);font-weight:700;font-size:13px;color:var(--c);min-width:24px;padding-top:2px}
.step b{font-size:14.5px}.step p{font-size:12.5px;color:var(--muted)}
.cta{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:12px;background:var(--text);color:var(--bg);font-weight:700;font-size:14px;align-self:flex-start}
.v-accent .cta{background:#061019;color:var(--text)}

/* grade do Encaixe (cores da marca Encaixe) */
.cw{display:grid;grid-template-columns:repeat(var(--n),var(--cell));gap:4px;padding:8px;background:#1F5F8B;border-radius:14px;align-self:center}
.cw i{width:var(--cell);height:var(--cell);background:#F6F1E7;border-radius:5px;position:relative;display:grid;place-items:center}
.cw i.blk{background:#1C3F5C}
.cw sup{position:absolute;top:3px;left:5px;font-family:var(--mono);font-size:10px;font-weight:700;color:#5A5650}
.cw em{font-style:normal;font-family:var(--display);font-weight:700;font-size:calc(var(--cell)*.48);color:#1C1B19}
.cw-clues h4{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--c);margin-bottom:6px}
.cw-clues ol{list-style:none;display:flex;flex-direction:column;gap:5px}
.cw-clues li{font-size:13px;line-height:1.35;display:flex;gap:8px}
.cw-clues li b{font-family:var(--mono);color:var(--c);min-width:12px}
/* Palavra do dia (Encaixe): certa = azul da marca, presente = amarelo, ausente = cinza */
.pw{display:grid;grid-template-columns:repeat(5,var(--cell));gap:5px;align-self:center}
.pw i{width:var(--cell);height:var(--cell);border-radius:6px;border:2px solid rgba(246,241,231,.18);display:grid;place-items:center}
.pw i.certa,.pw i.presente,.pw i.ausente{border-color:transparent}
.pw em{font-style:normal;font-family:var(--display);font-weight:700;font-size:calc(var(--cell)*.46);color:#fff}
.pw .certa{background:#1F5F8B}.pw .presente{background:#F2B632}.pw .presente em{color:#1C1B19}.pw .ausente{background:#7C766B}
.pw-share{display:inline-flex;flex-direction:column;gap:4px;padding:14px 16px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid var(--line);align-self:flex-start}
.pw-share b{font-family:var(--mono);font-size:11px;margin-bottom:4px}
.pw-share div{display:flex;gap:3px}
.pw-share i{width:18px;height:18px;border-radius:3px}
.pw-share .certa{background:#1F5F8B}.pw-share .presente{background:#F2B632}.pw-share .ausente{background:#7C766B}
.pw-share span{font-family:var(--mono);font-size:10px;color:var(--muted);margin-top:4px}
</style></head>
<body>
<div class="ig-frame">
  <div class="ig-header"><div class="av">__MARK__</div><div><b>__HANDLE__</b><small>Cuca Pensante</small></div></div>
  <div class="carousel-viewport">
    <button class="nav-btn prev" aria-label="Anterior">‹</button>
    <div class="carousel-track">
__SLIDES__
    </div>
    <button class="nav-btn next" aria-label="Próximo">›</button>
  </div>
  <div class="ig-dots">__DOTS__</div>
  <div class="ig-actions">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.5-9.5-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.5 6c-2.5 4.5-9.5 9-9.5 9z"/></svg>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a8.5 8.5 0 0 1-12.6 7.4L3 21l1.6-5.4A8.5 8.5 0 1 1 21 12z"/></svg>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 3 11 14M22 3l-7 19-4-8-8-4z"/></svg>
    <span class="sp"></span>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1z"/></svg>
  </div>
  <div class="ig-caption"><b>__HANDLE__</b>__CAPTION__</div>
</div>
<script>
(function(){
  const W=parseInt(getComputedStyle(document.documentElement).getPropertyValue('--W'));
  const track=document.querySelector('.carousel-track'),vp=document.querySelector('.carousel-viewport');
  const dots=[...document.querySelectorAll('.ig-dots i')],n=dots.length;let i=0,x0=null;
  function go(k){i=Math.max(0,Math.min(n-1,k));track.style.transform='translateX('+(-i*W)+'px)';dots.forEach((d,j)=>d.classList.toggle('on',j===i));}
  document.querySelector('.prev').onclick=()=>go(i-1);document.querySelector('.next').onclick=()=>go(i+1);
  vp.addEventListener('pointerdown',e=>{x0=e.clientX});
  vp.addEventListener('pointerup',e=>{if(x0===null)return;const dx=e.clientX-x0;if(Math.abs(dx)>40)go(i+(dx<0?1:-1));x0=null});
  addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(i+1);if(e.key==='ArrowLeft')go(i-1)});
  window.__goSlide=go;go(0);
})();
</script>
</body></html>
"""
