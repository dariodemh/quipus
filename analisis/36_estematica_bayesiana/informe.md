# 36 · Estemática cuantitativa y modelo bayesiano de error de copia

Fecha: 2026-11-23. Semilla: `20261123`.

## 1. Calibración empírica del canal de error

Combinamos las tres dobles lecturas independientes (`UR1107=UR237`, `AS125=UR247`, `KH0033=UR044`; $N = 64$ pares alineados) y las variantes entre testigos de copias reales en `analisis/33_estematica/variantes.csv` ($N = 225$ pares):

| Canal | Doble lectura ($N=64$) | Variantes entre copias ($N=225$) | Tasa calibrada |
|---|---:|---:|---:|
| Exacta (`a == b`) | 60 | 38 | 0.7500 |
| Error `±1` nudo/unidad | 0 | 15 | 0.0542 |
| Corrimiento decimal `×10 / ÷10` | 2 | 0 | 0.0102 |
| Transposición de dígitos | 0 | 0 | 0.0017 |
| Omisión / cuerda rota (`0`) | 0 | 108 | 0.3695 |
| Otra diferencia | 2 | 64 | 0.2271 |

---

## 2. Escáner bayesiano tolerante a errores sobre blancos sin lectura y fuera de muestra

Aplicamos alineación local de Smith-Waterman con log-verosimilitudes calibradas por canal (`LLR`) y **500 permutaciones** por candidato (`BH-FDR`) sobre:
1. Los **4 quipus sin lectura firme de Inkawasi** (`UR272, UR276, UR277, UR279`) contra Inkawasi y los mejores candidatos del corpus.
2. Los **30 quipus fuera de muestra** (`11 Huacones` + `19 OKR extra`) entre sí y contra el corpus de 651 quipus.

Archivo: [`candidatos_bayesianos.csv`](candidatos_bayesianos.csv).

- **Total de pares que superan el prefiltro (`LLR >= 8,0`, ≥4 coincidencias):** 210 (53 en Inkawasi sin lectura; 157 en el lote fuera de muestra).
- **Pares significativos tras BH-FDR (`q < 0,05`):** **0**.
- **Resultado honesto:** ni siquiera permitiendo errores `±1`, corrimientos `×10` y transposiciones de dígitos aparece ninguna copia oculta ni enlace aritmético significativo (`q < 0,05`) que conecte `UR272, UR276, UR277, UR279` con la cadena de Inkawasi, ni que conecte las 11 fichas de Huacones o los 19 OKR extra con Inkawasi o entre sí.

| Grupo | Quipu A | Quipu B | Sentido | LLR | Nulo máx | Exactas | ±1 | ×10 | p | q (BH) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| OOS-OKR-extra | KH0648 | UR113 | directo | 21.67 | 24.53 | 17 | 6 | 0 | 0.0080 | 0.2096 |
| OOS-OKR-extra | KH0648 | KH0702 | directo | 18.53 | 19.08 | 15 | 3 | 0 | 0.0080 | 0.2096 |
| Inkawasi-sin-lectura | UR272 | JC001 | directo | 18.48 | 17.86 | 11 | 1 | 1 | 0.0020 | 0.2096 |
| OOS-OKR-extra | KH0651 | UR011 | directo | 16.79 | 16.99 | 12 | 1 | 1 | 0.0060 | 0.2096 |
| OOS-Huacones | JC027 | UR1140 | directo | 15.63 | 14.83 | 5 | 2 | 0 | 0.0020 | 0.2096 |
| OOS-OKR-extra | KH0643 | KH0083 | directo | 12.7 | 12.7 | 4 | 0 | 0 | 0.0040 | 0.2096 |
| OOS-OKR-extra | KH0649 | UR011 | directo | 10.82 | 12.39 | 7 | 0 | 0 | 0.0080 | 0.2096 |
| OOS-OKR-extra | KH0633 | JC027 | directo | 8.8 | 9.0 | 2 | 1 | 0 | 0.0040 | 0.2096 |
| OOS-OKR-extra | KH0648 | UR004 | directo | 21.15 | 25.46 | 18 | 2 | 0 | 0.0140 | 0.2257 |
| OOS-OKR-extra | KH0633 | JC034 | inverso | 11.3 | 13.7 | 4 | 0 | 0 | 0.0120 | 0.2257 |
| OOS-OKR-extra | KH0633 | KH0645 | directo | 9.56 | 9.99 | 6 | 0 | 0 | 0.0120 | 0.2257 |
| OOS-Huacones | JC034 | HP004 | inverso | 8.34 | 8.34 | 4 | 2 | 0 | 0.0100 | 0.2257 |
| OOS-OKR-extra | KH0702 | UR278 | directo | 8.05 | 9.71 | 6 | 1 | 0 | 0.0140 | 0.2257 |
| OOS-OKR-extra | KH0648 | KH0650 | directo | 15.91 | 19.2 | 12 | 0 | 0 | 0.0180 | 0.2515 |
| OOS-OKR-extra | KH0651 | QU014 | directo | 13.74 | 15.89 | 6 | 1 | 0 | 0.0180 | 0.2515 |

---

## 3. Estemática filogenética cuantitativa (10 000 réplicas bootstrap)

Archivo: [`estematica_bootstrap.csv`](estematica_bootstrap.csv).

| Familia | Sitios | Sinapomorfías compartidas | Soporte bootstrap | Interpretación |
|---|---:|---:|---:|---|
| Inkawasi (UR278, UR266, UR275) | 12 | 5 | **99.8%** | Los desajustes compartidos en ambos libros dan soporte >99% al nodo alpha frente a errores independientes (no separa alpha de UR278->UR266->UR275 sin desglose). |
| Leymebamba F02 (UR006, UR009, UR021) | 4 | 1 | **14.3%** | Bootstrap repartido: (9,21)=14.3%, (6,21)=49.8%, (6,9)=15.0%. Confirma estrella no resuelta. |
| Costa Sur F08 (KH0049, UR122) | 44 | 1 | **100.0%** | 15652 presente en KH0049 B1[1] y UR122 B0[1] frente a suma 15649; UR122 omite/rompe 12 posiciones que KH0049 conserva. |

- **Conclusión estemática:** el nodo perdido `α` en Inkawasi (`UR278 → α → {UR266, UR275}`) recibe **>99 % de soporte bootstrap** frente a la hipótesis de derivación independiente (porque los desajustes compartidos entre `UR266` y `UR275` exigirían el doble de pasos evolutivos en paralelo; sigue indecidible frente a una copia serial `UR278 → UR266 → UR275` sin desglose). En Leymebamba (`F02`), el bootstrap cuantifica formalmente por qué el árbol es una estrella no resuelta con un único sitio informativo `UR009 = UR021 ≠ UR006`.
