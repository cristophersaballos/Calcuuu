from math import *
import statistics as st
import sympy as sp

# 1. OPERACIONES BÁSICAS
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero.")
    return a / b

def potencia(base, exp):
    return base ** exp

def raiz(n, indice=2):
    if n < 0 and indice % 2 == 0:
        raise ValueError("No se puede calcular raíz par de un número negativo en R.")
    return n ** (1 / indice)

PI, E = pi, e

def logb(x, b=10):
    return log(x, b)

def ln(x):
    return log(x)

# 2. ESTADÍSTICA Y GEOMETRÍA
def media(*d):
    return st.mean(d)

def mediana(*d):
    return st.median(d)

def moda(*d):
    return st.mode(d)

def rec2pol(x, y):
    return sqrt(x**2 + y**2), degrees(atan2(y, x))

def pol2rec(r, deg):
    return r * cos(radians(deg)), r * sin(radians(deg))

# 3. CÁLCULO
x, y, z, t = sp.symbols('x y z t')
f = sp.Function('f')

def diff(e, v='x', o=1):
    return sp.diff(sp.sympify(e), sp.symbols(v), o)

def diff_imp(eq, y_v='y', x_v='x'):
    xv, yv = sp.symbols(x_v), sp.symbols(y_v)
    lhs, rhs = eq.split('=') if '=' in eq else (eq, '0')
    return sp.idiff(sp.sympify(f'({lhs}) - ({rhs})'), yv, xv)

def tangente(e, x0):
    expr = sp.sympify(e)
    f_x0 = expr.subs(x, x0)
    m = sp.diff(expr, x).subs(x, x0)
    y_tan = m * (x - x0) + f_x0
    print(f'Punto: ({x0}, {f_x0}) | m: {m} | Recta: y = {y_tan}')
    return y_tan

def graficar(e, x_min=-10, x_max=10):
    sp.plot(sp.sympify(e), (x, x_min, x_max))

def graficar_tangente(e, x0, x_min=-10, x_max=10):
    expr = sp.sympify(e)
    y_tan = sp.diff(expr, x).subs(x, x0) * (x - x0) + expr.subs(x, x0)
    sp.plot(expr, y_tan, (x, x_min, x_max))

def integ(e, *lim):
    expr = sp.sympify(e)
    if not lim:
        return sp.integrate(expr, x)
    l = lim[0]
    return (
        sp.integrate(expr, (sp.symbols(l[0]), l[1], l[2]))
        if isinstance(l[0], str)
        else sp.integrate(expr, (x, l[0], l[1]))
    )

def itriple(e, lx, ly, lz):
    return sp.integrate(
        sp.sympify(e), (z, lz[0], lz[1]), (y, ly[0], ly[1]), (x, lx[0], lx[1])
    )

def masa_3d(densidad, lx, ly, lz):
    return itriple(densidad, lx, ly, lz)

def centroide_3d(densidad, lx, ly, lz):
    m = masa_3d(densidad, lx, ly, lz)
    m_yz = itriple(f"x * ({densidad})", lx, ly, lz)
    m_xz = itriple(f"y * ({densidad})", lx, ly, lz)
    m_xy = itriple(f"z * ({densidad})", lx, ly, lz)
    return m_yz / m, m_xz / m, m_xy / m

# ECUACIONES DIFERENCIALES

def _obtener_contexto_sympy():
    return {
        'x': x, 'y': f(x), 'z': z, 't': t, 'f': f,
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
        'sinh': sp.sinh, 'cosh': sp.cosh
    }

def edo(eq):
    p = eq.replace("y''", 'f(x).diff(x, 2)').replace("y'", 'f(x).diff(x)')
    lhs, rhs = p.split('=') if '=' in p else (p, '0')
    ctx = _obtener_contexto_sympy()
    return sp.dsolve(sp.sympify(f'({lhs}) - ({rhs})', locals=ctx), f(x))

def edo_pvi(eq, x0, y0):
    p = eq.replace("y''", 'f(x).diff(x, 2)').replace("y'", 'f(x).diff(x)')
    lhs, rhs = p.split('=') if '=' in p else (p, '0')
    ctx = _obtener_contexto_sympy()
    return sp.dsolve(
        sp.sympify(f'({lhs}) - ({rhs})', locals=ctx), f(x), ics={f(x0): y0}
    )

# 4. MENÚ
def menu():
    while True:
        print("\nCALCULADORA")
        print("1. Operaciones básicas (+, -, *, /)")
        print("2. Exponentes y radicales")
        print("3. Estadística (Media, Mediana, Moda)")
        print("4. Derivadas e Integrales")
        print("5. Ecuaciones Diferenciales")
        print("0. Salir")
        
        opcion = input("\nOpción: ")

        if opcion == "1":
            print("\nOperaciones Básicas")
            a = float(input("Primer número: "))
            b = float(input("Segundo número: "))
            print(f"Suma: {sumar(a, b)}")
            print(f"Resta: {restar(a, b)}")
            print(f"Multiplicación: {multiplicar(a, b)}")
            try:
                print(f"División: {dividir(a, b)}")
            except ValueError as err:
                print(f"Error: {err}")

        elif opcion == "2":
            print("\nExponentes y Radicales")
            sub = input("1. Potencia | 2. Raíz: ")
            if sub == "1":
                base = float(input("Base: "))
                exp = float(input("Exponente: "))
                print(f"Resultado: {potencia(base, exp)}")
            elif sub == "2":
                n = float(input("Número: "))
                ind = float(input("Índice (por defecto 2): ") or 2)
                try:
                    print(f"Resultado: {raiz(n, ind)}")
                except ValueError as err:
                    print(f"Error: {err}")

        elif opcion == "3":
            print("\nEstadística")
            datos = list(map(float, input("Ingresa los datos separados por espacio: ").split()))
            if datos:
                print(f"Media: {media(*datos)}")
                print(f"Mediana: {mediana(*datos)}")
                print(f"Moda: {moda(*datos)}")

        elif opcion == "4":
            print("\nCálculo")
            expr = input("Expresión (ej: x**2 + sin(x)): ")
            sub = input("1. Derivar | 2. Integrar: ")
            if sub == "1":
                print(f"Derivada: {diff(expr)}")
            elif sub == "2":
                print(f"Integral: {integ(expr)}")

        elif opcion == "5":
            print("\nEcuaciones Diferenciales")
            eq = input("Ecuación (ej: y' + y = x): ")
            print(f"Solución: {edo(eq)}")

        elif opcion == "0":
            print("Chao!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()