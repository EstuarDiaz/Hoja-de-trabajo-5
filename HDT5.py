# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:33:48 2019

@author: Estuardo Diaz, Juan Rodolfo Alonzo
"""
import simpy
import random

interval = 10
numero_de_procesos = 5
tiempo_simulacion = 50
random_seed = 17
capacidad_RAM = 100
cantidad_CPU = 1
numero_instrucciones = 3
max_size_proceso = 10
max_size_ram = 10

random.seed(random_seed) # fijar el inicio de random
def proceso(env,nombre,tiempo_creacion,memoria_requerida,instrucciones):
    yield env.timeout(tiempo_creacion)
    print ('%s creado a las %f, tiene %d instrucciones' % (nombre,env.now,instrucciones))
    # NEW
    with RAM.get(memoria_requerida) as turnoRAM:
        yield turnoRAM
        print('%d unidades de RAM disponibles' % (RAM.level))
        print ('%s ocupa %d de memoria a las %f' % (nombre,memoria_requerida,env.now))
        
    while instrucciones > 0:
    # READY
        with CPU.request() as turnoCPU:
            print('%s esperando turno de CPU a las %f' % (nombre,env.now))
            yield turnoCPU
            
    # RUNNING
            instrucciones -= min(numero_instrucciones,instrucciones)
            yield env.timeout(1) # el proceso ejecuta numero_instrucciones por unidad de tiempo
            print('%s tiene %d instrucciones faltantes' % (nombre,instrucciones))
            CPU.release(turnoCPU)
        
    # WAITING    
        if instrucciones > 0:
            if random.randint(1,2) == 1:
                print('%s esperando I/O a las %f' % (nombre,env.now))
                yield env.timeout(1) # simluar interrupcion de I/O

    # TERMINATED
    RAM.put(memoria_requerida)
    print('%s terminado a las %f' % (nombre,env.now))

env = simpy.Environment() #ambiente de simulación
RAM = simpy.Container(env, init = capacidad_RAM, capacity = capacidad_RAM) # Cointainer para RAM
CPU = simpy.Resource(env, capacity = cantidad_CPU) # Resource para CPU
for i in range(numero_de_procesos):
    env.process(proceso(env,'Proceso %d'%i,random.expovariate(1.0/interval),
                            random.randint(1,max_size_ram),random.randint(1,max_size_proceso)))

env.run(until = tiempo_simulacion)  #correr la simulación hasta el tiempo especificado

# Usar pyChart para graficar los timpos