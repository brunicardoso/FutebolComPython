"""Configurações do vestiário. O endereço do repositório fica só aqui
(e na célula de preparação de cada notebook)."""

from pathlib import Path

REPO_URL = "https://github.com/brunicardoso/FutebolComPython"
RAMO = "main"

RAIZ = Path(__file__).resolve().parents[1]
PASTA_DADOS = RAIZ / "dados"
PASTA_JOGOS = RAIZ / "jogos"
PASTA_MIDIA = RAIZ / "midia"
PASTA_GIFS = PASTA_MIDIA / "gifs"
PASTA_NOTEBOOKS = RAIZ / "notebooks"

ARQUIVO_JOGADORES = PASTA_DADOS / "jogadores_2025_26.csv.gz"
ARQUIVO_CURIOSIDADES = PASTA_DADOS / "curiosidades.json"
ARQUIVO_REACOES = PASTA_MIDIA / "reacoes.json"
ARQUIVO_CATALOGO = PASTA_NOTEBOOKS / "catalogo.json"

# Identificação exigida pela Wikimedia para chamadas à API.
USER_AGENT = f"FutebolComPython/1.0 ({REPO_URL}; projeto educativo)"

# Tempo de atividade (em minutos) até sugerir um intervalo.
MINUTOS_INTERVALO = 20
