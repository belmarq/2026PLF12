import re

from Atomo import Atomo
from Clausula import Clausula
from Formula import Formula


def infijo2postfijo(infijo):
    postfijo = []
    pila = []
    for ch in infijo:
        p=getPrioridad(ch)
        if p == -1:
            pila.append(ch)
        elif p == -2:
    #Extraer el elemento del tope de la pila e introducir a postfijo,
    # hasta encontrar (  pero no introducir el paréntesis a postfijo.
            while (len(pila) > 0):
                tope = pila.pop()
                if (tope != "("):
                    postfijo.append(tope)
                else:
                    break
        elif p > 0:
    # la pila esta vacı́a or ch tiene
    # más alta prioridad que el elemento del tope de la pila
            if len(pila) == 0 or p > getPrioridad(pila[-1]):
                pila.append(ch)
    # Extraer el elemento del tope de la pila e introducir a postfijo.
    # Y repetir la comparación con el nuevo tope
            else:
                while len(pila)>0 and p < getPrioridad(pila[-1]):
                    tope = pila.pop()
                    postfijo.append(tope)
                pila.append(ch)
        else:
            postfijo.append(ch)
    while len(pila) > 0:
        postfijo.append(pila.pop())
    return postfijo

def getPrioridad(a):
    if (a == "|"):
        return 1
    if (a == "&"):
        return 2
    if (a == ">"):
        return 3
    if (a == "="):
        return 4
    if (a == "-"):
        return 5
    if (a == "("):
        return -1
    if (a == ")"):
        return -2
    else:
        return 0

def evaluar(postfijo):
    pila = []
    for ch in postfijo:
        p = getPrioridad(ch)
        if p == 0:  # operando
            a = Atomo(ch)
            c = Clausula()
            f = Formula()
            c = c.orAtomo(a)
            c = f.andClausula(c)
            pila.append(c)
        elif p == 1: # or
            b = pila.pop()
            a = pila.pop()
            c = a.orFormula(b)
            pila.append(c)
        elif p == 2:  # and
            b = pila.pop()
            a = pila.pop()
            c = a.andFormula(b)
            pila.append(c)
        elif p == 3:  # entonces
            b = pila.pop()
            a = pila.pop()
            a = a.negar()
            c = a.orFormula(b)
            pila.append(c)
        elif p == 4:  # si y solo si
            b = pila.pop()
            a = pila.pop()
            an = a.negar()
            bn = b.negar()
            c = a.orFormula(bn)
            d = b.orFormula(an)
            c = c.andFormula(d)
            pila.append(c)
        elif p == 5:  # not
            a = pila.pop()
            c = a.negar()
            pila.append(c)
    return pila.pop()

def davisPutnam(formula, certificado={}, atomo=None, bifurcacion=0):
    f = formula.__copy__()
    if bifurcacion > 0:
        certificado[atomo.nombre] = not atomo.negado
        print(f"\nFormula: {f}")
        f = f.reducirClausulas([atomo])
        print(f"B{bifurcacion}: {atomo}")
        print(f"Formula: {f}\n")
    while (True):
        cv = f.hayClausulaVacia()
        if cv:
            return (False, f, certificado)
        else:
            fv = f.esFormulaVacia()
            if fv:
                return (True, f, certificado)
        cu = f.clausulaUnitaria()
        if len(cu) > 0:
            print(f"\nFormula: {f}")
            for a in cu:
                certificado[a.nombre]=not a.negado
                print(f"CU: {a}")
            f = f.reducirClausulas(cu)
            print(f"Formula: {f}\n")
        lp = f.literalPura()
        if len(lp) > 0:
            print(f"\nFormula: {f}")
            for a in lp:
                certificado[a.nombre]=not a.negado
                print(f"LP: {a}")
            f = f.reducirClausulas(lp)
            print(f"Formula: {f}\n")
        if len(cu) == 0 and len(lp) == 0:
            atomo=f.getAtomo()
            resolucion, formula, certificado = davisPutnam(f,
                                                           certificado=certificado,
                                                           bifurcacion=1,
                                                           atomo=atomo)
            if resolucion:
                return (resolucion, formula, certificado)
            atomo=atomo.negar()
            return davisPutnam(f,
                               certificado=certificado,
                               bifurcacion=2,
                               atomo=atomo)




archivo = open("datos/formula1.txt")
lineas = archivo.readlines()
for linea in lineas:
    linea = linea.rstrip()
    print(f'\n{"Formula:":9} {linea}')
    infijo = re.findall("(\\w+|\\||\\&|\\>|\\-|\\(|\\)|\\=)", linea)
    print(f'{"Infijo:":9} {infijo}')
    postfijo = infijo2postfijo(infijo)
    print(f'{"Postfijo:":9} {postfijo}')
    fnc = evaluar(postfijo)
    print(f'{"FNC:":9} {fnc}')
    ''' 
    print(f'FNC: {fnc}')
    fnc=fnc.literalPura()
    print("LP:")
    for a in fnc:
        print(a)
    '''

    


resolucion, formula, certificado = davisPutnam(fnc.borraTautologias())
print(f'resolucion: {resolucion}')
if resolucion:
    print(f'formula: {formula}')
    print(f'Certificado: ')
    for key, value in certificado.items():
        print(f'{key}: {value}')



'''
c1 = Clausula()
c1 = c1.orAtomo(Atomo('a'))
c1 = c1.orAtomo(Atomo('b'))
#c1 = c1.negar()

c2 = Clausula()
c2 = c2.orAtomo(Atomo('r'))
c2 = c2.orAtomo(Atomo('s').negar())
c2 = c2.orAtomo(Atomo('t'))

f1 = Formula()

f1 = f1.andClausula(c1)
f1 = f1.andClausula(c2)
#c = c.orAtomo(Atomo("B"))
p1 = c1.negar()
p2 = c2.negar()
p3 = p1.orFormula(p2)
print(f'paso1: {p1}')
print(f'paso2: {p2}')
print(f'paso3: {p3}')
print(f'formula negada: {f1.negar()}')


'''

