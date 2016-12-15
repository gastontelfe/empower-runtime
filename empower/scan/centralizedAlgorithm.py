import copy
import pdb

class CentralizedAlgorithm(object):
	
    def __init__(self, graph, neighborsConstraint):
    	self.channels = [1,6,11]
    	self.graph = graph
    	self.neighborsConstraint = neighborsConstraint

    def invoke(self):
    	t = Tupla(self.graph, self.neighborsConstraint, len(self.graph), 0)
    	sol = Tupla(self.graph, self.neighborsConstraint, len(self.graph), 1000000.0)

    	return self.calculate(t, 0, sol)

    def calculate(self, t, i, sol):
    	if self.esMejor(t, sol):
    		if self.solucion(t, i):
    			self.copiar(sol, t)
    		else:
    			for c in range(len(self.channels)):
    				aux = t.inteferenceLevel
    				self.calculate(self.asignarCanal(t, i, self.channels[c]), i + 1, sol)
    				t.inteferenceLevel = aux
    	return sol.channelAssignments

    def copiar(self, sol, t):
    	sol.copiar(t)

    def solucion(self, t, i):
    	return i == len(self.graph)

    def esMejor(self, t, sol):
    	return t.inteferenceLevel < sol.inteferenceLevel

    def asignarCanal(self, tupla, i, channel):
    	tupla.asignar(i, channel)
    	return tupla

class Tupla:
    def __init__(self, graph, neighborsConstraint, length, d):
        self.channelAssignments = [0 for i in range(length)]
        self.inteferenceLevel = d
        self.graph = graph
        self.neighborsConstraint = neighborsConstraint
        self.filename = 'algorithm.txt'

    def asignar(self, i, channel):
        self.channelAssignments[i] = channel
        self.calcularInterferenceLevel(i)

    def calcularInterferenceLevel(self, i):
        for j in range(i):
            # if self.channelAssignments[j] == self.channelAssignments[i]:
            #pdb.set_trace()
            for x in range(len(self.graph[i])):
                n = self.graph[i][x]
                if n.getId() == j:
                    self.inteferenceLevel += self.calcularFactor(self.channelAssignments[j], self.channelAssignments[i]) * n.getQuality()
                    break

        externalNeighbors = self.neighborsConstraint[i]
        if externalNeighbors != None:
            for x in range(len(externalNeighbors)):
                n = externalNeighbors[x]
                # if n.getChannel() == self.channelAssignments[i]:
                self.inteferenceLevel += self.calcularFactor(n.getChannel(), self.channelAssignments[i]) * n.getQuality()

    def calcularFactor(self, channel1, channel2):
        dif = abs(channel1 - channel2)
        if dif >= 5:
            return 0

        return 1 - dif * 0.2


    def copiar(self, t):
        with open(self.filename, 'a') as file_d:
            file_d.write('     Mejor por ahora:\n')
            

            print("     Mejor por ahora: ")
            self.channelAssignments = copy.copy(t.channelAssignments)
            for i in range(len(self.channelAssignments)):
                print("     Nodo: " + str(i) + " canal " + str(self.channelAssignments[i]))
                file_d.write("     Nodo: " + str(i) + " canal " + str(self.channelAssignments[i]) + "\n")
                self.inteferenceLevel = t.inteferenceLevel

            print("                " + str(t.inteferenceLevel))
            file_d.write("                " + str(t.inteferenceLevel) + "\n")



if __name__ == "__main__":
    c = CentralizedAlgorithm("ass", "ccc")
    t = Tupla(15, 12)
    print(t.channelAssignments)
