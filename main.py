import numpy as np

def validar_datos(matriz, vector, dias):

    if not (60 <= dias <= 90):
        print("\nERROR: Número de días inválido, debe estar entre 60 y 90.")
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
    print("--- SISTEMA AGROMARKOV: APOYO AGRÍCOLA ---")
    
    # Estads climáticos
    estados = ["Soleado", "Nublado", "Parcialmente Nublado", "Parcialmente Soleado"]
    
    # Ingreso datos
    try:
        dias_n = int(input("Ingrese la cantidad de días actuales (60-90): "))
    except ValueError:
        print("Error: Ingrese un número entero válido.")
        return

    # Matriz 4x4
    matriz_transicion = np.array([
        [0.6, 0.2, 0.1, 0.1], # Desde Soleado
        [0.3, 0.4, 0.2, 0.1], # Desde Nublado
        [0.2, 0.2, 0.4, 0.2], # Desde Parcialmente Nublado
        [0.2, 0.1, 0.2, 0.5]  # Desde Parcialmente Soleado
    ])

    vector_inicial = np.array([1.0, 0.0, 0.0, 0.0])

    if validar_datos(matriz_transicion, vector_inicial, dias_n):
        print("\n--- PREDICCIÓN DE ESTADOS FUTUROS ---")
        vector_actual = vector_inicial
        
        # Cálculo de predicciones
        for i in range(1, 5):
            vector_actual = np.dot(vector_actual, matriz_transicion)
            
            dia_futuro = dias_n + i
            indice_max = np.argmax(vector_actual)
            
            print(f"Día {dia_futuro}: {estados[indice_max]} ({vector_actual[indice_max]*100:.2f}%)")
            for j, est in enumerate(estados):
                print(f"   - {est}: {vector_actual[j]*100:.2f}%")

if __name__ == "__main__":
    agromarkov()