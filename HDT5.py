# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:33:48 2019

@author: Estuardo Diaz, Juan Rodolfo Alonzo
"""
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

def graficar(name,x,y):    
    fig, ax = plt.subplots()
    ax.set_title(name)
    plt.bar(x = x, height = y, width = 20)
    plt.show()
    
interval = 10
numero_de_procesos = 5
tiempo_simulacion = 50
random_seed = 17
capacidad_RAM = 100
cantidad_CPU = 1
numero_instrucciones = 3
max_size_proceso = 10
max_size_ram = 10
tiempos = []
tiempoPorProcesos = []
desviacionPorProcesos = []
listadoNumeroProcesos = [25,50,100,150,200]
mostrarLog = False # SI SE PONE COMO TRUE, PERMITE VER EL DETALLE DE TODAS
                    # LAS ACCIONES REALIZADAS POR LA SIMULACION

for numero_instrucciones in (3,6):
    for cantidad_CPU in (1,2):
        for capacidad_RAM in (100,200):
            for interval in (10,5,1):
                tiempos = []
                tiempoPorProcesos = []
                desviacionPorProcesos = []
                for numero_de_procesos in listadoNumeroProcesos:
                    random.seed(random_seed) # fijar el inicio de random
                    def proceso(env,nombre,tiempo_creacion,memoria_requerida,instrucciones):
                        yield env.timeout(tiempo_creacion)
                        if mostrarLog:
                            print ('%s creado a las %f, tiene %d instrucciones' % (nombre,env.now,instrucciones))
                        tiempoin = env.now
                        # NEW
                        with RAM.get(memoria_requerida) as turnoRAM:
                            yield turnoRAM
                            if mostrarLog:
                                print('%d unidades de RAM disponibles' % (RAM.level))
                                print ('%s ocupa %d de memoria a las %f' % (nombre,memoria_requerida,env.now))
                            
                        while instrucciones > 0:
                        # READY
                            with CPU.request() as turnoCPU:
                                if mostrarLog:
                                    print('%s esperando turno de CPU a las %f' % (nombre,env.now))
                                yield turnoCPU
                                
                        # RUNNING
                                instrucciones -= min(numero_instrucciones,instrucciones)
                                yield env.timeout(1) # el proceso ejecuta numero_instrucciones por unidad de tiempo
                                if mostrarLog:
                                    print('%s tiene %d instrucciones faltantes' % (nombre,instrucciones))
                                CPU.release(turnoCPU)
                            
                        # WAITING    
                            if instrucciones > 0:
                                if random.randint(1,2) == 1:
                                    if mostrarLog:
                                        print('%s esperando I/O a las %f' % (nombre,env.now))
                                    yield env.timeout(1) # simluar interrupcion de I/O
                    
                        # TERMINATED
                        RAM.put(memoria_requerida)
                        if mostrarLog:
                            print('%s terminado a las %f' % (nombre,env.now))
                        tiempofin = env.now
                        tiempos.append(tiempofin - tiempoin)
                        if mostrarLog:
                            print('%s tardo %f' % (nombre,tiempofin - tiempoin))
                        
                    env = simpy.Environment() #ambiente de simulación
                    RAM = simpy.Container(env, init = capacidad_RAM, capacity = capacidad_RAM) # Cointainer para RAM
                    CPU = simpy.Resource(env, capacity = cantidad_CPU) # Resource para CPU
                    for i in range(numero_de_procesos):
                        env.process(proceso(env,'Proceso %d'%i,random.expovariate(1.0/interval),
                                                random.randint(1,max_size_ram),random.randint(1,max_size_proceso)))
                    
                    env.run(until = tiempo_simulacion)  #correr la simulación hasta el tiempo especificado
                    tiempoPorProcesos.append(np.average(tiempos))
                    desviacionPorProcesos.append(np.std(tiempos))
                    if mostrarLog:
                       print("Desviacion estandar para %d proceso: %d" % (numero_de_procesos,np.std(tiempos)))
                    if mostrarLog:
                        print("Promedio para %d proceso: %d" % (numero_de_procesos,np.average(tiempos)))
                
                graficar("Promedio de tiempos por numero de procesos (intervalo de llegada: %d , capacidad: %d , procesadores %d , instrucciones: %d)" % 
                              (interval,capacidad_RAM,cantidad_CPU,numero_instrucciones),
                            listadoNumeroProcesos,tiempoPorProcesos)
                graficar("Desviacion estandar de tiempos por numero de procesos (intervalo de llegada: %d, capacidad: %d , procesadores %d , instrucciones: %d)" % 
                          (interval,capacidad_RAM,cantidad_CPU,numero_instrucciones)
                    ,listadoNumeroProcesos,desviacionPorProcesos)