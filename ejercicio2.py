
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numTrabajos=5
p=RangeSet(1, numTrabajos)

# PARA EL PROBLEMA 1 PONEMOS UN DICCIONARIO CON EL NUMERO DE TAREA Y UNA TUPLA CON EL PUNTAJE Y LA PRIORIDAD
# 7 MAXIMO
# 6 ALTO
# 5 MEDIO ALTO
# 4 MEDIO
# 3 MEDIO BAJO
# 2 BAJO 
# 1 MINIMO

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
Model.x = Var(p, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i]*valor[i][1] for i in p), sense=maximize)

# Restricciones
Model.res1 = Constraint(expr = sum(Model.x[i]*valor[i][0] for i in p) <=52)

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()



    


