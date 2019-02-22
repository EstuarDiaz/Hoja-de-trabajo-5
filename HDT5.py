# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:33:48 2019

@author: Estuardo Diaz, Juan Rodolfo Alonzo
"""
import simpy
import random

interval = 10
numero_de_procesos = 10
tiempo_simulacion = 50

def proceso(env,nombre,tiempo_creacion,instrucciones):
    yield env.timeout(tiempo_creacion)
    horaLlegada = env.now
    print ('%s llega a las %f tiene %d instrucciones' % (nombre,horaLlegada,instrucciones))

env = simpy.Environment() #ambiente de simulación
RAM = simpy.Container(env, init = 100, capacity = 100) # Cointainer para RAM
CPU = simpy.Resource(env, capacity=1) # Resource para CPU
random.seed(10) # fijar el inicio de random
for i in range(numero_de_procesos):
    env.process(proceso(env,'Proceso %d'%i,random.expovariate(1.0/interval),random.randint(1,10)))

env.run(until = tiempo_simulacion)  #correr la simulación hasta el tiempo especificado

# Usar pyChart para graficar los timpos