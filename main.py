import numpy 
import matplotlib.pyplot as plt
import time

##Definimos una clase coordenadas que tiene 2 metdos para calcular las distancias 
##entre los puntos. Uno recibe todos los puntos, otro recibe solo un par de puntos
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def getDistance(a, b):
        return numpy.sqrt(numpy.abs(a.x - b.x)+numpy.abs(a.y - b.y))

    @staticmethod
    def getTotalDistance(coords):
        dist = 0
        for first, second in zip(coords[:-1],coords[1:]):
            dist += Coordinate.getDistance(first, second)
        dist += Coordinate.getDistance(coords[0], coords[-1])
        return dist

if __name__ == '__main__':
    # Llenar las coordenadas de manera aleatoria e inicializacion de los arreglos que contienen las coordenadas
    # graficas
    coordenadas =[]
    numeroPuntos = 75
    tempGraph = []
    costGraph = []
    for i in range(numeroPuntos):
        coordenadas.append(Coordinate(numpy.random.uniform(), numpy.random.uniform()))
    
    #Plot puntos iniciales, une los puntos en orden generado
    figure = plt.figure(figsize = (10, 5))
    ax1 = figure.add_subplot(221)
    ax2 = figure.add_subplot(222)
    ax3 = figure.add_subplot(223)
    ax4 = figure.add_subplot(224)
    for first, second in zip(coordenadas[:-1], coordenadas[1:]):
        ax1.plot([first.x, second.x], [first.y, second.y])
    ax1.plot([coordenadas[0].x, coordenadas[-1].x], [coordenadas[0].y, coordenadas[-1].y], 'b')
    for c in coordenadas:
        ax1.plot(c.x, c.y, 'ro')

    #Iniciamos el Simulated annealing
    costo0 = Coordinate.getTotalDistance(coordenadas)

    startTime = time.time()
    T = 15
    factor = 0.99
    T_init = T
    for i in range(1000):

        T = T*factor
        tempGraph.append(T)
        for j in range(100):
            #Intercambio de 2 coordenadas aleatorias para obtener un vecino que posibilite la solucion
            r1, r2 = numpy.random.randint(0, len(coordenadas), size=2)

            temp = coordenadas[r1]
            coordenadas[r1] = coordenadas[r2]
            coordenadas[r2] = temp

            #Obtener el nuevo costo
            costo1 = Coordinate.getTotalDistance(coordenadas)
            costGraph.append(costo1)
            if costo1 < costo0:
                costo0 = costo1
            else:
                x = numpy.random.uniform()
                if x < numpy.exp((costo0-costo1)/T):
                    costo0 = costo1
                else:
                    temp = coordenadas[r1]
                    coordenadas[r1] = coordenadas[r2]
                    coordenadas[r2] = temp

    print("Costo funcion objetivo", costo1)
    print("Tiempo de ejecucion", time.time()-startTime)
    #Ploteamos el resultado y las graficas necesarias
    iteration = range(len(tempGraph))
    for first, second in zip(coordenadas[:-1], coordenadas[1:]):
        ax2.plot([first.x, second.x], [first.y, second.y])
    ax2.plot([coordenadas[0].x, coordenadas[-1].x], [coordenadas[0].y, coordenadas[-1].y], 'b')
    for c in coordenadas:
        ax2.plot(c.x, c.y, 'ro')
    ax3.plot(iteration, tempGraph)
    ax4.plot(range(len(costGraph)), costGraph)
    plt.show()




