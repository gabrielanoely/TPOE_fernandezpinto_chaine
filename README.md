# Trabajo Práctico: Gestión Colaborativa, Control de Versiones y Organización Empresarial (Git, GitHub y Jira)

## Integrantes del equipo
* **Gabriela Noely Fernández Pinto**
* **Nicolás Marcelo Chaine**

## Escenario Elegido
Seleccionamos el **Escenario D - Estadísticas de Resultados Deportivos**. El objetivo es analizar datos de resultados de un torneo deportivo.

## Descripción del Dataset
Utilizaremos un conjunto de datos en formato CSV que contiene las siguientes columnas
| Name | Type | Format | Description |
| :--- | :--- | :--- | :--- |
| Date | date | %d/%m/%y | Match Date (dd/mm/yy) |
| HomeTeam | string | default | Home Team |
| AwayTeam | string | default | Away Team |
| FTHG | integer | default | Full Time Home Team Goals |
| FTAG | integer | default | Full Time Away Team Goals |
| FTR | string | default | Full Time Result (H=Home Win, D=Draw, A=Away Win) |
| HTHG | integer | default | Half Time Home Team Goals |
| HTAG | integer | default | Half Time Away Team Goals |
| HTR | string | default | Half Time Result (H=Home Win, D=Draw, A=Away Win) |
| HS | integer | default | Home Team Shots |
| AS | integer | default | Away Team Shots |
| HST | integer | default | Home Team Shots on Target |
| AST | integer | default | Away Team Shots on Target |
| HF | integer | default | Home Team Fouls Committed |
| AF | integer | default | Away Team Fouls Committed |
| HC | integer | default | Home Team Corners |
| AC | integer | default | Away Team Corners |
| HY | integer | default | Home Team Yellow Cards |
| AY | integer | default | Away Team Yellow Cards |
| HR | integer | default | Home Team Red Cards |
| AR | integer | default | Away Team Red Cards |

Los datos se encuentran almacenados en la carpeta '/datos' y fueron obtenidos desde https://datahub.io/core/spanish-la-liga#season-2021 season-9900.

## Instrucciones básicas para ejecutar el script
1. Abrir el entorno de Google Colab.
2. Clonar el repositorio https://github.com/gabrielanoely/TPOE_fernandezpinto_chaine.git.
3. Asegurarse de que el dataset se encuentre en la ruta '/datos/filtered_data.csv'.
4. Ejecutar el script ubicado en la carpeta '/scripts' para procesar la información.
5. Los gráficos y tablas resultantes se generarán automáticamente en la carpeta '/resultados'.
