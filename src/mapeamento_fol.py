import re
import unicodedata
from pathlib import Path

from src.mapeamento import varrer

# EDITE: tema e professor por pasta de primeiro nivel
TEMAS = {"Fontes PAA": "Algoritmos"}
PROFESSORES = {"Fontes PAA": "ProfPAA"}


def _const(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    limpo = re.sub(r"\W", "", sem_acento.title())
    return limpo if limpo else "X"


def popular_kb_fol(kb, raiz):
    raiz = Path(raiz)
    itens = varrer(raiz)

    mapa = {raiz: "PRaiz"}
    for it in itens:
        prefixo = "P" if it["eh_pasta"] else "F"
        mapa[it["caminho"]] = f"{prefixo}{it['id']}"

    kb.tell("Pasta(PRaiz)")
    for it in itens:
        c = mapa[it["caminho"]]
        kb.tell(f"Pasta({c})" if it["eh_pasta"] else f"Arquivo({c})")

        # Contem(ancestral, item) para todos os ancestrais (fecho transitivo feito aqui)
        for anc in it["caminho"].parents:
            if anc in mapa:
                kb.tell(f"Contem({mapa[anc]}, {c})")

        if it["eh_pasta"] and it["caminho"].parent == raiz:
            nome = it["caminho"].name
            tema = TEMAS.get(nome, _const(nome))
            prof = PROFESSORES.get(nome, "ProfDesconhecido")
            kb.tell(f"TemaPasta({c}, {tema})")
            kb.tell(f"AutorPasta({c}, {prof})")

    # regras universais
    kb.tell("Contem(p, y) & TemaPasta(p, t) ==> Tema(y, t)")
    kb.tell("Contem(p, y) & AutorPasta(p, a) ==> Autor(y, a)")
    kb.tell("Arquivo(y) & Tema(y, Algoritmos) & Autor(y, ProfPAA) ==> RevisarParaProva(y)")

    return {c: str(p) for p, c in mapa.items()}
