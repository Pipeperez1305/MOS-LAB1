from pyomo.environ import *
import matplotlib.pyplot as plt

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

#Data for plotting
resources = list(recursos.keys())
values = [recursos[r][0] for r in resources]

#Selection status for each plane
selected = [[Model.x[i,j]() for j in resources] for i in p]

# Creating a stacked bar chart
colors = ['red', 'blue', 'green']

# Plot the resource allocation
for i, j in enumerate(p):
    plt.bar(resources, [v * sel for v, sel in zip(values, selected[i])], color=colors[i], label=f'Plane {j}', bottom=[sum(selected[k][r]*values[r] for k in range(i)) for r in range(len(resources))])

plt.xlabel("Recursos")
plt.ylabel("Valor")
plt.title("Asignación de recursos a aviones")

# labels 
rec=["Alimentos Básicos", "Medicinas", "Equipos Médicos", "Agua Potable", "Mantas"]
plt.xticks(range(1,len(resources)+1),rec)
plt.legend()

plt.show()