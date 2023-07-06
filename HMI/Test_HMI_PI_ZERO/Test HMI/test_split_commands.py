texto = "conetion_status = true, false, true"

# Dividir el texto en partes utilizando la coma como separador
comando,valores = texto.split('=')
print(comando, len(comando))
print(valores)

# Analizar cada parte para extraer el comando y los valores asociados

# Verificar que el comando sea "conetion_status"
if comando=="conetion_status ":
    datos = valores.split(',')
    # Asignar los valores a la lista "status"
    status = [valor.strip() for valor in datos]
    for i in range(len(status)):
        if status[i]=='true':
            status[i] = True
        else:
            status[i] = False
    print("Comando:", comando)
    print("Valores:", status)
else:
    print("Comando inválido")

if(status[0]):
    print('Si funciona como boll')