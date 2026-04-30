import csv
import os
import matplotlib.pyplot as plt

# Creamos la carpeta resultados para guardar todos los archivos generados.
os.makedirs("resultados", exist_ok=True)


# Esta función inicializa las estadísticas de un equipo si todavía no existe.
def inicializar_equipo(tabla_posiciones, equipo):
    if equipo not in tabla_posiciones:
        tabla_posiciones[equipo] = {
            "PJ": 0,
            "PG": 0,
            "PE": 0,
            "PP": 0,
            "GF": 0,
            "GC": 0,
            "PTS": 0
        }


# Esta función suma una victoria al equipo recibido.
def sumar_victoria(victorias, equipo):
    if equipo not in victorias:
        victorias[equipo] = 0

    victorias[equipo] = victorias[equipo] + 1


# Esta función acumula los goles de cada equipo.
def sumar_goles(goles_por_equipo, equipo, goles):
    if equipo not in goles_por_equipo:
        goles_por_equipo[equipo] = 0

    goles_por_equipo[equipo] = goles_por_equipo[equipo] + goles


# Ordenamos un diccionario de mayor a menor según sus valores.
def ordenar_diccionario(diccionario):
    return sorted(diccionario.items(), key=lambda item: item[1], reverse=True)


# Ordenamos la tabla de posiciones por puntos, diferencia de gol y goles a favor.
def ordenar_tabla(tabla_posiciones):
    return sorted(
        tabla_posiciones.items(),
        key=lambda item: (
            item[1]["PTS"],
            item[1]["GF"] - item[1]["GC"],
            item[1]["GF"]
        ),
        reverse=True
    )


# Diccionarios donde vamos a acumular los resultados del análisis.
victorias = {}
goles_por_equipo = {}
tabla_posiciones = {}

total_partidos = 0
total_goles = 0
cantidad_empates = 0


# Abrimos el archivo CSV con los resultados de los partidos.
# Usamos DictReader porque permite acceder a cada columna por su nombre.
with open("datos/filtered_data.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        equipo_local = fila["HomeTeam"]
        equipo_visitante = fila["AwayTeam"]

        goles_local = int(fila["FTHG"])
        goles_visitante = int(fila["FTAG"])

        resultado = fila["FTR"]

        # Inicializamos los equipos para poder acumular sus estadísticas.
        inicializar_equipo(tabla_posiciones, equipo_local)
        inicializar_equipo(tabla_posiciones, equipo_visitante)

        total_partidos = total_partidos + 1
        total_goles = total_goles + goles_local + goles_visitante

        # Sumamos un partido jugado para ambos equipos.
        tabla_posiciones[equipo_local]["PJ"] = tabla_posiciones[equipo_local]["PJ"] + 1
        tabla_posiciones[equipo_visitante]["PJ"] = tabla_posiciones[equipo_visitante]["PJ"] + 1

        # Sumamos goles a favor y goles en contra para construir la tabla de posiciones.
        tabla_posiciones[equipo_local]["GF"] = tabla_posiciones[equipo_local]["GF"] + goles_local
        tabla_posiciones[equipo_local]["GC"] = tabla_posiciones[equipo_local]["GC"] + goles_visitante

        tabla_posiciones[equipo_visitante]["GF"] = tabla_posiciones[equipo_visitante]["GF"] + goles_visitante
        tabla_posiciones[equipo_visitante]["GC"] = tabla_posiciones[equipo_visitante]["GC"] + goles_local

        # Sumamos goles a favor sin importar si el equipo jugó de local o visitante.
        sumar_goles(goles_por_equipo, equipo_local, goles_local)
        sumar_goles(goles_por_equipo, equipo_visitante, goles_visitante)

        # Según el valor de FTR determinamos quién ganó.
        # H = gana local - A = gana visitante - D = empate.
        if resultado == "H":
            sumar_victoria(victorias, equipo_local)

            tabla_posiciones[equipo_local]["PG"] = tabla_posiciones[equipo_local]["PG"] + 1
            tabla_posiciones[equipo_local]["PTS"] = tabla_posiciones[equipo_local]["PTS"] + 3

            tabla_posiciones[equipo_visitante]["PP"] = tabla_posiciones[equipo_visitante]["PP"] + 1

        elif resultado == "A":
            sumar_victoria(victorias, equipo_visitante)

            tabla_posiciones[equipo_visitante]["PG"] = tabla_posiciones[equipo_visitante]["PG"] + 1
            tabla_posiciones[equipo_visitante]["PTS"] = tabla_posiciones[equipo_visitante]["PTS"] + 3

            tabla_posiciones[equipo_local]["PP"] = tabla_posiciones[equipo_local]["PP"] + 1

        else:
            cantidad_empates = cantidad_empates + 1

            tabla_posiciones[equipo_local]["PE"] = tabla_posiciones[equipo_local]["PE"] + 1
            tabla_posiciones[equipo_visitante]["PE"] = tabla_posiciones[equipo_visitante]["PE"] + 1

            tabla_posiciones[equipo_local]["PTS"] = tabla_posiciones[equipo_local]["PTS"] + 1
            tabla_posiciones[equipo_visitante]["PTS"] = tabla_posiciones[equipo_visitante]["PTS"] + 1


# Calculamos el promedio de goles por partido.
# Validamos que haya partidos para evitar dividir por cero.
if total_partidos > 0:
    promedio_goles = total_goles / total_partidos
else:
    promedio_goles = 0


# Ordenamos resultados para mostrar rankings.
victorias_ordenadas = ordenar_diccionario(victorias)
goles_ordenados = ordenar_diccionario(goles_por_equipo)
tabla_ordenada = ordenar_tabla(tabla_posiciones)


# Generamos el archivo resumen.txt.
# Este archivo deja evidencia del análisis realizado y permite revisar los resultados sin tener que ejecutar nuevamente el programa.
with open("resultados/resumen.txt", "w", encoding="utf-8") as resumen:
    resumen.write("RESUMEN DEL ANÁLISIS DE RESULTADOS DEPORTIVOS\n")
    resumen.write("------------------------------------------------\n\n")

    resumen.write(f"Cantidad total de partidos analizados: {total_partidos}\n")
    resumen.write(f"Cantidad total de goles: {total_goles}\n")
    resumen.write(f"Promedio de goles por partido: {promedio_goles:.2f}\n")
    resumen.write(f"Cantidad de empates: {cantidad_empates}\n\n")

    resumen.write("CANTIDAD DE PARTIDOS GANADOS POR CADA EQUIPO:\n")
    for equipo, cantidad in victorias_ordenadas:
        resumen.write(f"{equipo}: {cantidad} partidos ganados\n")

    resumen.write("\nTABLA DE POSICIONES:\n")
    resumen.write("Equipo | PJ | PG | PE | PP | GF | GC | DG | PTS\n")
    resumen.write("------------------------------------------------\n")

    for equipo, datos in tabla_ordenada:
        diferencia_gol = datos["GF"] - datos["GC"]

        resumen.write(
            f"{equipo} | "
            f"{datos['PJ']} | "
            f"{datos['PG']} | "
            f"{datos['PE']} | "
            f"{datos['PP']} | "
            f"{datos['GF']} | "
            f"{datos['GC']} | "
            f"{diferencia_gol} | "
            f"{datos['PTS']}\n"
        )

    resumen.write("\nTOP 5 EQUIPOS CON MÁS GOLES A FAVOR:\n")
    for equipo, cantidad in goles_ordenados[:5]:
        resumen.write(f"{equipo}: {cantidad} goles\n")


# Generamos también la tabla de posiciones en CSV.
# Esto permite abrirla en Excel o incluirla fácilmente en el informe final.
with open("resultados/tabla_posiciones.csv", "w", encoding="utf-8", newline="") as archivo_csv:
    escritor = csv.writer(archivo_csv)

    escritor.writerow(["Equipo", "PJ", "PG", "PE", "PP", "GF", "GC", "DG", "PTS"])

    for equipo, datos in tabla_ordenada:
        diferencia_gol = datos["GF"] - datos["GC"]

        escritor.writerow([
            equipo,
            datos["PJ"],
            datos["PG"],
            datos["PE"],
            datos["PP"],
            datos["GF"],
            datos["GC"],
            diferencia_gol,
            datos["PTS"]
        ])


# Gráfico rendimiento entre equipos.
# Usamos los puntos como indicador principal de rendimiento porque resumen victorias y empates.
top_tabla = tabla_ordenada[:10]
equipos_rendimiento = [item[0] for item in top_tabla]
puntos_rendimiento = [item[1]["PTS"] for item in top_tabla]

plt.figure(figsize=(10, 6))
plt.bar(equipos_rendimiento, puntos_rendimiento)
plt.title("Rendimiento entre equipos")
plt.xlabel("Equipo")
plt.ylabel("Puntos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("resultados/grafico_rendimiento.png")
plt.close()


print("Análisis finalizado correctamente.")
print(f"Partidos analizados: {total_partidos}")
print(f"Promedio de goles por partido: {promedio_goles:.2f}")
print("Se generaron los archivos resumen.txt, tabla_posiciones.csv y grafico_rendimiento.png.")
