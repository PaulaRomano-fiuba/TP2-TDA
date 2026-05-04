import sys

def main():
    if len(sys.argv) < 2:
        print("falta el archivo pa")
        return
    
    ruta_archivo = sys.argv[1]

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = [linea.strip() for linea in f if linea.strip()]

    if len(lineas) < 1:
        raise ValueError("El archivo está vacío o mal formado")

    n = int(lineas[0])
    if len(lineas) != 1 + 2 * n:
        raise ValueError(
            f"Cantidad de líneas incorrecta. Se esperaba {1 + 2*n} y hay {len(lineas)}"
        )

    ganancias = [int(lineas[i]) for i in range(1, n + 1)]
    energia = [int(lineas[i]) for i in range(n + 1, 2 * n + 1)]

    matriz = crear_matriz(ganancias, energia)
    print("Ganancia maxima:", matriz[0][0])

    orden = reconstruccion(energia, ganancias, matriz)
    print("Plan de entrenamiento:", orden)


def crear_matriz(dias, energias):
    n = len(dias)
    matriz = [[0] * (n+1) for _ in range(n+1)]
    
    # Caso base: no quedan días
    for fila in range(n+1):
        matriz[fila][n] = 0

    # Llenado de derecha a izquierda
    for col in range(n-1, -1, -1):
        for fila in range(col+1):
            matriz[fila][col] = max(
                matriz[0][col+1],  # descansar
                ganancia_hoy(dias, col, energias, fila) + matriz[fila+1][col+1]  # entrenar
            )
    
    return matriz


def ganancia_hoy(dias, i, energias, j):
    return min(dias[i], energias[j])

def reconstruccion(energias, dias, Matriz):
    n = len(dias)
    res = []
    z = 0  # días consecutivos entrenando
    e = 0  # día actual

    while e < n:
        descanso = Matriz[0][e+1]
        entrenar = ganancia_hoy(dias, e, energias, z) + Matriz[z+1][e+1]

        if entrenar >= descanso:
            res.append("Entreno")
            z += 1
        else:
            res.append("Descansar")
            z = 0

        e += 1

    return res


if __name__ == "__main__":
    main()
