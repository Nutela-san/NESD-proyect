import tkinter as tk
from tkinter import ttk

#----------------------- creacion de la ventana -------------------------------------
window = tk.Tk() # crea la ventana apartir de un metodo de tk
window.title('NESD HMI') #titulo de la ventana

screen_w = int(window.winfo_screenwidth()*0.98) # Informacion de la pantalla
screen_h = int(window.winfo_screenheight()*0.9)

window.geometry(f'{screen_w}x{screen_h}+0+0')
window.resizable(False, False) # para no poder escalar las dimeciones de la ventana


#----------------------- widgets Plantillas-------------------------------------

class Tank_monitor(ttk.Frame):
  def __init__(self, parent, size, tank_number,level, SeedOuputs):  
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    self.tank_number = max(1,tank_number)
    self.level = level
    self.SeedOutputs = (SeedOuputs[0], SeedOuputs[1])

    #-- configurando grid --
    self.config(width= size[0])
    self.config(height= size[1])
    self.columnconfigure((0,1), weight= 1)
    self.rowconfigure((0,3), weight=1)
    self.rowconfigure(2,weight=2)
    self.rowconfigure(1, weight=7)

    #--Elementos (widgets) del monitor de tolva
    self.tank_size = (int(size[0]),int(size[1]*0.75)) # tamaño del dibujo de la tolva
    self.tank_draw =  tk.Canvas(self, 
                                width= self.tank_size[0], height= self.tank_size[1],
                                background= '#F0F0F0')
    text_size = int(size[1]*0.05)
    self.tank_label = ttk.Label(self, text=f'TOLVA {self.tank_number}', font= f'Arial {text_size} bold')
    text_size = int(size[1]*0.025)
    self.SeedOut1_label = ttk.Label(self, text=f'SALIDA {(self.tank_number*2)-1}', anchor='center', font= f'Arial {text_size} bold')
    self.SeedOut2_label = ttk.Label(self, text=f'SALIDA {(self.tank_number*2)}', anchor='center', font= f'Arial {text_size} bold')
    self.Seed_Count1 = ttk.Label(self, text= f'{0} semillas' ,anchor= 'center', relief= 'groove',font= f'Arial {text_size}') #, state='readonly')
    self.Seed_Count2 = ttk.Label(self, text= f'{0} semillas' ,anchor= 'center', relief= 'groove',font= f'Arial {text_size}') #, state='readonly')

    #-- empaquedato en grid
    self.tank_label.grid(row=0 , column=0, columnspan=2)
    self.tank_draw.grid(row=1, column=0, columnspan=2)
    self.Seed_Count1.grid(row=2,column=0, sticky= 'nswe')
    self.Seed_Count2.grid(row=2,column=1, sticky= 'nswe')
    self.SeedOut1_label.grid(row=3,column=0, sticky= 'nswe')
    self.SeedOut2_label.grid(row=3,column=1, sticky= 'nswe')

    self.update_level()
  
  def update_level(self):
    tank = self.tank_draw
    tank_canvas_size_o = (self.tank_size[0], self.tank_size[1])
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

    self.level.set(max(0,min(self.level.get(),100)))
    self.Seed_Count1.config(text= f'{self.SeedOutputs[0].get()} semillas')
    self.Seed_Count2.config(text= f'{self.SeedOutputs[1].get()} semillas')

    if tank.cget('state') != 'disabled':
      if(self.level.get() >= 90):
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
      elif (self.level.get() >=60):
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
      elif (self.level.get() >=40):
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
      elif (self.level.get() >=30):
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
      elif (self.level.get() <30):
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
                      text=f' {self.level.get()}%', fill='black', font= 'Arial 100 bold')
    else:
      tank.create_text((int(tank_canvas_size[0]/2),int(tank_canvas_size[1]*3/8)),
                        text='NoTank', fill='black', font= 'Arial 70 bold')
    
    self.parent.after(100, self.update_level)

class Odometry_monitor(ttk.Frame):
  def __init__(self, parent, odometry_data):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    self.tractor_img = tk.PhotoImage(file='resources/tractor_odometri_300.png',width=300)
    self.odometry_data = odometry_data
    #-- configurando grid --
    self.columnconfigure((0,1), weight=1)
    self.rowconfigure((0,2,3,4,5),weight=1)
    self.rowconfigure(1,weight=2)

    #--Elementos (widgets) --
    font_size = 40 #self.grid_info()

    self.monitor_title = ttk.Label(self, text= 'ODOMETRÍA' , font= f'Arial {font_size} bold' , anchor='center')
    self.tractor_draw = ttk.Label(self,image= self.tractor_img , anchor='center')
    self.tractor_draw.config(relief= 'groove') # marca el cuadro de label para imagen

    font_size = 40 #self.grid_info()
    self.speed_title = ttk.Label(self, text= 'Velocidad de Siembra', font= f'Arial {font_size} bold' , anchor='center' )
    self.speed_unit  = ttk.Label(self, text= 'Km/hr', font= f'Arial {font_size}' , anchor='center' )
    self.speed_var_text = ttk.Label(self, text= f'{self.odometry_data[0].get()}',  font= f'Arial {font_size}' , anchor='center' , relief='groove')

    self.distance_title = ttk.Label(self, text= 'Distancia de Siembra', font= f'Arial {font_size} bold' , anchor='center' )
    self.distance_unit  = ttk.Label(self, text= 'm', font= f'Arial {font_size}' , anchor='center' )
    self.distance_var_text = ttk.Label(self, text= f'{self.odometry_data[1].get()}',  font= f'Arial {font_size}' , anchor='center', relief='groove')

    #-- empaquedato en grid--
    self.monitor_title.grid(row=0 , column=0, columnspan=2, sticky='nswe' )
    self.tractor_draw.grid(row=1, column=0, columnspan=2, sticky= 'nswe' )
    self.speed_title.grid(row=2, column=0, columnspan=2, sticky= 'nswe')
    self.speed_var_text.grid(row=3, column=0, sticky= 'nswe')
    self.speed_unit.grid(row=3, column=1, sticky='nswe')
    self.distance_title.grid(row=4, column=0, columnspan=2, sticky= 'nswe')
    self.distance_var_text.grid(row=5, column=0, sticky= 'nswe')
    self.distance_unit.grid(row=5, column=1, sticky='nswe')

    #-- eventos
    self.update_monitor()

  def update_monitor(self):
    self.speed_var_text.config(text = f'{self.odometry_data[0].get()}')
    self.distance_var_text.config(text = f'{self.odometry_data[1].get()}')
    self.parent.after(100, self.update_monitor)

class Option_btns(ttk.Frame):
  def __init__(self, parent, Btn_UP_name, Btn_DOWN_name, height):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent
    self.height = height
    #-- configurando grid --
    self.config(height=self.height)
    self.rowconfigure((0,1), weight=1)
    self.columnconfigure(0, weight=1)

    #--Elementos (widgets) --
    self.Btn_UP = ttk.Button(self, text= Btn_UP_name)
    self.Btn_DOWN = ttk.Button(self, text= Btn_DOWN_name)

    #-- empaquedato en grid --
    self.Btn_UP.grid(row= 0, column=0, sticky='swe', ipady= int(self.height*0.1) , pady=10)
    self.Btn_DOWN.grid(row= 1, column=0, sticky='nwe',ipady= int(self.height*0.1), pady=10)

  def config_fuctions(self,Btn_UP_func, Btn_DOWN_func):
    self.Btn_UP.config(command= Btn_UP_func)
    self.Btn_DOWN.config(command= Btn_DOWN_func)

class Select_btns(ttk.Frame):
  def __init__(self, parent,Btn_OK_name, Btn_BACK_name):
    super().__init__(parent)
    super().configure(relief= 'groove', border= 5)#añade un borde para ver los limites
    self.parent = parent

    #-- configurando grid --
    self.rowconfigure(0,weight=1)
    self.columnconfigure((0,1), weight= 1)

    #--Elementos (widgets) --
    self.Btn_OK = ttk.Button(self, text= Btn_OK_name)
    self.Btn_BACK = ttk.Button(self, text= Btn_BACK_name)

    #-- empaquedato en grid --
    self.Btn_OK.grid(row=0,column=0, sticky= 'nswe')
    self.Btn_BACK.grid(row=0, column=1, sticky= 'nswe')

  def config_fuctions(self,Btn_OK_func, Btn_BACK_func):
    self.Btn_OK.config(command= Btn_OK_func)
    self.Btn_BACK.config(command= Btn_BACK_func)

class test_tab(ttk.Frame):
  def __init__(self, parent, size , tank_parameters, odometry_parameters):
    super().__init__(parent)
    self.parent = parent
    self.main_frame_size = size
    self.motitor_tank_size = (int(self.main_frame_size[0]*0.25) , int(self.main_frame_size[1]*0.85)) 

    self.tank_parameters = tank_parameters
    self.odometry_parameters = odometry_parameters
    #-- Frames principales
    self.selection_test_tab = ttk.Frame(self,
                                        width= self.main_frame_size[0],
                                        height= self.main_frame_size[1])
    self.sensores_test_tab = ttk.Frame(self,
                                        width= self.main_frame_size[0],
                                        height= self.main_frame_size[1])
    self.conection_test_tab = ttk.Frame(self,
                                        width= self.main_frame_size[0],
                                        height= self.main_frame_size[1])
    
    #-- configurando grid --
    self.rowconfigure(0,weight=1)
    self.columnconfigure(0,weight=1)

    self.selection_test_tab.rowconfigure(0,weight=1)
    self.selection_test_tab.columnconfigure(0,weight=2)
    self.selection_test_tab.columnconfigure(1,weight=8)

    self.sensores_test_tab.columnconfigure(0, weight=1)
    self.sensores_test_tab.columnconfigure((1,2), weight=5)
    self.sensores_test_tab.columnconfigure(3,weight=4)
    self.sensores_test_tab.rowconfigure(0,weight=9)
    self.sensores_test_tab.rowconfigure(1,weight=9)

    self.conection_test_tab.columnconfigure(0, weight=1)
    self.conection_test_tab.columnconfigure(1, weight=3)
    self.conection_test_tab.rowconfigure((0,1,2,4), weight=1)
    self.conection_test_tab.rowconfigure(3,weight=6)

    #--Elementos (widgets) --
    #Para deciption tab
    self.maid_descrip_label = ttk.Label(self.selection_test_tab, text='Selecciona ALGO' , anchor='center')
    self.selection_test_btns = Option_btns( self.selection_test_tab,
                                            Btn_UP_name='PRUEBAS\nDE\nCONEXIÓN',
                                            Btn_DOWN_name='PRUEBA\nDE\nSENSORES',
                                            height= self.motitor_tank_size[1])

    #Para sensor tab
    self.seed_level_monitor = Tank_monitor(self.sensores_test_tab, size= self.motitor_tank_size, 
                                      level= tank_parameters[0], tank_number=1, 
                                      SeedOuputs= (tank_parameters[1], tank_parameters[2]))
    self.selection_tank_btns = Option_btns(self.sensores_test_tab, Btn_UP_name= 'TOLVA1', Btn_DOWN_name= ' ', 
                              height= self.motitor_tank_size[1])
    self.set_back_btns = Select_btns(self.sensores_test_tab, Btn_OK_name= 'ACEPTAR', Btn_BACK_name= 'ATRAS')
    self.odometry_tractor_monitor = Odometry_monitor(self.sensores_test_tab,odometry_data= self.odometry_parameters)
    self.set_back_btns.Btn_OK.grid_forget()
    self.selection_tank_btns.Btn_DOWN.grid_forget()
    
    #Para conextion tab 
    self.conextion_test_btns = Option_btns(self.conection_test_tab,
                                            Btn_UP_name='PRUEBA\nCONEXIÓN\nINALAMBRICA',
                                            Btn_DOWN_name='PRUEBA\nINTERCONEXIÓN\nMÓDULOS',
                                            height= self.motitor_tank_size[1])
    self.conection_title1_label = ttk.Label(self.conection_test_tab, 
                                            text='Estado de Conexión', anchor='center')
    self.conection_state_label = ttk.Label( self.conection_test_tab, 
                                            text='COLOCA IMAGEN AQUI XD', anchor='center')
    self.conection_title2_label = ttk.Label(self.conection_test_tab,
                                            text='Módulos Disponibles', anchor='center')
    self.conection_module_list = ttk.Treeview(self.conection_test_tab,
                                              columns=('Tipo de Módulo','Función'),
                                              show='headings')
    self.conection_setBack_btns = Select_btns(self.conection_test_tab,
                                              Btn_OK_name='OCULTAR',
                                              Btn_BACK_name='ATRAS')
    self.conection_setBack_btns.Btn_OK.grid_forget()

    #-- empaquedato en grid --
    self.selection_test_tab.grid(row=0, column=0, sticky='nswe')
    self.selection_test_btns.grid(row=0, column=0, sticky='nswe')
    self.maid_descrip_label.grid(row=0, column=1, sticky='nswe')


    #->self.sensores_test_tab.grid(row=0, column=0, sticky='nswe')
    self.seed_level_monitor.grid(row=0, column=1, columnspan=2, sticky='nswe')
    self.selection_tank_btns.grid(row=0, column=0, sticky='nswe')
    self.odometry_tractor_monitor.grid(row=0,column=3, sticky= 'nswe')
    self.set_back_btns.grid(row=1, column=3, sticky= 'nswe')

    #->self.conection_test_tab.grid(row=0, column=0, sticky='nswe')
    self.conextion_test_btns.grid(row=0,rowspan=5,column=0, sticky='nswe')
    self.conection_title1_label.grid(row=0,column=1, sticky='nswe')
    self.conection_state_label.grid(row=1, column=1, sticky='nswe')
    self.conection_title2_label.grid(row=2,column=1, sticky='nswe')
    self.conection_module_list.grid(row=3, column=1, sticky='nswe')
    self.conection_setBack_btns.grid(row=4,column=1, sticky='nswe')


    #-- eventos --
    def change2SensorTestTab():
      self.selection_test_tab.grid_forget()
      self.conection_test_tab.grid_forget()
      self.sensores_test_tab.grid(row=0, column=0, sticky='nswe')

    def change2SelectTestTab():
      self.sensores_test_tab.grid_forget()
      self.conection_test_tab.grid_forget()
      self.selection_test_tab.grid(row=0, column=0, sticky='nswe')
    
    def change2ConectionTestTab():
      self.selection_test_tab.grid_forget()
      self.sensores_test_tab.grid_forget()
      self.conection_test_tab.grid(row=0, column=0, sticky='nswe')


    self.selection_test_btns.config_fuctions( Btn_UP_func= change2ConectionTestTab,
                                              Btn_DOWN_func= change2SensorTestTab)
    self.set_back_btns.config_fuctions( Btn_OK_func= lambda: print('xd'),
                                        Btn_BACK_func= change2SelectTestTab)
    self.conection_setBack_btns.config_fuctions(Btn_OK_func= lambda: print('ocultar boton'),
                                                Btn_BACK_func= change2SelectTestTab)

#----------------------- variables tkinter -------------------------------------
level1 = tk.IntVar(value=0)
SeedOut_t1 = (tk.IntVar(value=10),tk.IntVar(value=5))


tractor_odometry = (tk.IntVar(value=0), tk.IntVar(value=10))
tolva_variables = (level1,SeedOut_t1[0],SeedOut_t1[1])


#----------------------- widgets -------------------------------------
panel_pestanas = ttk.Notebook(window, width= int(screen_w), height=int(screen_h*0.99))

pestana_tests = test_tab( panel_pestanas,size=(int(screen_w),int(screen_h*0.99)),
                          tank_parameters= tolva_variables, odometry_parameters= tractor_odometry)


pestana_monitor = ttk.Frame(panel_pestanas, width= int(screen_w), height=int(screen_h*0.95))
pestana_monitor.columnconfigure((0,1), weight=2)
pestana_monitor.columnconfigure(2, weight=1)
pestana_monitor.rowconfigure(0,weight=9)
pestana_monitor.rowconfigure(1,weight=1)


tank_canvas_size_o = (int(screen_w*0.25) , int(screen_h*0.85))





monitor1_1  = Tank_monitor( pestana_monitor, size= tank_canvas_size_o,
                            level= level1, tank_number=1, SeedOuputs= SeedOut_t1)


#----------------------- enpaquetado -------------------------------------
panel_pestanas.add(pestana_tests ,   text= '     PRUEBAS     ')
panel_pestanas.add(pestana_monitor , text= '     MONITOR     ')
panel_pestanas.pack(expand=True)


monitor1_1.grid(row=0,column=0, sticky= 'ns')


#----------------------- EVENTOS ---------------------- ---------------
def incress_level(event):
  level1.set(level1.get()+1)
  #monitor1.update_level()

def decress_level(event):
  level1.set(level1.get()-1)
  #monitor1.update_level()
  

window.bind('<KeyPress-w>', incress_level)
window.bind('<KeyPress-s>', decress_level)
window.bind('<KeyPress-o>', lambda event: tractor_odometry[0].set(tractor_odometry[0].get() + 1))
window.bind('<KeyPress-l>', lambda event: tractor_odometry[0].set(tractor_odometry[0].get() - 1))

#lateral_select.config_fuctions(lambda: level1.set(level1.get()+1), lambda: level1.set(level1.get()-1))


#----------------------- Ciclo principal donde corre el programa de la interfaz -------------------------------------
window.mainloop() #este metodo esta en ejecuncion hasta que se cierre la ventana creada