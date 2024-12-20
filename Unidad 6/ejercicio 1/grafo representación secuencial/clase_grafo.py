import numpy as np
from clase_cola_secuencial import cola

class grafo_secuencial:
    __matriz_adyacencia:np.array
    __vertices:list
    __tiempo:int#para recorrido en profundidad. No es parte del objeto de dato
    
    def __init__(self, vertices, aristas):#Recibe una lista con los vertices y otro con las aristas 
        self.__vertices=vertices
        self.__matriz_adyacencia=np.zeros((len(vertices),len(vertices)), dtype=int)#arreglo bidimencional tamaño V x V
        self.__tiempo=0
        
        for i in aristas:#por cada arista
            #coloca 1 en el lugar ij y ji que implique 2 vertices adyacentes
            self.__matriz_adyacencia[i[0]][i[1]]=1
            self.__matriz_adyacencia[i[1]][i[0]]=1
            
        print(self.__matriz_adyacencia)


    def buscar_indice(self, vertice):
        i=0
        band=False
        while band!=True and i<=len(self.__vertices):
            if self.__vertices[i]==vertice:
                band=True
            i+=1
        
        if band==True:
            return i-1
        else:
            return band
        
        
    #recorrido en amplitud
    def REA(self, v_origen):
        vertices_visitados=[]#para marcar los vertices visitados
        #asigna infinito a todos los vertices
        for v in range(len(self.__vertices)):
            vertices_visitados.append(float("inf"))#float("inf") = infinito
            
        indice_origen=self.buscar_indice(v_origen)#busco el indice que tiene el vertice en el arreglo self.__vertices
        vertices_visitados[indice_origen]=0#lo marco como vertice de origen
        cola_secuencial=cola(len(self.__vertices))#creo cola con tamaño para guardar todos los vertices en caso de requerirlo
        cola_secuencial.insertar(indice_origen)#inserto el vertice origen en la cola
        
        while cola_secuencial.vacia()!=True:
            v=cola_secuencial.suprimir()
            i=0#para tener el indice del vertice que sea adyacente a "v"
            for u in self.__matriz_adyacencia[v]:#recorro de la matriz unicamente la fila de "v"
                if u==1:#el vertice con indice (i) es adyacente a "v"
                    if vertices_visitados[i]==float("inf"):#adyacente "i" tiene "infinito" en arreglo visitados
                        vertices_visitados[i]=vertices_visitados[v]+1
                        cola_secuencial.insertar(i)#se le asigna lo que tenga "v"+1 en arreglo visitados
                i+=1
                
        print(vertices_visitados)#muestra longitud de caminos mas cortos desde vertice origen hasta los demas
        
    
    def REP_Visita(self, v, t_descubierto, t_finalizacion):
        self.__tiempo += 1
        t_descubierto[v] = self.__tiempo  # marco el vértice como descubierto con el tiempo en el que se encontro
        print(f"Visitando nodo {v}, tiempo de descubrimiento: {self.__tiempo}")

        #recorro los adyacentes de "v"
        for u in range(len(self.__vertices)):
            if self.__matriz_adyacencia[v][u]==1 and t_descubierto[u] == 0:
                self.REP_Visita(u, t_descubierto, t_finalizacion)
        
        self.__tiempo += 1
        t_finalizacion[v] = self.__tiempo  #marco el tiempo de finalización del vertice "v"
        print(f"Finalizando nodo {v}, tiempo de finalización: {self.__tiempo}")

    def REP(self):
        # inicializo tiempos de descubrimiento y finalización
        t_descubierto= [0] * len(self.__vertices)
        t_finalizacion = [0] * len(self.__vertices)

        #para cada vértice no sido visitado, ejecutar REP_visita
        for v in range(len(self.__vertices)):
            if t_descubierto[v] == 0:
                self.REP_Visita(v, t_descubierto, t_finalizacion)
        
        print("Tiempos de descubrimiento:", t_descubierto)
        print("Tiempos de finalización:", t_finalizacion)
        self.__tiempo=0#reinicio el tiempo para futuros REP
        
        
    def adyacentes(self, vertice):
        indice=self.buscar_indice(vertice)#obtengo el indice asociado al vertice
        i=0
        for u in self.__matriz_adyacencia[indice]:#solo veo la fila de "vertice" en la matriz
            if u==1:#si hay un adyacente lo imprimo
                print(self.__vertices[i])
            i+=1
        
        
    #reconstruir el camino a partir del arreglo de predecesores
    def reconstruir_camino(self, camino, origen, destino):
        resultado=[]
        actual=destino
        
        #retrocedo desde el destino hasta el origen
        while actual!=-1:
            resultado.insert(0, self.__vertices[actual])#inserto al inicio del arreglo el vertice actual
            actual=camino[actual]
        
        if resultado[0] != self.__vertices[origen]:#si no se llega al origen, no hay un camino válido
            return print(f"No hay camino de {self.__vertices[origen]} a {self.__vertices[destino]}")
        
        return print(resultado)
        
        
    def camino(self, origen, destino):
        camino=[-1]*len(self.__vertices)#arreglo de predecesores para luego reconstruir el camino desde el destino al origen
        vertices_visitados=[float("inf")]*len(self.__vertices)
      
        indice_origen=self.buscar_indice(origen)
        indice_destino=self.buscar_indice(destino)
  
        cola_secuencial=cola(len(self.__vertices))
        cola_secuencial.insertar(indice_origen)
        vertices_visitados[indice_origen]=0#marco como visitado
        
        while cola_secuencial.vacia()!=True:
            v=cola_secuencial.suprimir()
 
            if v==indice_destino:#se llego al vertice destino
                return self.reconstruir_camino(camino, indice_origen, indice_destino)
            else:
                #recorro los adyacentes a "v"
                for i in range(len(self.__vertices)):
                    if self.__matriz_adyacencia[v][i]==1 and vertices_visitados[i]==float("inf"):
                        vertices_visitados[i]=0
                        camino[i]=v#agrego "v" como predecesor del siguiente vertice
                        cola_secuencial.insertar(i)
                        
        #sale del while sin encontrar el destino
        print(f"No hay camino de {origen} a {destino}")
        
        
    def conexo(self):
        vertices_visitados=[float("inf")]*len(self.__vertices)
        
        cola_secuencial=cola(len(self.__vertices))
        cola_secuencial.insertar(0)#recorro el grafo desde el primer vertice
        vertices_visitados[0]=0
        
        while cola_secuencial.vacia()!=True:
            v=cola_secuencial.suprimir()
            
            for i in range(len(self.__vertices)):
                if self.__matriz_adyacencia[v][i]==1 and vertices_visitados[i]==float("inf"):
                    vertices_visitados[i]=vertices_visitados[v]+1
                    cola_secuencial.insertar(i)
        
        #recorro el arreglo de visitados
        if float("inf") in vertices_visitados:
            return print("El grafo no es conexo")
        else:
            return print("El grafo es conexo")
        
        
    def aciclico(self):
        print("El grafo tiene ciclos pues es un grafo no dirigido")