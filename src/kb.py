import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vendor" / "aima-python"))

from aima.logic import PropDefiniteKB, pl_fc_entails, FolKB, expr, fol_bc_ask, subst, variables


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
        # FOL: backward chaining; devolve lista de {variavel: valor}
        vistos, resultado = set(), []
        for theta in fol_bc_ask(self.kb, q):
            binding = {v: subst(theta, v) for v in variables(q)}
            chave = tuple(sorted((str(k), str(val)) for k, val in binding.items()))
            if chave not in vistos:
                vistos.add(chave)
                resultado.append(binding)
        return resultado
