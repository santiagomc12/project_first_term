# Importación de librerias
from tkinter import *
from tkinter import ttk
from fuente.Controller.CafeteriaController import CafeteriaController  # llamado del controlador


class Aplication():
    def __init__(self):
        self.raiz = Tk()  # Definición de la ventana donde se ubica la interfaz grafica
        self.raiz.title("Simulación cafeteria")

        # Definición de los parametros iniciales
        self.tiempo_simulacion = IntVar(value=0)
        self.numero_cajeros = IntVar(value=0)
        self.numero_mesas = IntVar(value=0)
        self.respuesta = StringVar(value='Respuesta')
        self.productos_existentes = IntVar(value=0)

        picture_cafeteria = PhotoImage(file='../../Pictures/coffe_shop.png')  # Se define la ubicación de la imagen

        # Asignación de parametros para los elementos (labels, spinbox, etc) que estan involucrados en la interfaz
        self.etiq_title = ttk.Label(self.raiz, text="Simulación de una cafeteria")
        self.imagen1 = ttk.Label(self.raiz, image=picture_cafeteria, anchor="center")
        self.etiq1 = ttk.Label(self.raiz, text="Tiempo de simulación: ")
        self.tiempo = Spinbox(self.raiz, from_=1, to=20, wrap=True, textvariable=self.tiempo_simulacion)
        self.etiq_num_productos = ttk.Label(self.raiz, text="Productos en existencia")
        self.num_productos = Spinbox(self.raiz, from_=1, to=100, wrap=True, textvariable=self.productos_existentes)
        self.etiq2 = ttk.Label(self.raiz, text="Numero de cajeros: ")
        self.cajeros = Spinbox(self.raiz, from_=1, to=20, wrap=True, textvariable=self.numero_cajeros)
        self.etiq3 = ttk.Label(self.raiz, text="Numero de mesas: ")
        self.mesas = Spinbox(self.raiz, from_=1, to=20, wrap=True, textvariable=self.numero_mesas)
        self.etiq_respuesta = ttk.Label(
            self.raiz, textvariable=self.respuesta,
            foreground="black", background="#C2ECF3",
            borderwidth=5,
            anchor="e"
        )
        self.separador = ttk.Separator(self.raiz, orient=HORIZONTAL)
        self.boton1 = ttk.Button(self.raiz, text="Simular", command=self.simular)
        self.boton2 = ttk.Button(self.raiz, text="Salir", command=quit)

        # Ubicación de los elementos en la interfaz / Definición de separación entre elementos
        self.etiq_title.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)
        self.imagen1.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)
        self.etiq1.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)
        self.tiempo.pack(side=TOP, fill=X, expand=True, padx=20, pady=5)
        self.etiq_num_productos.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)
        self.num_productos.pack(side=TOP, fill=X, expand=True, padx=20, pady=5)
        self.etiq2.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)
        self.cajeros.pack(side=TOP, fill=X, expand=True, padx=20, pady=5)
        self.etiq3.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)
        self.mesas.pack(side=TOP, fill=X, expand=True, padx=20, pady=5)
        self.etiq_respuesta.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=5)
        self.separador.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.boton1.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.boton2.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        self.raiz.mainloop()  # Se encarga de estar al pendiente de los cambios de la interfaz

    # Llamado del controlador
    def simular(self):
        cafContr = CafeteriaController(
            tiempo=self.tiempo.get(),
            caje=self.cajeros.get(),
            mesas=self.mesas.get(),
            num_productos=self.num_productos.get()
        )
        cafContr.reportes() #Se da inicio al metodo
        description = cafContr.mytexto #Se obtiene el texto
        text_ordenado = f'Inicio de la simulación\n'
        for texto in description:
            text_ordenado += texto
        alert = f'{text_ordenado}\n'
        self.respuesta.set(alert)
        return 0


# Ejecución del programa
def main():
    mi_app = Aplication()
    return 0


if __name__ == '__main__':
    main()
