class Formula:
    def __init__(self):
        self.clausulas = []

    def andClausula(self, clausula):
        f = Formula()
        for c in self.clausulas:
            f.clausulas.append(c.__copy__())
        f.clausulas.append(clausula.__copy__())
        return f

    def andFormula(self, formula):
        f = Formula()
        for c in self.clausulas:
            f.clausulas.append(c.__copy__())
        for c in formula.clausulas:
            f.clausulas.append(c.__copy__())
        return f

    def orFormula(self, formula):
        f = Formula()
        if len(self.clausulas)==0:
            for c in formula.clausulas:
                f.clausulas.append(c.__copy__())
            return f
        for c in self.clausulas:
            for c2 in formula.clausulas:
                f.clausulas.append(c.orClausula(c2))
        return f

    def negar(self):
        f = Formula()
        for c in self.clausulas:
            g = c.negar()
            f = f.orFormula(g)
        return f


    def borraTautologias(self):
        f = Formula()
        for c in self.clausulas:
            if not c.esTautologia():
                f.clausulas.append(c.__copy__())
        return f

    def hayClausulaVacia(self):
        for clausula in self.clausulas:
            if len(clausula.atomos)==0:
                return True
        return False

    def esFormulaVacia(self):
        if len(self.clausulas)==0:
            return True
        return False

    def clausulaUnitaria(self):
        atomos = []
        for clausula in self.clausulas:
            if len(clausula.atomos)==1:
                atomos.append(clausula.atomos[0].__copy__())
        return atomos

    def reducirClausulas(self, atomos):
        f = Formula()
        clausulas = self.clausulas
        for atomo in atomos:
            for i in range(len(clausulas)):
                if clausulas[i] is not None:
                    clausulas[i] = clausulas[i].clausulaUnitaria(atomo)
        for clausula in clausulas:
            if clausula is not None:
                f.clausulas.append(clausula)
        return f

    def literalPura(self):
        lista = {}
        atomos = []
        for clausula in self.clausulas:
            for atomo in clausula.atomos:
                if atomo.nombre not in lista:
                    lista[atomo.nombre] = atomo
                elif lista[atomo.nombre] == None:
                    pass
                elif not atomo.comparar(lista[atomo.nombre]):
                    lista[atomo.nombre] = None
        for atomo in lista.values():
            if atomo is not None:
                atomos.append(atomo)
        return atomos

    def getAtomo(self):
        return self.clausulas[0].atomos[0]

    def __copy__(self):
        f = Formula()
        for clausula in self.clausulas:
            f.clausulas.append(clausula.__copy__())
        return f

    def __str__(self):
        cadena = "["
        for indice, clausula in enumerate(self.clausulas):
            cadena += "\n" + clausula.__str__()
            #if indice != len(self.clausulas) - 1:
            #    cadena += " & "
        cadena += "\n]"
        return cadena
