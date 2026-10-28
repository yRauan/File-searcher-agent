import sys
from pathlib import Path

# Permite importar o aima-python a partir da pasta vendor/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vendor" / "aima-python"))

from aima.logic import PropKB, FolKB, expr, fol_fc_ask


class KnowledgeBase:
    """Base de conhecimento com dois modos:
    - 'prop': lógica proposicional (ask retorna True/False)
    - 'fol':  lógica de primeira ordem (ask retorna lista de substituições)
    """

    def __init__(self, modo="fol"):
        if modo not in ("prop", "fol"):
            raise ValueError("modo deve ser 'prop' ou 'fol'")
        self.modo = modo
        self.kb = PropKB() if modo == "prop" else FolKB()

    def tell(self, sentence):
        """Insere um fato ou regra na KB.
        Exemplo: kb.tell("Pasta_Planos & Ext_PDF ==> PrioridadeAlta")
        """
        self.kb.tell(expr(sentence))

    def ask(self, query):
        """Consulta a KB.
        - prop: retorna True ou False
        - fol:  retorna lista de substituições (dicts); lista vazia = nada provado
        """
        q = expr(query)
        if self.modo == "prop":
            return bool(self.kb.ask_if_true(q))
        return list(fol_fc_ask(self.kb, q))