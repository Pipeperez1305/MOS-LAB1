
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numTrabajadores=3
numTrabajos=5
p=RangeSet(1, numTrabajadores)
t=RangeSet(1, numTrabajos)


trabajadores = {
    1: 8,
    2: 10,
    3: 6
}

trabajos = {
    1: (50, 4),   # Máxima
    2: (60, 5),   # Media alta
    3: (40, 3),  # Alta
    4: (70, 6),   # Media baja
    5: (30, 2)
}

# Variable de decisión
Model.x = Var(p,t, domain=Binary)


# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i, j] * trabajos[j][0] for i in p for j in t), sense = maximize)

# Restricciones

def regla1 (Model, j):
    return sum(Model.x[i,j] for i in p) == 1

Model.res1 = Constraint(t, rule=regla1)

def regla2 (Model, i):
    return sum(Model.x[i,j] * trabajos[j][1] for j in t) <= trabajadores[i]

Model.res2 = Constraint(p, rule=regla2)


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()



    

