---
name: cuca-instagram
description: Cria carrosséis e posts de Instagram para o perfil do Cuca Pensante (estúdio dos jogos Blueprint Mansion, Nodyx, Tramela e Encaixe), na identidade da marca, com prints dos jogos e desafios reais (grades do Encaixe, casos do Tramela). Gera prévia arrastável e exporta PNGs 1080×1440. Use sempre que o usuário pedir post, carrossel, desafio, story ou conteúdo de Instagram do Cuca Pensante ou de qualquer um dos quatro jogos, mesmo sem dizer "skill"; tem prioridade sobre a skill genérica instagram-carousel neste projeto.
---

# Instagram do Cuca Pensante

Perfil: **@cucapensante.jogos** (nome exibido: Cuca Pensante). Foto de perfil: `assets/brand/cuca-perfil-instagram.png`.

Carrosséis na identidade do site: fundo noturno `#070B14` com grade sutil, símbolo do Cuca Pensante, títulos em Unbounded Black, texto em Instrument Sans, rótulos em JetBrains Mono, e a cor de destaque do jogo do post.

Antes de escrever, leia:
- `references/jogos.md` — fatos, mecânicas, desafios, cores e onde ficam os prints de cada jogo.
- `references/formatos.md` — sequências de slides (Desafio, Conheça o jogo, Estúdio, Novidade, Bastidores) e regras de legenda.

## Pastas

```
instagram/
  prints/<jogo>/        prints que o usuário prepara (blueprint, nodyx, tramela, encaixe)
  posts/AAAA-MM-DD-<jogo>-<formato>/
    build.py            script que monta o post (guarde, para ajustes depois)
    preview.html        prévia com moldura de Instagram
    legenda.txt         legenda pronta
    slides/slide_01.png …
```

`instagram/` está no `.gitignore`: o repositório é publicado pelo GitHub Pages e os posts não devem ir para o site.

## Fluxo

1. **Entender o pedido.** Jogo, formato e assunto. Se faltar algo que muda o post (qual jogo, qual desafio), pergunte uma vez. O resto decida pelo `formatos.md`.
2. **Juntar o material.**
   - Prints: primeiro `instagram/prints/<jogo>/`; depois os caminhos de alta resolução em `jogos.md`; por último `assets/<jogo>-N.jpg` do site (pequenos, só para celular de até ~170 px).
   - Abra e olhe os prints antes de escolher (Read na imagem). Use prints na vertical dentro de `phone()`.
   - Desafio do Encaixe: `load_encaixe("AAAA-MM-DD")` com data **anterior a hoje**. Nunca a grade do dia nem futura.
   - Desafio do Tramela: pistas de um caso real em `tramela/app/assets/packs/` ou pistas conferidas por você, com uma única resposta.
3. **Escrever o texto** (português do Brasil, frases curtas, sem clichês de IA, sem emoji como marcador). Slide 1 é gancho: pergunta, desafio ou fato concreto. Nunca o nome do estúdio como título.
4. **Montar** com um `build.py` na pasta do post, em Python:

   ```python
   import sys; sys.path.insert(0, ".claude/skills/cuca-instagram/scripts")
   from carousel_kit import *

   c = Carousel(game="tramela")          # None = estúdio (ciano); fmt="4:5" se pedirem 1080×1350
   c.add('<div class="label">Caso do Dia</div><div class="h1">Quem estava com a vítima?</div>'
         + phone("instagram/prints/tramela/tabuleiro.png", width=200, tilt=-4),
         variant="glow", tag="Desafio")
   c.add(clue("BIOMETRIA", "…") + clue("CÂMERA", "…"), variant="dark", tag="Pistas")
   c.add('<div class="h1">Comenta o nome do culpado.</div><div class="cta">Link na bio</div>',
         variant="accent", tag="Tramela")
   c.write("instagram/posts/2026-10-06-tramela-desafio/preview.html", caption="…")
   ```

   Rode da raiz do repositório: `python3 instagram/posts/<post>/build.py`.
5. **Revisar antes de mostrar.** Exporte (`export.py`), junte os PNGs numa folha de contato e olhe uma vez: texto cortado, sobreposição com a barra ou a seta, print ilegível. Corrija e só então mostre.
6. **Mostrar** a prévia: `open instagram/posts/<post>/preview.html` (abre no navegador do usuário) e a folha de contato. Pergunte: **"Quais slides precisam de ajuste?"**
7. **Ajustar** só os slides citados, editando o `build.py`. Não refaça o post inteiro sem pedido.
8. **Exportar** a versão final quando o usuário aprovar:
   `python3 .claude/skills/cuca-instagram/scripts/export.py instagram/posts/<post>/preview.html`
   e entregue o caminho de `slides/` e o texto de `legenda.txt`.

## Kit (`scripts/carousel_kit.py`)

| Função | Para quê |
|---|---|
| `Carousel(game, fmt)` | `game`: `blueprint`, `nodyx`, `tramela`, `encaixe` ou `None`. Define a cor de destaque. `fmt`: `3:4` (feed, padrão), `4:5`, ou `9:16` para story (cada slide vira um quadro de 1080×1920, sem barra nem seta; topo e base ficam livres para a interface do Instagram). |
| `.add(html, variant, tag, align, accent)` | `variant`: `glow`, `dark`, `accent`. `align`: `center`, `end`, `start`. `tag`: rótulo no canto superior direito. `accent`: troca a cor só nesse slide. |
| `.write(caminho, caption)` | Gera `preview.html` e `legenda.txt`. |
| `phone(img, width, tilt)` / `phones(a, b[, c])` | Print dentro de um celular; dois ou três em leque. |
| `game_icon(jogo, size)` | Ícone oficial do jogo (de `assets/`). |
| `clue(rótulo, texto)` | Cartão de pista do Tramela. |
| `steps((título, texto), …)` | Passos numerados. Só para sequências reais. |
| `chips("a", "b")` | Etiquetas de recursos. |
| `crossword(grid, words, reveal, cell)` / `crossword_clues(words, "across"|"down")` | Grade e pistas do Encaixe. |
| `load_encaixe(data)` | Lê a grade de uma data passada. |
| `palavra(tentativas, resposta, rows, cell)` / `palavra_compartilhar(tentativas, resposta, numero)` | Tabuleiro e resultado compartilhado da Palavra do dia (Encaixe). `numero` só quando for a palavra real daquele número. |

Classes de texto: `.label` (rótulo mono), `.h1` (34 px), `.h2` (24 px), `.body`, `.big-num`, `.hl` (cor de destaque), `.grad` (degradê ciano→índigo, só no estúdio), `.cta`, `.row`, `.stack`, `.center`.

Já fica em todos os slides: símbolo + "cuca pensante" no topo, rótulo, barra de progresso com contador, seta de deslizar (some no último).

## Regras de marca

- Sempre fundo escuro; `accent` (fundo colorido) no máximo uma vez por post.
- Uma cor de destaque por post: a do jogo. Posts do estúdio usam ciano e podem dar a cada slide de jogo a cor dele.
- O símbolo do Cuca Pensante não muda de forma nem de cor; em fundo colorido o kit já usa a versão de uma cor.
- Nome sempre em minúsculas na marca ("cuca pensante"); no texto corrido, "Cuca Pensante".
- Ícones dos jogos: use os oficiais de `assets/`, nunca redesenhe.
- Não invente recurso, número de fases ou plataforma: confira em `jogos.md` ou no site.
- Encaixe ainda não está nas lojas (só navegador). Não diga "baixe na App Store" para ele.

## Exportação

`export.py` usa o Chrome instalado (`channel="chrome"`), porque o navegador próprio do Playwright não está baixado nesta máquina. Saída: 1080×1440 (3:4) ou 1080×1350 (4:5), um PNG por slide.
