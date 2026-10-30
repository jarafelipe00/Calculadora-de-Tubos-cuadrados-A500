import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import math
import io
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple

# ==============================================================================
# 1. BASE DE DATOS TÉCNICA OFICIAL (ACTUALIZADA CON NUEVO CATÁLOGO)
# ==============================================================================
CATALOGO_OFICIAL = {
    "Tubo Rectangular LAC": [
        {"denominacion": "20 x 40 x 1.5 mm", "A": 40.0, "B": 20.0, "e": 1.5, "peso_kg_m": 1.35, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "20 x 40 x 2.0 mm", "A": 40.0, "B": 20.0, "e": 2.0, "peso_kg_m": 1.70, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "20 x 50 x 2.0 mm", "A": 50.0, "B": 20.0, "e": 2.0, "peso_kg_m": 2.10, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 50 x 1.2 mm", "A": 50.0, "B": 25.0, "e": 1.2, "peso_kg_m": 1.34, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 50 x 1.5 mm", "A": 50.0, "B": 25.0, "e": 1.5, "peso_kg_m": 1.65, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 50 x 1.8 mm", "A": 50.0, "B": 25.0, "e": 1.8, "peso_kg_m": 2.07, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 50 x 2.0 mm", "A": 50.0, "B": 25.0, "e": 2.0, "peso_kg_m": 2.26, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 50 x 2.5 mm", "A": 50.0, "B": 25.0, "e": 2.5, "peso_kg_m": 2.98, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 50 x 3.0 mm", "A": 50.0, "B": 25.0, "e": 3.0, "peso_kg_m": 3.35, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 50 x 2.0 mm", "A": 50.0, "B": 40.0, "e": 2.0, "peso_kg_m": 2.62, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 60 x 2.0 mm", "A": 60.0, "B": 40.0, "e": 2.0, "peso_kg_m": 3.03, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 60 x 2.5 mm", "A": 60.0, "B": 40.0, "e": 2.5, "peso_kg_m": 3.60, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 60 x 3.0 mm", "A": 60.0, "B": 40.0, "e": 3.0, "peso_kg_m": 4.25, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 80 x 2.0 mm", "A": 80.0, "B": 40.0, "e": 2.0, "peso_kg_m": 3.66, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 80 x 3.0 mm", "A": 80.0, "B": 40.0, "e": 3.0, "peso_kg_m": 5.19, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 70 x 2.0 mm", "A": 70.0, "B": 50.0, "e": 2.0, "peso_kg_m": 3.58, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 75 x 2.0 mm", "A": 75.0, "B": 50.0, "e": 2.0, "peso_kg_m": 3.95, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 75 x 3.0 mm", "A": 75.0, "B": 50.0, "e": 3.0, "peso_kg_m": 5.42, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 100 x 2.0 mm", "A": 100.0, "B": 50.0, "e": 2.0, "peso_kg_m": 4.50, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 100 x 3.0 mm", "A": 100.0, "B": 50.0, "e": 3.0, "peso_kg_m": 6.85, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 100 x 4.0 mm", "A": 100.0, "B": 50.0, "e": 4.0, "peso_kg_m": 8.59, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 150 x 3.0 mm", "A": 150.0, "B": 50.0, "e": 3.0, "peso_kg_m": 9.17, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 200 x 3.0 mm", "A": 200.0, "B": 50.0, "e": 3.0, "peso_kg_m": 11.75, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "75 x 100 x 3.0 mm", "A": 100.0, "B": 75.0, "e": 3.0, "peso_kg_m": 8.16, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "100 x 150 x 3.0 mm", "A": 150.0, "B": 100.0, "e": 3.0, "peso_kg_m": 11.56, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "100 x 200 x 4.0 mm", "A": 200.0, "B": 100.0, "e": 4.0, "peso_kg_m": 18.45, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"}
    ],
    "Tubo Cuadrado LAC": [
        {"denominacion": "20 x 20 x 0.9 mm", "A": 20.0, "B": 20.0, "e": 0.9, "peso_kg_m": 0.49, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "20 x 20 x 1.5 mm", "A": 20.0, "B": 20.0, "e": 1.5, "peso_kg_m": 0.86, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "20 x 20 x 2.0 mm", "A": 20.0, "B": 20.0, "e": 2.0, "peso_kg_m": 1.04, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 25 x 1.5 mm", "A": 25.0, "B": 25.0, "e": 1.5, "peso_kg_m": 1.06, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 25 x 2.0 mm", "A": 25.0, "B": 25.0, "e": 2.0, "peso_kg_m": 1.46, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "25 x 25 x 3.0 mm", "A": 25.0, "B": 25.0, "e": 3.0, "peso_kg_m": 1.93, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "30 x 30 x 2.0 mm", "A": 30.0, "B": 30.0, "e": 2.0, "peso_kg_m": 1.86, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 40 x 2.0 mm", "A": 40.0, "B": 40.0, "e": 2.0, "peso_kg_m": 2.24, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "40 x 40 x 3.0 mm", "A": 40.0, "B": 40.0, "e": 3.0, "peso_kg_m": 3.54, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 50 x 2.0 mm", "A": 50.0, "B": 50.0, "e": 2.0, "peso_kg_m": 3.12, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 50 x 3.0 mm", "A": 50.0, "B": 50.0, "e": 3.0, "peso_kg_m": 4.49, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "50 x 50 x 4.0 mm", "A": 50.0, "B": 50.0, "e": 4.0, "peso_kg_m": 6.57, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "60 x 60 x 2.0 mm", "A": 60.0, "B": 60.0, "e": 2.0, "peso_kg_m": 3.56, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "75 x 75 x 2.0 mm", "A": 75.0, "B": 75.0, "e": 2.0, "peso_kg_m": 4.50, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "75 x 75 x 3.0 mm", "A": 75.0, "B": 75.0, "e": 3.0, "peso_kg_m": 6.81, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "100 x 100 x 3.0 mm", "A": 100.0, "B": 100.0, "e": 3.0, "peso_kg_m": 9.20, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "100 x 100 x 4.0 mm", "A": 100.0, "B": 100.0, "e": 4.0, "peso_kg_m": 12.17, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "125 x 125 x 4.0 mm", "A": 125.0, "B": 125.0, "e": 4.0, "peso_kg_m": 14.87, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "150 x 150 x 4.0 mm", "A": 150.0, "B": 150.0, "e": 4.0, "peso_kg_m": 18.01, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"},
        {"denominacion": "200 x 200 x 6.0 mm", "A": 200.0, "B": 200.0, "e": 6.0, "peso_kg_m": 35.82, "longitudes": [6.0], "norma": "ASTM A500 Gr. A"}
    ],
    "Viga Estructural W (Perfil H)": [
        {"denominacion": "W 4\" x 4\" x 13.0 lb/pie", "A": 106.0, "B": 103.0, "ta": 7.11, "tb": 8.76, "peso_kg_m": 19.39, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 6\" x 4\" x 9.0 lb/pie", "A": 150.0, "B": 100.0, "ta": 4.32, "tb": 5.46, "peso_kg_m": 13.42, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 6\" x 4\" x 12.0 lb/pie", "A": 153.0, "B": 102.0, "ta": 5.84, "tb": 7.11, "peso_kg_m": 17.90, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 6\" x 6\" x 15.0 lb/pie", "A": 152.0, "B": 152.0, "ta": 5.84, "tb": 6.60, "peso_kg_m": 22.37, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 6\" x 6\" x 20.0 lb/pie", "A": 157.0, "B": 153.0, "ta": 6.60, "tb": 9.27, "peso_kg_m": 29.83, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 8\" x 4\" x 10.0 lb/pie", "A": 200.0, "B": 100.0, "ta": 4.32, "tb": 5.21, "peso_kg_m": 14.91, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 8\" x 4\" x 13.0 lb/pie", "A": 203.0, "B": 102.0, "ta": 5.84, "tb": 8.38, "peso_kg_m": 19.39, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 8\" x 5 1/4\" x 18.0 lb/pie", "A": 207.0, "B": 133.0, "ta": 5.84, "tb": 8.38, "peso_kg_m": 26.84, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 8\" x 8\" x 31.0 lb/pie", "A": 203.0, "B": 203.0, "ta": 7.24, "tb": 11.05, "peso_kg_m": 46.23, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 10\" x 4\" x 15.0 lb/pie", "A": 254.0, "B": 102.0, "ta": 5.84, "tb": 6.86, "peso_kg_m": 22.37, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 10\" x 5 3/4\" x 22.0 lb/pie", "A": 258.0, "B": 146.0, "ta": 6.10, "tb": 9.14, "peso_kg_m": 32.81, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 12\" x 4\" x 19.0 lb/pie", "A": 309.0, "B": 102.0, "ta": 5.97, "tb": 8.89, "peso_kg_m": 28.33, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"},
        {"denominacion": "W 12\" x 6 1/2\" x 26.0 lb/pie", "A": 310.0, "B": 165.0, "ta": 5.84, "tb": 9.65, "peso_kg_m": 38.77, "longitudes": [6.0, 9.0, 12.0], "norma": "ASTM A36"}
    ],
    "Canal C": [
        {"denominacion": "C 2\" x 2.58 lb/pie", "A": 50.8, "B": 25.4, "tw": 4.75, "tf": 4.75, "peso_kg_m": round(2.58 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "C 3\" x 4.10 lb/pie", "A": 76.2, "B": 35.8, "tw": 4.32, "tf": 6.93, "peso_kg_m": round(4.10 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36/A572-G50"},
        {"denominacion": "C 3\" x 5.00 lb/pie", "A": 76.2, "B": 38.1, "tw": 6.55, "tf": 6.93, "peso_kg_m": round(5.00 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36/A572-G50"},
        {"denominacion": "C 4\" x 5.40 lb/pie", "A": 101.6, "B": 40.1, "tw": 4.67, "tf": 7.52, "peso_kg_m": round(5.40 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36/A572-G50"},
        {"denominacion": "C 4\" x 7.25 lb/pie", "A": 101.6, "B": 43.7, "tw": 8.15, "tf": 7.52, "peso_kg_m": round(7.25 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36/A572-G50"},
        {"denominacion": "C 6\" x 8.20 lb/pie", "A": 152.4, "B": 48.8, "tw": 5.08, "tf": 8.71, "peso_kg_m": round(8.20 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36/A572-G50"},
        {"denominacion": "C 6\" x 10.50 lb/pie", "A": 152.4, "B": 51.6, "tw": 7.98, "tf": 8.71, "peso_kg_m": round(10.50 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36/A572-G50"},
        {"denominacion": "C 8\" x 11.50 lb/pie", "A": 203.2, "B": 57.4, "tw": 5.59, "tf": 9.91, "peso_kg_m": round(11.50 * 1.48816, 2), "longitudes": [6.0], "norma": "ASTM A36/A572-G50"}
    ],
    "Perfil TEE": [
        {"denominacion": "T 20 x 20 x 3.0 mm", "A": 20.0, "B": 20.0, "e": 3.0, "peso_kg_m": 0.88, "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "T 25 x 25 x 3.0 mm", "A": 25.0, "B": 25.0, "e": 3.0, "peso_kg_m": 1.10, "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "T 1 1/4\" x 1 1/4\" x 1/8\"", "A": 31.75, "B": 31.75, "e": 3.18, "peso_kg_m": 1.54, "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "T 1 1/2\" x 1 1/2\" x 1/8\"", "A": 38.1, "B": 38.1, "e": 3.18, "peso_kg_m": 1.84, "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "T 1 1/2\" x 1 1/2\" x 3/16\"", "A": 38.1, "B": 38.1, "e": 4.76, "peso_kg_m": 2.72, "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "T 2\" x 2\" x 1/4\"", "A": 50.8, "B": 50.8, "e": 6.35, "peso_kg_m": 4.97, "longitudes": [6.0], "norma": "ASTM A36"}
    ],
    "Platina de Acero": [
        {"denominacion": "PL 1/8\" x 1/2\" (3.0 x 12 mm)", "A": 12.0, "B": 0.0, "e": 3.0, "peso_kg_m": round(1.92 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 1/8\" x 3/4\" (3.0 x 19 mm)", "A": 19.0, "B": 0.0, "e": 3.0, "peso_kg_m": round(2.88 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 1/8\" x 1\" (3.0 x 25 mm)", "A": 25.0, "B": 0.0, "e": 3.0, "peso_kg_m": round(3.84 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 3/16\" x 1\" (4.5 x 25 mm)", "A": 25.0, "B": 0.0, "e": 4.5, "peso_kg_m": round(5.88 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 3/16\" x 1 1/2\" (4.5 x 38 mm)", "A": 38.0, "B": 0.0, "e": 4.5, "peso_kg_m": round(8.52 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 3/16\" x 2\" (4.5 x 50 mm)", "A": 50.0, "B": 0.0, "e": 4.5, "peso_kg_m": round(11.40 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 1/4\" x 1\" (6.0 x 25 mm)", "A": 25.0, "B": 0.0, "e": 6.0, "peso_kg_m": round(7.68 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 1/4\" x 2\" (6.0 x 50 mm)", "A": 50.0, "B": 0.0, "e": 6.0, "peso_kg_m": round(15.18 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 1/4\" x 3\" (6.0 x 75 mm)", "A": 75.0, "B": 0.0, "e": 6.0, "peso_kg_m": round(22.80 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 1/4\" x 4\" (6.0 x 100 mm)", "A": 100.0, "B": 0.0, "e": 6.0, "peso_kg_m": round(30.36 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 3/8\" x 2\" (9.5 x 50 mm)", "A": 50.0, "B": 0.0, "e": 9.5, "peso_kg_m": round(22.80 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "PL 1/2\" x 4\" (12.0 x 100 mm)", "A": 100.0, "B": 0.0, "e": 12.0, "peso_kg_m": round(60.78 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"}
    ],
    "Ángulo L de Alas Iguales": [
        {"denominacion": "L 19 x 19 x 2.0 mm (3/4\" x 5/64\")", "A": 19.0, "B": 19.0, "e": 2.0, "peso_kg_m": round(3.582 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 25 x 25 x 3.0 mm (1\" x 1/8\")", "A": 25.0, "B": 25.0, "e": 3.0, "peso_kg_m": round(7.143 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 25 x 25 x 4.5 mm (1\" x 3/16\")", "A": 25.0, "B": 25.0, "e": 4.5, "peso_kg_m": round(10.358 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 38 x 38 x 3.0 mm (1 1/2\" x 1/8\")", "A": 38.0, "B": 38.0, "e": 3.0, "peso_kg_m": round(10.983 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 38 x 38 x 4.5 mm (1 1/2\" x 3/16\")", "A": 38.0, "B": 38.0, "e": 4.5, "peso_kg_m": round(16.072 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 50 x 50 x 3.0 mm (2\" x 1/8\")", "A": 50.0, "B": 50.0, "e": 3.0, "peso_kg_m": round(14.733 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 50 x 50 x 4.5 mm (2\" x 3/16\")", "A": 50.0, "B": 50.0, "e": 4.5, "peso_kg_m": round(21.787 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 50 x 50 x 6.0 mm (2\" x 1/4\")", "A": 50.0, "B": 50.0, "e": 6.0, "peso_kg_m": round(28.483 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 63 x 63 x 6.0 mm (2 1/2\" x 1/4\")", "A": 63.0, "B": 63.0, "e": 6.0, "peso_kg_m": round(36.609 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 75 x 75 x 6.0 mm (3\" x 1/4\")", "A": 75.0, "B": 75.0, "e": 6.0, "peso_kg_m": round(42.752 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"},
        {"denominacion": "L 100 x 100 x 6.0 mm (4\" x 1/4\")", "A": 100.0, "B": 100.0, "e": 6.0, "peso_kg_m": round(58.932 / 6.0, 3), "longitudes": [6.0], "norma": "ASTM A36"}
    ],
    # ACTUALIZACIÓN EXACTA: Tabla técnica de Barras Redondas Lisas y Pulidas
    "Barra Redonda Maciza (Eje)": [
        {"denominacion": "Redondo 3/8\"", "A": 9.53, "B": 0.0, "e": 0.0, "peso_kg_m": 0.559, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045"},
        {"denominacion": "Redondo 1/2\"", "A": 12.70, "B": 0.0, "e": 0.0, "peso_kg_m": 0.994, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045"},
        {"denominacion": "Redondo 5/8\"", "A": 15.88, "B": 0.0, "e": 0.0, "peso_kg_m": 1.554, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045"},
        {"denominacion": "Redondo 3/4\"", "A": 19.05, "B": 0.0, "e": 0.0, "peso_kg_m": 2.237, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045"},
        {"denominacion": "Redondo 7/8\"", "A": 22.23, "B": 0.0, "e": 0.0, "peso_kg_m": 3.045, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045"},
        {"denominacion": "Redondo 1\"", "A": 25.40, "B": 0.0, "e": 0.0, "peso_kg_m": 3.978, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045"},
        {"denominacion": "Redondo 1 1/8\"", "A": 28.58, "B": 0.0, "e": 0.0, "peso_kg_m": 5.034, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 1 1/4\"", "A": 31.75, "B": 0.0, "e": 0.0, "peso_kg_m": 6.215, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 1 3/8\"", "A": 34.93, "B": 0.0, "e": 0.0, "peso_kg_m": 7.520, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 1 1/2\"", "A": 38.10, "B": 0.0, "e": 0.0, "peso_kg_m": 8.950, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 1 3/4\"", "A": 44.45, "B": 0.0, "e": 0.0, "peso_kg_m": 12.182, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 2\"", "A": 50.80, "B": 0.0, "e": 0.0, "peso_kg_m": 15.911, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 2 1/4\"", "A": 57.15, "B": 0.0, "e": 0.0, "peso_kg_m": 20.137, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 2 1/2\"", "A": 63.50, "B": 0.0, "e": 0.0, "peso_kg_m": 24.860, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 3\"", "A": 76.20, "B": 0.0, "e": 0.0, "peso_kg_m": 35.770, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 3 1/2\"", "A": 88.90, "B": 0.0, "e": 0.0, "peso_kg_m": 48.680, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 4\"", "A": 101.60, "B": 0.0, "e": 0.0, "peso_kg_m": 63.590, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 4 1/2\"", "A": 114.30, "B": 0.0, "e": 0.0, "peso_kg_m": 80.480, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 5\"", "A": 127.00, "B": 0.0, "e": 0.0, "peso_kg_m": 99.350, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"},
        {"denominacion": "Redondo 6\"", "A": 152.40, "B": 0.0, "e": 0.0, "peso_kg_m": 143.070, "longitudes": [6.0], "norma": "ASTM A36 / SAE 1045 Pulido"}
    ]
}

# ==============================================================================
# 2. MODELOS MATEMÁTICOS DE SUPERFICIE EXPUESTA
# ==============================================================================
def calcular_perimetro_superficial(familia: str, A: float, B: float, e: float) -> float:
    """
    Retorna el perímetro desarrollado exterior en metros lineales (m2/m).
    A, B, e en milímetros.
    """
    if familia in ["Tubo Rectangular LAC", "Tubo Cuadrado LAC"]:
        return round((2.0 * (A + B)) / 1000.0, 4)
    elif familia == "Barra Redonda Maciza (Eje)":
        return round((math.pi * A) / 1000.0, 4)
    elif familia == "Platina de Acero":
        return round((2.0 * (A + e)) / 1000.0, 4)
    elif familia == "Ángulo L de Alas Iguales":
        return round((2.0 * (A + B)) / 1000.0, 4)
    elif familia in ["Canal C", "Viga Estructural W (Perfil H)"]:
        return round((2.0 * A + 4.0 * B) / 1000.0, 4)
    elif familia == "Perfil TEE":
        return round((2.0 * A + 2.0 * B) / 1000.0, 4)
    return 0.0

# ==============================================================================
# 3. MOTOR DE OPTIMIZACIÓN 1D CON SOPORTE DE EMPALME POR SOLDADURA
# ==============================================================================
@dataclass
class PiezaCorte:
    id_partida: str
    descripcion: str
    longitud: float
    es_soldado: bool = False

@dataclass
class BarraResultado:
    id_barra: str
    tipo_origen: str  # 'COMERCIAL' o 'RETAZO'
    longitud_nominal: float
    piezas: List[PiezaCorte] = field(default_factory=list)
    num_cortes: int = 0
    perdida_corte_m: float = 0.0
    longitud_util_m: float = 0.0
    longitud_sobrante_m: float = 0.0
    es_retazo_utilizable: bool = False
    rendimiento_pct: float = 0.0

def optimizar_1d_cutting_stock(
    demandas: List[Tuple[str, str, float, int]],  # (id_partida, desc, long_m, cant)
    longitudes_comerciales: List[float],
    retazos_inventario: List[Dict[str, Any]],
    kerf_m: float = 0.003,
    despunte_m: float = 0.0,
    min_retazo_m: float = 0.50,
    permitir_soldadura: bool = False,
    modo: str = "Minimizar Desperdicio"
) -> Dict[str, Any]:
    
    long_comercial_base = min(longitudes_comerciales) if longitudes_comerciales else 6.0
    piezas_solicitadas: List[PiezaCorte] = []

    # 1. Procesar demandas y descomponer en tramos si se permite soldar
    for partida_id, desc, l_m, cant in demandas:
        l_req = round(l_m, 4)
        for _ in range(cant):
            if l_req > (long_comercial_base - despunte_m):
                if permitir_soldadura:
                    # Descomponer en segmentos comerciales con empalme por soldadura
                    l_restante = l_req
                    tramo_idx = 1
                    while l_restante > 0:
                        cap_max = long_comercial_base - despunte_m - kerf_m
                        tramo = min(l_restante, cap_max)
                        piezas_solicitadas.append(
                            PiezaCorte(partida_id, f"{desc} (Tramo {tramo_idx} Soldado)", round(tramo, 4), es_soldado=True)
                        )
                        l_restante = round(l_restante - tramo, 4)
                        tramo_idx += 1
                else:
                    # Se mantiene entera para que el motor emita la advertencia de desborde
                    piezas_solicitadas.append(PiezaCorte(partida_id, desc, l_req, es_soldado=False))
            else:
                piezas_solicitadas.append(PiezaCorte(partida_id, desc, l_req, es_soldado=False))

    # Ordenamiento heurístico First-Fit Decreasing
    piezas_solicitadas.sort(key=lambda p: p.longitud, reverse=True)
    
    barras_procesadas: List[BarraResultado] = []
    retazos_consumidos_ids = []
    contador_barras = 1

    # 2. Prioridad de Retazos en Inventario (Best-Fit)
    retazos_disponibles = sorted(
        [r for r in retazos_inventario if r["estado"] == "Disponible"],
        key=lambda x: x["longitud_m"]
    )

    for ret in retazos_disponibles:
        if not piezas_solicitadas:
            break
        
        capacidad = ret["longitud_m"] - despunte_m
        piezas_asignadas = []
        long_acumulada = 0.0
        restantes = []

        for pieza in piezas_solicitadas:
            costo_corte = kerf_m if len(piezas_asignadas) > 0 else 0.0
            if (long_acumulada + pieza.longitud + costo_corte) <= (capacidad + 1e-6):
                piezas_asignadas.append(pieza)
                long_acumulada += pieza.longitud + costo_corte
            else:
                restantes.append(pieza)

        if piezas_asignadas:
            piezas_solicitadas = restantes
            n_c = len(piezas_asignadas)
            perdida = (n_c - 1) * kerf_m + despunte_m if n_c > 0 else 0.0
            util = sum(p.longitud for p in piezas_asignadas)
            sobrante = round(ret["longitud_m"] - (util + perdida), 4)
            reutilizable = sobrante >= min_retazo_m
            rend = round((util / ret["longitud_m"]) * 100.0, 2)

            barras_procesadas.append(BarraResultado(
                id_barra=f"RET-{ret['id']:03d}",
                tipo_origen="RETAZO",
                longitud_nominal=ret["longitud_m"],
                piezas=piezas_asignadas,
                num_cortes=n_c,
                perdida_corte_m=round(perdida, 4),
                longitud_util_m=round(util, 4),
                longitud_sobrante_m=max(0.0, sobrante),
                es_retazo_utilizable=reutilizable,
                rendimiento_pct=rend
            ))
            retazos_consumidos_ids.append(ret["id"])

    # 3. Asignación a Barras Comerciales
    while piezas_solicitadas:
        capacidad = long_comercial_base - despunte_m
        piezas_asignadas = []
        long_acumulada = 0.0
        restantes = []

        for pieza in piezas_solicitadas:
            costo_corte = kerf_m if len(piezas_asignadas) > 0 else 0.0
            if (long_acumulada + pieza.longitud + costo_corte) <= (capacidad + 1e-6):
                piezas_asignadas.append(pieza)
                long_acumulada += pieza.longitud + costo_corte
            else:
                restantes.append(pieza)

        # Si una pieza no cabe ni siquiera en una barra vacía (longitud > barra comercial sin soldar)
        if not piezas_asignadas and piezas_solicitadas:
            p_exceso = piezas_solicitadas.pop(0)
            piezas_asignadas.append(p_exceso)
            long_acumulada = p_exceso.longitud

        piezas_solicitadas = restantes
        n_c = len(piezas_asignadas)
        perdida = (n_c - 1) * kerf_m + despunte_m if n_c > 0 else 0.0
        util = sum(p.longitud for p in piezas_asignadas)
        sobrante = round(long_comercial_base - (util + perdida), 4)
        reutilizable = sobrante >= min_retazo_m
        rend = round((util / long_comercial_base) * 100.0, 2) if long_comercial_base > 0 else 0.0

        barras_procesadas.append(BarraResultado(
            id_barra=f"B-{contador_barras:03d}",
            tipo_origen="COMERCIAL",
            longitud_nominal=long_comercial_base,
            piezas=piezas_asignadas,
            num_cortes=n_c,
            perdida_corte_m=round(perdida, 4),
            longitud_util_m=round(util, 4),
            longitud_sobrante_m=max(0.0, sobrante),
            es_retazo_utilizable=reutilizable,
            rendimiento_pct=rend
        ))
        contador_barras += 1

    # Totales y Balances Globales
    tot_comprado = sum(b.longitud_nominal for b in barras_procesadas if b.tipo_origen == "COMERCIAL")
    tot_util = sum(b.longitud_util_m for b in barras_procesadas)
    tot_perdida = sum(b.perdida_corte_m for b in barras_procesadas)
    tot_retazos = sum(b.longitud_sobrante_m for b in barras_procesadas if b.es_retazo_utilizable)
    tot_scrap = sum(b.longitud_sobrante_m for b in barras_procesadas if not b.es_retazo_utilizable)
    tot_lineal_consumido = sum(b.longitud_nominal for b in barras_procesadas)
    aprov_global = round((tot_util / tot_lineal_consumido * 100.0), 2) if tot_lineal_consumido > 0 else 0.0

    return {
        "barras": barras_procesadas,
        "retazos_consumidos": retazos_consumidos_ids,
        "balance": {
            "long_comprada_m": round(tot_comprado, 3),
            "long_util_m": round(tot_util, 3),
            "perdida_corte_m": round(tot_perdida, 3),
            "retazos_recuperables_m": round(tot_retazos, 3),
            "desperdicio_real_m": round(tot_scrap, 3),
            "rendimiento_global_pct": aprov_global
        }
    }

# ==============================================================================
# 4. CONFIGURACIÓN Y ESTILOS DE LA INTERFAZ STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="SteelCalc 1D | Metrados y Optimización",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { color: #0b1f3a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700; }
    .stDataFrame thead tr th {
        background-color: #0b2545 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        padding: 14px 18px;
        border-radius: 8px;
        border-left: 6px solid #0b2545;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de Estados
if "metrado_partidas" not in st.session_state:
    st.session_state.metrado_partidas = []
if "inventario_retazos" not in st.session_state:
    st.session_state.inventario_retazos = []
if "optim_resultado" not in st.session_state:
    st.session_state.optim_resultado = None
if "catalogos_app" not in st.session_state:
    st.session_state.catalogos_app = CATALOGO_OFICIAL

# ==============================================================================
# 5. BARRA LATERAL (PARÁMETROS DE TALLER, SOLDADURA Y PROYECTO)
# ==============================================================================
with st.sidebar:
    st.title("⚙️ SteelCalc Pro")
    st.caption("Cálculo Estructural, Metrados y Optimización 1D")
    st.divider()

    st.subheader("Parámetros de Taller")
    param_kerf_mm = st.number_input("Espesor Disco de Corte (mm)", value=3.0, min_value=0.5, max_value=10.0, step=0.5)
    param_despunte_mm = st.number_input("Despunte de Extremos (mm)", value=0.0, min_value=0.0, max_value=50.0, step=5.0)
    param_min_retazo_m = st.number_input("Longitud Mín. Retazo Reutilizable (m)", value=0.50, min_value=0.10, max_value=3.0, step=0.10)
    param_costo_kg = st.number_input("Precio Estimado Acero ($/kg)", value=1.50, min_value=0.10, step=0.05)

    st.markdown("---")
    # OPCIÓN REQUERIDA: Aceptar unión con soldadura si falta medida
    check_permitir_soldar = st.checkbox(
        "⚡ Aceptar unión con soldadura si falta medida", 
        value=False,
        help="Permite descomponer piezas que superen la longitud comercial en tramos empalmados por soldadura."
    )

    kerf_m = param_kerf_mm / 1000.0
    despunte_m = param_despunte_mm / 1000.0

    st.divider()
    st.subheader("Gestión de Proyectos")
    proyecto_nombre = st.text_input("Nombre del Proyecto", value="Estructura Metálica")
    
    proj_data = {
        "proyecto": proyecto_nombre,
        "partidas": st.session_state.metrado_partidas,
        "retazos": st.session_state.inventario_retazos
    }
    st.download_button(
        "💾 Guardar Proyecto (JSON)",
        data=json.dumps(proj_data, indent=2),
        file_name=f"{proyecto_nombre.replace(' ', '_')}.json",
        mime="application/json",
        use_container_width=True
    )

    archivo_cargado = st.file_uploader("📂 Abrir Proyecto Existente", type=["json"])
    if archivo_cargado:
        try:
            datos_cargados = json.load(archivo_cargado)
            st.session_state.metrado_partidas = datos_cargados.get("partidas", [])
            st.session_state.inventario_retazos = datos_cargados.get("retazos", [])
            st.success("Proyecto cargado exitosamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al leer proyecto: {e}")

# ==============================================================================
# 6. CUERPO PRINCIPAL: PESTAÑAS FUNCIONALES
# ==============================================================================
tabs = st.tabs([
    "📋 Metrado Estructurado (Editable)",
    "✂️ Optimización y Plan de Corte",
    "♻️ Inventario de Retazos",
    "📊 Reportes Ejecutivos",
    "📚 Catálogo Técnico Actualizado"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: METRADO ESTRUCTURADO Y EDICIÓN INTERACTIVA CELDA POR CELDA
# ------------------------------------------------------------------------------
with tabs[0]:
    st.header("Metrado Jerárquico de Elementos Metálicos")
    
    with st.expander("➕ Formulario de Selección Inteligente de Materiales", expanded=True):
        f_col1, f_col2, f_col3 = st.columns([1.5, 2, 1.5])
        
        with f_col1:
            partida_codigo = st.text_input("N.º Partida Jerárquica", value=f"01.01.{len(st.session_state.metrado_partidas)+1:02d}")
            agrupador_nombre = st.text_input("Agrupador / Subpartida", value="01.01 — PERFILES METÁLICOS")
        
        with f_col2:
            familia_opciones = list(st.session_state.catalogos_app.keys())
            familia_seleccionada = st.selectbox("Familia del Perfil", familia_opciones)
            
            perfiles_en_familia = st.session_state.catalogos_app[familia_seleccionada]
            denominaciones = [p["denominacion"] for p in perfiles_en_familia]
            perfil_seleccionado_txt = st.selectbox("Perfil Comercial Catálogo", denominaciones)
            
            perfil_obj = next(p for p in perfiles_en_familia if p["denominacion"] == perfil_seleccionado_txt)

        with f_col3:
            long_comerciales_disp = perfil_obj.get("longitudes", [6.0])
            long_comercial_elegida = st.selectbox("Longitud Comercial (m)", long_comerciales_disp)
            st.info(f"**Peso Lineal:** {perfil_obj['peso_kg_m']} kg/m\n\n**Norma:** {perfil_obj.get('norma', 'ASTM A36')}")

        st.markdown("##### Despiece Requerido")
        st.caption("Registre longitudes requeridas. Si supera la barra comercial, active soldadura en la barra lateral.")
        
        d_col1, d_col2, d_col3 = st.columns([2, 2, 2])
        with d_col1:
            max_limit = 24.0 if check_permitir_soldar else long_comercial_elegida
            long_pieza_req = st.number_input("Longitud a Cortar (m)", min_value=0.10, max_value=float(max_limit), value=2.30, step=0.05)
        with d_col2:
            cant_piezas_req = st.number_input("Cantidad de Piezas", min_value=1, value=2, step=1)
        with d_col3:
            st.write("")
            st.write("")
            btn_agregar = st.button("➕ Insertar al Metrado", use_container_width=True, type="primary")

        if btn_agregar:
            perimetro_sup = calcular_perimetro_superficial(
                familia_seleccionada, perfil_obj["A"], perfil_obj.get("B", 0.0), perfil_obj.get("e", 0.0)
            )
            peso_unit = round(perfil_obj["peso_kg_m"] * long_pieza_req, 3)
            peso_tot = round(peso_unit * cant_piezas_req, 3)
            area_tot = round(perimetro_sup * long_pieza_req * cant_piezas_req, 3)

            nueva_fila = {
                "id": len(st.session_state.metrado_partidas) + 1,
                "partida": partida_codigo,
                "agrupador": agrupador_nombre,
                "familia": familia_seleccionada,
                "perfil": perfil_seleccionado_txt,
                "descripcion": f"{perfil_seleccionado_txt}, L = {long_pieza_req:.2f} m",
                "longitud_m": float(long_pieza_req),
                "und": "UND",
                "cantidad": int(cant_piezas_req),
                "peso_unit_kg": peso_unit,
                "peso_total_kg": peso_tot,
                "area_m2": area_tot,
                "peso_lineal_kg_m": perfil_obj["peso_kg_m"],
                "perimetro_m": perimetro_sup,
                "long_comercial_m": long_comercial_elegida
            }
            st.session_state.metrado_partidas.append(nueva_fila)
            st.success("Partida agregada correctamente.")
            st.rerun()

    # Visualización y Edición Dinámica Celda por Celda (st.data_editor)
    if st.session_state.metrado_partidas:
        st.subheader("Tabla Principal de Metrados (Editable Directamente)")
        st.caption("💡 **Doble clic** sobre cualquier celda para modificar valores. Para eliminar filas, selecciónelas a la izquierda y presione la tecla **Supr** (Delete).")

        df_editor = pd.DataFrame(st.session_state.metrado_partidas)
        
        # Columnas editables directamente por el usuario
        df_editado = st.data_editor(
            df_editor[[
                "partida", "descripcion", "longitud_m", "und", "cantidad", 
                "peso_unit_kg", "peso_total_kg", "area_m2"
            ]],
            column_config={
                "partida": st.column_config.TextColumn("N.º PARTIDA", required=True),
                "descripcion": st.column_config.TextColumn("ELEMENTO / DESCRIPCIÓN", required=True),
                "longitud_m": st.column_config.NumberColumn("LONGITUD (M)", min_value=0.05, format="%.2f m", required=True),
                "und": st.column_config.TextColumn("UND", disabled=True),
                "cantidad": st.column_config.NumberColumn("CANTIDAD", min_value=1, step=1, required=True),
                "peso_unit_kg": st.column_config.NumberColumn("PESO UNIT (KG/UND)", format="%.3f"),
                "peso_total_kg": st.column_config.NumberColumn("PESO TOTAL (KG)", format="%.2f"),
                "area_m2": st.column_config.NumberColumn("ÁREA SUP (M²)", format="%.3f")
            },
            num_rows="dynamic",
            use_container_width=True,
            key="editor_metrado"
        )

        # Sincronización automática de cambios y recálculo de fórmulas
        if len(df_editado) != len(st.session_state.metrado_partidas) or not df_editado.equals(df_editor[df_editado.columns]):
            nuevas_partidas = []
            for idx, r in df_editado.iterrows():
                # Conservar propiedades técnicas base o heredarlas
                p_base = st.session_state.metrado_partidas[idx] if idx < len(st.session_state.metrado_partidas) else st.session_state.metrado_partidas[-1]
                peso_lin = p_base["peso_lineal_kg_m"]
                perim = p_base["perimetro_m"]
                
                l_m = float(r["longitud_m"])
                cant = int(r["cantidad"])
                p_unit = round(peso_lin * l_m, 3)
                p_tot = round(p_unit * cant, 3)
                a_tot = round(perim * l_m * cant, 3)

                nuevas_partidas.append({
                    "id": idx + 1,
                    "partida": str(r["partida"]),
                    "agrupador": p_base.get("agrupador", "01.01 — PERFILES METÁLICOS"),
                    "familia": p_base.get("familia", "Tubo Rectangular LAC"),
                    "perfil": p_base.get("perfil", ""),
                    "descripcion": str(r["descripcion"]),
                    "longitud_m": l_m,
                    "und": "UND",
                    "cantidad": cant,
                    "peso_unit_kg": p_unit,
                    "peso_total_kg": p_tot,
                    "area_m2": a_tot,
                    "peso_lineal_kg_m": peso_lin,
                    "perimetro_m": perim,
                    "long_comercial_m": p_base.get("long_comercial_m", 6.0)
                })
            st.session_state.metrado_partidas = nuevas_partidas
            st.rerun()

        m1, m2, m3 = st.columns(3)
        m1.metric("Peso Neto Fabricación", f"{sum(p['peso_total_kg'] for p in st.session_state.metrado_partidas):,.2f} kg")
        m2.metric("Área Pintura Expuesta", f"{sum(p['area_m2'] for p in st.session_state.metrado_partidas):,.2f} m²")
        m3.metric("Total de Piezas a Cortar", f"{sum(p['cantidad'] for p in st.session_state.metrado_partidas)} und")

        col_b1, col_b2 = st.columns([5, 1])
        with col_b2:
            if st.button("🗑️ Vaciar Todo", use_container_width=True):
                st.session_state.metrado_partidas = []
                st.rerun()
    else:
        st.info("La tabla principal de metrados está actualmente vacía. Ingrese elementos mediante el formulario superior.")

# ------------------------------------------------------------------------------
# PESTAÑA 2: OPTIMIZACIÓN INTELIGENTE Y PLAN DE CORTE VISUAL
# ------------------------------------------------------------------------------
with tabs[1]:
    st.header("Optimizador de Corte 1D y Secuencias de Taller")
    
    if not st.session_state.metrado_partidas:
        st.warning("Debe ingresar elementos al metrado para ejecutar la optimización.")
    else:
        perfiles_unicos = sorted(list(set(p["perfil"] for p in st.session_state.metrado_partidas)))
        
        c_opt1, c_opt2, c_opt3 = st.columns([2, 2, 2])
        with c_opt1:
            perfil_objetivo = st.selectbox("Seleccione el Perfil a Optimizar", perfiles_unicos)
        with c_opt2:
            modo_optim = st.selectbox("Estrategia", ["Minimizar Desperdicio", "Minimizar Barras", "Optimizar por Costo"])
        with c_opt3:
            st.write("")
            st.write("")
            btn_ejecutar_opt = st.button("⚡ Ejecutar Optimización", type="primary", use_container_width=True)

        partidas_del_perfil = [p for p in st.session_state.metrado_partidas if p["perfil"] == perfil_objetivo]
        demandas_corte = [(p["partida"], p["descripcion"], p["longitud_m"], p["cantidad"]) for p in partidas_del_perfil]
        long_com = [partidas_del_perfil[0]["long_comercial_m"]]
        
        retazos_del_perfil = [
            r for r in st.session_state.inventario_retazos 
            if r["perfil"] == perfil_objetivo and r["estado"] == "Disponible"
        ]

        if btn_ejecutar_opt or (st.session_state.optim_resultado and st.session_state.get("perfil_opt_activo") == perfil_objetivo):
            res_opt = optimizar_1d_cutting_stock(
                demandas=demandas_corte,
                longitudes_comerciales=long_com,
                retazos_inventario=retazos_del_perfil,
                kerf_m=kerf_m,
                despunte_m=despunte_m,
                min_retazo_m=param_min_retazo_m,
                permitir_soldadura=check_permitir_soldar,
                modo=modo_optim
            )
            st.session_state.optim_resultado = res_opt
            st.session_state.perfil_opt_activo = perfil_objetivo
            
            bal = res_opt["balance"]
            
            # Métricas del Resultado
            r1, r2, r3, r4, r5 = st.columns(5)
            r1.metric("Longitud Comprada", f"{bal['long_comprada_m']} m")
            r2.metric("Longitud Útil", f"{bal['long_util_m']} m")
            r3.metric("Rendimiento", f"{bal['rendimiento_global_pct']}%")
            r4.metric("Retazos Útiles", f"{bal['retazos_recuperables_m']} m")
            r5.metric("Desperdicio Real", f"{bal['desperdicio_real_m']} m")

            st.markdown("#### Diagrama Visual del Plan de Corte (Proporcional)")
            
            fig = go.Figure()
            paleta_colores = ["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b", "#e377c2", "#17becf"]

            for b_idx, b in enumerate(res_opt["barras"]):
                eje_y = f"{b.id_barra} ({b.tipo_origen} {b.longitud_nominal}m)"
                
                # Graficar piezas útiles
                for p_idx, p in enumerate(b.piezas):
                    c_pieza = "#7c3aed" if p.es_soldado else paleta_colores[p_idx % len(paleta_colores)]
                    lbl_txt = f"{p.longitud}m (S)" if p.es_soldado else f"{p.longitud}m"
                    fig.add_trace(go.Bar(
                        y=[eje_y],
                        x=[p.longitud],
                        name="Pieza Soldada" if p.es_soldado else f"Pieza {p.longitud}m",
                        orientation='h',
                        marker=dict(color=c_pieza),
                        text=lbl_txt,
                        textposition='inside',
                        hoverinfo='text',
                        hovertext=f"Pieza: {p.descripcion} ({p.longitud}m) | Partida: {p.id_partida}",
                        showlegend=False
                    ))
                    # Espesor de disco
                    if kerf_m > 0 and p_idx < len(b.piezas) - 1:
                        fig.add_trace(go.Bar(
                            y=[eje_y],
                            x=[kerf_m],
                            name="Corte Disco",
                            orientation='h',
                            marker=dict(color="#111827"),
                            hoverinfo='skip',
                            showlegend=False
                        ))

                # Graficar remanente (Retazo vs Scrap)
                if b.longitud_sobrante_m > 0:
                    c_sobrante = "#f59e0b" if b.es_retazo_utilizable else "#ef4444"
                    txt_sobrante = f"Retazo: {b.longitud_sobrante_m}m" if b.es_retazo_utilizable else f"Scrap: {b.longitud_sobrante_m}m"
                    fig.add_trace(go.Bar(
                        y=[eje_y],
                        x=[b.longitud_sobrante_m],
                        name="Sobrante",
                        orientation='h',
                        marker=dict(color=c_sobrante),
                        text=txt_sobrante,
                        textposition='inside',
                        hoverinfo='text',
                        hovertext=f"Sobrante: {b.longitud_sobrante_m}m",
                        showlegend=False
                    ))

            fig.update_layout(
                barmode='stack',
                height=150 + len(res_opt["barras"]) * 45,
                margin=dict(l=10, r=10, t=30, b=30),
                xaxis_title="Longitud Desarrollada (Metros)",
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig, use_container_width=True)

            # Botón para almacenar retazos aprovechables
            if st.button("📥 Registrar Retazos Reutilizables en Almacén"):
                registrados = 0
                for b in res_opt["barras"]:
                    if b.es_retazo_utilizable:
                        st.session_state.inventario_retazos.append({
                            "id": len(st.session_state.inventario_retazos) + 1,
                            "perfil": perfil_objetivo,
                            "longitud_m": b.longitud_sobrante_m,
                            "origen": f"{b.id_barra} - {proyecto_nombre}",
                            "estado": "Disponible"
                        })
                        registrados += 1
                st.success(f"Se registraron {registrados} retazos aprovechables en el inventario.")
                st.rerun()

# ------------------------------------------------------------------------------
# PESTAÑA 3: INVENTARIO DE RETAZOS REUTILIZABLES
# ------------------------------------------------------------------------------
with tabs[2]:
    st.header("Gestión y Trazabilidad de Retazos Reutilizables")
    
    with st.expander("➕ Registro Manual de Retazo en Almacén"):
        r_col1, r_col2, r_col3 = st.columns(3)
        with r_col1:
            fam_r = st.selectbox("Familia", list(st.session_state.catalogos_app.keys()), key="fam_ret_man")
            perfiles_r = [p["denominacion"] for p in st.session_state.catalogos_app[fam_r]]
            perfil_r = st.selectbox("Perfil", perfiles_r, key="perf_ret_man")
        with r_col2:
            long_ret = st.number_input("Longitud Disponible (m)", min_value=0.20, max_value=12.0, value=1.80, step=0.05)
        with r_col3:
            orig_ret = st.text_input("Proyecto / Partida de Origen", value="Taller Central / Sobrante Obra")
            st.write("")
            if st.button("Guardar en Almacén", use_container_width=True):
                st.session_state.inventario_retazos.append({
                    "id": len(st.session_state.inventario_retazos) + 1,
                    "perfil": perfil_r,
                    "longitud_m": long_ret,
                    "origen": orig_ret,
                    "estado": "Disponible"
                })
                st.success("Retazo ingresado.")
                st.rerun()

    if st.session_state.inventario_retazos:
        df_retazos = pd.DataFrame(st.session_state.inventario_retazos)
        st.dataframe(df_retazos, use_container_width=True, hide_index=True)
        if st.button("Limpiar Almacén de Retazos"):
            st.session_state.inventario_retazos = []
            st.rerun()
    else:
        st.info("No hay retazos registrados en el almacén.")

# ------------------------------------------------------------------------------
# PESTAÑA 4: REPORTES EJECUTIVOS Y LISTAS DE COMPRA
# ------------------------------------------------------------------------------
with tabs[3]:
    st.header("Informes Técnicos y Presupuesto Consolidado")
    
    if st.session_state.metrado_partidas:
        df_base = pd.DataFrame(st.session_state.metrado_partidas)
        
        rep_compra = df_base.groupby(["familia", "perfil", "long_comercial_m"]).agg(
            longitud_util_total=("longitud_m", lambda x: sum(x * df_base.loc[x.index, "cantidad"])),
            peso_lineal=("peso_lineal_kg_m", "first"),
            area_total=("area_m2", "sum")
        ).reset_index()

        rep_compra["barras_comerciales_estimadas"] = np.ceil(rep_compra["longitud_util_total"] / rep_compra["long_comercial_m"]).astype(int)
        rep_compra["peso_bruto_compra_kg"] = round(rep_compra["barras_comerciales_estimadas"] * rep_compra["long_comercial_m"] * rep_compra["peso_lineal"], 2)
        rep_compra["costo_estimado_$"] = round(rep_compra["peso_bruto_compra_kg"] * param_costo_kg, 2)

        st.subheader("REPORTE B: Lista de Compra de Materiales Consolidada")
        st.dataframe(rep_compra.rename(columns={
            "familia": "FAMILIA",
            "perfil": "PERFIL TÉCNICO",
            "long_comercial_m": "LONG. COMERCIAL (M)",
            "longitud_util_total": "LONG. ÚTIL (M)",
            "peso_lineal": "PESO (KG/M)",
            "area_total": "ÁREA SUP. (M²)",
            "barras_comerciales_estimadas": "BARRAS REQUERIDAS",
            "peso_bruto_compra_kg": "PESO BRUTO (KG)",
            "costo_estimado_$": "PRESUPUESTO ($)"
        }), use_container_width=True, hide_index=True)

        col_tot1, col_tot2, col_tot3 = st.columns(3)
        col_tot1.metric("Peso Neto de Fabricación", f"{df_base['peso_total_kg'].sum():,.2f} kg")
        col_tot2.metric("Peso Bruto Comercial", f"{rep_compra['peso_bruto_compra_kg'].sum():,.2f} kg")
        col_tot3.metric("Presupuesto Estimado", f"$ {rep_compra['costo_estimado_$'].sum():,.2f}")

        # Generador de Excel descargable (.xlsx)
        buffer_excel = io.BytesIO()
        with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
            df_base.to_excel(writer, sheet_name="Metrado_General", index=False)
            rep_compra.to_excel(writer, sheet_name="Lista_Compra", index=False)
        
        st.download_button(
            "📊 Descargar Reporte Completo en Excel (.xlsx)",
            data=buffer_excel.getvalue(),
            file_name=f"Reporte_Estructuras_{proyecto_nombre.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
    else:
        st.info("Registre partidas en el metrado para generar los balances ejecutivos.")

# ------------------------------------------------------------------------------
# PESTAÑA 5: CONSULTA DIRECTA DE CATÁLOGOS TÉCNICOS
# ------------------------------------------------------------------------------
with tabs[4]:
    st.header("Biblioteca de Catálogos Homologados")
    st.caption("Propiedades geométricas, pesos y normas oficiales verificadas contra los catálogos proporcionados.")
    
    fam_sel_cat = st.selectbox("Seleccione Familia a Consultar", list(st.session_state.catalogos_app.keys()))
    df_cat_view = pd.DataFrame(st.session_state.catalogos_app[fam_sel_cat])
    st.dataframe(df_cat_view, use_container_width=True, hide_index=True)
