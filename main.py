import tkinter;

ventana = tkinter.Tk()
ventana.title("Proyecto Simulación")

intro_frame = tkinter.Frame()
datos_frame = tkinter.Frame()
mesas_frame = tkinter.Frame()

intro_frame.pack()
intro_frame.config(bg = "green")
intro_frame.config(width = "650", height = "50")

datos_frame.pack()
datos_frame.config(bg = "red")
datos_frame.config(width = "650", height = "350")

mesas_frame.pack()
mesas_frame.config(width = "650", height = "350")


title_label = tkinter.Label(intro_frame, text = "Simulación de una cafeteria", bg = "green")
title_label.place(x = 0, y = 0)

cajero_label = tkinter.Label(ventana, text = "Numero de cajeros")



ventana.mainloop()
