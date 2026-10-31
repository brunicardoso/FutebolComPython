"""Pontos de aura, sequências, níveis e o easter egg do 67.

Aqui fica só a matemática (sem nada de tela), para dar para testar fácil.
"""

from __future__ import annotations

from dataclasses import dataclass, field

PONTOS_ACERTO = 100
BONUS_PRIMEIRA = 50
PONTOS_DIFICIL = 500
PONTOS_CHUTE = 100
MAX_AURA_JOGO = 50

# (aura mínima, nome do nível)
NIVEIS = [
    (0, "Reserva"),
    (1_000, "Titular"),
    (3_000, "Craque"),
    (6_000, "Lenda"),
    (10_000, "Sigma Supremo"),
]

NUMEROS_67 = {67, 670, 6_700, 67_000}


def eh_67(valor) -> bool:
    """Verdadeiro se o valor for 67 (ou 670, 6.700, 67.000)."""
    if isinstance(valor, bool):
        return False
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except (TypeError, ValueError):
        return False
    return numero in NUMEROS_67


def nivel(total: int) -> tuple[str, str | None, float]:
    """Devolve (nível atual, próximo nível, quanto já andou até o próximo de 0 a 1)."""
    atual = 0
    for i, (minimo, _) in enumerate(NIVEIS):
        if total >= minimo:
            atual = i
    nome = NIVEIS[atual][1]
    if atual == len(NIVEIS) - 1:
        return nome, None, 1.0
    inicio, (fim, proximo) = NIVEIS[atual][0], NIVEIS[atual + 1]
    return nome, proximo, (total - inicio) / (fim - inicio)


@dataclass
class Resultado:
    """O que aconteceu depois de uma resposta certa."""
    pontos: int = 0
    primeira: bool = False
    sequencia: int = 0
    marco_sequencia: int | None = None  # 3 ou 5 quando chega nesses números
    subiu_para: str | None = None
    repetida: bool = False


@dataclass
class EstadoAura:
    total: int = 0
    sequencia: int = 0
    erros: dict[str, int] = field(default_factory=dict)
    missoes_feitas: set[str] = field(default_factory=set)
    jogos: set[str] = field(default_factory=set)
    notebooks: set[int] = field(default_factory=set)
    avisos_67: set[str] = field(default_factory=set)
    chutes_premiados: set[str] = field(default_factory=set)
    jogadas_pagas: dict[str, int] = field(default_factory=dict)

    def ganhar(self, pontos: int) -> tuple[int, str | None]:
        """Soma aura (nunca tira). Devolve (pontos ganhos, novo nível se subiu)."""
        pontos = max(0, int(pontos))
        antes = nivel(self.total)[0]
        self.total += pontos
        depois = nivel(self.total)[0]
        return pontos, (depois if depois != antes else None)

    def acertou(self, chave: str, dificil: bool = False) -> Resultado:
        """Registra um acerto. Uma missão só dá aura uma vez."""
        self.sequencia += 1
        marco = self.sequencia if self.sequencia in (3, 5) else None
        if chave in self.missoes_feitas:
            return Resultado(sequencia=self.sequencia, marco_sequencia=marco, repetida=True)
        primeira = self.erros.get(chave, 0) == 0
        pontos = PONTOS_DIFICIL if dificil else PONTOS_ACERTO
        if primeira:
            pontos += BONUS_PRIMEIRA
        self.missoes_feitas.add(chave)
        ganhos, subiu = self.ganhar(pontos)
        return Resultado(pontos=ganhos, primeira=primeira, sequencia=self.sequencia,
                         marco_sequencia=marco, subiu_para=subiu)

    def errou(self, chave: str) -> int:
        """Registra um erro: quebra a sequência, mas não tira aura. Devolve quantos erros."""
        self.sequencia = 0
        self.erros[chave] = self.erros.get(chave, 0) + 1
        return self.erros[chave]

    def desistiu(self, chave: str) -> None:
        """Depois de 3 erros a resposta aparece; a missão conta como feita, sem aura."""
        self.missoes_feitas.add(chave)

    def avisar_67(self, valor, chave: str) -> bool:
        """Verdadeiro se for um 67 e ainda não teve 67 nesta missão."""
        if chave in self.avisos_67 or not eh_67(valor):
            return False
        self.avisos_67.add(chave)
        return True

    def premiar_chute(self, chave: str) -> int:
        """Palpite na trave dá aura, mas só uma vez por pergunta."""
        if chave in self.chutes_premiados:
            return 0
        self.chutes_premiados.add(chave)
        return self.ganhar(PONTOS_CHUTE)[0]

    def premiar_jogo(self, nome: str, pontos: int, limite_jogadas: int = 3) -> int:
        """Jogo de campeão dá no máximo +50 por partida e paga só algumas partidas."""
        feitas = self.jogadas_pagas.get(nome, 0)
        if feitas >= limite_jogadas:
            return 0
        self.jogadas_pagas[nome] = feitas + 1
        return self.ganhar(min(MAX_AURA_JOGO, max(0, int(pontos))))[0]
