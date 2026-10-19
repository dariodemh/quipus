# -*- coding: utf-8 -*-
"""
03_conversion.py -- de unidades a toneladas, hectareas, jornadas y hogares.
Genera escenarios_agronomia.csv con supuestos explicitos.
"""
import numpy as np, pandas as pd
from pathlib import Path
AQUI = Path(__file__).resolve().parent

UNIDADES = 61790
POR_COLUMNA = UNIDADES/9
DENS_MANI = 0.286          # kg/L, medido (IJCMAS 2019, vaina GG-20: 0.285-0.289)
DENS_BAJA, DENS_ALTA = 0.25, 0.32
AREA_AGRIC_PROV = 38900    # ha, 8.5% de 457716 ha (Wikipedia/INEI, orden de magnitud)
AREA_RIEGO_VALLE = 15000   # ha, supuesto
AREA_LUNALUANA = 1500      # ha, supuesto (valle alto estrecho)
CAP_ALMACEN = (8300, 13000)  # m3, n_hyslop
HOGARES_GUARANGA = 1000
HOGARES_4G = 4000
PERSONAS_HOGAR = 5

def fila(nombre, tipo, unidades, L, dens, rend, campanas, jornadas_ha,
         nivel, nota, frac=1.0):
    kg_u = L*dens
    t = unidades*kg_u/1000
    ha_reg = t*1000/rend          # hectareas equivalentes a lo registrado
    ha = ha_reg/frac              # hectareas cultivadas si solo se registro una fraccion
    ha_anual = ha/campanas
    vol = unidades*L/1000
    jor = ha*jornadas_ha
    hog_ha = ha_anual/1.5          # 1.5 ha de maní por hogar (supuesto)
    hog_jor = jor/80               # 80 jornadas de mit'a por hogar (supuesto)
    return dict(escenario=nombre, tipo=tipo, unidades=round(unidades,1),
                L_por_unidad=L, densidad_kg_L=dens, kg_por_unidad=round(kg_u,2),
                toneladas=round(t,1), rendimiento_kg_ha=rend, campanas_ano=campanas,
                fraccion_registrada=round(frac,3),
                hectareas_campana=round(ha,0), hectareas_anuales=round(ha_anual,0),
                volumen_m3=round(vol,0),
                pct_cap_8300_m3=round(100*vol/CAP_ALMACEN[0],1),
                pct_cap_13000_m3=round(100*vol/CAP_ALMACEN[1],1),
                jornadas_ha=jornadas_ha, jornadas_total=round(jor,0),
                hogares_estimados_tierra=round(hog_ha,0), hogares_estimados_trabajo=round(hog_jor,0),
                pct_4000_hogares=round(100*max(hog_ha,hog_jor)/HOGARES_4G,1),
                pct_area_agricola_prov=round(100*ha_anual/AREA_AGRIC_PROV,1),
                pct_valle_riego_sup=round(100*ha_anual/AREA_RIEGO_VALLE,1),
                pct_lunahuana_sup=round(100*ha_anual/AREA_LUNALUANA,0),
                kg_persona_ano=round(1000*t/(HOGARES_4G*PERSONAS_HOGAR),1),
                nivel=nivel, nota=nota)

filas = [
 fila("E1 mínimo (30 L, rinde 1200)", "total", UNIDADES, 30, DENS_MANI, 1200, 1, 60,
      "calculado", "extremo bajo de volumen y rinde tradicional alto; una campaña"),
 fila("E2 bajo (51 L, rinde 1000)", "total", UNIDADES, 51, DENS_MANI, 1000, 1, 80,
      "calculado", "límite inferior del IC90 de capacidad"),
 fila("E3 central (82 L, rinde 1000)", "total", UNIDADES, 82, DENS_MANI, 1000, 1, 80,
      "propuesto", "mediana de capacidad (IC90 51-127) y rinde tradicional medio"),
 fila("E4 central, 2 campañas", "total", UNIDADES, 82, DENS_MANI, 1000, 2, 80,
      "propuesto", "si 61 790 es el total anual y el valle hace 2 campañas de maní"),
 fila("E5 alto (127 L, rinde 800)", "total", UNIDADES, 127, DENS_MANI, 800, 1, 100,
      "calculado", "límite superior del IC90 y rinde tradicional bajo (década de 1950)"),
 fila("E6 máximo (130 L, rinde 700)", "total", UNIDADES, 130, DENS_MANI, 700, 1, 120,
      "calculado", "extremo alto de volumen y rinde bajo; cota superior"),
 fila("E7 central con rinde moderno", "total", UNIDADES, 82, DENS_MANI, 2000, 1, 80,
      "especulativo", "rinde moderno con insumos (Cañete 3437 kg/ha como techo)"),
 fila("E8 columna media (6866 u.)", "columna", POR_COLUMNA, 82, DENS_MANI, 1000, 1, 80,
      "propuesto", "una de las 9 partes como grupo de cultivadores o campo"),
 fila("E13 registro medio (2207 u.)", "registro", UNIDADES/28, 82, DENS_MANI, 1000, 1, 80,
      "propuesto", "media de las 28 filas; escala de un solo registro, no del libro"),
 fila("E9 cuota 47 (82 L)", "cuota", 47, 82, DENS_MANI, 1000, 1, 80,
      "calculado", "47/61790 del flujo total"),
 fila("E10 cuota 208 (82 L)", "cuota", 208, 82, DENS_MANI, 1000, 1, 80,
      "calculado", "208/61790 del flujo total"),
 fila("E11 sensibilidad densidad baja", "total", UNIDADES, 82, DENS_BAJA, 1000, 1, 80,
      "calculado", "vaina poco compactada (0.25 kg/L)"),
 fila("E12 sensibilidad densidad alta", "total", UNIDADES, 82, DENS_ALTA, 1000, 1, 80,
      "calculado", "vaina muy compactada (0.32 kg/L)"),
 fila("E14 E3 si solo registra 1/3 de la cosecha", "total", UNIDADES, 82, DENS_MANI, 1000, 1, 80,
      "especulativo", "si el quipu anota el tercio del Estado, el área cultivada se triplica", frac=1/3),
 fila("E15 E3 si solo registra 1/2 de la cosecha", "total", UNIDADES, 82, DENS_MANI, 1000, 1, 80,
      "especulativo", "si anota la mitad, el área cultivada se duplica", frac=1/2),
]
E = pd.DataFrame(filas)
E.to_csv(AQUI/"escenarios_agronomia.csv", index=False)

pd.set_option("display.width", 250)
print(E[["escenario","toneladas","hectareas_campana","volumen_m3","pct_cap_8300_m3",
         "pct_cap_13000_m3","jornadas_total","pct_4000_hogares",
         "pct_area_agricola_prov","kg_persona_ano"]].to_string(index=False))

print("\nPeso por unidad (kg): 30 L=%.1f, 51 L=%.1f, 82 L=%.1f, 127 L=%.1f, 130 L=%.1f"
      % tuple(L*DENS_MANI for L in (30,51,82,127,130)))
print("Total 61 790 unidades a 82 L: %.0f m3 = %.1f%%-%.1f%% de 8300-13000 m3"
      % (UNIDADES*82/1000, 100*UNIDADES*82/1000/13000, 100*UNIDADES*82/1000/8300))
print("Por columna: %.0f unidades -> %.1f t -> %.0f ha a 1000 kg/ha -> %.0f jornadas a 80/ha"
      % (POR_COLUMNA, POR_COLUMNA*82*DENS_MANI/1000,
         POR_COLUMNA*82*DENS_MANI/1000, POR_COLUMNA*82*DENS_MANI/1000*80))
print("\nGuardado: escenarios_agronomia.csv")
