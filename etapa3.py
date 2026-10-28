import logging
import sys
import time
from pathlib import Path

from pypdf import PdfReader

import src.busca_conteudo as bc
import src.busca_logica as bl
from src.kb import KnowledgeBase
from src.mapeamento_fol import popular_kb_fol

logging.getLogger("pypdf").setLevel(logging.ERROR)

RAIZ = "tests/docencia/fontes"
palavra = (sys.argv[1] if len(sys.argv) > 1 else "algoritmo").lower()
MAX_PAGINAS = int(sys.argv[2]) if len(sys.argv) > 2 else 20

_original = bc.extrair_texto


def extrair_limitado(arquivo):
    """Mesmo limite de paginas para todos os agentes (comparacao justa)."""
    caminho = Path(arquivo)
    if caminho.suffix.lower() == ".pdf":
        try:
            leitor = PdfReader(str(caminho))
            return "\n".join((p.extract_text() or "") for p in leitor.pages[:MAX_PAGINAS])
        except Exception:
            return ""
    return _original(arquivo)


bc.extrair_texto = extrair_limitado
bl.extrair_texto = extrair_limitado


def astar_tradicional(raiz, palavra):
    r = bc.buscar_conteudo(raiz, palavra, "ASTAR")
    lidos = r["arquivos_lidos"]
    achou = r["caminho"] is not None
    return {
        "pastas_abertas": r["pastas_abertas"],
        "arquivos_lidos": lidos,
        "falsos_positivos": lidos - 1 if achou else lidos,
        "podadas": 0, "asks": 0,
        "encontrado": r["caminho"],
        "tempo_ms": r["tempo_ms"],
        "memoria_kb": r["memoria_kb"],
    }


def rodar_logico(raiz, palavra):
    t0 = time.perf_counter()
    kb = KnowledgeBase("fol")
    caminhos = popular_kb_fol(kb, raiz)
    const_de = {p: c for c, p in caminhos.items()}
    bl.adicionar_regras_poda(kb, const_de, raiz)
    montagem = (time.perf_counter() - t0) * 1000
    s = bl.agente_logico(kb, raiz, palavra, const_de)
    s["montagem_ms"] = montagem
    return s


def linha(nome, s, ms, pico):
    print(f"{nome:<24}{s['pastas_abertas']:>8}{s['arquivos_lidos']:>8}"
          f"{s['falsos_positivos']:>11}{ms:>12.0f}{pico:>11.0f}", flush=True)
    print(f"   encontrado: {s['encontrado']}", flush=True)
    if s["asks"]:
        print(f"   pastas podadas: {s['podadas']} | ASKs: {s['asks']} | "
              f"montagem da KB: {s['montagem_ms']:.0f} ms", flush=True)


print(f"Palavra-chave: '{palavra}' | limite: {MAX_PAGINAS} paginas por PDF\n", flush=True)
print(f"{'Algoritmo':<24}{'Pastas':>8}{'Lidos':>8}{'FalsosPos':>11}{'Tempo(ms)':>12}{'Pico(KB)':>11}", flush=True)

s, ms, pico = bl.medir(rodar_logico, RAIZ, palavra)
linha("Agente Logico (KB)", s, ms, pico)

s, ms, pico = bl.medir(bl.bfs, RAIZ, palavra)
linha("Busca Cega (BFS)", s, ms, pico)

s = astar_tradicional(RAIZ, palavra)
linha("A* Tradicional (nome)", s, s["tempo_ms"], s["memoria_kb"])
