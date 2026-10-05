"""Exporta cada slide da prévia como PNG pronto para o Instagram.

    python3 .claude/skills/cuca-instagram/scripts/export.py instagram/posts/<post>/preview.html

Gera <pasta do post>/slides/slide_01.png… em 1080 px de largura
(1080×1440 no formato 3:4, 1080×1350 no 4:5). O layout continua em 420 px;
o device_scale_factor amplia sem mudar nada de lugar.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT_W = 1080


def launch(p):
    # O navegador próprio do Playwright não está baixado neste Mac; usa o Chrome instalado.
    try:
        return p.chromium.launch(channel="chrome")
    except Exception:
        return p.chromium.launch()


def main(html_path: str) -> None:
    html = Path(html_path).resolve()
    out_dir = html.parent / "slides"
    out_dir.mkdir(exist_ok=True)
    for old in out_dir.glob("slide_*.png"):
        old.unlink()

    with sync_playwright() as p:
        browser = launch(p)
        probe = browser.new_page()
        probe.goto(html.as_uri())
        w, h = probe.evaluate("""() => {
            const s = getComputedStyle(document.documentElement);
            return [parseInt(s.getPropertyValue('--W')), parseInt(s.getPropertyValue('--H'))];
        }""")
        probe.close()

        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=OUT_W / w)
        page.goto(html.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(800)
        page.evaluate("""() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption,.nav-btn')
              .forEach(el => el.style.display = 'none');
            const f = document.querySelector('.ig-frame');
            f.style.borderRadius = '0'; f.style.boxShadow = 'none';
            document.body.style.cssText = 'padding:0;margin:0;display:block;min-height:0;background:#070B14';
            document.querySelector('.carousel-track').style.transition = 'none';
        }""")
        total = page.evaluate("document.querySelectorAll('.slide').length")
        for i in range(total):
            page.evaluate(f"window.__goSlide({i})")
            page.wait_for_timeout(150)
            target = out_dir / f"slide_{i + 1:02d}.png"
            page.screenshot(path=str(target), clip={"x": 0, "y": 0, "width": w, "height": h})
            print(target.name)
        browser.close()
    print(f"{total} slides em {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("uso: export.py caminho/para/preview.html")
    main(sys.argv[1])
