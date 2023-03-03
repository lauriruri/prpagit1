
'''
Implementar un merge concurrente:
- Tenemos NPROD procesos que producen números no negativos de forma
creciente. Cuando un proceso acaba de producir, produce un -1
- Hay un proceso merge que debe tomar los números y almacenarlos de
forma creciente en una única lista (o array). El proceso debe esperar a que
los productores tengan listo un elemento e introducir el menor de
ellos.
- Se debe crear listas de semáforos. Cada productor solo maneja los
sus semáforos para sus datos. El proceso merge debe manejar todos los
semáforos.
- OPCIONAL: mente se puede hacer un búffer de tamaño fijo de forma que
los productores ponen valores en el búffer.

PRIMERA VERSIÓN:
para poder elegir el mínimo tienen que haber producido un valor todos los consumidores

luego el consumidor va cogiendo los numeros y ordenandolos de menor a mayor

el proceso acaba cuando algún productor esta  -1, ponemos un numero aleatorio de vueltas.

fijamos n numero de vueltas y cada proceso crea 

idea es que la lista de C sea una lista ordenada y con todos los numeros positivos.

SEGUNDA VERSIÓN:
cada productor tiene una lista! en vez de un valor. 
Se controla con semáforos. Si en un proceso encuentra el -1 se acaba.

-----------------------------------------------------------
los elementos son tipo value, objeto compartido por Proceso y Consumidor

¿como paso los values al consumidor? con una lista
¿como genero los procesos? con una lista

values =[Value('i',-2)
    for _ in range(NPROD)]

P[i]
Process(_,argr(val=values[i]))

cada proceso tendrá que tener un semáforo

un semaforo por cada proceso para indicar que el consumidor a consumido (un semaforo por cada productor)
un semaforo para decir que el consumidor ha consumido

'''

from multiprocessing import Process, Manager
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Semaphore
#from multiprocessing import Manager
from random import random,randint

##randint(1,30) me genera un numero entre 1 y 30 -> 14
##randint(14,30*2) etc.
COTA = 100
N=5 #numero de procesos
#sem = Semaphore(0) #numero es numero de procesos que pueden entrar
values=[]
procesos=[]
lleno=[]
vacio=[]
#resultado = [] #usar algo compartido mejor
#resultado = Array('i',range(N*100))

def llamar_proceso(proc_id):
    value = 0
    #LIMITE = randint(2,10)
    LIMITE=10
    for i in range(0,LIMITE):
        print("process",proc_id,"wait")
        vacio[proc_id].acquire()
        value = value + randint(0, COTA)
        values[proc_id].value = value
        print("process",proc_id,"produced value",values[proc_id].value)
        lleno[proc_id].release()
        print("process",proc_id,"release")

    vacio[proc_id].acquire()
    values[proc_id].value = -1
    lleno[proc_id].release()


def minimum_pos(l):
    aux = l[0]
    pos = 0
    contador = 0
    longitud = len(l)
    for i in range(0,len(l)):
        if (aux == -1 and contador < longitud-1):
            aux = l[i+1]
            pos = i+1
        if (l[i] == -1):
            contador = contador + 1
        if (l[i]<aux and l[i]!=-1):
            aux = l[i]
            pos = i
    return (aux, pos, contador)

################################3
def llamar_consumidor(lleno,values,resultado):

    local_values=[]
    for i in range(0,N):       
        print("consumer waiting for", i)
        lleno[i].acquire()
        local_values.append(values[i].value)
        print ("este es el valor: ", values[i].value)
        print("y así queda mi local_values ,", local_values)
    print("initial values are:", local_values)
    
    #j=0
    while True:
        (minimo, posicion, contador)=minimum_pos(local_values)
        if (contador == len(local_values)):
            break
        resultado.append(minimo)
        #j=j+1
        print("consumer releasing", posicion)
        vacio[posicion].release()
        print("consumer waiting", posicion)
        lleno[posicion].acquire()
        local_values[posicion]=values[posicion].value
        print("values are:", local_values)

    #print(resultado, "EN EL CONSUMIDOR")
########################################

def main():
    manager = Manager()
    resultado = manager.list()
#inicializo los procesos
    for i in range(0,N):
        values.append(Value('i',-2)) #inicializo los valores a -2
        vacio.append(Semaphore(1))
        lleno.append(Semaphore(0))
        procesos.append(Process(target=llamar_proceso, args = (i,)))
    for proceso in procesos:
        proceso.start()

#llamada al consumidor
    consumidor = Process(target=llamar_consumidor, args=(lleno,values,resultado,))
    consumidor.start()
    consumidor.join()
    for proceso in procesos:
        proceso.join()

    print("\n")
    print(resultado, "en el main")
    print('Ha terminado')



'''
producer(i)
loop
    empty(i).wait()
    producer
    non_empty(i).signal()

consumer //necesito que haya al menos un valor distinto de -1
//si un proceso esta en -1 ya no produce mas!!!!
for i
    non_empty(i).wait()
loop
    i <- minimo
    almacenamos
    empty(i).signal() //despertamos al que ha producido al mínimo
    non.empty(i).wait() 
'''

if __name__ == "__main__" :
    main()
    print("fin")
