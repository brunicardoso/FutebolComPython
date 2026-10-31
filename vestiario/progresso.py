"""Guardar e recuperar o progresso.

O Colab esquece tudo quando a sessão acaba. Por isso existe o código
secreto, como AURA-1350-J3N5-7F2:
  1350 = aura total
  J3   = jogos desbloqueados (cada bit é um jogo, em hexadecimal)
  N5   = notebooks terminados (cada bit é um notebook, em hexadecimal)
  7F2  = verificador, para descobrir erros de digitação
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .aura import EstadoAura

# A ordem desta lista nunca muda: só acrescente jogos novos no final.
ORDEM_JOGOS = ["embaixadinhas", "goleiro_reflexo", "tabela_maluca", "penalti",
               "falta_barreira", "album_relampago"]

PADRAO = re.compile(r"^AURA-(\d+)-J([0-9A-F]+)N([0-9A-F]+)-([0-9A-F]{3})$")
ARQUIVO_DRIVE = Path("/content/drive/MyDrive/futebol_python_progresso.json")


def _verificador(aura: int, jogos: int, notebooks: int) -> str:
    base = f"{aura}|{jogos}|{notebooks}|vestiario"
    return hashlib.sha256(base.encode()).hexdigest()[:3].upper()


def gerar_codigo(estado: EstadoAura) -> str:
    jogos = sum(1 << i for i, nome in enumerate(ORDEM_JOGOS) if nome in estado.jogos)
    notebooks = sum(1 << (n - 1) for n in estado.notebooks if 1 <= n <= 64)
    return (f"AURA-{estado.total}-J{jogos:X}N{notebooks:X}-"
            f"{_verificador(estado.total, jogos, notebooks)}")


def ler_codigo(codigo: str) -> EstadoAura | None:
    """Transforma o código de volta em progresso. Devolve None se estiver errado."""
    limpo = re.sub(r"\s+", "", str(codigo)).upper()
    achou = PADRAO.match(limpo)
    if not achou:
        return None
    aura, jogos, notebooks = int(achou[1]), int(achou[2], 16), int(achou[3], 16)
    if _verificador(aura, jogos, notebooks) != achou[4]:
        return None
    return EstadoAura(
        total=aura,
        jogos={nome for i, nome in enumerate(ORDEM_JOGOS) if jogos >> i & 1},
        notebooks={n + 1 for n in range(64) if notebooks >> n & 1},
    )


def salvar_drive(estado: EstadoAura) -> bool:
    """Salva no Google Drive (pede permissão). Devolve True se deu certo."""
    try:
        from google.colab import drive
        drive.mount("/content/drive")
        ARQUIVO_DRIVE.write_text(json.dumps({"codigo": gerar_codigo(estado)}))
        return True
    except Exception:
        return False


def ler_drive() -> EstadoAura | None:
    """Lê o progresso do Drive só se ele já estiver conectado (não pede nada)."""
    try:
        return ler_codigo(json.loads(ARQUIVO_DRIVE.read_text())["codigo"])
    except Exception:
        return None
