import re
import time
from pathlib import Path

PASTA_ALVO = "Fontes PAA"
EXT_ALVO = "pdf"
ANO_ALVO = 2026


def _limpa(texto):
    return re.sub(r"\W", "_", texto).capitalize()


def varrer(raiz):
    itens = []
    for caminho in sorted(Path(raiz).rglob("*")):
        st = caminho.stat()
        itens.append({
            "id": len(itens),
            "caminho": caminho,
            "eh_pasta": caminho.is_dir(),
            "ext": caminho.suffix.lower().lstrip("."),
            "ano": time.localtime(st.st_mtime).tm_year,
            "pai": caminho.parent.name,
        })
    return itens


def popular_kb(kb, itens):
    for it in itens:
        if it["eh_pasta"]:
            continue
        i = it["id"]
        kb.tell(f"Pasta_{_limpa(it['pai'])}_f{i}")
        kb.tell(f"Ext_{_limpa(it['ext'])}_f{i}")
        kb.tell(f"Mod_{it['ano']}_f{i}")
        kb.tell(
            f"Pasta_{_limpa(PASTA_ALVO)}_f{i} & Ext_{_limpa(EXT_ALVO)}_f{i} "
            f"& Mod_{ANO_ALVO}_f{i} ==> PrioridadeAlta_f{i}"
        )
    return {it["id"]: it["caminho"] for it in itens if not it["eh_pasta"]}
