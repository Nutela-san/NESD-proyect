import tkinter as tk
from tkinter import ttk

#creacion de la ventana
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('NESD HMI') #titulo de la ventana

screen_w = int(window.winfo_screenwidth()*0.98) # Informacion de la pantalla
screen_h = int(window.winfo_screenheight()*0.9)

window.geometry(f'{screen_w}x{screen_h}+0+0')
window.resizable(False, False) # para no poder escalar las dimeciones de la ventana

#variables tkinter
TOP_btn_text = tk.StringVar(value='genericTOP')
DOWN_btn_text = tk.StringVar(value='genericDOW')
var1 = tk.Variable()

level1 = int(50)
level1_last = int(50)
#widgets



panel_pestanas = ttk.Notebook(window, width= int(screen_w), height=int(screen_h*0.95))

pestana_monitor = ttk.Frame(panel_pestanas, width= int(screen_w), height=int(screen_h*0.95))
pestana_monitor.columnconfigure((0,3), weight=1)
pestana_monitor.columnconfigure((1,2), weight=9)
pestana_monitor.rowconfigure(0,weight=1)


pestana_config = ttk.Frame(panel_pestanas, width= int(screen_w), height=int(screen_h*0.95))

tank_canvas_size = (int(screen_w*0.3) , int(screen_h*0.8))

tank1 = tk.Canvas(pestana_monitor, 
                  width= tank_canvas_size[0], height= tank_canvas_size[1],
                  background= '#F0F0F0')

def update_Tank_SeedLevel_Monitor_canvas(level):
  tank1.delete(tk.ALL)
  tank_line_wight = 5
  offSet = tank_line_wight*2
  tank_offset = tank_line_wight
  tank_canvas_size = (int(screen_w*0.3)-offSet , int(screen_h*0.8)-offSet)

  tank_points = ( (tank_offset,tank_offset),
                  (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                  (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                  (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                  (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                  (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                  (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                  (tank_offset+int(tank_canvas_size[0]*1),tank_offset))

  tank1.create_polygon(*tank_points, fill='grey', outline='black', width= tank_line_wight)

  
  if(level >= 90):
    tank_line_wight = 8
    offSet = tank_line_wight*2
    tank_offset = tank_line_wight
    tank_canvas_size = (int(screen_w*0.3)-offSet , int(screen_h*0.8)-offSet)

    fill_points = ( (tank_offset,tank_offset),
                    (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset))
    tank1.create_polygon(*fill_points, fill='green')
  elif (level >=60):
    tank_line_wight = 8
    offSet = tank_line_wight*2
    tank_offset = tank_line_wight
    tank_canvas_size = (int(screen_w*0.3)-offSet , int(screen_h*0.8)-offSet)

    fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.2)),
                    (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.2)))
    tank1.create_polygon(*fill_points, fill='green')
  elif (level >=40):
    tank_line_wight = 8
    offSet = tank_line_wight*2
    tank_offset = tank_line_wight
    tank_canvas_size = (int(screen_w*0.3)-offSet , int(screen_h*0.8)-offSet)

    fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.4)),
                    (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.4)))
    tank1.create_polygon(*fill_points, fill='yellow')
  elif (level >=30):
    tank_line_wight = 8
    offSet = tank_line_wight*2
    tank_offset = tank_line_wight
    tank_canvas_size = (int(screen_w*0.3)-offSet , int(screen_h*0.8)-offSet)

    fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.55)),
                    (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.55)))
    tank1.create_polygon(*fill_points, fill='orange')
  elif (level <30):
    tank_line_wight = 8
    offSet = tank_line_wight*2|1
    tank_offset = tank_line_wight
    tank_canvas_size = (int(screen_w*0.3)-offSet , int(screen_h*0.8)-offSet)

    fill_points = ( (tank_offset,tank_offset+int(tank_canvas_size[1]*0.7)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*0.2), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*1)),
                    (tank_offset+int(tank_canvas_size[0]*0.8), tank_offset+int(tank_canvas_size[1]*0.9)),
                    (tank_offset+int(tank_canvas_size[0]*1),tank_offset+int(tank_canvas_size[1]*0.7)))
    tank1.create_polygon(*fill_points, fill='red')
  
  tank1.create_text((int(tank_canvas_size[0]/2),int(tank_canvas_size[1]*3/8)),
                    text=f' {level}%', fill='black', font= 'Arial 100 bold')


update_Tank_SeedLevel_Monitor_canvas(level1)
#tank2_monitor = create_Tank_SeedLevel_Monitor_canvas(pestana_monitor,100)


def TOP_btn_func():
  pestana = panel_pestanas.index('current')
  global level1
  if pestana == 0:
    print('TOP_BUTTON IN MONITOOR')
    level1 += 1
    level1 = max(0,min(level1,100))

    update_Tank_SeedLevel_Monitor_canvas(level1)
  elif pestana == 1:
    print('ARREMANGALARECPUJALA SI')
    

def DOWN_btn_func():
  pestana = panel_pestanas.index('current')
  global level1
  if pestana == 0:
    print('DOWN_BUTTON IN MONITOOR')
    level1 -= 1
    level1 = max(0,min(level1,100))
    update_Tank_SeedLevel_Monitor_canvas(level1)
  elif pestana == 1:
    print('ARREMANGALARECPUJALA NOO')
    

def create_buttons_UPDOWN_frame(contenedor, btnTop_name, btnDown_name):
  btn_frame = ttk.Frame(contenedor)
  btn_frame.rowconfigure((0,1),weight=1)
  btn_frame.columnconfigure(0,weight=1)

  TOP_btn =  ttk.Button(btn_frame, text= btnTop_name, textvariable = TOP_btn_text , command= TOP_btn_func)
  DOWN_btn =  ttk.Button(btn_frame, text= btnDown_name, textvariable = DOWN_btn_text, command= DOWN_btn_func)
  
  TOP_btn.grid(row=0,column=0, sticky='swe', ipady=int(screen_h*0.1) , pady=int(screen_h*0.02))
  DOWN_btn.grid(row=1,column=0,sticky='nwe',ipady=int(screen_h*0.1), pady=int(screen_h*0.02))
  
  return btn_frame

side_buttons_monitor = create_buttons_UPDOWN_frame(pestana_monitor, 'TOP','DOWN')
side_buttons_config = create_buttons_UPDOWN_frame(pestana_config, 'TOP','DOWN')

#enpaquetado 
panel_pestanas.pack(expand=True)
pestana_monitor.pack(expand=True)
pestana_config.pack(expand= True )

side_buttons_monitor.grid(row=0, column=0, sticky='nswe')
tank1.grid(row= 0,column=1 , columnspan=2)

side_buttons_config.pack()
#tank2_monitor.grid(row= 0,column=2)

panel_pestanas.add(pestana_monitor, text= '     Monotor     ')
panel_pestanas.add(pestana_config, text=  'Configuraciones')


#EVENTOS
top_texts = ('TOP_monitor', 'AH SU MAKINA')
down_texts = ('DOWN_monitor', 'SI JALAAAAA')

def set_n_and_f_topdown_btn(event):
  pestana = panel_pestanas.index('current')
  print('cambio de pestaña')
  print(pestana)
  TOP_btn_text.set(top_texts[pestana])
  DOWN_btn_text.set(down_texts[pestana])
  

def set_pestana(pestana):
  panel_pestanas.select(tab_id=pestana)

panel_pestanas.bind('<<NotebookTabChanged>>',set_n_and_f_topdown_btn)
window.bind('<F1>', lambda event: set_pestana(0))
window.bind('<F2>', lambda event: set_pestana(1))

#Ciclo principal donde corre el programa de la interfaz
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada


#window.update()


print("solo se imprime hasta despues de cerrar la ventana.")