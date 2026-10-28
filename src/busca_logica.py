import difflib
import heapq
import os
import time
import tracemalloc
from collections import deque
from pathlib import Path

from src.busca_conteudo import extrair_texto
from src.mapeamento_fol import TEMAS, _const


def pdf_contem(caminho, palavra):
    """Le o arquivo inteiro (extrair_texto) e procura a palavra."""
    return palavra in extrair_texto(caminho).casefold()


def _listar(pasta):
    """Abre a pasta: retorna (subpastas, arquivos) ordenados."""
    try:
        itens = sorted(Path(pasta).iterdir())
    except PermissionError:
        return [], []
    return [i for i in itens if i.is_dir()], [i for i in itens if i.is_file()]


def _novo():
    return {"pastas_abertas": 0, "arquivos_lidos": 0, "falsos_positivos": 0,
            "podadas": 0, "asks": 0, "encontrado": None}


def _ler(s, arq, palavra):
    s["arquivos_lidos"] += 1
    if pdf_contem(arq, palavra):
        s["encontrado"] = str(arq)
        return True
    s["falsos_positivos"] += 1
    return False


def bfs(raiz, palavra):
    s = _novo()
    fila = deque([Path(raiz)])
    while fila:
        pasta = fila.popleft()
        s["pastas_abertas"] += 1
        subs, arqs = _listar(pasta)
        for a in arqs:
            if a.suffix.lower() == ".pdf" and _ler(s, a, palavra):
                return s
        fila.extend(subs)
    return s


def adicionar_regras_poda(kb, const_de, raiz, tema_alvo="Algoritmos"):
    """Regras e fatos que permitem a KB provar Invalida(pasta)."""
    kb.tell("BackupAntigo(p) ==> Invalida(p)")
    kb.tell("SemAcesso(p) ==> Invalida(p)")
    kb.tell("TemaPasta(p, t) & TemaIrrelevante(t) ==> Invalida(p)")
    for caminho, c in const_de.items():
        p = Path(caminho)
        if not p.is_dir():
            continue
        if "backup" in p.name.lower():
            kb.tell(f"BackupAntigo({c})")
        if not os.access(p, os.R_OK):
            kb.tell(f"SemAcesso({c})")
    for pasta in Path(raiz).iterdir():
        if pasta.is_dir():
            tema = TEMAS.get(pasta.name, _const(pasta.name))
            if tema != tema_alvo:
                kb.tell(f"TemaIrrelevante({tema})")


def agente_logico(kb, raiz, palavra, const_de, tema="Algoritmos", prof="ProfPAA"):
    s = _novo()

    def ask(q):
        s["asks"] += 1
        return bool(kb.ask(q))

    def valida(c):
        return not ask(f"Invalida({c})")

    def h(c):
        """Proposicoes que ainda faltam na KB para satisfazer a regra do alvo."""
        falta = 0
        if not (ask(f"TemaPasta({c}, {tema})") or ask(f"Tema({c}, {tema})")):
            falta += 1
        if not (ask(f"AutorPasta({c}, {prof})") or ask(f"Autor({c}, {prof})")):
            falta += 1
        return falta

    cont = 0
    heap = [(h(const_de[str(raiz)]), 0, Path(raiz), 0)]
    while heap:
        _, _, pasta, g = heapq.heappop(heap)
        c = const_de[str(pasta)]
        if not valida(c):
            s["podadas"] += 1
            continue
        s["pastas_abertas"] += 1
        subs, arqs = _listar(pasta)
        for a in arqs:
            if (a.suffix.lower() == ".pdf"
                    and ask(f"RevisarParaProva({const_de[str(a)]})")
                    and _ler(s, a, palavra)):
                return s
        for sub in subs:
            cont += 1
            heapq.heappush(heap, (g + 1 + h(const_de[str(sub)]), cont, sub, g + 1))
    return s


def medir(funcao, *args):
    tracemalloc.start()
    t0 = time.perf_counter()
    resultado = funcao(*args)
    ms = (time.perf_counter() - t0) * 1000
    pico = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    return resultado, ms, pico
