# Importación de librerias
import simpy as sim
import numpy as np
import operator
from collections import namedtuple
import random

#Definición de variables GLOBALES
global cont
tiempoEspera = []


class CafeteriaController:
    def __init__(self, tiempo, caje, mesas, num_productos):
        # Asiganación de variables para la simulación
        self.tiempo = int(tiempo)
        self.caje = int(caje)
        self.mesas = int(mesas)
        self.num_items = int(num_productos)

        self.env = sim.Environment()  # Entorno en el que se desarrolla la simulación
        self.opciones = [
            'Empanada y Jugo',
            'Galleta y Avena',
            'Café y Croissant',
            'Masato y Mantecada'
        ]  # Opciones que ofrece la cafetería
        self.myFile = open('Informe.txt', 'w+')  # Creación de archivo con el informe generado
        self.mytexto = []  # Variable que envia los datos a la interfaz
        self.disponible = {op: self.num_items for op in self.opciones}  # Cantidad existente de cada producto
        self.momento_sin_op = {op: 0 for op in self.opciones}  # Tiempo en el que la opción agotó sus existencias
        self.clientes_fuera = {op: 0 for op in self.opciones}  # Número de clientes que salen del establecimiento

        # Asignación de etiquetas
        self.cafe = namedtuple('Cafe', 'opciones, disponible, momento_sin_op, clientes_fuera')
        self.caf = self.cafe(self.opciones, self.disponible, self.momento_sin_op, self.clientes_fuera)

        print("Cafeteria Controller is run")
        self.env.process(self.proceso(self.env, self.caf))  # Pasar el entorno a la clase cafetería
        # Indica que la capacidad de atención de la cafetería se limita al número de cajeros
        self.cajeros = sim.Resource(self.env, capacity=self.caje)
        self.env.run(tiempo)  # Ejecutar entorno
        self.myFile.close()  # Cerrar archivo para lectura

    def llegadas(self):
        return np.random.exponential(3 / 1)  # Random para llegadas de clientes (1 cliente cada 3 minutos)

    def aleatorio(self, caje):
        return np.random.exponential(
            1 / caje)  # Random para cajero (Caje = número de cajeros que atienden la cafetería)

    def procesoEnCajero(self):
        return self.aleatorio(
            self.caje)  # Utilizado para procesos realizados en caja (Pedido, Pago, Preparación, Entrega)

    def consumo(self, mesas):
        return np.random.exponential(
            1 / mesas)  # Para consumo de producto se tiene en cuenta el número de mesas disponibles

    def proceso(self, env, caf):
        cont = 0
        while True:
            yield env.timeout(self.llegadas())
            cont += 1
            comida = random.choice(caf.opciones)  # Se selecciona una opción del menú
            num_comida = random.randint(1, 3)  # Número de porciones de opción seleccionadas
            if caf.disponible[comida]:  # SI NO HAY COMIDA, NO ENTRA AL PROCESO, Y LA SIMULACIÓN SE DETIENE :)
                env.process(self.cliente(env, cont, self.cajeros, comida, num_comida, caf))

    def cliente(self, env, num, cajeros, comida, num_comida, caf):
        with cajeros.request() as solicitud:
            t_llegada = env.now
            texto_a_mostrar = f'Llega el cliente a la cafeteria ' \
                              f'\nCliente {num}: {env.now} \n<--------------------------->'
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            yield solicitud
            texto_a_mostrar = f"El cliente {num} desea ordenar {num_comida} unidades de {comida}"
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            texto_a_mostrar = f'Ordenando... \nCliente {num}: {env.now}'
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            yield env.timeout(self.procesoEnCajero())

            # Si no estan disponibles las unidades que el cliente desea, el cliente se va
            if caf.disponible[comida] < num_comida:
                caf.clientes_fuera[comida] += 1
                texto_a_mostrar = f"El cliente {num} se fue del establecimiento porque " \
                                  f"no hay las unidades de {comida}" \
                                  f"que queria o el producto se agoto\n" \
                                  f"Tiempo de salida: {env.now}"
                self.myFile.write(texto_a_mostrar + '\n')
                print(texto_a_mostrar)
                return
            caf.disponible[comida] -= num_comida  # Se reduce la cantidad de comida disponible
            texto_a_mostrar = f"El cliente {num} ordenó {num_comida} unidades de {comida}, " \
                              f"queda {caf.disponible[comida]}" \
                              f"unidades en existencia\n" \
                              f"<--------------------------->"
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)

            if caf.disponible[comida] == 0:
                # caf.sin_opcion[comida].succeed()
                caf.momento_sin_op[comida] = env.now
                texto_a_mostrar = f"Las unidades de {comida} se agotaron a los {caf.momento_sin_op[comida]} minutos"
                self.myFile.write(texto_a_mostrar + '\n')
                print(texto_a_mostrar)

            texto_a_mostrar = f'Pagando... \nCliente {num}: {env.now} \n <--------------------------->'
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            yield env.timeout(self.procesoEnCajero())

            texto_a_mostrar = f'Preparando pedido... \nCliente {num}: {env.now}\n <------------>'
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            yield env.timeout(self.procesoEnCajero())

            texto_a_mostrar = f'Entregando pedido... \n Cliente {num}: {env.now}\n <--------------------->'
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            yield env.timeout(self.procesoEnCajero())

            texto_a_mostrar = f"Consumiendo Producto... \nCliente {num}: {env.now}\n <---------------->"
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            yield env.timeout(self.consumo(self.mesas))

            texto_a_mostrar = f'Cliente {num} sale de cafeteria {env.now}\n <------------------>'
            self.myFile.write(texto_a_mostrar + '\n')
            print(texto_a_mostrar)
            t_salida = env.now
            tiempoEspera.append(t_salida - t_llegada)

    def reportes(self):
        from tabulate import tabulate
        # Tiempo en que se acabaron los productos
        texto_informe = f"Tiempo en que se terminaron los productos: {tabulate(sorted(self.momento_sin_op.items(), key=operator.itemgetter(1)))}"
        self.mytexto.append(texto_informe)
        print(texto_informe)
        # Cantidad de clientes que se fueron por falta de existencias de cada combo
        texto_informe = f"Número de personas que se fueron: {tabulate(sorted(self.clientes_fuera.items(), key=operator.itemgetter(1)))}"
        self.mytexto.append(texto_informe)
        print(texto_informe)  # Producto con menor tiempo registrado, producto más vendido
        # Numero final de productos existentes
        texto_informe = f"Número de productos existentes {tabulate(sorted(self.disponible.items(), key=operator.itemgetter(1)))}"
        self.mytexto.append(texto_informe)
        print(texto_informe)
