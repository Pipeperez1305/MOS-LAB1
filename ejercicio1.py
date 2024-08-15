
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numTareas=11

p=RangeSet(1, numTareas)

# PARA EL PROBLEMA 1 PONEMOS UN DICCIONARIO CON EL NUMERO DE TAREA Y UNA TUPLA CON EL PUNTAJE Y LA PRIORIDAD
# 7 MAXIMO
# 6 ALTO
# 5 MEDIO ALTO
# 4 MEDIO
# 3 MEDIO BAJO
# 2 BAJO 
# 1 MINIMO



valor = {
    1: (5, 7),   # Máxima
    2: (3, 5),   # Media alta
    3: (13, 6),  # Alta
    4: (1, 3),   # Media baja
    5: (21, 1),  # Mínima
    6: (2, 4),   # Media
    7: (2, 6),   # Alta
    8: (5, 6),   # Alta
    9: (8, 2),   # Baja
    10: (13, 7), # Máxima
    11: (21, 6), # Alta
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



    


