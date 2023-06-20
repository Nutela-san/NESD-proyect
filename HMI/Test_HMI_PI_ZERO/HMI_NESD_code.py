import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time



#----------------------- creacion de la ventana -------------------------------------
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('NESD HMI') #titulo de la ventana

screen_w = int(window.winfo_screenwidth()*0.98) # Informacion de la pantalla
screen_h = int(window.winfo_screenheight()*0.9)

window.geometry(f'{screen_w}x{screen_h}+0+0')
window.resizable(False, False) # para no poder escalar las dimeciones de la ventana

cursor_type = 'none' # cursor que aparecera en todas las ventanas
#----------------------- variables tkinter -------------------------------------
TOP_btn_text = tk.StringVar(value='genericTOP')
DOWN_btn_text = tk.StringVar(value='genericDOW')

level1 = tk.Variable()
level2 = tk.Variable()

level1.set(0)
level2.set(0)

#----------------------- widgets -------------------------------------

#--- PESTAÑAS ---
panel_pestanas = ttk.Notebook(window, width= int(screen_w), height=int(screen_h*0.95))

pestana_inicio = ttk.Frame(panel_pestanas, width= int(screen_w), height=int(screen_h*0.95))
pestana_inicio.rowconfigure(0, weight=1)
pestana_inicio.columnconfigure(0, weight=1)

pestana_config = ttk.Frame(panel_pestanas, width= int(screen_w), height=int(screen_h*0.95))
pestana_config.columnconfigure((0,3), weight=1)
pestana_config.columnconfigure((1,2), weight=9)
pestana_config.rowconfigure(0,weight=1)

pestana_tests = ttk.Frame(panel_pestanas, width= int(screen_w), height=int(screen_h*0.95))
pestana_tests.columnconfigure((0,3), weight=1)
pestana_tests.columnconfigure((1,2), weight=9)
pestana_tests.rowconfigure(0,weight=9)
pestana_tests.rowconfigure(1,weight=1)

pestana_monitor = ttk.Frame(panel_pestanas, width= int(screen_w), height=int(screen_h*0.95))
pestana_monitor.columnconfigure((0,1), weight=2)
pestana_monitor.columnconfigure(2, weight=1)
pestana_monitor.rowconfigure(0,weight=9)
pestana_monitor.rowconfigure(1,weight=1)

subpestanta_test_1= ttk.Frame(panel_pestanas, width= int(screen_w*0.75), height=int(screen_h*0.95))
subpestanta_test_comunicacion= ttk.Frame(panel_pestanas, width= int(screen_w*0.75), height=int(screen_h*0.95))
subpestanta_test_modulos= ttk.Frame(panel_pestanas, width= int(screen_w*0.75), height=int(screen_h*0.95))


#--- Frames_tanques ---

tank_canvas_size_o = (int(screen_w*0.25) , int(screen_h*0.7))

#tanque 1
tank1_test =  ttk.Frame(pestana_tests, 
                        width= tank_canvas_size_o[0], 
                        height= tank_canvas_size_o[1])

tank1_test.columnconfigure((0,1), weight= 1)
tank1_test.rowconfigure((0,2,3),weight= 1)
tank1_test.rowconfigure(1,weight= 10)

tank1_test_draw = tk.Canvas(tank1_test, 
                  width= tank_canvas_size_o[0], height= tank_canvas_size_o[1],
                  background= '#F0F0F0')

tank1_label = ttk.Label(tank1_test, text= 'TANQUE 1' , font='Arial 35 bold')
tank1_out1_label = ttk.Label(tank1_test, text= 'SALIDA 1' , font='Arial 20 bold',relief = 'groove')
tank1_out2_label = ttk.Label(tank1_test, text= 'SALIDA 2' , font='Arial 20 bold',relief = 'groove')
tank1_seed1_label = ttk.Label(tank1_test, text= '0 semillas' , font='Arial 20 bold',relief = 'groove')
tank1_seed2_label = ttk.Label(tank1_test, text= '0 semillas' , font='Arial 20 bold',relief = 'groove')

tank1_label.grid(row=0 ,column=0, columnspan=2)
tank1_test_draw.grid(row=1 ,column=0, columnspan=2)
tank1_out1_label.grid(row=2,column=0)
tank1_out2_label.grid(row=2,column=1)
tank1_seed1_label.grid(row=3,column=0)
tank1_seed2_label.grid(row=3,column=1)


tank1_monitor =  ttk.Frame(pestana_monitor, 
                        width= tank_canvas_size_o[0], 
                        height= tank_canvas_size_o[1])

tank1_monitor.columnconfigure((0,1), weight= 1)
tank1_monitor.rowconfigure((0,2,3),weight= 1)
tank1_monitor.rowconfigure(1,weight= 10)

tank1_monitor_draw = tk.Canvas(tank1_monitor, 
                  width= tank_canvas_size_o[0], height= tank_canvas_size_o[1],
                  background= '#F0F0F0')

tank1_label = ttk.Label(tank1_monitor, text= 'TANQUE 1' , font='Arial 35 bold')
tank1_out1_label = ttk.Label(tank1_monitor, text= 'SALIDA 1' , font='Arial 20 bold',relief = 'groove')
tank1_out2_label = ttk.Label(tank1_monitor, text= 'SALIDA 2' , font='Arial 20 bold',relief = 'groove')
tank1_seed1_label = ttk.Label(tank1_monitor, text= '0 semillas' , font='Arial 20 bold',relief = 'groove')
tank1_seed2_label = ttk.Label(tank1_monitor, text= '0 semillas' , font='Arial 20 bold',relief = 'groove')

tank1_label.grid(row=0 ,column=0, columnspan=2)
tank1_monitor_draw.grid(row=1 ,column=0, columnspan=2)
tank1_out1_label.grid(row=2,column=0)
tank1_out2_label.grid(row=2,column=1)
tank1_seed1_label.grid(row=3,column=0)
tank1_seed2_label.grid(row=3,column=1)


def update_Tank_SeedLevel_Monitor_canvas(tank , level):
  global tank_canvas_size_o
  tank.delete(tk.ALL)
  tank_line_wight = 5
  offSet = tank_line_wight*2
  tank_offset = tank_line_wight
  tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

  tank_points = ( (tank_offset,tank_offset),
                  (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                  (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                  (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                  (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                  (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                  (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                  (tank_offset+int(tank_canvas_size[0]*1),tank_offset))

  tank.create_polygon(*tank_points, fill='grey', outline='black', width= tank_line_wight)

  if tank.cget('state') != 'disabled':
    if(level.get() >= 90):
      tank_line_wight = 8
      offSet = tank_line_wight*2
      tank_offset = tank_line_wight
      tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

      fill_points = ( (tank_offset,tank_offset),
                      (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset))
      tank.create_polygon(*fill_points, fill='green')
    elif (level.get() >=60):
      tank_line_wight = 8
      offSet = tank_line_wight*2
      tank_offset = tank_line_wight
      tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

      fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.2)),
                      (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.2)))
      tank.create_polygon(*fill_points, fill='green')
    elif (level.get() >=40):
      tank_line_wight = 8
      offSet = tank_line_wight*2
      tank_offset = tank_line_wight
      tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

      fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.4)),
                      (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.4)))
      tank.create_polygon(*fill_points, fill='yellow')
    elif (level.get() >=30):
      tank_line_wight = 8
      offSet = tank_line_wight*2
      tank_offset = tank_line_wight
      tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

      fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.55)),
                      (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.55)))
      tank.create_polygon(*fill_points, fill='orange')
    elif (level.get() <30):
      tank_line_wight = 8
      offSet = tank_line_wight*2|1
      tank_offset = tank_line_wight
      tank_canvas_size = (tank_canvas_size_o[0]-offSet , tank_canvas_size_o[1]-offSet)

      fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                      (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                      (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)))
      tank.create_polygon(*fill_points, fill='red')
    tank.create_text((int(tank_canvas_size[0]/2),int(tank_canvas_size[1]*3/8)),
                    text=f' {level.get()}%', fill='black', font= 'Arial 100 bold')
  else:
    tank.create_text((int(tank_canvas_size[0]/2),int(tank_canvas_size[1]*3/8)),
                      text='NoTank', fill='black', font= 'Arial 70 bold')

def TOP_btn_func():
  pestana = panel_pestanas.index('current')
  global level1
  if pestana == 2:
    print('TOP_BUTTON IN MONITOOR')
    level1.set(level1.get() + 1) 
    level1.set(max(0,min(level1.get(),100))) 
  elif pestana == 1:
    print('ARREMANGALARECPUJALA SI')

def DOWN_btn_func():
  pestana = panel_pestanas.index('current')
  global level1
  if pestana == 2:
    print('DOWN_BUTTON IN MONITOOR')
    level1.set(level1.get() - 1) 
    level1.set(max(0,min(level1.get(),100))) 
    
  elif pestana == 1:
    print('ARREMANGALARECPUJALA NOO')
  elif pestana == 3:
    pass



def create_buttons_UPDOWN_frame(contenedor, btnTop_name, btnDown_name):
  btn_frame = ttk.Frame(contenedor)
  btn_frame.rowconfigure((0,1),weight=1)
  btn_frame.columnconfigure(0,weight=1)

  TOP_btn =  ttk.Button(btn_frame, text= btnTop_name, textvariable = TOP_btn_text , command= TOP_btn_func)
  DOWN_btn =  ttk.Button(btn_frame, text= btnDown_name, textvariable = DOWN_btn_text, command= DOWN_btn_func)
  
  TOP_btn.grid(row=0,column=0, sticky='swe', ipady=int(screen_h*0.1) , pady=int(screen_h*0.02))
  DOWN_btn.grid(row=1,column=0,sticky='nwe',ipady=int(screen_h*0.1), pady=int(screen_h*0.02))
  
  return btn_frame


side_buttons_config = create_buttons_UPDOWN_frame(pestana_config, 'TOP','DOWN')
side_buttons_test = create_buttons_UPDOWN_frame(pestana_tests,'TOP','DOWN')

#----------------------- enpaquetado -------------------------------------
panel_pestanas.pack(expand=True)
pestana_monitor.pack(expand=True)
pestana_config.pack(expand= True )
pestana_tests.pack(expand=True)

tank1_monitor.grid(row=0, column=0)
tank1_monitor_draw.configure(state='disabled')
tank1_test.grid(row=0, column=1,columnspan= 2)
tank1_test_draw.configure(state='disabled')


side_buttons_config.grid(row=0, column=0)

side_buttons_test.grid(row=0, column=0)

panel_pestanas.add(pestana_inicio, text= '     INICIO      ')
panel_pestanas.add(pestana_config, text= ' CONFIGURACIONES ')
panel_pestanas.add(pestana_tests,  text= '     PRUEBAS     ')
panel_pestanas.add(pestana_monitor,text= '     MONITOR     ')


panel_pestanas.hide(tab_id=1)
panel_pestanas.hide(tab_id=2)
panel_pestanas.hide(tab_id=3)

#----------------------- EVENTOS -------------------------------------


def set_n_and_f_topdown_btn(event):
  pestana = panel_pestanas.index('current')
  print('cambio de pestaña')
  print(pestana)
  if pestana == 1:
    TOP_btn_text.set('Numero de Semillas')
    DOWN_btn_text.set('Distancia')
  elif pestana == 2:
    TOP_btn_text.set('Prueba\nConexiones')
    DOWN_btn_text.set('Prueba\nSensores')


def set_pestana(pestana):
  panel_pestanas.select(tab_id=pestana)

panel_pestanas.bind('<<NotebookTabChanged>>',set_n_and_f_topdown_btn)

window.bind('<F1>', lambda event: set_pestana(1))
window.bind('<F2>', lambda event: set_pestana(2))
window.bind('<F3>', lambda event: set_pestana(3))
window.bind('<KeyPress-u>', lambda event: update_Tank_SeedLevel_Monitor_canvas(tank1_test_draw, level1))

def alerta(event):
  messagebox.showwarning('ALERTA','SEMILLA INSUFICIENTE EN EL TANQUE 1')
  

def habilitar_tank1(event):
  tank1_test_draw.config(state= 'normal')
  tank1_monitor_draw.config(state= 'normal')

window.bind('<KeyPress-a>', habilitar_tank1)
window.bind('<KeyPress-space>', alerta)

def inicio(event):
  panel_pestanas.hide(tab_id=0)
  panel_pestanas.add(pestana_config, text= ' CONFIGURACIONES ')
  panel_pestanas.add(pestana_tests,  text= '     PRUEBAS     ')
  panel_pestanas.add(pestana_monitor,text= '     MONITOR     ')
  panel_pestanas.select(tab_id=1)

window.bind('<Any-KeyPress>', inicio)


#----------------------- Ciclo principal donde corre el programa de la interfaz -------------------------------------
segundo_hilo = True
def update_tank():
  global segundo_hilo
  while segundo_hilo:
    update_Tank_SeedLevel_Monitor_canvas(tank1_test_draw,level1)
    update_Tank_SeedLevel_Monitor_canvas(tank1_monitor_draw,level1)
    time.sleep(1)

t = threading.Thread(target= update_tank)
t.start()

window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada

segundo_hilo = False

print("solo se imprime hasta despues de cerrar la ventana.")