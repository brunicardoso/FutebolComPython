# Futebol com Python ⚽🐍

Notebooks do Google Colab para uma criança de uns 8 anos aprender **Python, matemática, estatística e lógica** com futebol. Cada notebook responde uma pergunta de torcedor ("Quem é a melhor joia jovem da Europa?", "Qual é a chance de fazer o gol de pênalti?") usando código.

Acertou uma missão? Ganha **aura**, reações e **jogos** que ficam guardados no vestiário. Errou? Entra no **modo beta**: dica, um treino rápido e nova tentativa. A aura nunca diminui.

## 🌐 Comece pelo site

O jeito mais fácil é o site do projeto, com todos os notebooks, explicações e um botão **Abrir no Colab** em cada um:

**https://brunicardoso.github.io/FutebolComPython/**

(O link funciona depois que o GitHub Pages estiver ligado; veja "Para quem mantém o projeto" mais abaixo.)

## 📚 A trilha

| Nível | Notebooks | Situação |
|---|---|---|
| 1 · Sub-9 (fundamentos) | 01 Python é uma calculadora · 02 Olheiro de Joias · 03 Monte sua escalação · 04 Cara ou coroa e pênaltis | ✅ prontos |
| 2 · Sub-11 (lógica) | 05 O VAR decide · 06 Tabela do campeonato · 07 Gols por 90 minutos · 08 Média ou mediana? | 🔒 em breve |
| 3 · Sub-13 (geometria e simulação) | 09 Desenhe o campo · 10 Distância e ângulo do chute · 11 10.000 disputas de pênaltis · 12 O álbum de figurinhas | 🔒 em breve |
| 4 · Sub-15 (construindo coisas) | 13 Sua carta de jogador · 14 Idade e gols andam juntos? · 15 Simulador de campeonato · 16 Projeto final | 🔒 em breve |

## 👨‍👩‍👦 Para os pais

**Como abrir no computador ou tablet:** no site, toque em **Abrir no Colab**, entre com uma conta Google e aperte ▶️ na primeira célula ("Preparar o vestiário"). Se o Colab avisar que o notebook não é do Google, toque em **Executar assim mesmo**. Depois é só ir descendo e apertando ▶️.

**No celular:** funciona no navegador (Chrome ou Safari). Toque numa célula para digitar e no ▶️ para rodar. Uma tela maior é mais confortável.

**Progresso:** o Colab esquece tudo quando a sessão acaba. No fim de cada notebook aparece um **código secreto**, como `AURA-1350-J3N5-7F2`. Anote num papel. No próximo notebook, a criança escreve `carregar_progresso("AURA-…")`. Também dá para salvar no Google Drive com `salvar_progresso(drive=True)`.

**Ritmo:** cada missão leva de 3 a 5 minutos e cada notebook de 15 a 25. Depois de uns 20 minutos, aparece a sugestão de um **intervalo**.

**Privacidade:** nenhum dado pessoal é coletado ou enviado. Não há anúncios, compras nem chat.

**Reações (GIFs):** o arquivo `midia/reacoes.json` vem só com emojis. Se quiser GIFs, coloque links do GIPHY ou do Tenor no campo `"url"` (só links, nunca os arquivos).

## 📊 Dados

Os dados vêm do projeto [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets), sob a licença **CC0 1.0**. As atualizações pararam em julho de 2026, então usamos a **temporada 2025–26 completa** das 5 grandes ligas (Inglaterra, Espanha, Alemanha, Itália e França). O retrato fica em `dados/jogadores_2025_26.csv.gz`.

As curiosidades (`dados/curiosidades.json`) são conferidas uma a uma, com fonte e data, e levam para a Wikipédia em português.

## 🛠️ Para quem mantém o projeto

Tudo roda com [pixi](https://pixi.sh):

```bash
pixi run testes                  # testes (pytest)
pixi run testar-notebooks        # roda os notebooks prontos com as respostas escondidas
pixi run checar-idioma           # procura inglês em textos que a criança lê
pixi run verificar-curiosidades  # confere fontes e links da Wikipédia (via Wikidata)
pixi run preparar-dados          # refaz o retrato dos dados
pixi run site                    # abre o site em http://localhost:8000
pixi run verificar               # testes + idioma + site + notebooks
```

**Antes de publicar:**

1. O endereço do repositório fica em `vestiario/config.py` e na primeira célula de cada notebook. Se mudar, troque nos dois lugares (o teste `tests/test_catalogo.py` confere se batem).
2. No GitHub, em *Settings → Pages*, escolha **GitHub Actions** como fonte. O site é publicado a cada push na `main`.

Os notebooks são guardados **sem saídas** (filtro `nbstripout`, ativado com `pixi run nbstripout --install`). As regras completas para quem escreve conteúdo estão em [AGENTS.md](AGENTS.md).

## 🤝 Contribuições

Sugestões e relatos de problemas são bem-vindos nas *issues*. Para enviar código ou conteúdo (*pull request*), é preciso antes assinar um **Acordo de Licença de Contribuidor (CLA)**: você continua dono do que escreveu, mas dá ao mantenedor o direito de usar, alterar e licenciar a contribuição, inclusive em versões comerciais do projeto. Sem o CLA assinado, a contribuição não pode ser aceita. Para pedir o CLA, abra uma *issue*.

## 📄 Licença

Este projeto tem **duas licenças**, conforme o tipo de arquivo (detalhes em [LICENSES.md](LICENSES.md)):

| O quê | Licença | Arquivo |
|---|---|---|
| Código e jogos (`vestiario/`, `scripts/`, `tests/`, `jogos/`, `site/`) | [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/) | [LICENSE](LICENSE) |
| Conteúdo educativo (`notebooks/`, textos, `dados/curiosidades.json`, `midia/reacoes.json`) | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt_BR) | [LICENSE-CONTEUDO](LICENSE-CONTEUDO) |

As duas permitem uso **não comercial** (famílias, escolas, estudo, pesquisa). **Uso comercial precisa de uma licença comercial**, que pode ser negociada com o autor.

Os dados do transfermarkt-datasets continuam sob CC0 1.0. As reações em `midia/reacoes.json` são só links: as imagens pertencem aos seus donos e não fazem parte destas licenças.
