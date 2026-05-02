import numpy as np

def validar_datos(matriz, vector, dias):

    if not (60 <= dias <= 90):
        print("\nERROR: Número de días inválido.")
        return False
    
    for i, fila in enumerate(matriz):
        if not np.isclose(np.sum(fila), 1.0):
            print(f"\nERROR: La fila {i+1} de la matriz no suma 1.")
            return False
            
    if not np.isclose(np.sum(vector), 1.0):
        print("\nERROR: El vector de probabilidad inicial debe sumar 1.")
        return False
        
    return True

def generar_matriz_desde_historico(datos, n_estados=4):
    """
    Calcula la matriz de transición a partir de una secuencia de estados históricos.
    Aplica el concepto de frecuencias relativas para obtener probabilidades.
    """
    matriz_conteos = np.zeros((n_estados, n_estados))
    
    # Contar transiciones entre estados consecutivos
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
            # Si un estado no tiene transiciones registradas, se asigna equiprobabilidad
            matriz_prob[i] = np.full(n_estados, 1.0 / n_estados)
            
    return matriz_prob

def agromarkov():
    print("========================================")
    print("           SISTEMA AGROMARKOV           ")
    print("========================================")
    
    estados = ["Soleado", "Nublado", "Parcialmente Nublado", "Parcialmente Soleado"]
    
    print("\n[CONFIGURACIÓN DEL MODELO]")
    print("1. Usar matriz de transición por defecto")
    print("2. Generar matriz a partir de datos históricos (Recomendado)")
    
    try:
        opcion_modelo = int(input("\nSeleccione una opción: "))
    except ValueError:
        print("Error: Ingrese un número válido.")
        return

    if opcion_modelo == 2:
        print("\nIngrese la secuencia de climas de los últimos días usando números:")
        print("1: Soleado, 2: Nublado, 3: Parcialmente Nublado, 4: Parcialmente Soleado")
        print("Ejemplo: 1,2,1,1,3,4,2,1")
        entrada = input("Secuencia: ")
        try:
            datos_historicos = [int(x.strip()) for x in entrada.split(",")]
            if len(datos_historicos) < 2:
                print("Error: Se necesitan al menos 2 datos para calcular transiciones.")
                return
            matriz_transicion = generar_matriz_desde_historico(datos_historicos)
            print("\n✅ Matriz de transición generada con éxito a partir de frecuencias.")
        except ValueError:
            print("Error: Formato de datos inválido.")
            return
    else:
        # MATRIZ DE TRANSICIÓN POR DEFECTO (ESTOCÁSTICA)
        matriz_transicion = np.array([
            [0.6, 0.2, 0.1, 0.1],  # Soleado
            [0.3, 0.4, 0.2, 0.1],  # Nublado
            [0.2, 0.2, 0.4, 0.2],  # Parcialmente Nublado
            [0.2, 0.1, 0.2, 0.5]   # Parcialmente Soleado
        ])
        print("\nℹ️ Usando matriz de transición estándar.")

    try:
        dias_n = int(input("\nIngrese la cantidad de días actuales acumulados (60-90): "))
    except ValueError:
        print("Error: Debe ingresar un número entero válido.")
        return

    print("\n¿Cuál es el estado del clima el día de HOY?")
    for i, estado in enumerate(estados):
        print(f"{i + 1}. {estado}")
        
    try:
        opcion_clima = int(input("Elija una opción (1-4): "))
        if opcion_clima < 1 or opcion_clima > 4:
            print("Error: Opción inválida.")
            return
    except ValueError:
        print("Error: Debe ingresar un número entero.")
        return

    vector_inicial = np.zeros(4)
    vector_inicial[opcion_clima - 1] = 1.0

    # Predicción
    if validar_datos(matriz_transicion, vector_inicial, dias_n):
        print("-----------------------------------------------------------")
        print(f" PREDICCIÓN DE ESTADOS FUTUROS (A PARTIR DEL DÍA {dias_n})")
        print("   Fórmula utilizada: Vn = V0 * P^n")
        print("-----------------------------------------------------------")
        
        # Realizamos las predicciones para los días n+1, n+2, n+3, n+4
        for i in range(1, 5):
            # Aplicación estricta de la fórmula matemática: Vn = V0 * P^i
            # P^i se calcula usando la potencia de la matriz de transición
            matriz_potencia = np.linalg.matrix_power(matriz_transicion, i)
            vector_prediccion = np.dot(vector_inicial, matriz_potencia)
            
            dia_futuro = dias_n + i
            indice_max = np.argmax(vector_prediccion)
            
            print(f"\n▶ Día {dia_futuro}: PRONÓSTICO -> {estados[indice_max]} ({vector_prediccion[indice_max]*100:.2f}%)")

            for j, est in enumerate(estados):
                print(f"   - {est}: {vector_prediccion[j]*100:.2f}%")
        
        print("\n" + "-----------------------------------------------------------")

if __name__ == "__main__":
    agromarkov()