"""Vestiário: as funções que você usa nos notebooks do Futebol com Python.

    iniciar(nivel, notebook)       prepara tudo e mostra sua aura
    checar(resposta, missao="m1")  confere a resposta de uma missão
    chute(palpite, real)           mostra o quão perto o seu palpite chegou
    comemorar(tipo="aura")         comemoração (para os pais apertarem)
    dica(missao="m1")              mostra a dica de uma missão
    curiosidades(tabela, n=3)      curiosidades dos jogadores da tabela
    vestiario()                    seus jogos e seu nível de aura
    som(True) / som(False)         liga ou desliga o som (começa ligado; o ícone 🔊 também)
    jogar(nome)                    abre um jogo desbloqueado
    terminar()                     fecha o notebook e libera o jogo do vestiário
    salvar_progresso() / carregar_progresso(codigo)
    carregar_jogadores()           a tabela de jogadores da temporada 2025–26
"""

from __future__ import annotations

import json
import time

from . import aura as _aura
from . import config, erros, missoes, progresso, reacoes
from . import som as _som
from . import curiosidades as _curiosidades
from . import jogos as _jogos
from .dados import carregar_jogadores
from .tela import caixa, escapar, exibir, numero

__all__ = ["iniciar", "checar", "chute", "comemorar", "dica", "curiosidades", "vestiario",
           "som", "jogar", "terminar", "salvar_progresso", "carregar_progresso", "carregar_jogadores"]

_estado = _aura.EstadoAura()
_sessao = {"nivel": 1, "notebook": "", "inicio": time.monotonic(), "intervalo": False}


# ---------------------------------------------------------------- ajudantes internos

def _catalogo() -> list[dict]:
    with open(config.ARQUIVO_CATALOGO, encoding="utf-8") as arquivo:
        return json.load(arquivo)["notebooks"]


def _info_notebook(ident: str) -> dict | None:
    return next((n for n in _catalogo() if n["id"] == ident), None)


def _barra_aura() -> str:
    nome, proximo, fracao = _aura.nivel(_estado.total)
    largura = max(3, int(fracao * 100))
    alvo = f"próximo nível: <b>{proximo}</b>" if proximo else "nível máximo!"
    return (f'<div style="font-family:system-ui,sans-serif;max-width:460px;margin:8px 0">'
            f'<div style="font-size:1.1em">✨ Aura: <b>{numero(_estado.total)}</b> · '
            f'Nível <b>{nome}</b> · {alvo}</div>'
            f'<div style="background:#ddd;border-radius:10px;height:16px;overflow:hidden">'
            f'<div style="width:{largura}%;height:100%;background:linear-gradient(90deg,#43a047,#fdd835)">'
            f'</div></div></div>')


def _linha_aura(pontos: int) -> str:
    return caixa(f"✨ +{numero(pontos)} de aura! Você está farmando aura: "
                 f"<b>{numero(_estado.total)}</b> ✨", cor="#6a1b9a", fundo="#f3e5f5",
                 tamanho="1.3em")


def _talvez_intervalo() -> None:
    minutos = (time.monotonic() - _sessao["inicio"]) / 60
    if minutos >= config.MINUTOS_INTERVALO and not _sessao["intervalo"]:
        _sessao["intervalo"] = True
        exibir(caixa("⏸️ <b>Intervalo!</b> Você já está treinando há um tempão. "
                     "Que tal se alongar, beber água ou chutar uma bola de verdade? "
                     "Depois é só voltar aqui.", cor="#0d47a1", fundo="#e3f2fd"))


def _checar_67(valor, chave: str) -> None:
    if _estado.avisar_67(valor, chave):
        reacoes.mostrar("seis_sete")
    if _estado.avisar_67(_estado.total, f"total:{_estado.total}"):
        reacoes.mostrar("seis_sete")


def _vazio(resposta) -> bool:
    return resposta is None or (isinstance(resposta, str) and resposta.strip() in ("", "___"))


def _eh_tabela(resposta) -> bool:
    return hasattr(resposta, "columns") or (hasattr(resposta, "index") and hasattr(resposta, "dtype"))


def _desbloquear(nome: str | None) -> None:
    if not nome or nome in _estado.jogos:
        return
    _estado.jogos.add(nome)
    info = _jogos.CATALOGO[nome]
    exibir(caixa(f"🔓 <b>Jogo desbloqueado:</b> {info['icone']} {escapar(info['titulo'])}!<br>"
                 f"Para jogar, escreva: <code>jogar(\"{nome}\")</code>",
                 cor="#e65100", fundo="#fff3e0"))


def _aura_do_jogo(nome: str, pontos) -> None:
    ganhos = _estado.premiar_jogo(nome, pontos)
    if ganhos:
        exibir(_linha_aura(ganhos))


# ---------------------------------------------------------------- funções do aluno

def iniciar(nivel: int = 1, notebook: str = "", codigo: str = "") -> None:
    """Prepara o vestiário: progresso, dados e boas-vindas.

    `codigo` vem do campo "código secreto" da primeira célula (pode ficar vazio)."""
    _sessao.update(nivel=nivel, notebook=notebook, inicio=time.monotonic(), intervalo=False)
    do_drive = progresso.ler_drive()
    if do_drive and do_drive.total > _estado.total:
        _carregar_estado(do_drive)
    codigo = str(codigo or "").strip()
    do_codigo = progresso.ler_codigo(codigo) if codigo else None
    if do_codigo:
        _carregar_estado(do_codigo)
    _jogos.registrar_callback(_aura_do_jogo)
    _som.registrar_callback()
    erros.instalar(notebook)
    info = _info_notebook(notebook)
    if info and info.get("usa_dados"):
        carregar_jogadores()
    titulo = f"{info['icone']} {escapar(info['titulo'])}" if info else "Futebol com Python"
    reacoes.mostrar("boas_vindas", extra=f'<div style="margin-top:4px">{titulo}</div>')
    if do_codigo:
        exibir(caixa("🔐 Código secreto aceito! Sua aura e seus jogos voltaram.", tamanho="1em"))
    elif codigo:
        exibir(caixa("Hmm, esse código secreto não bateu. Confira letra por letra (o 0 é zero, "
                     "o O é letra), corrija no campo da primeira célula e aperte o play de novo. "
                     "Enquanto isso, dá para jogar normalmente.", cor="#37474f", fundo="#eceff1",
                     tamanho="1em"))
    exibir(_barra_aura())
    exibir(caixa("Som: toque no ícone para desligar ou ligar. " + _som.botao(),
                 cor="#37474f", fundo="#eceff1", tamanho="1em"))
    if _estado.total == 0 and not codigo:
        exibir(caixa("Já jogou antes? Cole seu código secreto no campo 🔐 da primeira célula "
                     "e aperte o play de novo.", cor="#37474f", fundo="#eceff1", tamanho="1em"))


def checar(resposta, missao: str = "m1") -> bool:
    """Confere a resposta de uma missão e dá a recompensa."""
    _talvez_intervalo()
    m = missoes.buscar(_sessao["notebook"], missao)
    if m is None:
        exibir(caixa(f"Não achei a missão <b>{escapar(missao)}</b> neste notebook. "
                     "Confira se escreveu igual ao enunciado.", cor="#37474f", fundo="#eceff1"))
        return False
    if _vazio(resposta):
        exibir(caixa("Ainda tem um <b>___</b> esperando você! Troque pelo que a missão pede "
                     "e aperte o play de novo.", cor="#37474f", fundo="#eceff1"))
        return False
    if _eh_tabela(resposta):
        exibir(caixa("Isso é uma tabela inteira. Aqui eu preciso de uma resposta só "
                     "(um número ou um nome).", cor="#37474f", fundo="#eceff1"))
        return False

    chave = f"{_sessao['notebook']}:{missao}"
    _checar_67(resposta, chave)
    if missoes.comparar(resposta, m):
        resultado = _estado.acertou(chave, dificil=m.dificil)
        rara = m.dificil or resultado.marco_sequencia == 5
        reacoes.mostrar("yamal_danca" if rara else ("sigma" if resultado.sequencia % 2 else "aura"))
        if resultado.pontos:
            extra = " (de primeira! +50 de bônus)" if resultado.primeira else ""
            exibir(_linha_aura(resultado.pontos) + (caixa(extra, tamanho="1em") if extra else ""))
        elif resultado.repetida:
            exibir(caixa("Certo de novo! Essa missão já deu aura antes. ✅", tamanho="1em"))
        if resultado.marco_sequencia:
            if not rara:
                reacoes.mostrar("sequencia")
            exibir(caixa(f"🔥 Sequência de {resultado.marco_sequencia}!", cor="#bf360c",
                         fundo="#fbe9e7", tamanho="1.3em"))
        if resultado.subiu_para:
            exibir(caixa(f"🏆 Você subiu de nível: <b>{resultado.subiu_para}</b>!",
                         cor="#f57f17", fundo="#fffde7", tamanho="1.3em"))
            exibir(_barra_aura())
        _mostrar_empate_e_escrita(resposta, m)
        _desbloquear(m.desbloqueia)
        _checar_67(_estado.total, f"total:{_estado.total}")
        return True

    erros = _estado.errou(chave)
    if erros >= 3:
        _estado.desistiu(chave)
        exibir(caixa(f"Vamos ver juntos? A resposta é <b>{escapar(missoes.texto_resposta(m))}</b>.<br>"
                     f"🧠 {escapar(m.explicacao)}<br>Agora você já sabe. Bora para a próxima missão!",
                     cor="#0d47a1", fundo="#e3f2fd"))
        return False
    perto = _numero_perto(resposta, m)
    reacoes.mostrar("quase" if perto else "beta")
    exibir(caixa(f"💡 <b>Dica:</b> {escapar(m.dica)}<br>🔁 Tente de novo!",
                 cor="#0d47a1", fundo="#e3f2fd"))
    if erros == 1:  # o treino rápido aparece só no primeiro erro de cada missão
        exibir(_jogos.html_jogo("treino_rapido", modo="treino", dica=m.dica))
    return False


def _mostrar_empate_e_escrita(resposta, m: missoes.Missao) -> None:
    certo = missoes.escrita_certa(resposta, m)
    if certo:
        exibir(caixa(f"✍️ Valeu! O nome escrito certinho é <b>{escapar(certo)}</b>.", tamanho="1em"))
    nomes = missoes.empatados(m)
    if len(nomes) > 1:
        lista = " e ".join(escapar(n) for n in nomes) if len(nomes) == 2 else ", ".join(escapar(n) for n in nomes)
        exibir(caixa(f"🤝 <b>Empate!</b> {lista} têm o mesmo número. Todos valem!", tamanho="1em"))


def _numero_perto(resposta, m: missoes.Missao) -> bool:
    esperado = m.esperado()
    try:
        r, e = float(resposta), float(esperado)
    except (TypeError, ValueError):
        return False
    return e != 0 and abs(r - e) / abs(e) <= 0.10


def chute(palpite, real) -> float | None:
    """Jogo do palpite: mostra o erro em porcentagem. Na trave = até 10% de diferença."""
    _talvez_intervalo()
    if _vazio(palpite):
        exibir(caixa("Escreva o seu palpite no lugar do <b>___</b> primeiro!", cor="#37474f",
                     fundo="#eceff1"))
        return None
    try:
        p, r = float(palpite), float(real)
    except (TypeError, ValueError):
        exibir(caixa("O palpite precisa ser um número.", cor="#37474f", fundo="#eceff1"))
        return None
    chave = f"{_sessao['notebook']}:chute:{r}"
    _checar_67(p, chave)
    _checar_67(r, chave + ":real")
    erro = abs(p - r) / abs(r) * 100 if r else (0.0 if p == r else 100.0)
    exibir(caixa(f"🎯 Seu palpite: <b>{numero(p)}</b> · Valor real: <b>{numero(r)}</b><br>"
                 f"Você errou por <b>{numero(round(erro, 1))}%</b>.", cor="#1a237e", fundo="#e8eaf6"))
    if erro <= 10:
        reacoes.mostrar("quase" if erro > 0 else "sigma")
        ganhos = _estado.premiar_chute(chave)
        if ganhos:
            exibir(_linha_aura(ganhos))
    else:
        exibir(caixa("Bom chute! Olheiro de verdade também chuta e depois confere. "
                     "Quanto mais você treina, mais perto chega. 👀", tamanho="1em"))
    return round(erro, 1)


def som(ligado: bool = True) -> None:
    """Liga (som()) ou desliga (som(False)) o som das reações e dos jogos."""
    _som.ligar(ligado)
    if ligado:
        exibir(caixa("🔊 Som ligado! Para desligar, toque no ícone ou escreva <code>som(False)</code>.",
                     tamanho="1em") + _som.html_som("sigma"))
    else:
        exibir(caixa("🔇 Som desligado. Para ligar de novo, escreva <code>som()</code>.",
                     cor="#37474f", fundo="#eceff1", tamanho="1em"))


def comemorar(tipo: str = "aura") -> None:
    """Comemoração manual (por exemplo, quando os pais querem celebrar)."""
    reacoes.mostrar(tipo)


def dica(missao: str = "m1") -> None:
    m = missoes.buscar(_sessao["notebook"], missao)
    texto = m.dica if m else "Essa missão não existe neste notebook."
    exibir(caixa(f"💡 <b>Dica:</b> {escapar(texto)}", cor="#0d47a1", fundo="#e3f2fd"))


def curiosidades(tabela, n: int = 3) -> None:
    """Mostra até n curiosidades (com link da Wikipédia) dos jogadores da tabela."""
    _curiosidades.mostrar(tabela, n=n)


def vestiario() -> None:
    """Mostra seus jogos desbloqueados e o seu nível de aura."""
    exibir(_barra_aura())
    cartoes = []
    for nome, info in _jogos.CATALOGO.items():
        if info["tipo"] != "campeao":
            continue
        if nome in _estado.jogos:
            cartoes.append(f'<div style="{_ESTILO_CARTAO};background:#e8f5e9;color:#1b5e20">'
                           f'<div style="font-size:2.4em">{info["icone"]}</div>'
                           f'<b>{escapar(info["titulo"])}</b><br>'
                           f'<code>jogar("{nome}")</code></div>')
        else:
            cartoes.append(f'<div style="{_ESTILO_CARTAO};background:#eceff1;color:#607d8b">'
                           f'<div style="font-size:2.4em">🔒</div><b>???</b></div>')
    exibir(f'<div style="display:flex;flex-wrap:wrap;gap:10px;font-family:system-ui,sans-serif">'
           f'{"".join(cartoes)}</div>')


_ESTILO_CARTAO = ("width:140px;min-height:120px;border-radius:12px;padding:10px;"
                  "text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.2)")


def jogar(nome: str) -> None:
    """Abre um jogo do vestiário."""
    info = _jogos.CATALOGO.get(nome)
    if info is None or info["tipo"] != "campeao":
        exibir(caixa(f"Não conheço o jogo <b>{escapar(nome)}</b>. Veja seus jogos com "
                     "<code>vestiario()</code>.", cor="#37474f", fundo="#eceff1"))
        return
    if nome not in _estado.jogos:
        exibir(caixa("🔒 Esse jogo ainda está trancado. Continue as missões para liberar!",
                     cor="#37474f", fundo="#eceff1"))
        return
    exibir(_jogos.html_jogo(nome))


def terminar() -> None:
    """Fim do notebook: libera o jogo do vestiário e mostra o resumo."""
    info = _info_notebook(_sessao["notebook"])
    if info:
        _estado.notebooks.add(info["numero"])
    reacoes.mostrar("fim_notebook")
    exibir(caixa("🏁 <b>Notebook completo!</b> Você treinou como profissional.",
                 cor="#1b5e20", fundo="#e8f5e9", tamanho="1.3em"))
    if info and info.get("jogo"):
        _desbloquear(info["jogo"])
    exibir(_barra_aura())
    salvar_progresso()


def salvar_progresso(drive: bool = False) -> str:
    """Mostra o seu código secreto. Com drive=True, também salva no Google Drive."""
    codigo = progresso.gerar_codigo(_estado)
    exibir(caixa(f"🔐 Seu código secreto: <b style=\"font-size:1.3em;letter-spacing:1px\">"
                 f"{codigo}</b><br>Anote num papel! No próximo notebook, cole o código no campo "
                 f"🔐 <b>código secreto</b> da primeira célula.", cor="#4a148c", fundo="#f3e5f5"))
    if drive:
        ok = progresso.salvar_drive(_estado)
        exibir(caixa("☁️ Salvo no Google Drive!" if ok else
                     "Não deu para salvar no Drive, mas o código acima sempre funciona.",
                     tamanho="1em"))
    return codigo


def _carregar_estado(novo: _aura.EstadoAura) -> None:
    _estado.total = max(_estado.total, novo.total)
    _estado.jogos |= novo.jogos
    _estado.notebooks |= novo.notebooks


def carregar_progresso(codigo: str) -> bool:
    """Recupera a aura, os jogos e os notebooks a partir do código secreto."""
    novo = progresso.ler_codigo(codigo)
    if novo is None:
        exibir(caixa("Hmm, esse código não bateu. Confira letra por letra (o 0 é zero, "
                     "o O é letra) e tente de novo.", cor="#37474f", fundo="#eceff1"))
        return False
    _carregar_estado(novo)
    reacoes.mostrar("aura", extra='<div>Progresso recuperado!</div>')
    exibir(_barra_aura())
    return True
