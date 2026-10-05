# Os jogos

Fonte da verdade: o site (`index.html` e `apps/<jogo>/index.html`) e o projeto de cada jogo em `/Volumes/ssd/Desenvolvimento/<pasta>`. Se algo aqui divergir do site, o site vence; atualize este arquivo.

Todos: grátis, sem cadastro, em português do Brasil, desafio diário igual para todo mundo, toda fase com solução garantida. Site do estúdio: cucapensante.com.br.

---

## Blueprint Mansion — `blueprint` · `#00E5FF`

- **Gênero:** roguelike de arquitetura tática. iOS e Android. PT-BR / EN.
- **Frase:** "Desenhe a sua própria fuga."
- **Premissa:** você está preso numa mansão que ainda não existe. Cada cômodo desenhado no caderno de plantas ganha vida. Gire as cartas (0°, 90°, 180°, 270°), alinhe as portas, administre a carga da lanterna e ache a saída antes que a estrutura colapse.
- **Mecânicas para posts:** rotação de cartas; paredes não podem bloquear portas existentes; energia da lanterna gasta a cada cômodo; salas sinérgicas (gerador ao lado da segurança revela a planta); moedas ficam entre runs.
- **Desafio diário:** Protocolo de Crise. Uma operação nova a cada 24 h, gerada pela data, a mesma mansão para todos. Modificadores: falha elétrica, patrulhas, plantas roubadas. Uma tentativa por dia, placar mundial e streak.
- **Expansões:** Fortaleza das Relíquias (Sir Galahad), Sanatório St. Jude (Dra. Helen Vance).
- **Prints em alta:** `blueprint_mansion/store_assets/` (iPhone 1290×2796), `blueprint_mansion/docs/images/screenshot_*.png`, arte larga `blueprint_mansion/assets/store/feature_graphic_1024x500.png`.
- **Ganchos que combinam:** "Essa porta fecha o seu caminho. Para onde você gira?", "Você tem 3 de energia. Qual cômodo desenha?".

## Nodyx — `nodyx` · `#7C7FF5`

- **Gênero:** puzzles casuais táteis. iOS e Android. PT-BR / EN.
- **Frase:** "Três mecânicas. Um desafio diário mundial."
- **Modos:**
  - **Pontos:** ligue círculos da mesma cor sem cruzar nem repetir célula.
  - **Setas:** toque numa seta e ela voa na direção que aponta, se o caminho até a borda estiver livre. A ordem certa é o puzzle.
  - **Blocos deslizantes:** grade 4×5 com dois espaços vazios; leve o bloco mestre 2×2 até a saída.
- **Progressão:** 5 capítulos de 30 fases: Descoberta, Despertar, Equilíbrio, Harmonia, Maestria (modos Master).
- **Desafio Diário:** três puzzles sincronizados para o mundo todo, placar de tempo e sequência.
- **Outros:** dicas em sub-metas (não entregam a resposta), estrelas e recordes, temas desbloqueáveis (Cyber Gadget, Obsidiana & Ouro), vibração háptica.
- **Prints:** ainda não há prints em alta no projeto. Peça ao usuário (`instagram/prints/nodyx/`). Os do site (`assets/nodyx-*.jpg`, 416×900) servem só para celular pequeno.
- **Ganchos:** "Qual seta sai primeiro?", "Ligue as cores sem cruzar. Dá?".

## Tramela — `tramela` · `#38BDF8`

- **Gênero:** dedução lógica / mistério espacial. iOS e Android. PT-BR / EN.
- **Frase:** "Mistério, lógica e dedução a bordo."
- **Premissa:** alguém sabotou o suporte de vida de um módulo da Estação Tramela, e só um tripulante estava no mesmo compartimento que a vítima. Cruze pistas para posicionar os suspeitos: um por linha, um por coluna. Quem ficou sozinho com a vítima é o culpado.
- **Tipos de pista:** absolutas, negativas, relativas ("a norte de"), adjacência, contagem, condicionais. Rótulos usados no site: BIOMETRIA, CÂMERA, SENSOR, CONDICIONAL.
- **Exemplos de pista (do site):**
  - BIOMETRIA: "Arianna passou pela escotilha do setor 7 às 03:10 — ela está na linha mais ao norte."
  - CÂMERA: "Nenhum suspeito foi visto no corredor B. A coluna 2 está vazia entre as linhas 1 e 3."
  - SENSOR: "Colleen estava adjacente ao Laboratório Bio, mas não dentro dele."
  - CONDICIONAL: "Se Brycen está na hidroponia, então Dan está a leste dele."
- **Tripulação:** Arianna (comandante e piloto, Ponte de Comando), Brycen (engenheiro-chefe de propulsão, Reator Central), Colleen (médica-chefe e bioquímica, Laboratório Bio), Dan (cientista-chefe e astrofísico, Observatório), Evan (suporte de vida, Domo de Hidroponia), Fiona (segurança e carga, Eclusa de Ar), Virgil (auditor externo da frota; é a vítima). Bios completas: `tramela/app/lib/presentation/screens/crew_dossier_screen.dart`.
- **Progressão:** 30 módulos. Fases 1–10 tutorial 4×4; 11–40 básico 5×5; 41+ intermediário 6×6; Mestre com condicionais. Módulos: Engenharia, Laboratórios Centrais, Domo de Hidroponia…
- **Modos:** Caso do Dia (um caso por dia, o mesmo para todos); Alerta Vermelho (casos em sequência contra o relógio: Alerta Rápido 4×4 e Sobrecarga Crítica 5×5; usa vermelho `#F43F5E` como destaque).
- **Casos reais em dados:** `tramela/app/assets/packs/pack_*.json` (solução, vítima, culpado, pistas codificadas). Para um post de desafio, use um print do tabuleiro e reescreva as pistas em português com `clue()`.
- **Prints em alta:** `tramela/store_assets/novas_imagens/*_1242x2688.png`.
- **Ganchos:** "Quem estava com a vítima?", "3 pistas. 1 culpado. Você acha?".

## Encaixe — `encaixe` · `#F2B632`

- **Gênero:** cruzadinha diária 5×5. Navegador (jogoencaixe.com.br); App Store e Google Play em breve.
- **Frase:** "Uma cruzadinha por dia, a mesma para todo o Brasil."
- **Regras:** grade 5×5 resolvida em 1–2 minutos; sai à meia-noite; dificuldade cresce ao longo da semana; desafio 7×7 no fim de semana; compartilhar o tempo sem entregar respostas.
- **Pistas:** brasileiras de propósito: novela, futebol, música, comida, gíria.
- **Marca própria:** azul `#1F5F8B`, creme `#F6F1E7`, tinta `#1C1B19`, amarelo `#F2B632`. A função `crossword()` do kit já usa essas cores.
- **Grades reais:** `encaixe/conteudo/grades/AAAA-MM-DD.json` (`grid`, `words` com `number`, `direction`, `row`, `col`, `answer`, `clue`). Carregue com `load_encaixe("AAAA-MM-DD")`.
- **⚠️ Spoiler:** as grades de dias futuros já estão no repositório e marcadas como `publicada`. Use só datas anteriores a hoje (`load_encaixe` recusa hoje e o futuro). Nunca mostre a grade do dia.
- **Ganchos:** "Você fecha essa grade em 2 minutos?", "Só brasileiro acerta essa pista:", "Qual palavra de 5 letras é…".
