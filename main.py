import numpy as np

def validar_datos(matriz, vector, dias):
    # Valida que los datos de entrada
    if not (60 <= dias <= 90):
        print("\n ERROR: Número de días inválido (Debe ser entre 60 y 90).")
        return False
    
    for i, fila in enumerate(matriz):
        if not np.isclose(np.sum(fila), 1.0):
            print(f"\n ERROR: La fila {i+1} de la matriz no suma 100%.")
            return False
            
    if not np.isclose(np.sum(vector), 1.0):
        print("\n ERROR: El vector de probabilidad inicial debe sumar 100%.")
        return False
        
    return True

def generar_matriz_desde_historico(datos, n_estados=4):
    # Calcula la matriz de probabilidad basada en cuantas veces cambió el clima en el pasado
    matriz_conteos = np.zeros((n_estados, n_estados))
    
    for i in range(len(datos) - 1):
        estado_actual = datos[i] - 1
        estado_siguiente = datos[i+1] - 1
        if 0 <= estado_actual < n_estados and 0 <= estado_siguiente < n_estados:
            matriz_conteos[estado_actual][estado_siguiente] += 1
            
    matriz_prob = np.zeros((n_estados, n_estados))
    
    for i in range(n_estados):
        suma_fila = np.sum(matriz_conteos[i])
        if suma_fila > 0:
            matriz_prob[i] = matriz_conteos[i] / suma_fila
        else:
            matriz_prob[i] = np.full(n_estados, 1.0 / n_estados)
            
    return matriz_prob

def mostrar_matriz(matriz, estados):
    # Muestra la matriz de transición
    print("\n[MATRIZ DE TRANSICIÓN P - PROBABILIDADES DE CAMBIO]")
    header = "          " + "  ".join([f"{est[:10]:>10}" for est in estados])
    print(header)
    for i, fila in enumerate(matriz):
        row_str = f"{estados[i][:10]:>10} " + "  ".join([f"{val*100:9.1f}%" for val in fila])
        print(row_str)

def obtener_recomendacion(estado):
    # Retorna un consejo agrícola basado en el clima pronosticado
    recomendaciones = {
        "Soleado": "Óptimo para riego intensivo y cosecha. Proteger cultivos sensibles al calor.",
        "Nublado": "Baja evapotranspiración. Reducir riego y monitorear posible presencia de hongos.",
        "Parcialmente Nublado": "Condiciones moderadas. Ideal para aplicación de fertilizantes.",
        "Parcialmente Soleado": "Buen clima para mantenimiento general y control de plagas."
    }
    return recomendaciones.get(estado, "Sin recomendación específica.")

def ejecutar_agromarkov():
    print("\n" + "="*50)
    print("           SISTEMA DE APOYO AGROMARKOV          ")
    print("="*50)
    
    estados = ["Soleado", "Nublado", "P. Nublado", "P. Soleado"]
    
    # 1. Validación de Selección de Modelo
    while True:
        print("\n[CONFIGURACIÓN DEL MODELO]")
        print("1. Usar matriz estándar (Predefinida)")
        print("2. Generar matriz desde históricos (Datos reales)")
        try:
            opcion_modelo = int(input("\nSeleccione una opción (1-2): "))
            if opcion_modelo in [1, 2]:
                break
            else:
                print("-" * 60)
                print(" Error: Opción inválida. Elija 1 o 2.")
                print("-" * 60)
        except ValueError:
            print(" Error: Debe ingresar un número entero.")

    if opcion_modelo == 2:
        while True:
            print("\nIngrese la secuencia de climas pasados (1:Sol, 2:Nub, 3:P.Nub, 4:P.Sol):")
            print("Ejemplo: 1,1,2,3,1,4,2,1")
            entrada = input("Secuencia: ")
            try:
                datos_historicos = [int(x.strip()) for x in entrada.split(",")]
                if len(datos_historicos) >= 2:
                    matriz_transicion = generar_matriz_desde_historico(datos_historicos)
                    print("\n Matriz calculada exitosamente.")
                    break
                else:
                    print("Error: Se necesitan al menos 2 datos para calcular.")
            except ValueError:
                print("Error: Formato incorrecto.")
    else:
        matriz_transicion = np.array([
            [0.6, 0.2, 0.1, 0.1],
            [0.3, 0.4, 0.2, 0.1],
            [0.2, 0.2, 0.4, 0.2],
            [0.2, 0.1, 0.2, 0.5]
        ])
        print("\n Usando matriz estándar.")

    mostrar_matriz(matriz_transicion, estados)

    # 2. Validación de Días Acumulados
    while True:
        try:
            dias_n = int(input("\nIngrese cantidad de días acumulados (60-90): "))
            if 60 <= dias_n <= 90:
                break
            else:
                print("-" * 60)
                print("Error: El número de días debe estar entre 60 y 90.")
                print("-" * 60)
        except ValueError:
            print("Error: Debe ingresar un número entero.")

    # 3. Validación de Clima Actual
    while True:
        print("\n¿Clima de HOY?")
        for i, estado in enumerate(estados):
            print(f"{i + 1}. {estado}")
        try:
            opcion_clima = int(input("Elija (1-4): "))
            if 1 <= opcion_clima <= 4:
                break
            else:
                print("-" * 60)
                print("Error: Opción inválida. Elija un número del 1 al 4.")
                print("-" * 60)
        except ValueError:
            print("Error: Debe ingresar un número entero.")

    vector_inicial = np.zeros(4)
    vector_inicial[opcion_clima - 1] = 1.0

    # Predicción final
    if validar_datos(matriz_transicion, vector_inicial, dias_n):
        print("\n" + "-"*60)
        print(f" PREDICCIÓN BASADA EN EL MODELO MARKOVIANO (A PARTIR DEL DÍA {dias_n})")
        print(" Fórmula: Vn = V0 * P^n")
        print("-"*60)
        
        for i in range(1, 5):
            matriz_potencia = np.linalg.matrix_power(matriz_transicion, i)
            vector_prediccion = np.dot(vector_inicial, matriz_potencia)
            
            dia_futuro = dias_n + i
            indice_max = np.argmax(vector_prediccion)
            clima_predicho = estados[indice_max]
            prob_max = vector_prediccion[indice_max] * 100
            
            print(f"\nDía {dia_futuro}: {clima_predicho.upper()} ({prob_max:.1f}%)")
            print(f"RECOMENDACIÓN: {obtener_recomendacion(clima_predicho)}")
            
            prob_str = "Detalle: " + " | ".join([f"{estados[j]}: {vector_prediccion[j]*100:.1f}%" for j in range(4)])
            print(prob_str)
        
        print("\n" + "-"*60)

if __name__ == "__main__":
    while True:
        ejecutar_agromarkov()
        print("\n" + "="*50)
        continuar = input("¿Desea realizar otra predicción? (s/n): ").lower()
        if continuar != 's':
            print("Saliendo del programa")
            break 