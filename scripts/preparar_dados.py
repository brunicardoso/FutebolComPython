"""Monta o retrato (snapshot) da temporada 2025–26 usado pelos notebooks.

Fonte: transfermarkt-datasets (https://github.com/dcaribou/transfermarkt-datasets),
licença CC0 1.0. As tabelas brutas ficam em dados/brutos/ (fora do git) e o
resultado vai para dados/jogadores_2025_26.csv.gz e dados/clubes.csv.

Uso: pixi run preparar-dados
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos"
SAIDA_JOGADORES = RAIZ / "dados" / "jogadores_2025_26.csv.gz"
SAIDA_CLUBES = RAIZ / "dados" / "clubes.csv"

URL_BASE = "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data"
TABELAS = ["players", "clubs", "appearances"]
# O servidor responde 403 para o User-Agent padrão do Python.
CABECALHOS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) futebol-python/1.0"}

LIGAS = {"GB1": "Premier League", "ES1": "La Liga", "L1": "Bundesliga",
         "IT1": "Serie A", "FR1": "Ligue 1"}
INICIO, FIM = "2025-07-01", "2026-06-30"

POSICOES = {"Attack": "Atacante", "Midfield": "Meio-campo",
            "Defender": "Zagueiro", "Goalkeeper": "Goleiro", "Missing": "Desconhecida"}

# Nomes curtos, como a gente fala no dia a dia (chave: club_id do Transfermarkt).
NOMES_CURTOS = {
    2036: "Heidenheim", 3: "Colônia", 89: "Union Berlin", 39: "Mainz", 5: "Milan",
    430: "Fiorentina", 989: "Bournemouth", 290: "Auxerre", 162: "Monaco", 1420: "Angers",
    11: "Arsenal", 405: "Aston Villa", 800: "Atalanta", 621: "Athletic Bilbao",
    13: "Atlético de Madrid", 15: "Bayer Leverkusen", 27: "Bayern de Munique",
    1025: "Bologna", 16: "Borussia Dortmund", 18: "Borussia Mönchengladbach",
    1148: "Brentford", 1237: "Brighton", 1132: "Burnley", 331: "Osasuna", 1390: "Cagliari",
    940: "Celta de Vigo", 631: "Chelsea", 1047: "Como", 873: "Crystal Palace",
    1108: "Alavés", 24: "Eintracht Frankfurt", 1531: "Elche", 29: "Everton",
    167: "Augsburg", 131: "Barcelona", 1158: "Lorient", 347: "Metz", 995: "Nantes",
    35: "St. Pauli", 415: "Toulouse", 931: "Fulham", 252: "Genoa", 3709: "Getafe",
    12321: "Girona", 41: "Hamburgo", 276: "Hellas Verona", 46: "Inter de Milão",
    506: "Juventus", 1082: "Lille", 398: "Lazio", 738: "Le Havre", 399: "Leeds United",
    3368: "Levante", 31: "Liverpool", 281: "Manchester City", 985: "Manchester United",
    762: "Newcastle", 703: "Nottingham Forest", 417: "Nice", 1041: "Lyon",
    244: "Olympique de Marselha", 10004: "Paris FC", 583: "PSG", 130: "Parma", 4172: "Pisa",
    23826: "RB Leipzig", 826: "Lens", 667: "Strasbourg", 714: "Espanyol", 237: "Mallorca",
    367: "Rayo Vallecano", 150: "Real Betis", 418: "Real Madrid", 2497: "Real Oviedo",
    681: "Real Sociedad", 12: "Roma", 60: "Freiburg", 6195: "Napoli", 86: "Werder Bremen",
    368: "Sevilla", 3911: "Brest", 273: "Rennes", 289: "Sunderland", 533: "Hoffenheim",
    416: "Torino", 148: "Tottenham", 2239: "Cremonese", 1005: "Lecce", 6574: "Sassuolo",
    410: "Udinese", 1049: "Valencia", 79: "Stuttgart", 82: "Wolfsburg", 1050: "Villarreal",
    379: "West Ham", 543: "Wolverhampton",
}

# Países em português do Brasil.
PAISES = {
    "Albania": "Albânia", "Algeria": "Argélia", "Angola": "Angola", "Argentina": "Argentina",
    "Armenia": "Armênia", "Australia": "Austrália", "Austria": "Áustria", "Belgium": "Bélgica",
    "Benin": "Benin", "Bosnia-Herzegovina": "Bósnia", "Brazil": "Brasil",
    "Bulgaria": "Bulgária", "Burkina Faso": "Burkina Faso", "Burundi": "Burundi",
    "Cameroon": "Camarões", "Canada": "Canadá", "Cape Verde": "Cabo Verde",
    "Central African Republic": "República Centro-Africana", "Chile": "Chile",
    "Colombia": "Colômbia", "Comoros": "Comores", "Congo": "Congo",
    "Cote d'Ivoire": "Costa do Marfim", "Croatia": "Croácia", "Cyprus": "Chipre",
    "Czech Republic": "Tchéquia", "DR Congo": "RD Congo", "Denmark": "Dinamarca",
    "Dominican Republic": "República Dominicana", "Ecuador": "Equador", "Egypt": "Egito",
    "England": "Inglaterra", "Equatorial Guinea": "Guiné Equatorial", "Estonia": "Estônia",
    "Faroe Islands": "Ilhas Faroé", "Finland": "Finlândia", "France": "França",
    "French Guiana": "Guiana Francesa", "Gabon": "Gabão", "Georgia": "Geórgia",
    "Germany": "Alemanha", "Ghana": "Gana", "Greece": "Grécia", "Guadeloupe": "Guadalupe",
    "Guinea": "Guiné", "Guinea-Bissau": "Guiné-Bissau", "Haiti": "Haiti",
    "Honduras": "Honduras", "Hungary": "Hungria", "Iceland": "Islândia",
    "Indonesia": "Indonésia", "Ireland": "Irlanda", "Israel": "Israel", "Italy": "Itália",
    "Jamaica": "Jamaica", "Japan": "Japão", "Jordan": "Jordânia", "Kenya": "Quênia",
    "Korea, South": "Coreia do Sul", "Kosovo": "Kosovo", "Latvia": "Letônia",
    "Libya": "Líbia", "Lithuania": "Lituânia", "Luxembourg": "Luxemburgo",
    "Madagascar": "Madagascar", "Malaysia": "Malásia", "Mali": "Mali",
    "Mauritania": "Mauritânia", "Mexico": "México", "Montenegro": "Montenegro",
    "Morocco": "Marrocos", "Mozambique": "Moçambique", "Netherlands": "Holanda",
    "New Zealand": "Nova Zelândia", "Niger": "Níger", "Nigeria": "Nigéria",
    "North Macedonia": "Macedônia do Norte", "Northern Ireland": "Irlanda do Norte",
    "Norway": "Noruega", "Panama": "Panamá", "Paraguay": "Paraguai", "Peru": "Peru",
    "Poland": "Polônia", "Portugal": "Portugal", "Romania": "Romênia", "Russia": "Rússia",
    "Saudi Arabia": "Arábia Saudita", "Scotland": "Escócia", "Senegal": "Senegal",
    "Serbia": "Sérvia", "Sierra Leone": "Serra Leoa", "Slovakia": "Eslováquia",
    "Slovenia": "Eslovênia", "South Africa": "África do Sul", "Spain": "Espanha",
    "Suriname": "Suriname", "Sweden": "Suécia", "Switzerland": "Suíça", "Syria": "Síria",
    "Tanzania": "Tanzânia", "Thailand": "Tailândia", "The Gambia": "Gâmbia", "Togo": "Togo",
    "Trinidad and Tobago": "Trinidad e Tobago", "Tunisia": "Tunísia", "Türkiye": "Turquia",
    "Ukraine": "Ucrânia", "United States": "Estados Unidos", "Uruguay": "Uruguai",
    "Uzbekistan": "Uzbequistão", "Venezuela": "Venezuela", "Wales": "País de Gales",
    "Zambia": "Zâmbia", "Zimbabwe": "Zimbábue",
}


def baixar(tabela: str) -> Path:
    """Baixa uma tabela bruta (só se ainda não existir) e devolve o caminho."""
    BRUTOS.mkdir(parents=True, exist_ok=True)
    destino = BRUTOS / f"{tabela}.csv.gz"
    if destino.exists():
        return destino
    url = f"{URL_BASE}/{tabela}.csv.gz"
    print(f"Baixando {url} …")
    resposta = requests.get(url, headers=CABECALHOS, timeout=120)
    if resposta.status_code != 200:
        sys.exit(
            f"Falhou ({resposta.status_code}). Alternativa: baixe o conjunto "
            "'davidcariboo/player-scores' do Kaggle e coloque os arquivos "
            f"{', '.join(t + '.csv.gz' for t in TABELAS)} em {BRUTOS}."
        )
    destino.write_bytes(resposta.content)
    return destino


def encurtar(club_id: int, nome: str) -> str:
    """Usa o nome curto do clube; se não tiver, fica o nome original."""
    return NOMES_CURTOS.get(int(club_id), nome)


def main() -> None:
    caminhos = {t: baixar(t) for t in TABELAS}
    jogadores = pd.read_csv(caminhos["players"])
    clubes = pd.read_csv(caminhos["clubs"])
    aparicoes = pd.read_csv(caminhos["appearances"],
                            usecols=["player_id", "player_club_id", "date", "competition_id",
                                     "goals", "assists", "minutes_played"])

    filtro = (aparicoes["competition_id"].isin(LIGAS)
              & aparicoes["date"].between(INICIO, FIM))
    temporada = aparicoes[filtro]
    if temporada.empty:
        sys.exit("Nenhum jogo encontrado na temporada 2025–26.")

    # O clube de cada jogador é aquele onde ele jogou mais minutos.
    clube_principal = (temporada.groupby(["player_id", "player_club_id", "competition_id"])
                       ["minutes_played"].sum().reset_index()
                       .sort_values("minutes_played", ascending=False)
                       .drop_duplicates("player_id"))

    totais = temporada.groupby("player_id").agg(
        jogos=("date", "count"), minutos=("minutes_played", "sum"),
        gols=("goals", "sum"), assistencias=("assists", "sum")).reset_index()

    tabela = (totais
              .merge(clube_principal[["player_id", "player_club_id", "competition_id"]],
                     on="player_id")
              .merge(jogadores[["player_id", "name", "position", "country_of_citizenship",
                                "date_of_birth", "market_value_in_eur"]],
                     on="player_id", how="left")
              .merge(clubes[["club_id", "name"]].rename(columns={"name": "nome_clube"}),
                     left_on="player_club_id", right_on="club_id", how="left"))

    tabela["nome_clube"] = [encurtar(i, n) for i, n in
                            zip(tabela["player_club_id"], tabela["nome_clube"].fillna(""))]
    resultado = pd.DataFrame({
        "player_id": tabela["player_id"],
        "club_id": tabela["player_club_id"],
        "nome": tabela["name"],
        "clube": tabela["nome_clube"],
        "liga": tabela["competition_id"].map(LIGAS),
        "posicao": tabela["position"].map(POSICOES).fillna("Desconhecida"),
        "pais": tabela["country_of_citizenship"].map(lambda p: PAISES.get(p, p)),
        "nascido": pd.to_datetime(tabela["date_of_birth"]).dt.year.astype("Int64"),
        "jogos": tabela["jogos"],
        "minutos": tabela["minutos"],
        "gols": tabela["gols"],
        "assistencias": tabela["assistencias"],
        "valor_milhoes": (tabela["market_value_in_eur"] / 1e6).round(1),
    }).sort_values(["gols", "assistencias"], ascending=False)

    resultado.to_csv(SAIDA_JOGADORES, index=False, compression="gzip")

    ids = set(resultado["club_id"])
    lista_clubes = clubes[clubes["club_id"].isin(ids)]
    pd.DataFrame({
        "club_id": lista_clubes["club_id"],
        "clube": [encurtar(i, n) for i, n in zip(lista_clubes["club_id"], lista_clubes["name"])],
        "liga": lista_clubes["domestic_competition_id"].map(LIGAS),
        "estadio": lista_clubes["stadium_name"],
        "lugares": lista_clubes["stadium_seats"],
    }).sort_values("clube").to_csv(SAIDA_CLUBES, index=False)

    print(f"Pronto: {len(resultado)} jogadores, {len(lista_clubes)} clubes.")
    print(resultado.head(10)[["nome", "clube", "liga", "gols", "nascido"]].to_string(index=False))


if __name__ == "__main__":
    main()
