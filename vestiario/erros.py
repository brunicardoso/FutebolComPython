"""Erros elegantes: quando uma célula dá erro, mostra uma caixa calma em pt-BR.

Muitas vezes o aluno apaga um pedaço do código sem querer. Por isso a caixa
mostra uma dica em palavras simples e, quando dá para achar, o **código
original** daquela célula (lido do notebook clonado) para copiar de volta.
O erro técnico do Python fica escondido em "ver erro técnico" (para os adultos).

Isto não muda a aura e não usa a reação "beta": foi um acidente, não uma
resposta errada. Se algo aqui falhar, o IPython mostra o erro do jeito normal.
"""

from __future__ import annotations

import builtins
import difflib
import json
import re
from functools import lru_cache

from . import config
from .tela import caixa, escapar, exibir

COR, FUNDO = "#4e342e", "#fff8e1"  # marrom calmo, nada de vermelho
SEMELHANCA_MINIMA = 0.5
_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_estado = {"notebook": "", "instalado": False}


# ---------------------------------------------------------------- dicas

def _nomes_conhecidos(espaco: dict | None) -> list[str]:
    nomes = set(dir(builtins))
    if espaco:
        nomes |= {n for n in espaco if not n.startswith("_")}
    return sorted(nomes)


def explicar(erro: BaseException, espaco: dict | None = None, celulas: list[str] | None = None) -> str:
    """Devolve uma dica curta (HTML) para o tipo de erro."""
    tipo = type(erro).__name__
    mensagem = str(erro)

    if isinstance(erro, NameError):
        nome = getattr(erro, "name", None) or (re.findall(r"'([^']+)'", mensagem) or [""])[0]
        if nome.strip("_") == "":
            return "Ainda tem um <b>___</b> esperando você! Troque pela sua resposta e aperte ▶️ de novo."
        if celulas and any(re.search(rf"^\s*{re.escape(nome)}\s*=", c, re.M) for c in celulas):
            return (f"O Python ainda não conhece <code>{escapar(nome)}</code>. A célula que cria "
                    f"<code>{escapar(nome)}</code> fica mais para cima: aperte ▶️ nela e depois volte aqui.")
        parecido = difflib.get_close_matches(nome, _nomes_conhecidos(espaco), n=1, cutoff=0.75)
        if parecido:
            return (f"O Python não conhece <code>{escapar(nome)}</code>. "
                    f"Será que você quis escrever <code>{escapar(parecido[0])}</code>?")
        return (f"O Python não conhece <code>{escapar(nome)}</code>. Confira se o nome está "
                "escrito igualzinho (sem acento) ou se um pedaço foi apagado.")

    if isinstance(erro, IndentationError):
        return ("Tem um espaço sobrando (ou faltando) no começo de uma linha. "
                "No Python, o começo da linha importa!" + _linha(erro))

    if isinstance(erro, SyntaxError):
        texto = (erro.msg or "").lower()
        if "unterminated string" in texto or "eol while scanning" in texto:
            dica = "Faltam aspas <code>\"</code>: todo texto abre e fecha aspas."
        elif "never closed" in texto or "unexpected eof" in texto or "unmatched" in texto \
                or "incomplete input" in texto \
                or "does not match" in texto:
            dica = "Um parêntese <code>( )</code> ou colchete <code>[ ]</code> ficou sem par."
        elif "comma" in texto:
            dica = "Parece que falta uma vírgula <code>,</code> entre duas coisas."
        elif "'=' " in texto or "maybe you meant '=='" in texto or "cannot assign" in texto:
            dica = "Lembre: um <code>=</code> guarda, dois <code>==</code> perguntam."
        else:
            dica = "O Python não entendeu como a linha está escrita. Talvez um pedaço tenha sumido."
        return dica + _linha(erro)

    if isinstance(erro, KeyError):
        coluna = mensagem.strip("'\"")
        return (f"Não achei <code>{escapar(coluna)}</code>. Se for uma coluna da tabela, confira "
                "o nome: é sem acento e com letra minúscula (ex.: <code>assistencias</code>).")

    if isinstance(erro, ZeroDivisionError):
        return "Não dá para dividir por zero! Confira o número que ficou embaixo da divisão."

    if isinstance(erro, IndexError):
        return ("Essa posição não existe. Lembre: a primeira posição da lista é o <b>0</b>, "
                "e a última é o tamanho menos 1.")

    if isinstance(erro, AttributeError):
        parte = (re.findall(r"attribute '([^']+)'", mensagem) or [""])[0]
        alvo = f"<code>.{escapar(parte)}</code>" if parte else "esse comando"
        return f"O Python não conhece {alvo} aqui. Confira se está escrito certinho, com os parênteses."

    if isinstance(erro, TypeError):
        return ("Os pedaços não combinam (por exemplo, somar número com texto, ou faltou algo "
                "dentro dos parênteses). Confira se alguma coisa foi apagada.")

    if isinstance(erro, ValueError):
        return "Esse valor não serviu aqui. Confira se escreveu um número onde a missão pede número."

    if isinstance(erro, ModuleNotFoundError):
        return "Parece que o vestiário não foi preparado. Aperte ▶️ na primeira célula do notebook."

    return f"Algo não deu certo nesta célula ({escapar(tipo)}). Confira se algum pedaço foi apagado."


def _linha(erro: SyntaxError) -> str:
    return f" Olhe a linha <b>{erro.lineno}</b>." if getattr(erro, "lineno", None) else ""


# ---------------------------------------------------------------- código original

@lru_cache(maxsize=8)
def celulas_originais(notebook: str) -> tuple[str, ...]:
    """As células de código do notebook como ele veio do GitHub (sem as escondidas)."""
    if not notebook:
        return ()
    caminhos = sorted(config.PASTA_NOTEBOOKS.glob(f"*/{notebook}.ipynb"))
    if not caminhos:
        return ()
    try:
        with open(caminhos[0], encoding="utf-8") as arquivo:
            nb = json.load(arquivo)
    except (OSError, ValueError):
        return ()
    fontes = []
    for celula in nb.get("cells", []):
        if celula.get("cell_type") != "code" or celula.get("metadata", {}).get("cellView") == "form":
            continue
        fonte = "".join(celula.get("source", []))
        if fonte.strip():
            fontes.append(fonte)
    return tuple(fontes)


def codigo_original(atual: str, celulas: tuple[str, ...] | list[str]) -> str | None:
    """Acha a célula original mais parecida com a que deu erro.

    Devolve None se nenhuma for parecida o bastante, ou se a célula já está igual
    à original (aí não há nada para recuperar)."""
    atual = (atual or "").strip()
    if not atual or not celulas:
        return None
    melhor, nota = None, 0.0
    for original in celulas:
        o = original.strip()
        if o == atual:
            return None
        pontos = difflib.SequenceMatcher(None, atual, o).ratio()
        if len(atual) >= 4 and atual in o:  # o aluno apagou o fim (ou o começo) da célula
            pontos = max(pontos, 0.6 + 0.4 * len(atual) / len(o))
        if pontos > nota:
            melhor, nota = o, pontos
    return melhor if nota >= SEMELHANCA_MINIMA else None


# ---------------------------------------------------------------- a caixa

def html_erro(dica: str, original: str | None, tecnico: str) -> str:
    partes = [f"🧩 <b>Ops! Esta célula não rodou.</b> Acontece com todo mundo, até com programador profissional.",
              f"<div style=\"margin-top:6px\">💡 {dica}</div>"]
    if original:
        partes.append(
            "<div style=\"margin-top:8px\">Se um pedaço sumiu sem querer, este é o código original. "
            "📋 Copie e cole de volta na célula:</div>"
            f"<pre style=\"background:#fff;border:1px solid #d7ccc8;border-radius:8px;padding:8px;"
            f"white-space:pre-wrap;font-size:.95em;margin:6px 0\">{escapar(original)}</pre>")
    partes.append("<div style=\"margin-top:4px\">🔁 Depois é só apertar ▶️ de novo.</div>")
    if tecnico:
        partes.append(
            "<details style=\"margin-top:6px;font-size:.8em\"><summary>ver erro técnico</summary>"
            f"<pre style=\"white-space:pre-wrap\">{escapar(_ANSI.sub('', tecnico))}</pre></details>")
    return caixa("".join(partes), cor=COR, fundo=FUNDO)


def mostrar(erro: BaseException, atual: str, espaco: dict | None = None, tecnico: str = "") -> None:
    celulas = celulas_originais(_estado["notebook"])
    exibir(html_erro(explicar(erro, espaco, list(celulas)), codigo_original(atual, celulas), tecnico))


# ---------------------------------------------------------------- ligação com o IPython

def _celula_atual(ip) -> str:
    try:
        return ip.history_manager.input_hist_raw[-1]
    except Exception:
        return ""


def _resumo(erro: BaseException) -> list[str]:
    """O que fica no quadro de erro do Colab: uma linha só, apontando para a caixa."""
    return [f"{type(erro).__name__}: {erro}  (veja a dica 🧩 acima)"]


def instalar(notebook: str = "") -> bool:
    """Liga os erros elegantes no IPython. Fora do Jupyter, não faz nada."""
    _estado["notebook"] = notebook
    try:
        from IPython import get_ipython
    except ImportError:
        return False
    ip = get_ipython()
    if ip is None or not hasattr(ip, "set_custom_exc"):
        return False
    if _estado["instalado"]:
        return True

    # O IPython chama ao_errar para qualquer Exception, inclusive SyntaxError ao ler a
    # célula. Ele não mostra o que a função devolve: por isso ela mesma mostra a caixa
    # e uma linha curta de erro (que mantém a célula marcada como "deu erro").
    def ao_errar(shell, etype, valor, tb, tb_offset=None):
        try:
            if issubclass(etype, SyntaxError):
                stb = shell.SyntaxTB.structured_traceback(etype, valor, [])
            else:
                stb = shell.InteractiveTB.structured_traceback(etype, valor, tb, tb_offset)
            mostrar(valor, _celula_atual(shell), shell.user_ns, "\n".join(stb))
            shell._showtraceback(etype, valor, _resumo(valor))
        except Exception:
            shell.showtraceback((etype, valor, tb), tb_offset=tb_offset)
        return []

    ip.set_custom_exc((Exception,), ao_errar)
    _estado["instalado"] = True
    return True
