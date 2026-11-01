"""Encolhe os GIFs escolhidos pelos pais para caberem no repositório.

Lê os arquivos de gifs/ (pasta local, fora do git) e grava versões menores em
midia/gifs/: no máximo 300 pixels de largura e cerca de 1,2 MB cada, para o
`git clone` do Colab continuar rápido.

Uso:  pixi run comprimir-gifs
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageSequence

RAIZ = Path(__file__).resolve().parents[1]
ORIGEM = RAIZ / "gifs"
DESTINO = RAIZ / "midia" / "gifs"
LARGURA = 300
LIMITE = 1_200_000  # cerca de 1,2 MB, para o git clone do Colab continuar rápido

# nome original -> nome no repositório (sem acentos nem espaços)
NOMES = {
    "aura.gif": "aura.gif",
    "cristiano_ronaldo_celebration.gif": "cristiano_ronaldo.gif",
    "haaland-rowing.webp": "haaland_remando.gif",
    "lamine-yamal-lamine.gif": "lamine_yamal.gif",
    "paqueta-dança.gif": "paqueta_danca.gif",
    "viniciusjr-dance.gif": "vinicius_danca.gif",
    # Escolhidos pelos pais na galeria de gifs/candidatos/ (todos do GIPHY).
    "candidatos/01_cr7_siuuu_salto.gif": "cr7_siuuu_salto.gif",  # https://giphy.com/gifs/manutd-manchester-united-mufc-ggmu-hryis7A55UXZNCUTNA
    "candidatos/02_cr7_siuuu_legenda.gif": "cr7_siuuu_legenda.gif",  # https://giphy.com/gifs/uefa-ucl-SJXKbJAoo3HXhjdV74
    "candidatos/03_cr7_siuuu_pintura.gif": "cr7_siuuu_pintura.gif",  # https://giphy.com/gifs/celebration-cristiano-ronaldo-cr7-y7Gbi4VdmRfx4h5Eia
    "candidatos/04_messi_contando.gif": "messi_contando.gif",  # https://giphy.com/gifs/fcbarcelona-goat-messi-leo-TjAcxImn74uoDYVxFl
    "candidatos/05_messi_punho.gif": "messi_punho.gif",  # https://giphy.com/gifs/dazn-messi-si-fist-x7D4ENuCQP7H54Zxa1
    "candidatos/06_messi_taca.gif": "messi_taca.gif",  # https://giphy.com/gifs/kiss-messi-trophy-WzR8zb0PN6bUmfz4DW
    "candidatos/07_neymar_silencio.gif": "neymar_silencio.gif",  # https://giphy.com/gifs/fifa-brazil-world-cup-neymar-sshZsPGCGsQIBKMp87
    "candidatos/08_neymar_ouro_rio2016.gif": "neymar_ouro_rio2016.gif",  # https://giphy.com/gifs/ByVVccPkAcpiw
    "candidatos/09_mbappe_bracos_cruzados.gif": "mbappe_bracos_cruzados.gif",  # https://giphy.com/gifs/equipedefrance-france-mbapp-clbration-xPYlrYkCu05iTkpsM2
    "candidatos/10_mbappe_desenho_oculos.gif": "mbappe_desenho_oculos.gif",  # https://giphy.com/gifs/psg-mbappe-kylian-Urbrsmf0XQcHsIo5SK
    "candidatos/11_haaland_comemora_city.gif": "haaland_comemora_city.gif",  # https://giphy.com/gifs/celebration-celly-haaland-bJrwFC7SAk6EkeojAF
    "candidatos/12_haaland_comemora_champions.gif": "haaland_comemora_champions.gif",  # https://giphy.com/gifs/uefa-sport-champions-league-ucl-gzoOh4SkStpZQxZTzG
    "candidatos/13_richarlison_pombo.gif": "richarlison_pombo.gif",  # https://giphy.com/gifs/cbf-9ufavUuob5fRMaeZjJ
    "candidatos/16_neymar_willian_danca.gif": "neymar_willian_danca.gif",  # https://giphy.com/gifs/brazil-neymar-worldcup-WQZuyEo0OMs80
    "candidatos/17_degea_defesa.gif": "degea_defesa.gif",  # https://giphy.com/gifs/manutd-mufc-ggmu-david-de-gea-sFcbRj6ySxiNicCUpQ
    "candidatos/18_goleiro_bayern_treino.gif": "goleiro_bayern_treino.gif",  # https://giphy.com/gifs/fcbayern-tom-save-26gR1A3Zp4s00vvag
    "candidatos/19_lloris_defesa.gif": "lloris_defesa.gif",  # https://giphy.com/gifs/spursofficial-football-soccer-3ohhwyqTKZQB2C1VIs
    "candidatos/20_defesa_historica_1970.gif": "defesa_historica_1970.gif",  # https://giphy.com/gifs/fifa-SqBSVpOUwjauJouEx0
    "candidatos/21_defesas_por_pouco.gif": "defesas_por_pouco.gif",  # https://giphy.com/gifs/football-goalkeeper-gk-zAUS3lEtBHYVp8K6VA
    "candidatos/22_napoli_travessao.gif": "napoli_travessao.gif",  # https://giphy.com/gifs/nss-sports-napoli-nsssports-milik-6yxYqX3w4rwaqhibcH
    "candidatos/23_dybala_por_pouco.gif": "dybala_por_pouco.gif",  # https://giphy.com/gifs/nss-sports-champions-league-juve-dybala-3gPIXu7frsn2FUFqH0
    "candidatos/24_neymar_escorrega.gif": "neymar_escorrega.gif",  # https://giphy.com/gifs/fifa-neymar-slip-fall-over-Wp6wn8ec276GGmngW9
    "candidatos/25_pavard_pensativo.gif": "pavard_pensativo.gif",  # https://giphy.com/gifs/fcbayern-pavard-benjamin-benji-SxGLjMhz1nLTJf9nHG
    "candidatos/26_var_arbitro.gif": "var_arbitro.gif",  # https://giphy.com/gifs/mls-var-ref-video-review-yEDBFA7QiMVrbMN7o7
    "candidatos/28_messi_filtro_sigma.gif": "messi_filtro_sigma.gif",  # https://giphy.com/gifs/sigma-filter-moai-sU4j7j9agUaPFE1zqC
    "candidatos/29_aura_67_porcento.gif": "aura_67_porcento.gif",  # https://giphy.com/gifs/aura-meme-tuff-J1qp2egzjIreyaI3VQ
    "candidatos/30_senhor_67.gif": "senhor_67.gif",  # https://giphy.com/gifs/67-six-seven-john-chungus-08uBcURaMq6vA93TGc
    "candidatos/31_pintinho_67.gif": "pintinho_67.gif",  # https://giphy.com/gifs/atriumart-7-6-67-tRsYgVhzOYoZR4hUcK
    "candidatos/32_conde_67.gif": "conde_67.gif",  # https://giphy.com/gifs/RespectiveCollective-67-the-count-von-fuNIJhRM2lqNR2NyAQ
}


def _quadros(imagem: Image.Image, largura: int, pular: int) -> tuple[list[Image.Image], list[int]]:
    """Redimensiona e fica com 1 de cada `pular` quadros (somando o tempo dos pulados)."""
    quadros, duracoes = [], []
    for i, quadro in enumerate(ImageSequence.Iterator(imagem)):
        duracao = quadro.info.get("duration") or imagem.info.get("duration") or 80
        if i % pular:
            if duracoes:
                duracoes[-1] += duracao
            continue
        quadro = quadro.convert("RGBA")
        if quadro.width > largura:
            altura = round(quadro.height * largura / quadro.width)
            quadro = quadro.resize((largura, altura), Image.LANCZOS)
        quadros.append(quadro)
        duracoes.append(duracao)
    return quadros, duracoes


def _gravar(quadros, duracoes, cores: int, caminho: Path) -> int:
    paleta = [q.convert("RGB").quantize(colors=cores, method=Image.Quantize.MEDIANCUT,
                                        dither=Image.Dither.NONE) for q in quadros]
    paleta[0].save(caminho, save_all=True, append_images=paleta[1:], duration=duracoes,
                   loop=0, optimize=True, disposal=2)
    return caminho.stat().st_size


def comprimir(origem: Path, destino: Path) -> int:
    """Tenta configurações cada vez menores até ficar abaixo do limite."""
    imagem = Image.open(origem)
    for largura, pular, cores in [(LARGURA, 1, 128), (LARGURA, 2, 96), (260, 2, 64),
                                  (240, 3, 64), (200, 3, 48), (180, 4, 32),
                                  (160, 4, 32), (150, 5, 24)]:
        quadros, duracoes = _quadros(imagem, largura, pular)
        tamanho = _gravar(quadros, duracoes, cores, destino)
        if tamanho < LIMITE:
            return tamanho
    raise SystemExit(f"Não consegui deixar {origem.name} pequeno o bastante.")


def main() -> int:
    if not ORIGEM.exists():
        print("A pasta gifs/ não existe. Coloque os GIFs originais lá primeiro.")
        return 1
    DESTINO.mkdir(parents=True, exist_ok=True)
    for original, novo in NOMES.items():
        caminho = ORIGEM / original
        if not caminho.exists():
            print(f"⚠️  faltando: {original}")
            continue
        tamanho = comprimir(caminho, DESTINO / novo)
        print(f"✅ {original} -> midia/gifs/{novo} ({tamanho // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
