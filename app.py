import math
import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(
    page_title="Calculadora de Tubos ASTM A500",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Catálogo completo de perfiles Tubo Cuadrado ASTM A500 (68 perfiles)
CATALOGO_DATOS = [
    {"selector": "20 x 20 | 0.9 mm", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_mm": 20, "espesor_mm": 0.9, "peso_kg_m": 0.49, "peso_6m_ficha": 2.96, "nota": ""},
    {"selector": "20 x 20 | 1.5 mm", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_mm": 20, "espesor_mm": 1.5, "peso_kg_m": 0.86, "peso_6m_ficha": 5.14, "nota": ""},
    {"selector": "20 x 20 | 2 mm", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_mm": 20, "espesor_mm": 2.0, "peso_kg_m": 1.04, "peso_6m_ficha": 6.24, "nota": ""},
    {"selector": "25 x 25 | 1.5 mm", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_mm": 25, "espesor_mm": 1.5, "peso_kg_m": 1.06, "peso_6m_ficha": 6.37, "nota": ""},
    {"selector": "25 x 25 | 2 mm", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_mm": 25, "espesor_mm": 2.0, "peso_kg_m": 1.46, "peso_6m_ficha": 8.76, "nota": ""},
    {"selector": "25 x 25 | 2.5 mm", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_mm": 25, "espesor_mm": 2.5, "peso_kg_m": 1.67, "peso_6m_ficha": 10.02, "nota": ""},
    {"selector": "25 x 25 | 3 mm", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_mm": 25, "espesor_mm": 3.0, "peso_kg_m": 1.93, "peso_6m_ficha": 11.58, "nota": ""},
    {"selector": "30 x 30 | 1.2 mm", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_mm": 30, "espesor_mm": 1.2, "peso_kg_m": 1.04, "peso_6m_ficha": 6.24, "nota": ""},
    {"selector": "30 x 30 | 1.5 mm", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_mm": 30, "espesor_mm": 1.5, "peso_kg_m": 1.30, "peso_6m_ficha": 7.80, "nota": ""},
    {"selector": "30 x 30 | 1.8 mm", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_mm": 30, "espesor_mm": 1.8, "peso_kg_m": 1.68, "peso_6m_ficha": 10.08, "nota": ""},
    {"selector": "30 x 30 | 2 mm", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_mm": 30, "espesor_mm": 2.0, "peso_kg_m": 1.86, "peso_6m_ficha": 11.16, "nota": ""},
    {"selector": "30 x 30 | 2.5 mm", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_mm": 30, "espesor_mm": 2.5, "peso_kg_m": 2.17, "peso_6m_ficha": 13.02, "nota": ""},
    {"selector": "40 x 40 | 1.5 mm", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_mm": 40, "espesor_mm": 1.5, "peso_kg_m": 1.77, "peso_6m_ficha": 10.62, "nota": ""},
    {"selector": "40 x 40 | 1.8 mm", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_mm": 40, "espesor_mm": 1.8, "peso_kg_m": 2.03, "peso_6m_ficha": 12.18, "nota": ""},
    {"selector": "40 x 40 | 2 mm", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_mm": 40, "espesor_mm": 2.0, "peso_kg_m": 2.24, "peso_6m_ficha": 13.46, "nota": ""},
    {"selector": "40 x 40 | 2.5 mm", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_mm": 40, "espesor_mm": 2.5, "peso_kg_m": 2.99, "peso_6m_ficha": 17.94, "nota": ""},
    {"selector": "40 x 40 | 3 mm", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_mm": 40, "espesor_mm": 3.0, "peso_kg_m": 3.54, "peso_6m_ficha": 21.24, "nota": ""},
    {"selector": "40 x 40 | 4.5 mm", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_mm": 40, "espesor_mm": 4.5, "peso_kg_m": 4.52, "peso_6m_ficha": 27.12, "nota": ""},
    {"selector": "50 x 50 | 1.2 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 1.2, "peso_kg_m": 1.87, "peso_6m_ficha": 11.24, "nota": ""},
    {"selector": "50 x 50 | 1.5 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 1.5, "peso_kg_m": 2.25, "peso_6m_ficha": 13.50, "nota": ""},
    {"selector": "50 x 50 | 1.8 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 1.8, "peso_kg_m": 2.70, "peso_6m_ficha": 16.20, "nota": ""},
    {"selector": "50 x 50 | 2 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 2.0, "peso_kg_m": 3.12, "peso_6m_ficha": 18.73, "nota": ""},
    {"selector": "50 x 50 | 2.5 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 2.5, "peso_kg_m": 3.87, "peso_6m_ficha": 23.23, "nota": ""},
    {"selector": "50 x 50 | 3 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 3.0, "peso_kg_m": 4.49, "peso_6m_ficha": 26.94, "nota": ""},
    {"selector": "50 x 50 | 4 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 4.0, "peso_kg_m": 6.57, "peso_6m_ficha": 39.41, "nota": "Revisar: valor 4 mm mayor que 4,5 mm"},
    {"selector": "50 x 50 | 4.5 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 4.5, "peso_kg_m": 6.02, "peso_6m_ficha": 36.12, "nota": ""},
    {"selector": "50 x 50 | 6 mm", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_mm": 50, "espesor_mm": 6.0, "peso_kg_m": 8.54, "peso_6m_ficha": 51.21, "nota": ""},
    {"selector": "60 x 60 | 2 mm", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_mm": 60, "espesor_mm": 2.0, "peso_kg_m": 3.56, "peso_6m_ficha": 21.36, "nota": ""},
    {"selector": "60 x 60 | 2.5 mm", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_mm": 60, "espesor_mm": 2.5, "peso_kg_m": 4.39, "peso_6m_ficha": 26.34, "nota": ""},
    {"selector": "60 x 60 | 3 mm", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_mm": 60, "espesor_mm": 3.0, "peso_kg_m": 5.19, "peso_6m_ficha": 31.14, "nota": ""},
    {"selector": "60 x 60 | 4 mm", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_mm": 60, "espesor_mm": 4.0, "peso_kg_m": 7.14, "peso_6m_ficha": 42.86, "nota": ""},
    {"selector": "60 x 60 | 4.5 mm", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_mm": 60, "espesor_mm": 4.5, "peso_kg_m": 7.43, "peso_6m_ficha": 44.58, "nota": ""},
    {"selector": "75 x 75 | 1.5 mm", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_mm": 75, "espesor_mm": 1.5, "peso_kg_m": 3.41, "peso_6m_ficha": 20.43, "nota": ""},
    {"selector": "75 x 75 | 2 mm", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_mm": 75, "espesor_mm": 2.0, "peso_kg_m": 4.50, "peso_6m_ficha": 27.00, "nota": ""},
    {"selector": "75 x 75 | 2.5 mm", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_mm": 75, "espesor_mm": 2.5, "peso_kg_m": 5.56, "peso_6m_ficha": 33.36, "nota": ""},
    {"selector": "75 x 75 | 3 mm", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_mm": 75, "espesor_mm": 3.0, "peso_kg_m": 6.81, "peso_6m_ficha": 40.86, "nota": ""},
    {"selector": "75 x 75 | 4 mm", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_mm": 75, "espesor_mm": 4.0, "peso_kg_m": 8.59, "peso_6m_ficha": 51.54, "nota": ""},
    {"selector": "75 x 75 | 4.5 mm", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_mm": 75, "espesor_mm": 4.5, "peso_kg_m": 9.55, "peso_6m_ficha": 57.30, "nota": ""},
    {"selector": "75 x 75 | 6 mm", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_mm": 75, "espesor_mm": 6.0, "peso_kg_m": 13.11, "peso_6m_ficha": 78.66, "nota": ""},
    {"selector": "100 x 100 | 2 mm", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_mm": 100, "espesor_mm": 2.0, "peso_kg_m": 6.17, "peso_6m_ficha": 36.99, "nota": ""},
    {"selector": "100 x 100 | 2.5 mm", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_mm": 100, "espesor_mm": 2.5, "peso_kg_m": 7.68, "peso_6m_ficha": 46.05, "nota": ""},
    {"selector": "100 x 100 | 3 mm", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_mm": 100, "espesor_mm": 3.0, "peso_kg_m": 9.20, "peso_6m_ficha": 55.21, "nota": ""},
    {"selector": "100 x 100 | 4 mm", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_mm": 100, "espesor_mm": 4.0, "peso_kg_m": 12.17, "peso_6m_ficha": 73.03, "nota": ""},
    {"selector": "100 x 100 | 4.5 mm", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_mm": 100, "espesor_mm": 4.5, "peso_kg_m": 13.59, "peso_6m_ficha": 81.56, "nota": ""},
    {"selector": "100 x 100 | 6 mm", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_mm": 100, "espesor_mm": 6.0, "peso_kg_m": 16.98, "peso_6m_ficha": 101.88, "nota": ""},
    {"selector": "100 x 100 | 9.5 mm", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_mm": 100, "espesor_mm": 9.5, "peso_kg_m": 25.70, "peso_6m_ficha": 154.20, "nota": ""},
    {"selector": "125 x 125 | 3 mm", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_mm": 125, "espesor_mm": 3.0, "peso_kg_m": 11.31, "peso_6m_ficha": 67.86, "nota": ""},
    {"selector": "125 x 125 | 4 mm", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_mm": 125, "espesor_mm": 4.0, "peso_kg_m": 14.87, "peso_6m_ficha": 89.22, "nota": ""},
    {"selector": "125 x 125 | 4.5 mm", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_mm": 125, "espesor_mm": 4.5, "peso_kg_m": 17.17, "peso_6m_ficha": 103.02, "nota": ""},
    {"selector": "125 x 125 | 4.7 mm", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_mm": 125, "espesor_mm": 4.7, "peso_kg_m": 17.81, "peso_6m_ficha": 106.86, "nota": ""},
    {"selector": "125 x 125 | 6 mm", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_mm": 125, "espesor_mm": 6.0, "peso_kg_m": 21.69, "peso_6m_ficha": 130.14, "nota": ""},
    {"selector": "125 x 125 | 6.35 mm", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_mm": 125, "espesor_mm": 6.35, "peso_kg_m": 23.24, "peso_6m_ficha": 139.44, "nota": ""},
    {"selector": "150 x 150 | 3 mm", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_mm": 150, "espesor_mm": 3.0, "peso_kg_m": 13.67, "peso_6m_ficha": 82.02, "nota": ""},
    {"selector": "150 x 150 | 4 mm", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_mm": 150, "espesor_mm": 4.0, "peso_kg_m": 18.01, "peso_6m_ficha": 108.06, "nota": ""},
    {"selector": "150 x 150 | 4.5 mm", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_mm": 150, "espesor_mm": 4.5, "peso_kg_m": 20.80, "peso_6m_ficha": 124.80, "nota": ""},
    {"selector": "150 x 150 | 6 mm", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_mm": 150, "espesor_mm": 6.0, "peso_kg_m": 27.39, "peso_6m_ficha": 164.32, "nota": ""},
    {"selector": "200 x 200 | 3 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 3.0, "peso_kg_m": 18.63, "peso_6m_ficha": 111.76, "nota": ""},
    {"selector": "200 x 200 | 4 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 4.0, "peso_kg_m": 24.29, "peso_6m_ficha": 145.74, "nota": ""},
    {"selector": "200 x 200 | 4.5 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 4.5, "peso_kg_m": 27.77, "peso_6m_ficha": 166.64, "nota": ""},
    {"selector": "200 x 200 | 4.7 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 4.7, "peso_kg_m": 29.21, "peso_6m_ficha": 175.26, "nota": ""},
    {"selector": "200 x 200 | 6 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 6.0, "peso_kg_m": 35.82, "peso_6m_ficha": 214.92, "nota": ""},
    {"selector": "200 x 200 | 8 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 8.0, "peso_kg_m": 48.68, "peso_6m_ficha": 292.10, "nota": ""},
    {"selector": "200 x 200 | 9 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 9.0, "peso_kg_m": 52.34, "peso_6m_ficha": 314.04, "nota": ""},
    {"selector": "200 x 200 | 9.5 mm", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_mm": 200, "espesor_mm": 9.5, "peso_kg_m": 56.08, "peso_6m_ficha": 336.48, "nota": ""},
    {"selector": "250 x 250 | 4.7 mm", "perfil": "250 x 250", "equiv_pulg": '10" x 10"', "lado_mm": 250, "espesor_mm": 4.7, "peso_kg_m": 36.86, "peso_6m_ficha": 221.14, "nota": ""},
    {"selector": "250 x 250 | 6 mm", "perfil": "250 x 250", "equiv_pulg": '10" x 10"', "lado_mm": 250, "espesor_mm": 6.0, "peso_kg_m": 45.24, "peso_6m_ficha": 271.44, "nota": ""},
    {"selector": "300 x 300 | 6 mm", "perfil": "300 x 300", "equiv_pulg": '12" x 12"', "lado_mm": 300, "espesor_mm": 6.0, "peso_kg_m": 54.66, "peso_6m_ficha": 327.96, "nota": ""},
    {"selector": "300 x 300 | 8 mm", "perfil": "300 x 300", "equiv_pulg": '12" x 12"', "lado_mm": 300, "espesor_mm": 8.0, "peso_kg_m": 73.82, "peso_6m_ficha": 442.90, "nota": ""},
]

# Enriquecer catálogo con las columnas calculadas de la hoja 'Catálogo'
for item in CATALOGO_DATOS:
    item["peso_6m_calc"] = round(item["peso_kg_m"] * 6.0, 2)
    item["area_m2_m"] = round(4.0 * item["lado_mm"] / 1000.0, 4)
    item["area_6m_m2"] = round(item["area_m2_m"] * 6.0, 4)

MAPA_PERFILES = {item["selector"]: item for item in CATALOGO_DATOS}
LISTA_SELECTORES = list(MAPA_PERFILES.keys())


# 3. Función de cálculo (fórmulas exactas de la hoja 'Calculadora')
def calcular_tubos_y_cortes(perfil_info, cantidad_elem, long_elem_m, largo_comercial_m, ancho_corte_mm):
    kerf_m = ancho_corte_mm / 1000.0
    peso_kg_m = perfil_info["peso_kg_m"]
    area_m2_m = perfil_info["area_m2_m"]

    # B17: Metraje requerido (m)
    metraje_requerido = cantidad_elem * long_elem_m

    # B18 y B19: Tramos completos por elemento y Tramo residual / pieza corta (m)
    if largo_comercial_m > 0:
        tramos_completos = int(long_elem_m // largo_comercial_m)
        tramo_residual = round(long_elem_m % largo_comercial_m, 6)
        if abs(tramo_residual - largo_comercial_m) < 1e-6:
            tramo_residual = 0.0
            tramos_completos += 1
    else:
        tramos_completos = 0
        tramo_residual = 0.0

    # B20: Piezas cortas por barra comercial
    if tramo_residual == 0:
        piezas_cortas_por_barra = 0
    else:
        denom = tramo_residual + kerf_m
        piezas_cortas_por_barra = int(math.floor((largo_comercial_m + kerf_m + 1e-9) / denom)) if denom > 0 else 0

    # B21: Barras completas (unidades)
    barras_completas = tramos_completos * cantidad_elem

    # B22: Barras para tramos cortos (unid.)
    if piezas_cortas_por_barra == 0:
        barras_tramos_cortos = 0
    else:
        barras_tramos_cortos = math.ceil(cantidad_elem / piezas_cortas_por_barra)

    # B23: Total barras comerciales
    total_barras = barras_completas + barras_tramos_cortos

    # B24: Cantidad de empalmes
    if largo_comercial_m > 0:
        empalmes = cantidad_elem * max(0, math.ceil(long_elem_m / largo_comercial_m) - 1)
    else:
        empalmes = 0

    # B25: Cantidad de piezas necesarias
    piezas_necesarias = cantidad_elem * (tramos_completos + (1 if tramo_residual > 0 else 0))

    # B26: Metraje comprado (m)
    metraje_comprado = total_barras * largo_comercial_m

    # B27: Pérdida por cortes (m)
    if barras_tramos_cortos == 0:
        perdida_cortes = 0.0
    else:
        # Pérdida en las primeras (B22 - 1) barras de tramos cortos
        if (largo_comercial_m - piezas_cortas_por_barra * tramo_residual - piezas_cortas_por_barra * kerf_m) >= -1e-7:
            perdida_barra_llena = piezas_cortas_por_barra * kerf_m
        else:
            perdida_barra_llena = max(0, piezas_cortas_por_barra - 1) * kerf_m

        # Pérdida en la última barra de tramos cortos
        piezas_ultima_barra = cantidad_elem - (barras_tramos_cortos - 1) * piezas_cortas_por_barra
        if (largo_comercial_m - piezas_ultima_barra * tramo_residual - piezas_ultima_barra * kerf_m) >= -1e-7:
            perdida_ultima_barra = piezas_ultima_barra * kerf_m
        else:
            perdida_ultima_barra = max(0, piezas_ultima_barra - 1) * kerf_m

        perdida_cortes = (barras_tramos_cortos - 1) * perdida_barra_llena + perdida_ultima_barra

    # B28: Sobrante aprovechable (m)
    sobrante_aprovechable = metraje_comprado - metraje_requerido - perdida_cortes

    # B29 a B32: Pesos y áreas
    peso_requerido = metraje_requerido * peso_kg_m
    peso_comprado = metraje_comprado * peso_kg_m
    area_requerida = metraje_requerido * area_m2_m
    area_comprada = metraje_comprado * area_m2_m

    # Nota dinámica D21
    if tramo_residual == 0:
        nota_piezas = "No se necesitan piezas cortadas."
    else:
        if tramos_completos == 0:
            nota_piezas = f"Se requieren {cantidad_elem} piezas de {tramo_residual:.2f} m, sin empalmes. Salen hasta {piezas_cortas_por_barra} piezas por barra."
        else:
            nota_piezas = f"Se requieren {cantidad_elem} extensiones de {tramo_residual:.2f} m. Salen hasta {piezas_cortas_por_barra} piezas por barra."

    # Texto resumen A35
    if tramo_residual == 0:
        texto_plan = f"Usar {barras_completas} barra(s) completa(s); no necesitas empalmes."
    else:
        texto_plan = (
            f"Usar {barras_completas} barra(s) completa(s) de {largo_comercial_m:.2f} m "
            f"y cortar {cantidad_elem} pieza(s) de {tramo_residual:.2f} m "
            f"desde {barras_tramos_cortos} barra(s) adicional(es)."
        )

    # Desglose de barras (Filas 40 en adelante)
    filas_plan = []
    # Fila 1: Barras completas
    filas_plan.append({
        "N.° barra(s)": f"1 a {barras_completas}" if barras_completas > 0 else "—",
        "Tipo de uso": "Barras completas" if barras_completas > 0 else "Sin barras completas",
        "Piezas": barras_completas,
        "Largo/pieza (m)": round(largo_comercial_m, 2) if barras_completas > 0 else 0.0,
        "Metraje útil (m)": round(barras_completas * largo_comercial_m, 2),
        "Pérdida corte (m)": 0.0,
        "Sobrante (m)": 0.0,
        "Destino / indicación": "Tramos principales sin corte" if barras_completas > 0 else "No se utilizan tubos enteros"
    })

    # Filas siguientes: Barras adicionales para cortes
    for i in range(1, barras_tramos_cortos + 1):
        num_barra = barras_completas + i
        tipo_uso = "Piezas cortas" if tramos_completos == 0 else "Extensiones"
        piezas_en_barra = min(piezas_cortas_por_barra, cantidad_elem - (i - 1) * piezas_cortas_por_barra)
        largo_pieza = tramo_residual
        metraje_util = piezas_en_barra * largo_pieza

        if (largo_comercial_m - metraje_util - piezas_en_barra * kerf_m) >= -1e-7:
            perdida_barra = piezas_en_barra * kerf_m
        else:
            perdida_barra = max(0, piezas_en_barra - 1) * kerf_m

        sobrante_barra = max(0.0, largo_comercial_m - metraje_util - perdida_barra)

        filas_plan.append({
            "N.° barra(s)": str(num_barra),
            "Tipo de uso": tipo_uso,
            "Piezas": piezas_en_barra,
            "Largo/pieza (m)": round(largo_pieza, 2),
            "Metraje útil (m)": round(metraje_util, 2),
            "Pérdida corte (m)": round(perdida_barra, 4),
            "Sobrante (m)": round(sobrante_barra, 2),
            "Destino / indicación": f"Cortar {piezas_en_barra} pieza(s) de {largo_pieza:.2f} m"
        })

    return {
        "metraje_requerido": metraje_requerido,
        "tramos_completos": tramos_completos,
        "tramo_residual": tramo_residual,
        "piezas_cortas_por_barra": piezas_cortas_por_barra,
        "barras_completas": barras_completas,
        "barras_tramos_cortos": barras_tramos_cortos,
        "total_barras": total_barras,
        "empalmes": empalmes,
        "piezas_necesarias": piezas_necesarias,
        "metraje_comprado": metraje_comprado,
        "perdida_cortes": perdida_cortes,
        "sobrante_aprovechable": sobrante_aprovechable,
        "peso_requerido": peso_requerido,
        "peso_comprado": peso_comprado,
        "area_requerida": area_requerida,
        "area_comprada": area_comprada,
        "nota_piezas": nota_piezas,
        "texto_plan": texto_plan,
        "df_plan": pd.DataFrame(filas_plan)
    }


# 4. Encabezado principal
st.title("🏗️ Calculadora de Tubos Cuadrados ASTM A500, Cortes y Empalmes")
st.markdown("Calcula barras comerciales necesarias al usar tramos completos y cortar extensiones para cada elemento.")

# 5. Barra lateral: Parámetros de Entrada (Celdas amarillas del Excel)
with st.sidebar:
    st.header("⚙️ Datos de Entrada")

    idx_default = LISTA_SELECTORES.index("40 x 40 | 2 mm")
    perfil_seleccionado = st.selectbox(
        "Perfil / espesor",
        options=LISTA_SELECTORES,
        index=idx_default
    )

    cantidad_elementos = st.number_input(
        "Cantidad de elementos",
        min_value=1,
        value=5,
        step=1
    )

    longitud_elemento = st.number_input(
        "Longitud final por elemento (m)",
        min_value=0.10,
        value=9.00,
        step=0.50,
        format="%.2f"
    )

    largo_comercial = st.number_input(
        "Largo comercial del tubo (m)",
        min_value=1.00,
        value=6.00,
        step=0.50,
        format="%.2f"
    )

    ancho_corte_mm = st.number_input(
        "Ancho de corte / disco (mm)",
        min_value=0.0,
        value=0.0,
        step=0.5,
        format="%.1f",
        help="Ancho de corte = 0 mm para reproducir el ejemplo sin pérdida por disco."
    )

    st.divider()
    st.subheader("📗 Datos del Catálogo")
    info_perfil = MAPA_PERFILES[perfil_seleccionado]
    st.markdown(f"**Equivalencia:** `{info_perfil['equiv_pulg']}`")
    st.markdown(f"**Lado exterior:** `{info_perfil['lado_mm']} mm`")
    st.markdown(f"**Espesor:** `{info_perfil['espesor_mm']} mm`")
    st.markdown(f"**Peso del perfil:** `{info_perfil['peso_kg_m']:.2f} kg/m`")
    st.markdown(f"**Área exterior:** `{info_perfil['area_m2_m']:.2f} m²/m`")
    st.markdown(f"**Peso barra 6 m (ficha):** `{info_perfil['peso_6m_ficha']:.2f} kg`")

    if info_perfil["nota"]:
        st.warning(f"⚠️ {info_perfil['nota']}")

# Avisos especiales de validación
if perfil_seleccionado == "50 x 50 | 4 mm":
    st.warning(
        "**Aviso del catálogo:** en 50 × 50 mm, el peso publicado para 4 mm (6.57 kg/m) supera al de 4.5 mm (6.02 kg/m). "
        "Confirmar con el proveedor antes de presupuestar ese perfil."
    )

if tramo_mayor := (
    round(longitud_elemento % largo_comercial, 6) > 0
    and int(math.floor((largo_comercial + ancho_corte_mm / 1000.0 + 1e-9) / (round(longitud_elemento % largo_comercial, 6) + ancho_corte_mm / 1000.0))) == 0
):
    st.error("El tramo residual más el ancho de corte supera el largo comercial del tubo.")

# 6. Ejecutar cálculos y organizar en pestañas (Calculadora y Catálogo)
res = calcular_tubos_y_cortes(
    info_perfil,
    cantidad_elementos,
    longitud_elemento,
    largo_comercial,
    ancho_corte_mm
)

tab_calc, tab_cat = st.tabs(["🧮 Calculadora y Despiece", "📒 Catálogo ASTM A500"])

with tab_calc:
    # Bloque 1: Resumen de Compra
    st.subheader("📦 Resumen de Compra")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("TUBOS A COMPRAR", f"{res['total_barras']} unid.")
    col2.metric("SOBRANTE APROVECHABLE", f"{res['sobrante_aprovechable']:.2f} m")
    col3.metric("EMPALMES TOTALES", f"{res['empalmes']}")
    col4.metric("PESO COMPRA", f"{res['peso_comprado']:.2f} kg")

    st.divider()

    # Bloque 2: Metrado y Despiece del Perfil
    col_izq, col_der = st.columns([3, 2])

    with col_izq:
        st.subheader("📐 Metrado y Despiece del Perfil")
        df_metrado = pd.DataFrame([
            {"Concepto": "Metraje requerido (m)", "Valor": f"{res['metraje_requerido']:.2f}"},
            {"Concepto": "Tramos completos por elemento", "Valor": f"{res['tramos_completos']}"},
            {"Concepto": "Tramo residual / pieza corta (m)", "Valor": f"{res['tramo_residual']:.2f}"},
            {"Concepto": "Piezas cortas por barra comercial", "Valor": f"{res['piezas_cortas_por_barra']}"},
            {"Concepto": "Barras completas (unidades)", "Valor": f"{res['barras_completas']}"},
            {"Concepto": "Barras para tramos cortos (unid.)", "Valor": f"{res['barras_tramos_cortos']}"},
            {"Concepto": "Total barras comerciales", "Valor": f"{res['total_barras']}"},
            {"Concepto": "Cantidad de empalmes", "Valor": f"{res['empalmes']}"},
            {"Concepto": "Cantidad de piezas necesarias", "Valor": f"{res['piezas_necesarias']}"},
            {"Concepto": "Metraje comprado (m)", "Valor": f"{res['metraje_comprado']:.2f}"},
            {"Concepto": "Pérdida por cortes (m)", "Valor": f"{res['perdida_cortes']:.3f}"},
            {"Concepto": "Sobrante aprovechable (m)", "Valor": f"{res['sobrante_aprovechable']:.2f}"},
            {"Concepto": "Peso del metraje requerido (kg)", "Valor": f"{res['peso_requerido']:.2f}"},
            {"Concepto": "Peso del material comprado (kg)", "Valor": f"{res['peso_comprado']:.2f}"},
            {"Concepto": "Área exterior requerida (m²)", "Valor": f"{res['area_requerida']:.2f}"},
            {"Concepto": "Área exterior comprada (m²)", "Valor": f"{res['area_comprada']:.2f}"},
        ])
        st.dataframe(df_metrado, use_container_width=True, hide_index=True, height=600)

    with col_der:
        st.subheader("📌 Notas Técnicas y Criterios")
        st.info(
            "**PLAN DE CORTE:** usar primero los tubos completos y después cortar las extensiones necesarias en barras adicionales."
        )
        st.success(f"**Detalle de extensiones:** {res['nota_piezas']}")
        st.markdown(
            """
            * **Optimización:** Este cálculo evita cortes innecesarios al usar barras completas y extensiones. No optimiza mezclas de distintas longitudes o perfiles.
            * **Superficie y Soldadura:** El área corresponde solo a la superficie exterior (4 caras). Los empalmes de columnas requieren validación del diseño estructural y del procedimiento de soldadura; esta herramienta calcula cantidades, no verifica resistencia estructural.
            """
        )

    st.divider()

    # Bloque 3: Plan de Barras
    st.subheader("🪚 Plan de Barras: Primero Barras Completas, Luego Cortes para Extensiones")
    st.markdown(f"**Resumen de ejecución:** {res['texto_plan']}")

    st.dataframe(res["df_plan"], use_container_width=True, hide_index=True)

    # Botón para descargar el plan de corte en CSV
    csv_plan = res["df_plan"].to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="⬇️ Descargar Plan de Corte (CSV)",
        data=csv_plan,
        file_name=f"plan_corte_{perfil_seleccionado.replace(' ', '').replace('|', '_')}.csv",
        mime="text/csv"
    )

with tab_cat:
    st.subheader("📒 Catálogo Tubo Cuadrado ASTM A500 — Pesos y Área Superficial")
    st.caption(
        "Pesos tomados del catálogo técnico. Área calculada sobre las cuatro caras exteriores del perfil; "
        "no incluye caras interiores ni extremos. El catálogo indica barras de 6 m."
    )

    df_catalogo = pd.DataFrame(CATALOGO_DATOS).rename(columns={
        "perfil": "Perfil (mm)",
        "equiv_pulg": "Equiv. pulg.",
        "lado_mm": "Lado (mm)",
        "espesor_mm": "Espesor (mm)",
        "peso_kg_m": "Peso ficha (kg/m)",
        "peso_6m_calc": "Peso 6 m calculado (kg)",
        "area_m2_m": "Área exterior (m²/m)",
        "area_6m_m2": "Área exterior 6 m (m²)",
        "peso_6m_ficha": "Peso 6 m ficha (kg)",
        "nota": "Control del dato",
        "selector": "Selector de perfil"
    })

    columnas_orden = [
        "Perfil (mm)", "Equiv. pulg.", "Lado (mm)", "Espesor (mm)",
        "Peso ficha (kg/m)", "Peso 6 m calculado (kg)", "Área exterior (m²/m)",
        "Área exterior 6 m (m²)", "Peso 6 m ficha (kg)", "Control del dato", "Selector de perfil"
    ]
    st.dataframe(df_catalogo[columnas_orden], use_container_width=True, hide_index=True, height=600)
