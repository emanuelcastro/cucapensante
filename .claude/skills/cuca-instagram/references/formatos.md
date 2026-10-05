# Formatos de post

Cada formato é um ponto de partida; corte slides que não tenham conteúdo de verdade. Entre 4 e 7 slides costuma bastar.

Variantes de slide do kit:
- `glow`: escuro com brilho na cor do jogo. Bom para capa e destaque.
- `dark`: escuro neutro. Bom para texto, pistas e listas.
- `accent`: fundo na cor do jogo, texto escuro. Use no máximo uma vez por post, quase sempre no último slide.

Regra de ritmo: alterne `glow` e `dark`; feche com `accent`. Não use slides claros: a marca é escura.

---

## 1. Desafio (o formato principal)

Feito para comentário e salvamento. O desafio precisa ser resolvível só com o que está no post.

| # | Slide | Variante |
|---|-------|----------|
| 1 | Gancho + o puzzle visível (grade, tabuleiro ou print) | glow |
| 2 | Regras em uma frase + pistas | dark |
| 3 | (opcional) Dica | dark |
| 4 | Convite: "Comenta sua resposta" ou "Resposta amanhã nos stories" | accent |

- **Encaixe:** `load_encaixe(data_passada)`, `crossword()` na capa, `crossword_clues()` no slide 2. O gabarito (`reveal=True`) entra só se o post for "desafio + resposta"; o padrão é publicar o gabarito no dia seguinte (story ou slide final de outro post).
- **Tramela:** print do tabuleiro (`phone()`) + 3 ou 4 `clue()` com rótulos BIOMETRIA / CÂMERA / SENSOR / CONDICIONAL. Pergunta: "Quem estava com a vítima?". As pistas precisam levar a uma única resposta: tire-as de um caso real (`pack_*.json`) ou confira a lógica antes de publicar.
- **Nodyx:** print de uma fase de Setas ou Pontos. Pergunta: "Qual seta sai primeiro?" / "Como você liga as cores?".
- **Blueprint:** print de uma situação de draft. Pergunta: "Qual carta você escolhe e em que rotação?".

## 2. Conheça o jogo

| # | Slide | Variante |
|---|-------|----------|
| 1 | Gancho da premissa + 1 celular | glow |
| 2 | Como se joga, em passos (`steps()`), só se for sequência de verdade | dark |
| 3 | Mecânica ou modo em destaque + print | glow |
| 4 | Desafio diário do jogo | dark |
| 5 | CTA com plataformas | accent |

## 3. Estúdio / apresentação

Primeiro post do perfil e posts institucionais. Sem `game`, a cor é o ciano do estúdio; cada slide de jogo usa `accent=GAMES[g]["color"]`.

| # | Slide | Variante |
|---|-------|----------|
| 1 | "Jogos de lógica para quem gosta de pensar." + 4 ícones | glow |
| 2–5 | Um jogo por slide: celular + gancho + 1 frase | glow, com `accent` do jogo |
| 6 | O que todos têm em comum | dark |
| 7 | "Qual você joga primeiro?" + site | accent |

## 4. Novidade / lançamento

Atualização, expansão, novo módulo, chegada às lojas (ex.: Encaixe na App Store).

| # | Slide | Variante |
|---|-------|----------|
| 1 | "Chegou: …" + visual principal | glow |
| 2 | O que mudou (até 3 itens) | dark |
| 3 | Print da novidade | glow |
| 4 | Onde baixar / atualizar | accent |

## 5. Bastidores

Como o jogo é feito: gerador de fases com solução única, escolha das pistas do Encaixe, design da tripulação do Tramela. Tom de conversa, primeira pessoa do estúdio.

| # | Slide | Variante |
|---|-------|----------|
| 1 | Pergunta curiosa ("Como garantir que toda fase tem solução?") | glow |
| 2–4 | A explicação em partes, com imagem quando houver | dark / glow |
| 5 | Ligação com o jogo + CTA | accent |

---

## Legenda

Sempre entregue a legenda junto (vai para `legenda.txt`):
- 1ª linha repete o gancho em outras palavras.
- 2 a 4 linhas curtas de contexto.
- Pergunta para comentário.
- "Link na bio" quando houver CTA. Para pedir que sigam, use @cucapensante.jogos (o @cucapensante é de outra pessoa).
- 3 a 6 hashtags no fim, específicas: `#cucapensante #jogosdelogica #puzzle #palavrascruzadas #jogosindie #gamedevbrasil` + a do jogo (`#tramela`, `#jogoencaixe`…).
