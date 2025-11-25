import machine
import time

llave = 100
uart = machine.UART(0, baudrate=9600)

print("Receptor Pico W listo...")

# --- Función de Ayuda para evitar errores ---
def convertir_seguro(dato_recibido):
    """
    Intenta convertir el dato a entero.
    Si falla o está vacío, devuelve None.
    """
    if dato_recibido is None:
        return None
    
    # Limpiamos espacios y saltos de línea
    texto_limpio = dato_recibido.strip()
    
    # Verificamos que no esté vacío y que sean solo dígitos
    if len(texto_limpio) > 0 and texto_limpio.isdigit():
        try:
            return int(texto_limpio)
        except:
            return None
    else:
        return None

while True:
    try:
        if uart.any():
            # Leemos las 4 líneas
            raw_luz = uart.readline()
            raw_temp = uart.readline()
            raw_ant = uart.readline()
            raw_agua = uart.readline()

            # Intentamos convertir usando nuestra función segura
            # Si algo sale mal, la variable valdrá None
            Luz_Cifrada = convertir_seguro(raw_luz)
            Temp_Cifrada = convertir_seguro(raw_temp)
            Ant_Cifrada = convertir_seguro(raw_ant)
            Agua_Cifrada = convertir_seguro(raw_agua)

            # VERIFICACIÓN: Solo procesamos si LOS 4 DATOS son válidos
            # Si alguno es None, saltamos esta vuelta y esperamos la siguiente limpia
            if (Luz_Cifrada is None or Temp_Cifrada is None or 
                Ant_Cifrada is None or Agua_Cifrada is None):
                # Opcional: imprimir un aviso pequeño si quieres depurar
                # print("Lectura incompleta o sucia, reintentando...")
                continue 

            # --- A partir de aquí todo es seguro ---
            
            # Desencriptar
            ValorLuz = Luz_Cifrada ^ llave
            ValorTemp = Temp_Cifrada ^ llave
            ValorAnt = Ant_Cifrada ^ llave
            ValorAgua = Agua_Cifrada ^ llave

            # Procesar Luz
            if ValorLuz > 200:
                print(f"Valor Luz: Dia ({ValorLuz})")
            else:
                print(f"Valor Luz: Noche ({ValorLuz})")

            # Procesar Temperatura
            temp_calculada = ValorTemp * 0.488
            # Usamos "%.2f" para mostrar solo 2 decimales y que se vea limpio
            print("valor Tem: {:.2f}".format(temp_calculada))

            # Procesar Resto
            print(f"valor Ant: {ValorAnt}")
            print(f"valor Agua: {ValorAgua}")
            print("-" * 20) # Separador visual

    except Exception as e:
        print(f"Error inesperado: {e}")
        # Limpiamos el buffer si hubo un error grave
        while uart.any():
            uart.read()
            
    time.sleep_ms(50)
