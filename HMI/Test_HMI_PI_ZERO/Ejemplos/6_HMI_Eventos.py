import tkinter as tk
from tkinter import ttk

#           ---Eventos----
# Los eventos en tkinter son cosas como: entradas de teclado, cambios en los widgets,
# cuando los widgets son seleccionados o deselecionados, cuando se presionan los botones
# del mouse , movimiento del mouse y/o scroll.

#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('Evetos en tkinter') #titulo de la ventana
window.geometry('600x500')

#variables tkinter


#widgets
text_area = tk.Text(window)
text_in = ttk.Entry(window)
boton =  ttk.Button(window,text='Boton A')
boton2 = ttk.Button(window, text= 'Boton X')


#eventos
window.bind('<F4>', lambda event: print(event))
def evento_boton1(event):
    print(f'x: {event.x}, y: {event.y}')
boton.bind('<Motion>', evento_boton1)
boton2.bind('<Enter>', lambda event: print('Entro al boton X'))
boton2.bind('<Leave>', lambda event: print('Salio del boton X') )


#enpaquetado 
text_area.pack()
text_in.pack()
boton.pack()
boton2.pack()

#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada

print("solo se imprime hasta despues de cerrar la ventana.")