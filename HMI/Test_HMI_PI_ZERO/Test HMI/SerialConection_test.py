import serial.tools.list_ports

def update_COM_PORT():
  global com_port
  ports = serial.tools.list_ports.comports()
  coms = [com[0] for com in ports]
  coms.insert(0, '-')
  if len(coms) > 1:
    com_port = str(coms[1])
  else:
    com_port = str(coms[0])
  #print(com_port)


def conect_Serial():
  global conected
  conected = False
  if com_port != '-':
    conected = True
    print(com_port, 115200)

  else:
    conected = False
    print('No Serial Port')


def read_serial():
  if comunication.readable :
    read = comunication.readline()
    data = read.decode('utf8') 
    try:
      #if len(read)>0 and read == b"\n" :
      if len(data)>0 :
        print(data)
      
    except:
      print('error')

update_COM_PORT()

conect_Serial()

if conected:
  global comunication
  comunication = serial.Serial(port=com_port, baudrate=115200)
  print('Succesfully conected')

while(conected and comunication.is_open):
  read_serial()

if conected:
  comunication.close()