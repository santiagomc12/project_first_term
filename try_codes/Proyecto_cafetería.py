global cont
tiempoEspera = []


def __init__(self, env):
    self.env = env
    self.action = env.process(self.proceso())


def llegadas(): return np.random.exponential(1 / 1)  # Random para llegadas de clientes (1 cliente por minuto)


def aleatorio(caje): return np.random.exponential(1 / caje)  # Random para cajero (Caje = número de cajeros que atienden la cafetería)


def procesosEnCajero(): return aleatorio(
    caje)  # Utilizado para procesos realizados en caja (Pedido, Pago, Preparación, Entrega)


def consumo(mesas): return np.random.exponential(
    1 / mesas)  # Para consumo de producto se tiene en cuenta el número de mesas disponibles


def proceso(env, caf):
    cont = 0
    while True:
        yield env.timeout(llegadas())
        cont = cont + 1
        comida = random.choice(caf.opciones)  # Se selecciona una opción del menú
        num_comida = random.randint(1, 3)  # Número de porciones de opción seleccionada

        if caf.disponible[comida]:
            env.process(cliente(env, cont, cajeros, comida, num_comida, caf))


def cliente(env, num, cajeros, comida, num_comida, caf):
    with cajeros.request() as solicitud:
        t_llegada = env.now

        print('Llega el cliente a la cafetería \n Cliente ', num, ':  ', env.now,
              '\n <-------------------------------------------------------------->')
        yield solicitud

        print(f"El cliente {num} desea ordenar {num_comida} unidades de {comida}")

        print('Ordenando... \n Cliente ', num, ':  ', env.now)
        yield env.timeout(procesosEnCajero())

        # Si no queda comida, el cliente se va del establecimiento
        if caf.disponible[comida] < num_comida:
            caf.clientes_fuera[comida] += 1
            print(f"El cliente {num} se fue del establecimiento porque no hay más unidades de {comida}",
                  '\n <-------------------------------------------------------------->')
            return

        caf.disponible[comida] -= num_comida

        print(
            f"El cliente {num} ordenó {num_comida} unidades de {comida}, quedan {caf.disponible[comida]} unidades en existencia",
            '\n <-------------------------------------------------------------->')

        print('Pagando... \n Cliente ', num, ':  ', env.now,
              '\n <-------------------------------------------------------------->')
        yield env.timeout(procesosEnCajero())

        print('Preparando Pedido... \n Cliente ', num, ':  ', env.now,
              '\n <-------------------------------------------------------------->')
        yield env.timeout(procesosEnCajero())

        print('Entregando Pedido... \n Cliente ', num, ':  ', env.now,
              '\n <-------------------------------------------------------------->')
        yield env.timeout(procesosEnCajero())

        print('Consumiendo Producto... \n Cliente ', num, ':  ', env.now,
              '\n <-------------------------------------------------------------->')
        yield env.timeout(consumo(mesas))

        print('Cliente ', num, ' sale de cafetería ', env.now,
              '\n <-------------------------------------------------------------->')
        t_salida = env.now
        tiempoEspera.append(t_salida - t_llegada)

        if caf.disponible[comida] == 0:
            caf.sin_opcion[comida].succeed()
            caf.momento_sin_op[comida] = env.now


# //----------------------------------------PROGRAMA PRINCIPAL---------------------------------------------------------------------------------//
import simpy as sim
import numpy as np
import random
from collections import namedtuple

env = sim.Environment()  # Entorno en el que se desarrolla la simulación

# Definir comidas y número de items por comida
NUM_ITEMS = 5  # Número de items por opción
opciones = ['Empanada y Jugo', 'Galleta y Avena', 'Café y Croissant',
            'Masato y Mantecada']  # Opciones que ofrece la cafetería
disponible = {op: NUM_ITEMS for op in opciones}  # Crear diccionario
sin_opcion = {op: env.event() for op in opciones}  # Eventos en los que cada opción se agota
momento_sin_op = {op: None for op in opciones}
clientes_fuera = {op: 0 for op in opciones}  # Número de clientes que salen del establecimiento
Cafe = namedtuple('Cafe', 'opciones, disponible, sin_opcion, momento_sin_op, clientes_fuera')
caf = Cafe(opciones, disponible, sin_opcion, momento_sin_op, clientes_fuera)

# Digitar información necesaria
tiempo = int(input("Digite el tiempo en el que la simulación se ejecutará "))
caje = int(input("Digite la cantidad de cajeros de la cafetería "))
mesas = int(input("Digite la cantidad de mesas de la cafetería "))
print("--------------------------------------INICIA SIMULACIÓN------------------------------------------")

env.process(proceso(env, caf))  # Pasar el entorno a la clase cafetería
cajeros = sim.Resource(env,
                       capacity=caje)  # Indica que la capacidad de atención de la cafetería se limita al número de cajeros
env.run(tiempo)  # Ejecutar entorno
