from pyomo.environ import *

# Inicializar el modelo
Model = ConcreteModel()

# Data de entrada
numAviones = 3
numRecursos = 5
p = RangeSet(1, numAviones)
t = RangeSet(1, numRecursos)

aviones = {
    1: (30, 25),   # (Capacidad en toneladas, Capacidad en volumen m^3)
    2: (40, 30),
    3: (50, 35)
}

recursos = {
    1: (50, 15, 8),    # Alimentos basicos (Valor, Peso en toneladas, Volumen en m^3)
    2: (100, 5, 2),    # Medicinas
    3: (120, 20, 10),  # Equipos Médicos
    4: (60, 18, 12),   # Agua Potable
    5: (40, 10, 6)     # Mantas
}

# Variable de decisión
Model.x = Var(p, t, domain=Binary)

# Función objetivo
Model.obj = Objective(expr=sum(Model.x[i, j] * recursos[j][0] for i in p for j in t), sense=maximize)

# Restricciones

def regla1(Model, j):
    return sum(Model.x[i, j] for i in p) == 1

Model.res1 = Constraint(t, rule=regla1)


def regla2(Model, i):
    return sum(Model.x[i, j] * recursos[j][1] for j in t) <= aviones[i][0]

Model.res2 = Constraint(p, rule=regla2)

def regla3(Model, i):
    return sum(Model.x[i, j] * recursos[j][2] for j in t) <= aviones[i][1]

Model.res3 = Constraint(p, rule=regla3)


def regla4(Model):
    return Model.x[1, 2] == 0

Model.res4 = Constraint(rule=regla4)


def regla5(Model, i):
    return Model.x[i, 3] + Model.x[i, 4] <= 1

Model.res5 = Constraint(p, rule=regla5)


SolverFactory('glpk').solve(Model)


Model.display()
