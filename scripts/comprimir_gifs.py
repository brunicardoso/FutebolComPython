"""Encolhe os GIFs escolhidos pelos pais para caberem no repositório.

Lê os arquivos de gifs/ (pasta local, fora do git) e grava versões menores em
midia/gifs/: no máximo 300 pixels de largura e menos de 2 MB cada, para o
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
LIMITE = 2 * 1024 * 1024  # 2 MB

# nome original -> nome no repositório (sem acentos nem espaços)
NOMES = {
    "aura.gif": "aura.gif",
    "cristiano_ronaldo_celebration.gif": "cristiano_ronaldo.gif",
    "haaland-rowing.webp": "haaland_remando.gif",
    "lamine-yamal-lamine.gif": "lamine_yamal.gif",
    "paqueta-dança.gif": "paqueta_danca.gif",
    "viniciusjr-dance.gif": "vinicius_danca.gif",
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
                                  (240, 3, 64), (200, 3, 48), (180, 4, 32)]:
        quadros, duracoes = _quadros(imagem, largura, pular)
        tamanho = _gravar(quadros, duracoes, cores, destino)
        if tamanho < LIMITE:
            return tamanho
    raise SystemExit(f"Não consegui deixar {origem.name} abaixo de 2 MB.")


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
