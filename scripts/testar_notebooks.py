"""Roda todos os notebooks "prontos" sem tela (nbclient), como se o aluno
tivesse preenchido tudo certo com as respostas escondidas.

- A célula de preparação troca o git clone pelo repositório local.
- Células com a etiqueta "missao" recebem a solução guardada nos metadados.
- Falha se der erro, se alguma missão não for aceita, ou se uma célula
  do aluno levar mais de 5 segundos.

Uso: pixi run testar-notebooks
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

RAIZ = Path(__file__).resolve().parents[1]
LIMITE_SEGUNDOS = 5.0
SINAIS_DE_ERRO = ["Modo beta", "💡 <b>Dica:</b>", "Vamos ver juntos?", "Ainda tem um <b>___</b>",
                  "Não achei a missão"]


def preparar(nb) -> None:
    for celula in nb.cells:
        if celula.cell_type != "code":
            continue
        if "Preparar o vestiário" in celula.source:
            iniciar = next(l for l in celula.source.splitlines() if l.startswith("iniciar("))
            celula.source = (f"import sys\nsys.path.insert(0, {str(RAIZ)!r})\n"
                             f"from vestiario import *\ncodigo_secreto = \"\"\n{iniciar}")
            celula.metadata["bootstrap"] = True
        elif "missao" in celula.metadata.get("tags", []):
            celula.source = celula.metadata["futebol"]["solucao"]


def duracao(celula) -> float:
    execucao = celula.metadata.get("execution", {})
    inicio, fim = execucao.get("iopub.execute_input"), execucao.get("shell.execute_reply")
    if not inicio or not fim:
        return 0.0
    ler = lambda t: datetime.fromisoformat(t.replace("Z", "+00:00"))
    return (ler(fim) - ler(inicio)).total_seconds()


def texto_saidas(celula) -> str:
    partes = []
    for saida in celula.get("outputs", []):
        partes.append(saida.get("text", ""))
        partes.extend(str(v) for v in saida.get("data", {}).values())
    return "\n".join(partes)


def testar(caminho: Path) -> list[str]:
    nb = nbformat.read(caminho, as_version=4)
    preparar(nb)
    cliente = NotebookClient(nb, timeout=120, kernel_name="python3", record_timing=True,
                             resources={"metadata": {"path": str(RAIZ)}})
    try:
        cliente.execute()
    except CellExecutionError as erro:
        return [f"erro ao rodar: {str(erro).splitlines()[-1] if str(erro) else erro}"]
    problemas = []
    for i, celula in enumerate(nb.cells):
        if celula.cell_type != "code":
            continue
        segundos = duracao(celula)
        if not celula.metadata.get("bootstrap") and segundos > LIMITE_SEGUNDOS:
            problemas.append(f"célula {i} levou {segundos:.1f} s")
        if "missao" in celula.metadata.get("tags", []):
            saida = texto_saidas(celula)
            for sinal in SINAIS_DE_ERRO:
                if sinal in saida:
                    missao = celula.metadata["futebol"]["missao"]
                    problemas.append(f"célula {i} ({missao}): a solução não foi aceita")
                    break
    return problemas


def main() -> int:
    catalogo = json.loads((RAIZ / "notebooks" / "catalogo.json").read_text(encoding="utf-8"))
    prontos = [RAIZ / n["arquivo"] for n in catalogo["notebooks"] if n["status"] == "pronto"]
    falhas = 0
    for caminho in prontos:
        problemas = testar(caminho)
        if problemas:
            falhas += 1
            print(f"❌ {caminho.name}")
            for p in problemas:
                print("   -", p)
        else:
            print(f"✅ {caminho.name}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
