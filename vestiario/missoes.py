"""As missões de cada notebook: resposta certa, dica e explicação.

Respostas que dependem dos dados são calculadas a partir do snapshot
(funções que recebem a tabela de jogadores), nunca escritas à mão.
"""

from __future__ import annotations

import math
import numbers
import random
import unicodedata
from dataclasses import dataclass
from typing import Any, Callable


class Qualquer(tuple):
    """Várias respostas valem (por exemplo, quando dois jogadores empatam)."""


@dataclass
class Missao:
    resposta: Any | Callable  # valor, Qualquer(...) ou função(tabela) -> valor
    dica: str
    explicacao: str
    tolerancia: float = 0.0
    desbloqueia: str | None = None
    dificil: bool = False
    parcial: bool = False  # aceita só o sobrenome (ou só o primeiro nome)
    usa_dados: bool = False

    def esperado(self):
        if not callable(self.resposta):
            return self.resposta
        if self.usa_dados:
            from .dados import carregar_jogadores
            return self.resposta(carregar_jogadores())
        return self.resposta()


# ---------------------------------------------------------------- comparação

def normalizar(texto: str) -> str:
    """Tira acentos, maiúsculas e espaços sobrando: ' Mbappé ' vira 'mbappe'."""
    sem_acento = unicodedata.normalize("NFKD", str(texto))
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return " ".join(sem_acento.lower().replace("ı", "i").split())


def _como_numero(valor):
    if isinstance(valor, bool):
        return None
    if isinstance(valor, numbers.Number):
        return float(valor)
    if isinstance(valor, str):
        try:
            return float(valor.strip().replace(",", "."))
        except ValueError:
            return None
    return None


def _igual(resposta, esperado, tolerancia: float, parcial: bool) -> bool:
    num_esperado = _como_numero(esperado)
    if num_esperado is not None:
        num_resposta = _como_numero(resposta)
        if num_resposta is None or math.isnan(num_resposta):
            return False
        return abs(num_resposta - num_esperado) <= tolerancia + 1e-9
    if isinstance(esperado, str):
        if not isinstance(resposta, str):
            return False
        r, e = normalizar(resposta), normalizar(esperado)
        if r == e:
            return True
        return parcial and len(r) >= 3 and r in e.split()
    if isinstance(esperado, (list, tuple)):
        try:
            return (len(resposta) == len(esperado) and
                    all(_igual(a, b, tolerancia, parcial) for a, b in zip(resposta, esperado)))
        except TypeError:
            return False
    return resposta == esperado


def comparar(resposta, missao: Missao) -> bool:
    esperado = missao.esperado()
    opcoes = esperado if isinstance(esperado, Qualquer) else (esperado,)
    return any(_igual(resposta, e, missao.tolerancia, missao.parcial) for e in opcoes)


def texto_resposta(missao: Missao) -> str:
    """A resposta certa escrita para mostrar depois de 3 tentativas."""
    esperado = missao.esperado()
    if isinstance(esperado, Qualquer):
        return " ou ".join(str(e) for e in esperado)
    return str(esperado)


# ---------------------------------------------------------------- ajudantes de dados

def _nomes_do_maximo(tabela, coluna: str) -> Qualquer:
    """Todos os nomes empatados no valor mais alto de uma coluna."""
    maior = tabela[coluna].max()
    return Qualquer(tabela.loc[tabela[coluna] == maior, "nome"].tolist())


def _joias(tabela):
    return tabela[tabela["nascido"] >= 2005]


def _mais_gols_por_jogo(tabela, id_a: int, id_b: int) -> str:
    a = tabela.loc[tabela["player_id"] == id_a].iloc[0]
    b = tabela.loc[tabela["player_id"] == id_b].iloc[0]
    return a["nome"] if a["gols"] / a["jogos"] > b["gols"] / b["jogos"] else b["nome"]


def _penaltis_com_semente(semente: int, cobrancas: int) -> int:
    """Repete a simulação da missão 3 do notebook 04 com a mesma semente."""
    sorteio = random.Random(semente)
    return sum(sorteio.choice([0, 1, 1, 1]) for _ in range(cobrancas))


SAID_EL_MALA, CARLOS_ESPI = 1168219, 1063338

# ---------------------------------------------------------------- missões

MISSOES: dict[str, dict[str, Missao]] = {
    "01_calculadora": {
        "aquecimento": Missao(3, "Só apertar o play ▶️ na célula.", "2 + 1 = 3."),
        "m1": Missao(
            4, "Troque o ___ pelo sinal de mais: +",
            "3 gols do Brasil + 1 gol da Argentina = 4 gols no jogo."),
        "m2": Missao(
            -4, "Saldo = gols feitos − gols sofridos. Use o sinal de menos: -",
            "10 − 14 = −4. Sofreu mais do que fez, então o saldo fica negativo."),
        "m3": Missao(
            24, "Cada vitória vale 3 pontos. Use o sinal de vezes: *",
            "8 vitórias × 3 pontos = 24 pontos."),
        "m4": Missao(
            2, "Gols por jogo = gols ÷ jogos. Use a barra: /",
            "30 ÷ 15 = 2. O Python mostra 2.0 porque a divisão sempre dá número com vírgula."),
        "desafio1": Missao(
            -2, "O saldo era 3. Num jogo de 0 x 5, o time fez 0 e sofreu 5.",
            "3 + 0 − 5 = −2."),
        "desafio2": Missao(
            5, "Do −3 até o 0 faltam 3 gols. Do 0 até o +2 faltam mais 2.",
            "−3 + 5 = +2. Precisa de 5 gols.", dificil=True),
    },
    "02_olheiro": {
        "aquecimento": Missao(
            lambda t: t.iloc[0]["nome"], "Olhe a primeira linha da tabela, na coluna nome.",
            "A tabela já vem ordenada pelos gols, então o primeiro é o artilheiro.",
            parcial=True, usa_dados=True),
        "m2": Missao(
            lambda t: _nomes_do_maximo(t, "assistencias"),
            "Escreva assistencias (sem acento) dentro das aspas e veja quem fica em primeiro.",
            "Quem está no topo depois de ordenar por assistencias é o rei dos passes. "
            "Se dois empatam, os dois valem!",
            parcial=True, usa_dados=True),
        "m3": Missao(
            lambda t: _nomes_do_maximo(_joias(t), "gols"),
            "Joia é quem nasceu em 2005 ou depois. Use 2005 no lugar do ___.",
            "Filtrando nascido >= 2005 e olhando o primeiro da lista, achamos a joia artilheira.",
            parcial=True, usa_dados=True),
        "m4": Missao(
            lambda t: _mais_gols_por_jogo(t, SAID_EL_MALA, CARLOS_ESPI),
            "Compare as duas divisões: qual número ficou maior?",
            "Quem tem MAIS gols no total nem sempre tem mais gols POR JOGO. "
            "Jogar menos jogos e marcar quase o mesmo tanto é sinal de eficiência!",
            parcial=True, usa_dados=True),
        "desafio1": Missao(
            lambda t: _nomes_do_maximo(t, "valor_milhoes"),
            "Ordene por valor_milhoes, do maior para o menor.",
            "Ordenando por valor_milhoes com ascending=False, o primeiro é o mais valioso.",
            parcial=True, usa_dados=True),
        "desafio2": Missao(
            lambda t: _nomes_do_maximo(_joias(t)[_joias(t)["pais"] == "Brasil"], "gols"),
            "Primeiro filtre as joias. Depois filtre de novo: pais == \"Brasil\".",
            "Dois filtros seguidos: nascido >= 2005 e depois pais == \"Brasil\".",
            parcial=True, usa_dados=True, dificil=True),
    },
    "03_escalacao": {
        "aquecimento": Missao([4, 3, 3], "Só apertar o play ▶️.", "A lista [4, 3, 3] guarda a formação."),
        "m1": Missao(11, "Use len(escalacao).", "len conta quantos itens a lista tem: 11 jogadores."),
        "m2": Missao(
            "Alisson", "No Python a contagem começa no 0. O primeiro da lista é o índice 0.",
            "escalacao[0] é o primeiro da lista: o goleiro."),
        "m3": Missao(10, "Some os três números da formação: 4 + 3 + 3.",
                     "4 + 3 + 3 = 10 jogadores de linha. Com o goleiro, são 11."),
        "m4": Missao(3, "Depois do append, o banco tem os 2 de antes e mais 1.",
                     "append coloca um item no fim da lista: 2 + 1 = 3."),
        "desafio1": Missao(10, "3 + 5 + 2 = ?", "Toda formação de linha soma 10."),
        "desafio2": Missao(
            12, "Liste com calma: comece com 2 zagueiros (2, 3, 5), (2, 4, 4)… e não esqueça a ordem!",
            "Existem 12 jeitos de escrever a + b + c = 10 com cada número de 2 a 5. "
            "Por exemplo 4-3-3, 3-4-3 e 3-3-4 contam como formações diferentes.",
            dificil=True),
    },
    "04_penaltis": {
        "aquecimento": Missao(Qualquer(["cara", "coroa"]), "Só apertar o play ▶️.",
                              "O random.choice sorteia um item da lista."),
        "m1": Missao(0.5, "Chance = casos bons ÷ casos possíveis. 1 / 2.",
                     "1 lado bom entre 2 lados: 1/2 = 0,5 = 50%.", tolerancia=0.001),
        "m2": Missao(1 / 3, "O goleiro tem 3 cantos para escolher. 1 / 3.",
                     "1 canto certo entre 3: 1/3 ≈ 0,33, mais ou menos 33%.", tolerancia=0.01),
        "m3": Missao(lambda: _penaltis_com_semente(67, 10),
                     "Coloque 10 no lugar do ___ e rode a célula inteira.",
                     "Com a mesma semente (seed), o sorteio dá sempre o mesmo resultado."),
        "m4": Missao(Qualquer(["nao", "não"]), "Conte: quantos números do dado fazem você ganhar? E o amigo?",
                     "Você ganha com 1 número (o 6) e o amigo com 5. 1/6 contra 5/6: não é justo."),
        "desafio1": Missao(0.5, "Os pares do dado são 2, 4 e 6.",
                           "3 pares entre 6 números: 3/6 = 0,5.", tolerancia=0.001),
        "desafio2": Missao(0.25, "Escreva todos os resultados: cara-cara, cara-coroa, coroa-cara, coroa-coroa.",
                           "São 4 resultados e só 1 é cara-cara: 1/4 = 0,25.",
                           tolerancia=0.001, dificil=True),
    },
}


def buscar(notebook: str, missao: str) -> Missao | None:
    return MISSOES.get(notebook, {}).get(missao)
