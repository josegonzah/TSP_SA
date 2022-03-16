from unicodedata import name
from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt

n = 21
nodos = [i for i in range(n)]
arcos = [(i,j) for i in nodos for j in nodos if i!=j]
np.random.seed(0)
X = np.random.random(n)*100
Y = np.random.random(n)*100

distance = {(i,j): np.hypot(X[i]-X[j], Y[i]-Y[j]) for i in nodos for j in nodos if i!=j}
plt.figure(figsize=(12, 5))
plt.scatter(X,Y, color='blue')

for n in range(len(X)):
    plt.annotate(str(n), xy=(X[n], Y[n]), xytext=(X[n]+0.5, Y[n]+1), color='red')

    plt.xlabel("Distancia X")
    plt.ylabel("Distancia Y")
    plt.title("Distancia Travel Salesman Problem")

    # plt.show()

model = Model('TSP')

x = model.addVars(arcos, vtype = GRB.BINARY, name='x')
u = model.addVars(arcos, vtype = GRB.CONTINUOUS, name='u')

model.setObjective(quicksum(distance[n]*x[n] for n in arcos), GRB.MINIMIZE)

model.addConstrs(quicksum(x[i,j] for j in nodos if j!=i)==1 for i in nodos)
model.addConstrs(quicksum(x[i,j] for i in nodos if j!=i)==1 for j in nodos)

model.addConstrs((x[i, j]==1) >> (u[i]+1==u[j]) for i,j in arcos if j!=0)
model.optimize()