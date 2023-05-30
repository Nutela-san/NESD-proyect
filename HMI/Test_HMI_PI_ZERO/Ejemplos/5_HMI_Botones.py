import tkinter as tk
from tkinter import ttk

#           ---Botones----
# En tkinter los botones hace referencia a los botones comunes, los cuadros de selecion y
# los de seleccion redondos y para usarlos a su maximo potencial es necesario usar
# variables tkinter

#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('BOTONES') #titulo de la ventana
window.geometry('600x400')

#variables tkinter
texto_btn_normal = tk.StringVar().set('btn normal')
var_check1 = tk.BooleanVar(value= True)
#var_check1 = tk.StringVar() # los botones admiten cualquier variable para trabajar
var_check2 = tk.IntVar(value=5)
var_check3 = tk. StringVar()

var_radbtn1 = tk.StringVar()
#var_radbtn2 = tk.StringVar()

#widgets(
def btn1_func():
  print('Presionaste el BOTON NORMAL')

boton1 = ttk.Button(master=window, text='btn normal', textvariable= texto_btn_normal ,command= btn1_func)

check_btn = ttk.Checkbutton(master=window, 
                            text= 'checkbox 1',
                            variable= var_check1,
                            command= lambda: print("el checkboton esta " + str( var_check1.get())))

check_btn2 = ttk.Checkbutton(master=window, 
                            text= 'checkbox 2',
                            variable= var_check2,
                            command= lambda: print("el checkboton esta " + str( var_check2.get())),
                            onvalue= 10,
                            offvalue=5)

check_btn3 = ttk.Checkbutton(master=window, 
                            text= 'checkbox 3',
                            variable= var_check3,
                            command= lambda: print("el checkboton esta " + var_check3.get()))

    # la funcionalida de los botones de radio recide en el uso de varios botones con una sola valiable ya que
    # se pretende que solo uno de todos los botones radiales este activado.
radial_btn = ttk.Radiobutton(window,
                            text= 'boton radial 1',
                            value= 10.14,
                            variable= var_radbtn1,
                            command= lambda: print('botonRadial = '+str(var_radbtn1.get())))

radial_btn2 = ttk.Radiobutton(window,
                            text= 'boton radial 2',
                            value= 'apoco si',
                            variable= var_radbtn1,
                            command= lambda: print('botonRadial = '+str(var_radbtn1.get())))



#enpaquetado 
boton1.pack()
check_btn.pack()
check_btn2.pack()
check_btn3.pack()
radial_btn.pack()
radial_btn2.pack()

#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada

print("solo se imprime hasta despues de cerrar la ventana.")