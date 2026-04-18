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

def agromarkov():
    print("AGROMARKOV")
    
    # Climas
    estados = ["Soleado", "Nublado", "Parcialmente Nublado", "Parcialmente Soleado"]
    
    try:
        dias_n = int(input("\nIngrese la cantidad de días actuales (60-90): "))
    except ValueError:
        print("Error: Debe ingresar un número entero válido.")
        return

    print("\n¿Cuál es el estado del clima el día de HOY?")
    for i, estado in enumerate(estados):
        print(f"{i + 1}. {estado}")
        
    try:
        opcion_clima = int(input("Elija una opción (1-4): "))
        if opcion_clima < 1 or opcion_clima > 4:
            print("Error: Opción inválida. Debe ser un número del 1 al 4.")
            return
    except ValueError:
        print("Error: Debe ingresar un número entero.")
        return

    vector_inicial = np.zeros(4)
    vector_inicial[opcion_clima - 1] = 1.0

    # MATRIZ DE TRANSICIÓN ESTOCÁSTICA
    matriz_transicion = np.array([
        [0.6, 0.2, 0.1, 0.1],  # Soleado
        [0.3, 0.4, 0.2, 0.1],  # Nblado
        [0.2, 0.2, 0.4, 0.2],  # Parcialmente Nublado
        [0.2, 0.1, 0.2, 0.5]   # Parcialmente Soleado
    ])

    # Predicción
    if validar_datos(matriz_transicion, vector_inicial, dias_n):
        print("-----------------------------------------------------------")
        print(f" PREDICCIÓN DE ESTADOS FUTUROS (A PARTIR DEL DÍA {dias_n})")
        print("-----------------------------------------------------------")
        
        vector_actual = vector_inicial
        
        for i in range(1, 5):
            vector_actual = np.dot(vector_actual, matriz_transicion)
            
            dia_futuro = dias_n + i
            indice_max = np.argmax(vector_actual)
            
            print(f"\n▶ Día {dia_futuro}: PRONÓSTICO -> {estados[indice_max]} ({vector_actual[indice_max]*100:.2f}%)")

            for j, est in enumerate(estados):
                print(f"   - {est}: {vector_actual[j]*100:.2f}%")
        
        print("\n" + "-----------------------------------------------------------")

if __name__ == "__main__":
    agromarkov()