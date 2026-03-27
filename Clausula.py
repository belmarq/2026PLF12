from Formula import Formula


class Clausula:
    def __init__(self):
        self.atomos = []

    def estaAtomo(self, atomo):
        for a in self.atomos:
            if a.comparar(atomo):
                return True
        return False

    def orAtomo(self, atomo):
        c = Clausula()
        for a in self.atomos:
            c.atomos.append(a.__copy__())
        if c.estaAtomo(atomo):
            return c
        c.atomos.append(atomo.__copy__())
        return c

    def orClausula(self, clausula):
        c = Clausula()
        for atomo in self.atomos:
            c.atomos.append(atomo.__copy__())
        for atomo in clausula.atomos:
            if not c.estaAtomo(atomo):
                c.atomos.append(atomo.__copy__())
        return c

    def andAtomo(self, atomo):
        f = Formula()
        f = f.andClausula(self.__copy__())
        c = Clausula()
        c = c.orAtomo(atomo.__copy__())
        f = f.andClausula(c)
        return f

    def andClausula(self, clausula):
        f = Formula()
        for c in self.clausulas:
            f.clausulas.append(c.__copy__())
        f.clausulas.append(clausula.__copy__())
        return f

    def negar(self):
        f = Formula()
        for atomo in self.atomos:
            c = Clausula()
            a = atomo.__copy__()
            a = a.negar()
            c.atomos.append(a)
            f = f.andClausula(c)
        return f

    def __copy__(self):
        c = Clausula()
        for atomo in self.atomos:
            c.atomos.append(atomo.__copy__())
        return c

    def esTautologia(self):
        atomos = {}
        for atomo in self.atomos:
            if atomo.nombre in atomos:
                if atomo.negado != atomos[atomo.nombre]:
                    return True
            else:
                atomos[atomo.nombre]=atomo.negado
        return False

    def clausulaUnitaria(self, atomo):
        c = Clausula()
        for a in self.atomos:
            if a.comparar(atomo):
                return None
            if a.nombre != atomo.nombre:
                c.atomos.append(a.__copy__())
        return c


    def __str__(self):
        cadena = "("
        for indice, atomo in enumerate(self.atomos):
            cadena += atomo.__str__()
            if indice != len(self.atomos) - 1:
                cadena +=  " | "
        cadena += ")"
        return cadena
