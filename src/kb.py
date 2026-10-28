import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vendor" / "aima-python"))

from aima.logic import PropDefiniteKB, pl_fc_entails, FolKB, expr, fol_fc_ask


class KnowledgeBase:
    def __init__(self, modo="fol"):
        if modo not in ("prop", "fol"):
            raise ValueError("modo deve ser 'prop' ou 'fol'")
        self.modo = modo
        self.kb = PropDefiniteKB() if modo == "prop" else FolKB()

    def tell(self, sentence):
        self.kb.tell(expr(sentence))

    def ask(self, query):
        q = expr(query)
        if self.modo == "prop":
            return bool(pl_fc_entails(self.kb, q))
        return list(fol_fc_ask(self.kb, q))
