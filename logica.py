class Atomo:
    def __init__(self, name, negado=False):
        self.name = name
        self.negado = negado
    def negar(self):
        a = Atomo(self.name, not self.negado)
        return a    
    def __str__(self):
        if self.negado:
            return f"~{self.name}"
        return self.name

class Clausula:
    def __init__(self):
        self.atomos = []
    def addAtomo(self, atomo):
        self.atomos.append(Atomo(atomo.name, atomo.negado))
    def __str__(self):
        texto = "("
        texto += " | ".join(str(atomo) for atomo in self.atomos)
        texto += ")"
        return texto

class Formula:
    def __init__(self):
        self.clausulas = []
    def addClausula(self, clausula):
        self.clausulas.append(clausula)
    def __str__(self):
        texto = "["
        texto += " & ".join(str(clausula) for clausula in self.clausulas)
        texto += "]"
        return texto

a1 = Atomo("A",True)
a2 = Atomo("B",True)
a3 = Atomo("C",False)
a4 = Atomo("D",False)
c1 = Clausula()
print(c1)