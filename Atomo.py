class Atomo:
    def __init__(self, nombre):
        self.nombre = nombre.upper()
        self.negado = False

    def negar(self):
        a = Atomo(self.nombre)
        a.negado = not self.negado
        return a

    def __copy__(self):
        a = Atomo(self.nombre)
        a.negado = self.negado
        return a

    def __eq__(self, otro):
        if isinstance(otro, Atomo):
            return self.nombre == otro.nombre and self.negado == otro.negado
        return False

    def comparar(self, atomo):
        return self.nombre == atomo.nombre and self.negado == atomo.negado

    def __str__(self):
        cadena = ""
        if self.negado:
            cadena +="-"
        cadena += self.nombre
        return cadena
