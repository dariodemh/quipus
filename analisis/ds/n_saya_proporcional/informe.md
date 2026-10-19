# Proporcionalidad wanka y capacidad real de Inkawasi

**Equipo:** DeepSeek · carpeta `analisis/ds/n_saya_proporcional/`
**Fecha:** 18 de octubre de 2026
**Semilla:** 20261018 (todo el código es reproducible)
**Datos primarios nuevos:** `analisis/fuentes_txt/LeVine1992_notas.md` (resumen de LeVine ed., *Inka Storage Systems*, 1992: Snead cap. 3 sobre Inkawasi; D'Altroy y Hastorf sobre los wanka; glosario de unidades).
**Datos de quipus:** `analisis/13_sistema_incahuasi/ur278_tabla.csv`, `ur270_ur278.csv`, `analisis/datos/cuerdas.csv` (UR270), e informes previos `ds/n_nueve_partes/` y `ds/n_almacenes/`.
**Scripts:** `01_datos.py`, `02_modelos.py`, `02b_diagnosticos.py`, `02c_sayas.py`, `02d_novenos.py`, `02e_independencia.py`, `03_capacidad.py`, `04_verificacion.py` (79/79 comprobaciones OK).

---

## Resumen de veredictos

| # | Hipótesis | Veredicto | Cifra clave | Nivel |
|---|---|---|---|---|
| A1 | Las 9 columnas de UR278 son cuotas **estrictamente proporcionales** a poblaciones fijas (leva wanka) | **Rechazada** | Las cuotas varían 3,68 veces más que el muestreo multinomial; LRT M1→M2 = 1 848; LOO M2−M1 = 1 028 puntos | **demostrado (negativo)** |
| A2 | Proporción fija **más una perturbación por registro** (Dirichlet-multinomial) | **Mucho mejor que A1, pero incompleta** | α = 165,6; sobredispersión 14,7× en N medio; falla en tamaño, tendencia, autocorrelación y PC1 | **apoyado con datos** como descripción; **no apoyado** como modelo completo |
| A3 | Proporciones **independientes por registro** (modelo saturado) | **No es un mecanismo; su victoria en AIC/BIC(24) es de saturación** | AIC M3 = 1 726 vs M2 = 2 062; pero BIC(54 601) favorece M2 por 1 294; W observado 0,484 vs 0,176 con columnas independientes | **demostrado** que no es producción independiente; **no apoyado** como modelo |
| A4 | Hay columnas de **cuota fija** y otras variables | **No hay ninguna cuota fija**; sí un gradiente de ~5× en variabilidad | ρ de c4 = 0,0024 vs c8 = 0,0123; LRT de heterogeneidad p = 0,003 (bootstrap 0,0125) | **demostrado (negativo)** para cuota fija; **apoyado con datos** para el gradiente |
| A5 | Las cuotas cambian con el **orden de los registros** (tendencia o cambio de régimen) | **Señal bruta fuerte, pero casi toda explicada por el tamaño del registro** | Tendencia bruta p = 0,0012; cambio de régimen p = 0,0004; tras controlar log N, p = 0,15; tamaño p = 0,041 | **apoyado con datos** (efecto de tamaño); **propuesto/especulativo** (efecto temporal residual) |
| A6 | Las 9 columnas se reparten en **dos sayas** con cuota fija | **Sin evidencia** | Mejor bipartición ρ = −0,056, p = 0,36 frente al nulo de selección; 4+5 ρ = 0,00057, p = 0,80 | **demostrado (negativo)** para las biparticiones probadas |
| A7 | Las 9 columnas reproducen las fracciones wanka **2/9, 3/9, 4/9** | **No las reproducen** | 0,281 / 0,318 / 0,401 vs 0,222 / 0,333 / 0,444; p = 0,00005 | **demostrado (negativo)** bajo el supuesto de columnas iguales |
| B1 | La capacidad de Inkawasi pone una **cota superior** al volumen unitario de UR278 | **146–181 L** si todo el libro se almacena a la vez | Cota superior: 146,5 L (202 cuartos) a 181,3 L (250); intervalo completo 32,0–181,3 L | **demostrado bajo los supuestos** |
| B2 | La fanega (56 L) o el saco (30–55 L) quedan **excluidos** por la capacidad | **No**: ambos caben; el extremo bajo del saco (30 L) es el único al borde | Fanega: 31–38 % de la cota superior, compatibilidad 0,50; saco 55 L: 0,46; saco 30 L: 0,00 | **demostrado (negativo)** para la exclusión de la fanega |
| B3 | El volumen unitario central es ~1 fanega | **Más bien ~1,5 fanegas**, pero con enorme incertidumbre | Mediana 82,4 L (IC90 51,4–126,9); fanega en el percentil ~9; costal de 69 L el más compatible (0,86) | **propuesto** |
| B4 | Si el libro de periodo L4 (300 378) se almacena a la vez, la fanega queda excluida | **Cierto, pero el supuesto es poco plausible** | L4: 6,6–37,3 L; fanega compatibilidad 0,00; arroba 0,94 | **condicional / especulativo** |

---

## 1. Pregunta

El encargo tiene dos partes independientes.

**A. La regla wanka de proporcionalidad.** D'Altroy y Hastorf resumen en LeVine (1992: 264–265) que, entre 1533 y 1537, las dos divisiones provinciales (`saya`) de Lurinwanka y Hatunxauxa movilizaron ciertos bienes "en proporción directa a las poblaciones relativas de las dos saya". Si las 9 columnas de UR278 (Inkahuasi, valle de Cañete) son unidades de población —pachacas u otras subunidades, la identificación que `n_nueve_partes` dejó como **propuesta**—, una leva proporcional predice que la **participación de cada columna en el total de la fila es constante** entre registros, salvo un ruido pequeño de conteo. Si las columnas fueran producciones independientes (chacras, cuadrillas, depósitos), las cuotas variarían mucho más. `n_nueve_partes` encontró que la cuota de cada columna varía ~3,5 veces más de lo que explica el muestreo; aquí se formaliza esa observación con tres modelos, una prueba de bondad de ajuste por simulación, un análisis por columna y controles de tamaño y orden.

La comparación es **analógica**, no genealógica: los documentos wanka son de Jauja (1533–1537) y los quipus son de Inkahuasi (Cañete, costa central). No se está probando que UR278 sea wanka, sino si el **modelo mecánico** que la regla wanka implica (cuotas proporcionales a poblaciones fijas) describe la estructura de las 9 columnas. Además, el propio `n_nueve_partes` advierte que las 9 columnas podrían no ser población; el test sirve para aceptar o rechazar esa lectura, no para presuponerla.

**B. La capacidad real de Inkawasi.** Snead (en LeVine 1992: 93, ficha 9, citando a Hyslop 1985) documenta **202 cuartos de almacén** (de unos 250 estimados), de **3,5–4 m de lado**, sin puertas, en el sector A de Inkawasi; el sitio fue una base militar ocupada poco tiempo (LeVine 1992: 78–79). Con esos datos —y no con el volumen agregado de 6 400 m³ que usó `n_almacenes`— se recalcula la **cota superior del volumen de la unidad** si todo lo registrado (UR278 = 61 790 unidades; el libro completo del flujo, no un solo registro) estuvo almacenado a la vez, y se compara con la fanega (≈56 L) y con el saco de 30–55 L propuesto por `n_almacenes`. Se actualiza la tabla de escenarios y se identifica qué supuestos dominan la incertidumbre.

---

## 2. Método

### 2.1 Datos y unidad de análisis

- **UR278:** la tabla de `13_sistema_incahuasi` tiene 28 filas × 9 columnas y suma **61 790 unidades**. Para los modelos de composición se usan las **24 filas completas** (9 columnas sin huecos), que suman **54 601 unidades**. Las 4 filas incompletas (grupos 10, 18, 26 y 32, con 7, 8, 10 y 12 columnas) se excluyen porque una composición de 9 partes no está definida; se usan solo en el control del total. Es la misma reconstrucción de `n_nueve_partes` (24 filas estrictas; 54 601 unidades), y la diferencia con 61 790 es de reconstrucción, no de datos.
- **UR270:** se reconstruyen los grupos de exactamente 9 colgantes de nivel 0; cada celda es colgante + primera subsidiaria (parte B + parte A), como en `13_sistema`. Quedan **6 grupos completos** (11 392 unidades), que corresponden a los mismos registros que 5 filas de UR278. **No son una muestra independiente**: son el detalle de los mismos registros. Se usan como replicación a nivel de cuerda, no como prueba independiente.
- **Unidad de análisis:** el registro (fila) y el quipu, no la cuerda. Los contrastes de orden y de tamaño se hacen sobre las 24 filas; no hay tests a nivel de cuerda suelta.
- **Valores 0 sin nudos = ausentes**, nunca ceros (regla del brief). En UR278 no hay celdas 0 en las 24 filas completas.
- **Orden:** la fila física del quipu (grupos 0, 1, 2, …, 31, con huecos en 15, 20, 23 y 24). Según `13_sistema`, las filas 11–19 corresponden a los registros 0–8 de UR273 y las filas 21–29 a los registros 9–19; las filas 0–10 son anteriores. El orden es, por tanto, el de registros sucesivos del mismo flujo.

### 2.2 Modelos de composición

Sea \(x_i=(x_{i1},…,x_{i9})\) el vector de las 9 columnas del registro \(i\), \(N_i=\sum_j x_{ij}\), \(p_{ij}=x_{ij}/N_i\).

- **M1 — proporción fija + ruido multinomial.** \(x_i \sim \mathrm{Multinomial}(N_i,p)\), con \(p\) común a todos los registros (8 parámetros libres). Es la forma estadística exacta de "cada unidad aporta una fracción fija de la población; el único ruido es el conteo". Su límite es el que la regla wanka predice si las poblaciones relativas son fijas.
- **M2 — proporción fija + perturbación por registro.** \(p_i \sim \mathrm{Dirichlet}(\alpha p)\), \(x_i\mid p_i \sim \mathrm{Multinomial}(N_i,p_i)\) (9 parámetros: 8 de \(p\) y \(\alpha\)). Es un Dirichlet-multinomial (DM). Con \(\alpha\to\infty\) se recupera M1; con \(\alpha\) finito, cada registro tiene su propia composición, pero todas giran alrededor del mismo perfil \(p\). "Concentración alta" significa \(\alpha\) grande; el modelo estima \(\alpha\) y también se ajusta una versión con \(p\) fijo en el MLE de M1 para el test de sobredispersión.
- **M3 — proporciones independientes por registro.** \(x_i \sim \mathrm{Multinomial}(N_i,p_i)\) con \(p_i\) libre para cada fila (192 parámetros). Es el modelo saturado: por construcción tiene devianza 0 y reproduce exactamente las proporciones observadas. No es un mecanismo; es el nulo "cada registro tiene su propia composición, sin nada común".

**Comparación.** Se reportan log-verosimilitud, AIC, BIC con \(n=24\) (número de filas) y con \(n=54\,601\) (número de unidades contadas), y una **verosimilitud predictiva leave-one-out (LOO)**: se ajusta cada modelo con 23 filas y se evalúa la probabilidad de la fila dejada fuera. La LOO es la comparación más limpia entre M1 y M2 porque castiga la complejidad por capacidad predictiva, no por un conteo ambiguo de \(n\). Para M3 no hay una LOO bien definida sin un prior sobre \(p_i\); el prior natural es precisamente el DM de M2. Se reporta el test de razón de verosimilitud (LRT) M1→M2 con **bootstrap paramétrico** (1 000 réplicas simuladas de M1) porque \(\alpha\to\infty\) está en la frontera del espacio de parámetros.

**Bondad de ajuste por simulación.** Se simulan 4 000 réplicas de M1 y 2 000 de M2 con los \(N_i\) observados y se calculan ocho estadísticos:

| estadístico | qué mide | dirección esperada si M1/M2 es cierto |
|---|---|---|
| `R_CV` | CV intra-columna medio de las cuotas / CV multinomial esperado | ≈1 |
| `CVcol` | CV entre las 9 medias de columna | ≈0,19 (control; no discrimina) |
| `W` | W de Kendall: acuerdo del orden de las 9 columnas entre filas | alto si hay perfil fijo |
| `PC1` | fracción de varianza del CLR explicada por el primer componente | alta si hay perfil fijo |
| `H` | SD entre columnas de \(\log(\mathrm{var\ observada}/\mathrm{var\ multinomial})\) | baja si la sobredispersión es homogénea |
| `T` | media de \(\rho^2\) parcial entre cada columna y el orden, controlando \(\log N\) | baja si no hay tendencia |
| `S` | máximo \(|\rho|\) entre una columna y \(\log N\) | bajo si la composición no depende del tamaño |
| `L` | distancia CLR media entre filas adyacentes / distancia entre pares al azar | ≈1 si no hay autocorrelación |

Los p-valores son **a dos colas** (2 × la cola menor), empíricos, \((k+1)/(B+1)\). Se aplica **BH-FDR dentro de cada modelo** sobre los 8 estadísticos, y se informa \(q\). Esto corrige por comparaciones múltiples; los estadísticos están correlacionados, así que BH es conservador en algunos y anti-conservador en otros, pero es la corrección estándar y explícita.

### 2.3 Análisis por columna, tamaño y orden

- **Beta-binomial marginal por columna:** \(x_{ij}\sim\mathrm{BetaBinomial}(N_i,p_j,\rho_j)\). \(\rho_j\) es la correlación intraclase de la cuota: \(\rho_j=0\) es cuota fija (solo ruido binomial); \(\rho_j>0\) es variabilidad extra. Se ajusta por máxima verosimilitud, se prueba \(\rho_j=0\) con LRT (mezcla \(0{,}5\chi^2_0+0{,}5\chi^2_1\) en la frontera) y se aplica BH sobre las 9 columnas. Se prueba también \(\rho_j\) común frente a \(\rho_j\) libre (LRT de 8 gl) y se calibra con bootstrap paramétrico (400 réplicas) porque las estimaciones pueden caer en la frontera.
- **Elasticidad al tamaño:** regresión \(\log x_{ij}=a_j+b_j\log N_i\). \(b_j=1\) es proporcionalidad estricta; \(b_j<1\) es sub-proporcional (componente fijo o saciedad); \(b_j>1\) es super-proporcional. El contraste conjunto es \(S=\sum_j(b_j-1)^2\), calibrado contra **3 000 simulaciones de M2** (el mejor modelo estacionario sin efecto de tamaño), no contra un bootstrap de filas (que rompe la estructura y da un p inflado). También se reportan los interceptos de \(x_{ij}=a_j+b_jN_i\) como descriptivos de un componente aditivo.
- **Orden:** \(\rho\) de Spearman parcial de cada cuota con el orden, controlando \(\log N\); estadístico multivariado \(T\) (media de \(\rho^2\) parcial) con **5 000 permutaciones del orden**; cambio de régimen (máximo estadístico de separación entre dos tramos sobre el CLR) con 5 000 permutaciones. Como el tamaño del registro también cambia con el orden, se repite el cambio de régimen **sobre los residuos de CLR tras regresar en \(\log N\)** y se calcula el \(R^2\) parcial del orden dado el tamaño y del tamaño dado el orden, con permutaciones. Esta es la prueba decisiva contra la explicación "aburrida": si el cambio desaparece al controlar el tamaño, no hay cambio de régimen, solo registros más pequeños.

### 2.4 Dos sayas y fracciones 2/9, 3/9, 4/9

- **Dos sayas:** la regla wanka es sobre **dos** divisiones, no sobre 9 columnas. Si las 9 columnas se agrupan en dos sayas, la cuota del grupo debería ser fija aunque las columnas individuales varíen. Se prueban las **126 biparticiones** de 4 columnas (el complemento de 5 es la misma partición) y las 8 particiones contiguas. Para cada grupo se estima \(\rho\) de la cuota por el método de momentos: \(\mathrm{Var}(q_i)\approx p(1-p)[\rho+(1-\rho)/N_i]\), regresando \((q_i-p)^2\) en \(1/N_i\). El estadístico es el **mínimo \(\rho\) sobre las 126 biparticiones**; se compara con el mismo mínimo en 1 000 simulaciones de M2 (que no tiene estructura de grupo). Así se corrige por haber elegido la mejor partición. Para las particiones contiguas se reporta el p de cada una y BH sobre las 8.
- **Fracciones 2/9, 3/9, 4/9:** Chirinos (2010), citado en la ficha local `2013-Curatola`, documenta para Hatun Xauxa fracciones de 2/9, 3/9 y 4/9. Si las 9 columnas son 9 unidades iguales y se agrupan 2+3+4 en el orden físico, las cuotas deberían ser 0,222/0,333/0,444. Se contrasta con 20 000 bootstrap de filas y un test de Mahalanobis conjunto. Supuesto fuerte: columnas iguales y agrupación contigua; si las columnas tienen poblaciones desiguales, el test no aplica.

### 2.5 Capacidad de Inkawasi

- **Geometría:** 202 cuartos documentados (250 estimados), lado \(l\in[3{,}5;4]\) m, altura \(h\in[2;3{,}5]\) m, llenado \(f\in[0{,}4;0{,}8]\). Volumen bruto \(G=n\,l^2h\); volumen ocupado \(V=fG\). El llenado se interpreta como fracción del volumen geométrico del cuarto ocupada por el producto o sus envases; no descuenta el hueco entre envases ni el espacio de acceso.
- **Cota superior si todo el ledger se almacena a la vez:** \(v\le 0{,}8\,G_{\max}/N\). La cota inferior, si el depósito estaba al menos al 40 %, es \(v\ge 0{,}4\,G_{\min}/N\). Se reporta el intervalo completo \([0{,}4G_{\min}/N,\,0{,}8G_{\max}/N]\) porque la cota superior sola no dice si la unidad es compatible con un llenado razonable.
- **Ledgers:** L2 = UR278, 61 790 unidades (el libro del flujo 47); L2b = UR266, 56 986; L3 = UR269, 122 609 (libro maestro); L4 = UR268, 300 378 (nivel de periodo). El encargo pide L2; L3 y L4 se incluyen como sensibilidad porque la elección de ledger resulta ser el supuesto dominante.
- **Monte Carlo:** 200 000 extracciones independientes con prior uniforme sobre cuartos, lado, altura y llenado. Se calcula la mediana y el IC90 del volumen unitario implicado \(v=VG/N\), la probabilidad de que el sitio sea lo bastante grande (\(V\ge Nv\)), y la **compatibilidad de dos lados** \(P(0{,}4G\le Nv\le 0{,}8G)\), que es la fracción del espacio de supuestos en que la unidad llena el depósito entre 40 y 80 %. No es una verosimilitud ni una probabilidad posterior; es una probabilidad predictiva bajo los supuestos declarados.
- **Descomposición de la incertidumbre:** \(\log v=\log n+2\log l+\log h+\log f-\log N\). Con priors uniformes independientes, la varianza de cada término es exacta: \(\mathrm{Var}(\log X)=(\log(b/a))^2/12\) para \(X\sim U(a,b)\), y \(4\,\mathrm{Var}(\log l)\) para el lado al cuadrado. Se reportan las participaciones con y sin la elección de ledger. Es una descomposición exacta, no una simulación.
- **Unidades de comparación:** fanega = 56 L (LeVine 1992, glosario p. 346: 1,6 bushels ≈ 56 L); saco = 30–55 L (`n_almacenes`); arroba = 15,5 L / 11,5 kg; carga de llama = 30–40 L / 23–30 kg; costal de 50 kg = 69 L; ración = 1,0–1,75 L; cuadro de 23 × 23 cm = 1,6–5,3 L. Las densidades para la masa son las de `n_almacenes` (0,20–0,30 t/m³ para maní con cáscara; 0,25–0,40 ají seco; 0,40–0,55 chuño; 0,60–0,80 maíz/frijol).

---

## 3. Resultados A: proporcionalidad de las 9 columnas

### 3.1 Comparación de modelos

| modelo | k | LL | AIC | BIC(24) | ΔAIC | ΔBIC(24) | BIC(54 601) |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1 multinomial (proporción fija) | 8 | −1 948,50 | 3 913,00 | 3 922,43 | 2 187,12 | 1 970,36 | 3 984,27 |
| M2 Dirichlet-multinomial (proporción fija + perturbación) | 9 | −1 021,94 | 2 061,87 | 2 072,47 | 335,99 | 120,40 | **2 142,04** |
| M3 proporciones libres por registro (saturado) | 192 | −670,94 | **1 725,88** | **1 952,07** | 0 | 0 | 3 436,18 |

- **M1 → M2:** la ganancia es de 926,6 puntos de log-verosimilitud con **un solo parámetro adicional**. LRT = **1 848,2**; p < 0,001 con la mezcla y p = 0,001 con el bootstrap paramétrico (1 000 réplicas; el mínimo posible con 1 000 es 0,001). α = **165,6**, que implica un factor de sobredispersión \((N+\alpha)/(1+\alpha)=\) **14,7** en el N medio (2 275). Es decir: la perturbación por registro no es pequeña; produce cuotas con una SD relativa de ~22 %, frente al ~6 % del muestreo.
- **M2 → M3:** M3 gana por AIC y por BIC(24) porque es saturado: tiene 192 parámetros para 24 filas y devianza 0 por construcción. Con \(n=54\,601\), BIC favorece a M2 por **1 294 puntos**. La conclusión no puede depender de qué se cuenta como \(n\), y por eso se usa la LOO.
- **LOO predictiva:** M1 = −2 062,79; M2 = −1 034,68; diferencia = **1 028,11** a favor de M2, que gana en **23 de 24** filas. Es la evidencia más limpia de que la proporción fija con ruido multinomial no describe los datos: un modelo que permite una perturbación por registro predice mucho mejor la fila que no ha visto.
- **Devianza residual de M2:** \(2(LL_3-LL_2)=701,9\) con 183 gl. Si M2 fuera el modelo verdadero, se esperaría ~183. La falta de ajuste residual es ~3,8× y anticipa los fallos de GOF de §3.2.

**Lectura.** M1 (proporcionalidad estricta) queda **rechazado**. M2 es una descripción mucho mejor, pero no completa. M3 no es un mecanismo: su victoria en AIC/BIC(24) es el comportamiento esperado de un modelo saturado con 8 parámetros por fila; además, la dirección de la falta de ajuste de M2 es hacia **más** estructura común (PC1 y W observados mayores que M2), no hacia la independencia. Es decir, M3 no debe leerse como "cada registro tiene su propia proporción independiente", sino como un recordatorio de que la perturbación de M2 (Dirichlet iid) no captura la estructura común, temporal y de tamaño.

### 3.2 Bondad de ajuste por simulación

| estadístico | observado | M1 (media simulada) | p M1 | q M1 | M2 (media simulada) | p M2 | q M2 | lectura |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `R_CV` | 3,684 | 1,042 | 0,0005 | 0,001 | 3,801 | 0,558 | 0,627 | M1 no reproduce la sobredispersión; M2 sí |
| `CVcol` | 0,1929 | 0,1735 | 0,0005 | 0,001 | 0,2014 | 0,627 | 0,627 | M1 subestima la dispersión entre medias; M2 ajusta |
| `W` | 0,4837 | 0,882 | 0,0005 | 0,001 | 0,407 | 0,172 | 0,229 | M1 predice demasiado acuerdo; M2 es consistente |
| `PC1` | 0,4277 | 0,2816 | 0,002 | 0,0027 | 0,2776 | **0,001** | **0,0027** | M2 **subestima** la concentración en un eje común |
| `H` | 0,4221 | 0,2996 | 0,141 | 0,141 | 0,292 | 0,097 | 0,155 | heterogeneidad de varianzas entre columnas, marginal |
| `T` | 0,1436 | 0,0492 | 0,0015 | 0,0024 | 0,0461 | **0,001** | **0,0027** | hay tendencia con el orden que M2 no recoge |
| `S` | 0,6435 | 0,3747 | 0,016 | 0,018 | 0,3753 | **0,021** | **0,042** | la composición depende del tamaño del registro |
| `L` | 0,8308 | 0,9994 | 0,0005 | 0,001 | 1,0000 | **0,001** | **0,0027** | las filas adyacentes son más parecidas que al azar |

- **M1 falla en 7 de 8 estadísticos** (todos menos `H`): no reproduce la sobredispersión, ni el desacuerdo de rangos, ni la dispersión entre columnas, ni la tendencia, ni el tamaño. La proporcionalidad estricta no es una descripción viable.
- **M2 ajusta lo marginal** (`R_CV`, `CVcol`, `W`: p ≥ 0,17) pero **falla en cuatro dimensiones** después de BH: `PC1` (q = 0,003), `T` (q = 0,003), `L` (q = 0,003) y `S` (q = 0,042). La dirección es informativa: los datos tienen **más** concentración en un eje común, **más** tendencia, **más** autocorrelación y **más** dependencia del tamaño que el DM con perturbaciones iid. No es que falte independencia; es que sobra estructura.
- **`H` marginal** (p = 0,097; q = 0,155): la heterogeneidad de varianzas entre columnas es sugerente pero no sobrevive BH en esta familia. Se examina aparte en §3.3, donde el LRT específico sí es significativo.

### 3.3 ¿Hay columnas de cuota fija y otras variables?

**Perfil y variabilidad por columna** (24 filas; `media_p` es la media de las cuotas, no el MLE):

| col | media_p | CV obs | CV multinomial | razón CV | ρ beta-binomial | EE ρ | q (ρ=0, BH) |
|---|---:|---:|---:|---:|---:|---:|---:|
| c1 | 0,1371 | 0,1716 | 0,0526 | 3,26 | 0,00402 | 0,00129 | 4,1·10⁻³⁵ |
| c2 | 0,1436 | 0,2066 | 0,0512 | 4,03 | 0,00724 | 0,00221 | 4,2·10⁻⁷¹ |
| c3 | 0,0960 | 0,2332 | 0,0643 | 3,62 | 0,00570 | 0,00178 | 1,6·10⁻⁵¹ |
| c4 | 0,1081 | 0,1533 | 0,0602 | **2,55** | **0,00238** | 0,00082 | 6,6·10⁻²¹ |
| c5 | 0,1141 | 0,2096 | 0,0584 | 3,59 | 0,00463 | 0,00147 | 3,5·10⁻⁴⁵ |
| c6 | 0,1258 | 0,1947 | 0,0553 | 3,52 | 0,00433 | 0,00138 | 3,1·10⁻⁴¹ |
| c7 | 0,1062 | 0,3031 | 0,0608 | **4,98** | **0,01054** | 0,00317 | 2,0·10⁻⁹⁵ |
| c8 | 0,0796 | 0,3278 | 0,0713 | 4,60 | **0,01230** | 0,00384 | 1,9·10⁻⁸⁸ |
| c9 | 0,0896 | 0,1935 | 0,0668 | 2,90 | 0,00316 | 0,00106 | 2,1·10⁻²⁴ |

- **Ninguna columna tiene cuota fija.** Las 9 tienen \(\rho>0\) con q < 10⁻²⁰; incluso la más estable (c4) tiene una varianza 6,4× la binomial en el N medio. En términos sustantivos, la cuota de una columna típica (p ≈ 0,11) tiene una SD de ~2,4 puntos porcentuales, es decir, ~22 % relativo; una leva proporcional con poblaciones fijas solo debería tener el ruido de conteo (~5–7 %).
- **Sí hay un gradiente real de estabilidad.** c4 y c9 son las más estables (ρ = 0,0024 y 0,0032; razón CV 2,6–2,9); c7 y c8 las más variables (ρ = 0,0105 y 0,0123; razón CV 4,6–5,0). El LRT de \(\rho\) común (0,00593) frente a \(\rho_j\) libre da **23,30** con 8 gl, p = **0,003** (chi²) y p = **0,0125** (bootstrap 400). La heterogeneidad es de ~5× y sobrevive la calibración por simulación. Es el matiz correcto a "todas las columnas son iguales": no son cuotas fijas, pero tampoco son igualmente variables.
- **No hay cuota absoluta fija.** Todas las columnas escalan con el total de la fila: \(\rho(x_{ij},N_i)\) va de 0,69 a 0,88; el CV de los totales de fila es **0,35** (rango 1 278–4 273, factor 3,3). Una cuota fija absoluta (\(x_{ij}\approx q_j\)) requeriría totales de fila constantes y columnas sin correlación con N; no es el caso.
- **La escala no es proporcional.** Elasticidades \(\log x\) vs \(\log N\):

| col | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| elasticidad | 0,789 | **0,577** | 0,750 | 1,091 | 1,116 | 1,003 | **1,524** | **1,665** | 0,990 |
| EE clásica | 0,102 | 0,119 | 0,161 | 0,101 | 0,126 | 0,116 | 0,180 | 0,305 | 0,131 |

  El contraste conjunto \(S=\sum(b_j-1)^2=1,024\) frente al nulo de M2 (mediana 0,18; p95 0,389) da **p = 0,0003**: la composición depende del tamaño del registro. Bajo el nulo de M2, las desviaciones más claras son **c2** (z = −3,34; sub-proporcional), **c7** (z = +3,49) y **c8** (z = +3,69; super-proporcionales); c1 (z = −1,65) y c3 (z = −1,63) son sugerentes pero no concluyentes. Con el SE clásico y BH, c2 (q = 0,016) y c7 (q = 0,036) sobreviven; c8 tiene un SE conservador (0,305) y su p clásico es 0,04, pero frente al nulo M2 es <0,001, porque el SE clásico sobreestima la incertidumbre.
- **Interceptos lineales** (\(x=a+bN\)): c1 +70 (p = 0,022), c2 +128 (p = 0,001), c7 −106 (p = 0,011), c8 −91 (p = 0,013); c3–c6 y c9 no significativos. Es decir, c1 y c2 tienen un componente aditivo positivo (una parte "fija" de ~70–128 unidades, 22–39 % de su media), mientras c7 y c8 tienen interceptos negativos (crecen más que proporcionalmente). Es consistente con las elasticidades, pero el modelo de potencia es más natural que el lineal; se reporta como descriptivo, no como prueba de una cuota fija.

**Respuesta a (2).** No hay columnas que "siempre aporten lo mismo" en sentido estricto: todas varían y todas escalan con el total. Lo que sí hay es un gradiente de ~5× en variabilidad relativa (c4/c9 más estables; c7/c8 más variables) y un patrón de escala distinto (c2 sub-proporcional; c7/c8 super-proporcionales). Eso es más compatible con unidades que producen/entregan cantidades variables con medias estables que con una cuota fija por unidad.

### 3.4 Orden de los registros: tendencia y cambio de régimen

**Señal bruta.**

- Tendencia multivariada \(T\) = 0,1436; nulo de M2 = 0,0461; **p = 0,0012** (5 000 permutaciones del orden).
- Cambio de régimen: estadístico 0,2248; **p = 0,0004** (5 000 permutaciones), en el **corte entre las filas 14 y 15** (grupos 14 | 16, justo en el hueco del grupo 15).
- Por columna en ese corte (p post-hoc, no corrige la selección del corte): c2 **+3,5 pp** (p = 0,0016), c3 +2,0 pp (p = 0,018), c7 **−4,9 pp** (p = 0,0002), c8 −2,5 pp (p = 0,012); BH q = 0,007 / 0,040 / 0,002 / 0,035. c1, c4, c5, c6 y c9 no cambian de forma robusta en ese corte.
- El tramo "después" tiene registros **más pequeños**: N medio 2 632 antes vs 1 775 después (Mann-Whitney p = 0,021); el CV de N es 0,35 y \(\rho(N,\text{orden})=-0,31\) (p = 0,14, no significativo como tendencia lineal).
- **Cautela:** el corte coincide con el hueco del grupo 15, que no se conserva. El cambio de escala puede ser real o un artefacto de la reconstrucción (los registros conservados después del hueco son distintos). Por eso no se interpreta como un cambio histórico: solo se usa como evidencia de que la composición depende del tamaño.

**Control decisivo: el tamaño explica casi todo.**

- Tras regresar el CLR de las cuotas en \(\log N\), el estadístico de cambio de régimen baja de 0,2248 a **0,116** y **p = 0,15**: el cambio de régimen deja de ser significativo.
- \(R^2\) parcial del orden dado el tamaño: **0,085, p = 0,095** (marginal, no significativo al 5 %).
- \(R^2\) parcial del tamaño dado el orden: **0,108, p = 0,041** (significativo).
- **Matiz entre las dos medidas:** \(T\) es una media de correlaciones de rango parciales (detecta una deriva monótona, aunque no sea lineal), mientras que el \(R^2\) parcial es una prueba lineal. Por eso \(T\) puede seguir siendo significativa (p = 0,0012) mientras el \(R^2\) parcial del orden queda marginal (p = 0,095): hay una deriva de rangos, pero el efecto lineal es débil. La conclusión prudente no cambia: el efecto de tamaño es robusto; el efecto temporal es débil y no sobrevive como explicación principal.
- El primer componente (PC1, 42,8 % de la varianza CLR) es un eje de **tamaño**: carga c8 (−0,89) contra c2 (+0,31); su correlación parcial con \(\log N\) dado el orden es **−0,426 (p = 0,038)**, y con el orden dado el tamaño es +0,290 (p = 0,170). El segundo componente (PC2, 25,6 %) es un eje de **tiempo**: carga c7 (−0,73) contra c3 (+0,44); su correlación parcial con el orden dado el tamaño es **+0,425 (p = 0,038)**, y con el tamaño dado el orden −0,316 (p = 0,132).

**Lectura.** La explicación aburrida es la correcta para la mayor parte del efecto: los registros del segundo tramo son más pequeños, y las cuotas dependen del tamaño (c2 sub-proporcional, c7/c8 super-proporcionales); al hacerse más pequeños, c2 sube y c7/c8 bajan. El "cambio de régimen" es, sobre todo, un **cambio de escala del flujo**, no un cambio en la identidad de las 9 unidades. Queda un efecto temporal residual, sobre todo en PC2 (c3 vs c7), con p ≈ 0,04 y sin supervivencia clara a la corrección por múltiples pruebas; es **sugerente, no demostrado**. La tendencia bruta no debe citarse como evidencia de un cambio histórico en las unidades.

### 3.5 ¿Dos sayas? ¿Fracciones 2/9, 3/9, 4/9?

**Dos sayas.** La regla wanka es sobre dos divisiones; si las 9 columnas se agrupan en dos sayas, la cuota del grupo debería ser estable aunque las columnas individuales varíen.

- La bipartición más estable es **c3, c7, c8, c9** (37,9 % del registro) frente a c1, c2, c4, c5, c6; su \(\rho\) de grupo es **−0,056** (negativo: más estable que el muestreo). Pero el mínimo sobre las 126 biparticiones bajo M2 tiene media −0,162 y p05 −0,478; el observado −0,056 **no es bajo** (p = **0,36**, cola inferior). Es decir, la mejor partición no es más estable de lo que se espera al elegir la mejor de 126 al azar.
- Las particiones contiguas: 4+5 (c1–c4 vs c5–c9) \(\rho\) = 0,00057, **p = 0,80**, q = 0,89; 6+3 (c1–c6 vs c7–c9) \(\rho\) = 0,00013, p = 0,68. Ninguna se distingue del nulo de M2. De hecho, las cuotas de grupo son **más** variables que el nulo estacionario (p ≈ 0,8), porque heredan la tendencia/tamaño.
- **Conclusión:** no hay evidencia de una estructura de dos sayas con cuota fija en las 9 columnas. Es un **resultado negativo** para la lectura más literal de la regla wanka a este nivel.

**Fracciones 2/9, 3/9, 4/9.** La agrupación contigua 2+3+4 da cuotas 0,2807 / 0,3182 / 0,4011, frente a 0,2222 / 0,3333 / 0,4444. El grupo c1–c2 es ~27 % mayor de lo previsto; el contraste conjunto de Mahalanobis da **p = 0,00005** (20 000 bootstrap de filas). Bajo el supuesto de que las 9 columnas son unidades iguales y el orden físico refleja el orden de los grupos, las fracciones wanka **no** se reproducen. Si las columnas tienen poblaciones desiguales, el test no aplica; por eso se etiqueta como negativo **bajo ese supuesto**, no como refutación de las fracciones en su contexto original.

### 3.6 Interpretación: ¿leva por población, cuota fija o producción variable?

Los tres modelos de referencia dejan un espacio de posibilidades:

1. **Leva proporcional a poblaciones fijas (wanka):** predice M1 (cuotas constantes, ruido multinomial). **Rechazada**: las cuotas varían 3,68× más que el muestreo; M1 pierde por 1 028 puntos de LOO; todas las columnas están sobredispersas; la escala no es proporcional (elasticidades 0,58–1,67); y hay dependencia del tamaño. La estructura de **medias** sí es proporcional en las medias (9 columnas de 8,0–14,4 %, CV 0,193, max/min 1,80; W = 0,484), pero la **rigidez** proporcional no.
2. **Cuota fija por unidad:** predice columnas constantes en valor absoluto, independientes del total. **Rechazada**: los totales de fila varían 3,3×; todas las columnas correlacionan con N (0,69–0,88); no hay ninguna columna constante. c1 y c2 tienen un componente aditivo positivo (70–128 unidades), pero es solo 22–39 % de su media y no las hace fijas.
3. **Producción variable (chacras, cuadrillas, depósitos):** predice columnas con medias estables pero cuotas variables, y posible dependencia del tamaño/temporada. **Compatible**, con matices: la variabilidad es grande (3,7× el muestreo), hay un gradiente de 5× entre columnas, la composición depende del tamaño y hay autocorrelación. Un modelo de "perfil común + perturbación iid" (M2) reproduce la dispersión marginal pero no la estructura (PC1, T, L, S), así que la producción no es ni independiente ni un simple ruido simétrico: comparte un eje común y está modulada por el tamaño.

**Contraste con producción independiente.** Si se permuta cada columna por separado (se conservan las marginales, se destruye la asociación entre columnas dentro de la fila), el acuerdo de rangos es W = **0,176**; el observado es **0,484** (p = 0,0002) y M1 predice 0,882, M2 0,407. Es decir: los registros se parecen **mucho más** que si las 9 columnas fueran producciones independientes, pero **mucho menos** que si fueran una cuota fija. La verdad está entre M1 y la independencia, más cerca de M2. Eso es exactamente lo que se espera de unidades reales que comparten un perfil administrativo pero entregan cantidades variables.

**Sobre la regla wanka.** La regla, tal como se aplicó en Jauja, es sobre **dos sayas** y poblaciones relativas; no dice que las 9 subunidades de una saya deban tener cuotas fijas. El test de las 9 columnas rechaza la versión fuerte (todas las subunidades proporcionales), pero no refuta la regla en su contexto original. Lo que sí se puede decir: **si** las 9 columnas son unidades de población y **si** la leva de Inkahuasi siguió la regla, deberíamos ver cuotas constantes; no las vemos. La lectura más económica es que las 9 columnas no son poblaciones fijas, o que la leva no era estrictamente proporcional, o ambas. La identificación "9 pachacas" de `n_nueve_partes` sigue siendo **propuesta**, no demostrada; este análisis la debilita como mecanismo de cuota fija, no como partición administrativa.

---

## 4. Resultados B: capacidad real de Inkawasi

### 4.1 Volumen del sitio

202 cuartos documentados (250 estimados), lado 3,5–4 m, altura 2–3,5 m, llenado 40–80 %:

| cuartos | volumen bruto (m³) | ocupado al 40 % (m³) | ocupado al 80 % (m³) |
|---:|---:|---:|---:|
| **202** (documentados) | 4 949–11 312 | 1 980–4 525 | 3 959–9 050 |
| **250** (estimados) | 6 125–14 000 | 2 450–5 600 | 4 900–11 200 |

El rango de volumen ocupado es **1 980–9 050 m³** (202 cuartos) o **2 450–11 200 m³** (250). La mediana del Monte Carlo con priors uniformes es **5 090 m³** (IC90 3 177–7 840). El antiguo valor de 6 400 m³ de `n_almacenes` cae en el **percentil 79** de esta distribución: es un valor alto pero plausible, no un punto central. El factor máximo/mínimo del volumen ocupado es **4,6** en ambos casos: la incertidumbre geométrica sola ya es de casi media década.

### 4.2 Intervalo admisible del volumen unitario

Si **todo** un ledger se almacena a la vez y el depósito estaba entre 40 y 80 % lleno, el volumen unitario \(v\) debe cumplir \(0{,}4G_{\min}/N\le v\le 0{,}8G_{\max}/N\). Para cada ledger:

| ledger | N | v mín. 202 (L) | v máx. 202 (L) | v mín. 250 (L) | v máx. 250 (L) |
|---|---:|---:|---:|---:|---:|
| **UR278** (flujo 47, libro completo) | 61 790 | **32,0** | **146,5** | **39,7** | **181,3** |
| UR266 (copia resumida) | 56 986 | 34,7 | 158,8 | 43,0 | 196,5 |
| UR269 (libro maestro) | 122 609 | 16,1 | 73,8 | 20,0 | 91,3 |
| UR268 (nivel de periodo) | 300 378 | 6,6 | 30,1 | 8,2 | 37,3 |

**La cota superior para UR278 es 146–181 L.** Es 2,6–3,2 veces la fanega (56 L) y 2,7–3,3 veces el extremo alto del saco (55 L). A primera vista, la capacidad **no** excluye ni la fanega ni el saco: ambos están muy por debajo de la cota superior. La restricción que sí muerde es la **cota inferior**: si el depósito estaba al menos al 40 %, la unidad no puede bajar de **32–40 L**, lo que excluye ítems sueltos (0,001–0,05 L), raciones (1–1,75 L), el cuadro de 23 × 23 cm (1,6–5,3 L) y deja al saco de 30 L justo por debajo del límite, por un margen estrecho (~6 %; compatibilidad 0,00). La fanega (56 L) está cómodamente dentro; el saco de 40–55 L también, aunque el extremo de 30 L es marginal.

### 4.3 Fanega y saco: comparación cuantitativa

| unidad | L/unidad | % de la cota superior de UR278 (146,5–181,3 L) | compatibilidad UR278 (L2) | compatibilidad L3 | compatibilidad L4 |
|---|---:|---:|---:|---:|---:|
| arroba (11,5 kg) | 15,5 | 8,6–10,6 % | 0,00 | 0,00 | **0,94** |
| saco 30 L | 30 | 16,6–20,5 % | **0,00** | 0,61 | 0,07 |
| saco 40 L | 40 | 22,1–27,3 % | 0,04 | **0,95** | 0,00 |
| saco 55 L | 55 | 30,3–37,5 % | 0,46 | 0,55 | 0,00 |
| **fanega** | **56** | **30,9–38,2 %** | **0,50** | **0,52** | **0,00** |
| costal 50 kg | 69 | 38,1–47,1 % | **0,86** | 0,15 | 0,00 |

La "compatibilidad" es \(P(0{,}4G\le Nv\le 0{,}8G)\) bajo los priors uniformes; no es una verosimilitud. Lectura:

- **Fanega (56 L):** cabe en el 91 % de los casos (el sitio es lo bastante grande), pero solo llena el depósito entre 40 y 80 % en el **50 %** del espacio de supuestos; en la otra mitad, el depósito quedaría por debajo del 40 % (si es grande/lleno) o por encima del 80 % (si es pequeño/vacío). Está en el **percentil ~9** de la distribución del volumen unitario implicado: la capacidad, tomada al pie de la letra, sugiere que la unidad era **mayor** que una fanega, no menor.
- **Saco de 30 L:** siempre cabe, pero **nunca** llena el depósito al 40 % (compatibilidad 0,00): es demasiado pequeño para el volumen disponible. El extremo bajo del saco propuesto por `n_almacenes` queda excluido por la cota inferior, no por la superior.
- **Saco de 40 L:** compatibilidad 0,04; también bajo.
- **Saco de 55 L:** compatibilidad 0,46; esencialmente una moneda al aire, igual que la fanega.
- **Costal de 69 L:** compatibilidad **0,86**; es el valor único más compatible con UR278 bajo los supuestos medianos.
- **Arroba (15,5 L):** incompatible con UR278 (0,00), pero es el valor más compatible si se asume que **todo L4** (300 378) se almacena a la vez (0,94).

El volumen unitario implicado por UR278 tiene mediana **82,4 L** (IC90 **51,4–126,9 L**). Es ~1,5 fanegas. La fanega está en el extremo bajo de ese intervalo; el costal de 69 L está cerca de la mediana. La capacidad **no identifica** la unidad: el intervalo admisible (32–181 L) abarca un factor 5,7, y la fanega, el saco alto y el costal de 69 L caen dentro. Lo que sí hace es **excluir** las unidades pequeñas (ítems, raciones, cuadro de 23 cm, saco de 30 L) y **favorecer** un bulto de ~50–70 L sobre uno de 30–40 L.

### 4.4 Tabla de escenarios actualizada (comparada con `n_almacenes`)

| unidad | L | UR278 61 790: m³ | % de la capacidad mediana (5 090) | compat. L2 | L3 122 609: % mediana | compat. L3 | L4 300 378: % mediana | compat. L4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ítem suelto | 0,001–0,05 | 0–3 | 0 % | 0,00 | 0 % | 0,00 | 0–1 % | 0,00 |
| ración 0,7 kg | 1–1,75 | 62–108 | 2 % | 0,00 | 4 % | 0,00 | 10 % | 0,00 |
| cuadro 23 cm | 1,6–5,3 | 99–327 | 6 % | 0,00 | 13 % | 0,00 | 31 % | 0,00 |
| arroba | 15,5 | 958 | 19 % | 0,00 | 37 % | 0,00 | 91 % | **0,94** |
| saco 30 L | 30 | 1 854 | 36 % | **0,00** | 72 % | 0,61 | 177 % | 0,07 |
| costal 25 kg | 34,5 | 2 132 | 42 % | 0,00 | 83 % | **0,85** | 204 % | 0,00 |
| carga de llama / saco 40 L | 30–40 | 1 854–2 472 | 36–49 % | 0,04 | 72–96 % | **0,95–0,98** | 177–236 % | 0,00–0,07 |
| saco 55 L | 55 | 3 398 | 67 % | 0,46 | 132 % | 0,55 | 325 % | 0,00 |
| **fanega** | **56** | **3 460** | **68 %** | **0,50** | **135 %** | **0,52** | **331 %** | **0,00** |
| costal 50 kg | 69 | 4 264 | 84 % | **0,86** | 166 % | 0,15 | 407 % | 0,00 |

**Qué cambia respecto de `n_almacenes`.** El informe anterior usaba 6 400 m³ como capacidad y concluía que el costal de 25 kg / 34,5 L ocupaba 63–69 % del volumen del libro maestro L3, y que la fanega ocupaba 106 %. Con la geometría real:

- La capacidad mediana baja a 5 090 m³ y el rango es 1 980–9 050 m³. El costal de 34,5 L para L3 pasa de "63–69 % de 6 400" a **"47–214 % del rango, 83 % de la mediana"**: sigue siendo compatible, pero la horquilla es mucho más ancha.
- La fanega para L3 pasa de 106 % de 6 400 a **135 % de la mediana, 76–347 % del rango**: compatible en ~52 % del espacio de supuestos; requiere un volumen bruto G entre 8 580 y 17 170 m³, es decir, cuartos grandes/altos y un llenado que no sea el mínimo.
- El punto de 6 400 m³ y el volumen unitario de 103,6 L que implicaba están en el **percentil 79** de la nueva distribución: eran valores altos, no centrales. La geometría real **baja** la estimación central de 103,6 a 82,4 L y **ensancha** el intervalo; no confirma el valor anterior.
- Para L2 (UR278), la fanega ocupa 68 % de la mediana y es compatible en la mitad del espacio; el costal de 69 L es el más compatible (0,86). Para L4, la fanega es imposible (331 % de la mediana; 186–850 % del rango) y solo la arroba (15,5 L) es compatible (0,94). La elección de ledger **invierte** el veredicto.

### 4.5 Qué supuestos dominan la incertidumbre

\(\log v=\log n+2\log l+\log h+\log f-\log N\). Con priors uniformes independientes, la descomposición es exacta:

| supuesto | Var(log) | % sin elegir ledger | % incluyendo el ledger |
|---|---:|---:|---:|
| llenado (40–80 %) | 0,0400 | **52,8 %** | 8,1 % |
| altura (2–3,5 m) | 0,0261 | **34,4 %** | 5,3 % |
| lado (3,5–4 m) | 0,0059 | 7,8 % | 1,2 % |
| cuartos (202–250) | 0,0038 | 5,0 % | 0,8 % |
| **qué ledger se almacena a la vez** | 0,4192 | — | **84,7 %** |
| total | 0,0759 / 0,4951 | 100 % | 100 % |

- **Si se fija el ledger,** la incertidumbre es **vertical**: llenado (53 %) + altura (34 %) = **87 %**; el área de planta (lado + cuartos) solo aporta el 13 %. No es la falta de medidas de los cuartos lo que impide decidir; es la altura y el grado de llenado.
- **Si se incluye la elección de ledger,** esa elección domina (85 %), porque L2 (61 790) y L4 (300 378) difieren en un factor 4,9. Es el supuesto más importante de toda la prueba B, y no es un supuesto geométrico: es un supuesto **archivístico** sobre qué representa el libro.
- El detalle "sin puertas" y la ocupación breve afectan justamente a los términos dominantes: sin puertas, el llenado efectivo pudo ser más bajo (favorece el extremo de ~40–50 L, es decir, la fanega/saco alto, no los 82 L); la ocupación breve favorece que el stock simultáneo sea L2 y no L3/L4 (favorece la fanega/saco frente a la arroba). Ambos son cualitativos y se etiquetan **propuestos**.

### 4.6 Interpretación de B

- **La cota superior pedida:** para UR278, **146,5 L** (202 cuartos) a **181,3 L** (250 cuartos). La fanega (56 L) y el saco (30–55 L) están **dentro**; la capacidad no los excluye. La idea de que la arqueología "obliga" a un saco pequeño no se sostiene con estos datos.
- **La restricción que sí muerde es la inferior:** si el depósito estaba al 40–80 %, una unidad de menos de ~32–40 L lo dejaría demasiado vacío. Eso excluye ítems, raciones, el cuadro de 23 cm y el saco de 30 L; deja dentro la fanega, el saco de 40–55 L y el costal de 69 L. La capacidad, por sí sola, favorece un bulto de **~50–70 L**, no de 30 L.
- **El valor central** es 82 L (IC90 51–127), ~1,5 fanegas. La fanega está en el percentil ~9: es compatible, pero es el extremo bajo. El costal de 69 L es el más compatible con el escenario mediano. No hay base para elegir entre "fanega" y "costal de 55–69 L" con estos datos; sí la hay para descartar "saco de 30 L" y "cuadro/ítem".
- **El escenario L4** (300 378 unidades a la vez) es el único que excluye la fanega y el saco alto: exigiría una unidad de 6,6–37,3 L, tipo arroba. Pero L4 es el nivel de **periodo** (30 registros, ~2–3 años según `n_almacenes`), no un stock simultáneo; en una base militar ocupada poco tiempo, el stock a la vez es L2 o menos. Por eso L4 se reporta como **condicional/especulativo**, no como el escenario por defecto.
- **Masa:** no discrimina. Una fanega de maíz (43 kg) daría 2 657 t para UR278, dentro del rango másico estimado (0,4–0,7 t/m³ × 1 980–9 050 m³ = 792–6 335 t) pero por encima de la cota mínima; una fanega de maní (14 kg) daría 865 t, también dentro. La capacidad en fanegas del sitio es ~90 900 (IC90 56 700–140 000), ~18 % (IC90 11–28 %) de las 500 000 fanegas que Cobo atribuye a Hatun Xauxa; Inkawasi es un sitio pequeño, no un depósito imperial comparable.

---

## 5. Controles, resultados negativos y límites

### 5.1 Controles y corrección múltiple

- **Nulos explícitos:** M1 y M2 paramétricos (4 000 y 2 000 simulaciones); permutación del orden (5 000); cambio de régimen con selección del corte (5 000); nulo de M2 para las elasticidades (3 000); permutación independiente de columnas (5 000); bootstrap de filas para los novenos (20 000); nulo de selección de la mejor bipartición (1 000); bootstrap de \(\rho\) heterogéneo (400).
- **Corrección múltiple:** BH-FDR dentro de cada modelo sobre 8 estadísticos de GOF; BH sobre 9 columnas (LRT de \(\rho_j=0\) y tendencias); BH sobre 8 particiones contiguas; BH sobre 4 columnas en el corte. Se indica el número de pruebas en cada tabla. Los p de las tendencias por columna en el corte son **post-hoc** (el corte se eligió con el estadístico multivariado); se reportan además los p ajustados por selección (`p_sel`) en `changepoint_columnas.csv`, que son más conservadores para c2, c3 y c7, y más fuertes para c5 y c8.
- **Robustez de la tendencia:** al quitar una fila, \(T\) va de 0,113 a 0,166 (nulo ≈ 0,046): no depende de un outlier. Dentro de cada tramo, \(T\) = 0,229 (p = 0,011) y 0,233 (p = 0,024): hay una deriva gradual además del escalón, pero al controlar el tamaño el escalón desaparece y la deriva parcial queda marginal (p = 0,095). La conclusión prudente es "efecto de tamaño robusto; efecto temporal residual débil".
- **Replicación UR270:** 6 grupos completos, 11 392 unidades; α = 216,5; \(R_{CV}\) = 3,16; W = 0,682. La sobredispersión está en las cuerdas de detalle, no solo en la tabla agregada de UR278. Pero **no es independiente**: son los mismos registros; se usa solo como control de nivel de agregación.
- **Verificación:** `04_verificacion.py` comprueba 79 cifras citadas (todas OK).

### 5.2 Resultados negativos (los que también cuentan)

1. **No hay ninguna columna de cuota fija.** Las 9 tienen \(\rho>0\) con q < 10⁻²⁰; la más estable (c4) varía 2,5× más que el muestreo.
2. **No hay una estructura de dos sayas con cuota fija.** La mejor de las 126 biparticiones no se distingue del azar de seleccionar la mejor (p = 0,36); la 4+5 tiene p = 0,80.
3. **Las fracciones 2/9, 3/9, 4/9 no se reproducen** en la agrupación contigua 2+3+4 (p = 0,00005), bajo el supuesto de columnas iguales.
4. **M2 no es un modelo completo.** Falla en PC1, T, L y S tras BH; la devianza residual es 702 con 183 gl. La perturbación por registro no es iid: tiene un componente común, depende del tamaño y está autocorrelacionada.
5. **M3 gana AIC/BIC(24) pero no es un mecanismo.** Es saturado (192 parámetros, devianza 0); BIC(54 601) favorece a M2 por 1 294; no tiene LOO sin un prior, y el prior natural es M2. La dirección de la falta de ajuste es hacia **más** estructura común, no hacia la independencia.
6. **El "cambio de régimen" es sobre todo un cambio de tamaño.** Los registros del segundo tramo son 33 % más pequeños (p = 0,021); al controlar \(\log N\), el cambio de régimen deja de ser significativo (p = 0,15) y el \(R^2\) parcial del orden es 0,085 (p = 0,095). El efecto temporal residual (PC2, c3 vs c7) es sugerente pero no robusto.
7. **La cota superior de capacidad no excluye la fanega ni el saco.** 146–181 L es 2,6–3,2× la fanega; la fanega es compatible en ~50 % del espacio de supuestos y el saco de 55 L en 46 %. El único excluido es el extremo bajo del saco (30 L, compatibilidad 0,00), y por la **cota inferior** (depósito demasiado vacío), no por la superior.
8. **El punto de 6 400 m³ de `n_almacenes` era alto.** Cae en el percentil 79 de la capacidad nueva; el volumen unitario implícito de 103,6 L también. La geometría real baja la estimación central a 82 L y ensancha el intervalo; no confirma el valor anterior.
9. **L4 a la vez excluye la fanega, pero es un supuesto poco plausible.** Si se almacenaran las 300 378 unidades de periodo a la vez, la unidad sería de 6,6–37,3 L (arroba), no una fanega/saco. Pero L4 es un libro acumulado, no un stock; la ocupación breve de Inkawasi hace que L2 sea el stock relevante.
10. **La correlación media entre columnas no sirve como prueba de perfil común.** Es −0,114 y no difiere del nulo (−0,112, p = 0,75) porque la suma constante domina la correlación. La prueba válida es W (0,484 vs 0,176), no la correlación media. Se reporta para que no se reintroduzca como "las columnas no covarían, luego son independientes".
11. **UR270 no es una muestra independiente.** Son los mismos registros vistos en el detalle; su α = 216,5 replica la sobredispersión, pero no añade grados de libertad independientes.
12. **La comparación wanka es analógica.** Los documentos son de Jauja (1533–1537); los quipus son de Inkahuasi (Cañete). El rechazo de M1 es un rechazo del mecanismo de cuota fija en estos registros, no de la regla wanka en su contexto original.

### 5.3 Límites

- **Reconstrucción de UR278:** 24 filas estrictas (54 601 unidades) vs 28 filas (61 790). Las 4 filas incompletas podrían cambiar algo los parámetros, pero no la conclusión: la sobredispersión es 3,7× y el LRT es 1 848, muy por encima de cualquier variación razonable por reconstrucción. Los totales de las tres versiones (UR266, UR275, UR278) difieren ~9 %, < 0,1 décadas.
- **Tamaño de muestra:** 24 filas y 9 columnas. Los contrastes multivariados tienen poca potencia para efectos pequeños; los p de las tendencias parciales (0,04–0,10) deben leerse con cautela. La conclusión robusta es la de tamaño (p = 0,0003) y la de M1 (p < 0,001), no la del efecto temporal residual.
- **La identificación de las 9 columnas:** sigue siendo desconocida. Este informe prueba propiedades de su **comportamiento conjunto** (proporcionalidad, estabilidad, escala, orden), no qué son. Si no son poblaciones, el test wanka no aplica literalmente.
- **La capacidad:** los 202 cuartos son "documentados" y 250 "estimados"; el lado 3,5–4 m y la altura 2–3,5 m son rangos, no mediciones individuales. No hay medidas de altura por cuarto ni de profundidad de llenado. El "sin puertas" sugiere un llenado por el techo, pero no hay datos de cómo se llenaban. La capacidad en fanegas usa 56 L; si la fanega local fuera 55,5 L (como en `n_almacenes`), los porcentajes cambian < 1 %.
- **La masa:** no hay ni un kilo de producto recuperado en Inkawasi (`n_almacenes`, N3); la capacidad másica se deriva de densidades de productos modernos, no de los antiguos.

---

## 6. Nivel de evidencia (resumen)

| afirmación | nivel |
|---|---|
| UR278: 24 filas completas × 9 columnas, 54 601 unidades; 61 790 en la tabla completa | **demostrado** |
| M1 (cuotas estrictamente proporcionales) no describe los datos | **demostrado** (LRT 1 848; LOO +1 028; GOF) |
| M2 (perfil fijo + perturbación por registro) es mucho mejor que M1 | **demostrado** (LOO, AIC/BIC(54 601), α) |
| M2 es una descripción completa | **no apoyado / rechazado** (PC1, T, L, S; devianza residual 702/183) |
| Ninguna columna tiene cuota fija | **demostrado** (ρ > 0, q < 10⁻²⁰) |
| Hay un gradiente de ~5× en variabilidad entre columnas | **apoyado con datos** (LRT p = 0,003; bootstrap 0,0125) |
| La composición depende del tamaño del registro (elasticidades ≠ 1) | **apoyado con datos** (S, p = 0,0003; c2/c7/c8) |
| El cambio de régimen aparente es sobre todo un efecto de tamaño | **apoyado con datos** (p = 0,041; cambio p = 0,15 tras controlar) |
| Queda un efecto temporal residual (PC2) | **propuesto / especulativo** (p ≈ 0,04, no robusto a múltiples pruebas) |
| No hay dos sayas con cuota fija | **demostrado (negativo)** para las biparticiones probadas |
| Las fracciones 2/9, 3/9, 4/9 no se reproducen | **demostrado (negativo)** bajo el supuesto de columnas iguales |
| Producción independiente | **rechazada** (W 0,484 vs 0,176; p = 0,0002) |
| Capacidad de Inkawasi: 1 980–9 050 m³ (202) / 2 450–11 200 m³ (250) | **demostrado bajo los supuestos geométricos** |
| Cota superior de UR278: 146–181 L | **demostrado bajo el supuesto de almacenar todo L2 a la vez** |
| Fanega (56 L) y saco (30–55 L) caben; no están excluidos | **apoyado con datos** |
| Volumen unitario central ~82 L; más compatible ~69 L | **propuesto** |
| El saco de 30 L queda excluido por la cota inferior | **apoyado con datos** (compatibilidad 0,00) |
| L4 a la vez excluye la fanega y exige ~arroba | **condicional / especulativo** |
| El llenado (53 %) y la altura (34 %) dominan la incertidumbre física; el ledger domina el total (85 %) | **demostrado** (descomposición exacta bajo priors) |

---

## 7. Para el coordinador

- **La proporcionalidad estricta wanka no describe UR278.** Las cuotas de las 9 columnas varían **3,68 veces** más de lo que explica el muestreo multinomial; el modelo de proporción fija (M1) pierde por **1 848** puntos de LRT y por **1 028** puntos de verosimilitud predictiva LOO frente al modelo con perturbación por registro (M2), que gana en 23/24 filas. La media es proporcional en las medias (9 columnas de 8–14 %, CV 0,193), pero la rigidez no. Nivel: **demostrado (negativo)**.
- **Ninguna columna es una cuota fija.** Las 9 tienen sobredispersión significativa (q < 10⁻²⁰); la más estable (c4) varía 2,5× más que el muestreo y la más variable (c8) 4,6×. El gradiente de ~5× es real (LRT p = 0,003; bootstrap 0,0125). Lo más parecido a una "cuota fija" es c1/c2, con un componente aditivo de 70–128 unidades (22–39 % de su media), pero siguen escalando con el total. Nivel: **demostrado** que no hay cuota fija; **apoyado** el gradiente.
- **La composición depende del tamaño del registro, no solo del tiempo.** Las elasticidades van de 0,58 (c2) a 1,52–1,67 (c7/c8); el contraste conjunto da p = 0,0003. El "cambio de régimen" en el grupo 15 se explica en gran parte porque los registros del segundo tramo son 33 % más pequeños (N 2 632 → 1 775, p = 0,021); al controlar el tamaño, el cambio de régimen deja de ser significativo (p = 0,15) y el efecto temporal residual es débil (PC2, p ≈ 0,04). Nivel: **apoyado** el efecto de tamaño; **propuesto/especulativo** el efecto temporal.
- **No hay estructura de dos sayas ni fracciones 2/9, 3/9, 4/9.** La mejor de las 126 biparticiones tiene ρ = −0,056, pero no se distingue del azar de elegir la mejor (p = 0,36); la 4+5 da p = 0,80. La agrupación 2+3+4 da 0,281/0,318/0,401, no 0,222/0,333/0,444 (p = 0,00005). Nivel: **demostrado (negativo)** para estas estructuras, con el caveat de que las columnas pueden no ser unidades iguales.
- **La producción independiente también queda rechazada.** Si se permuta cada columna por separado, W = 0,176; el observado es 0,484 (p = 0,0002) y M1 predice 0,882, M2 0,407. Los registros comparten mucha más estructura que producciones independientes, pero mucha menos que una cuota fija. Nivel: **demostrado**.
- **Capacidad de Inkawasi (202 cuartos, 3,5–4 m, 2–3,5 m, 40–80 %):** 1 980–9 050 m³ (mediana 5 090); con 250 cuartos, 2 450–11 200 m³. La **cota superior** para UR278 (61 790) es **146–181 L**; la **inferior** es 32–40 L. La fanega (56 L) y el saco de 30–55 L caben; la fanega es 31–38 % de la cota superior y compatible en ~50 % del espacio de supuestos. Nivel: **demostrado** bajo los supuestos; **apoyado** que no excluye la fanega/saco.
- **La capacidad no identifica la unidad; excluye las pequeñas.** El saco de 30 L tiene compatibilidad 0,00 (dejaría el depósito por debajo del 40 %); el de 40 L, 0,04; el de 55 L, 0,46; la fanega, 0,50; el costal de 69 L, 0,86. La estimación central es 82 L (IC90 51–127), ~1,5 fanegas: la fanega está en el percentil ~9, es el extremo bajo pero no está excluida. Nivel: **propuesto** para el valor central; **apoyado** para la exclusión de 30 L/ítems.
- **El supuesto que domina es cuál ledger se almacena a la vez (85 % de la varianza en log-volumen).** Si es L2 (UR278, 61 790), la fanega/saco son compatibles. Si se asume que todo L4 (300 378) estuvo a la vez, la unidad sería de 6,6–37,3 L (arroba) y la fanega quedaría excluida (compatibilidad 0,00). Pero L4 es un libro de periodo, no un stock; en una base ocupada poco tiempo, L2 es el stock relevante. Nivel: **condicional/especulativo** para L4. Si se fija el ledger, la incertidumbre es vertical: llenado 53 % + altura 34 %; el área de planta solo 13 %.
- **Recomendaciones para la próxima ronda:** (i) ajustar un modelo de cuotas que dependa del tamaño (DM con \(\log N\) en la media, o log-ratios con covariable) para ver si el efecto de tamaño agota la falta de ajuste de M2; (ii) buscar otro quipu de Inkahuasi con 9 columnas de **otro producto** y repetir el test de estabilidad de las 9 unidades (¿son genéricas o específicas del flujo 47?); (iii) medir **un** cuarto de pie y la altura de relleno de una colca para sustituir los priors de 2–3,5 m y 40–80 %; (iv) buscar en las transcripciones de Jauja 1558–61 las asignaciones 2/9, 3/9, 4/9 y ver si corresponden a grupos de columnas o a poblaciones; (v) no volver a usar la capacidad como confirmación de una unidad: usarla solo como cota, y reportar siempre el ledger asumido.

---

## 8. Archivos

| archivo | contenido |
|---|---|
| `01_datos.py` | construcción de `datos_ur278.csv` (24×9) y `datos_ur270.csv` (6×9); resumen en `resumen_datos.txt` |
| `02_modelos.py` | M1/M2/M3, AIC/BIC, LRT, LOO, GOF, beta-binomial por columna, tendencias, replicación UR270 → `modelos_ur278.csv`, `gof_ur278.csv`, `columnas_ur278.csv`, `tendencias_ur278.csv`, `resultados_02.json`, `salida_02.txt` |
| `02b_diagnosticos.py` | cambio de régimen, heterogeneidad de ρ, LOO, robustez de la tendencia, PC → `changepoint_columnas.csv`, `loo_ur278.csv`, `pc_ur278.csv`, `resultados_02b.json`, `salida_02b.txt` |
| `02c_sayas.py` | 126 biparticiones y 8 contiguas; nulo de selección → `sayas_ur278.csv`, `sayas_contiguas.csv`, `sayas_detalle.csv`, `salida_02c.txt` |
| `02d_novenos.py` | fracciones 2/9, 3/9, 4/9 → `salida_02d.txt` |
| `02e_independencia.py` | nulo de producción independiente (W, PC1, correlación media) → `salida_02e.txt` |
| `03_capacidad.py` | geometría, intervalos admisibles, Monte Carlo, escenarios, descomposición → `capacidad_inkawasi.csv`, `escenarios_unidad.csv`, `incertidumbre_capacidad.csv`, `resultados_03.json`, `salida_03.txt` |
| `04_verificacion.py` | 79 asserts de las cifras del informe (todos OK) |

---

## 9. Fuentes

**Datos primarios nuevos:**
- LeVine, T. (ed.) (1992). *Inka Storage Systems*. Norman: University of Oklahoma Press. Resumen del coordinador en `analisis/fuentes_txt/LeVine1992_notas.md`: Snead, cap. 3, pp. 78–79 y 93 (Inkawasi: 202 cuartos, 250 estimados, 3,5–4 m de lado, sin puertas, base militar breve, un tercio de los cuartos con función de almacén); D'Altroy y Hastorf, pp. 264–265 (regla wanka de proporcionalidad, 1533–1537); glosario p. 346 (fanega ≈ 56 L); Cobo, p. 22 (500 000 fanegas en Hatun Xauxa); Morris, pp. 143, 190, 242.
- Hyslop, J. (1985), citado por Snead en LeVine 1992 (202 unidades, ficha 9). No consultado directamente.

**Datos de quipus y análisis previos:**
- `analisis/13_sistema_incahuasi/informe.md`, `ur278_tabla.csv`, `ur270_ur278.csv` (reconstrucción y arquitectura del archivo).
- `analisis/ds/n_nueve_partes/informe.md` (24 filas estrictas, 54 601 unidades; CV 0,193; 3,5×; identificación "9 pachacas" como propuesta).
- `analisis/ds/n_almacenes/informe.md` y `capacidad_escenarios.csv` (6 400 m³, unidades de 30–55 L, masas, escenarios).
- `analisis/datos/cuerdas.csv` (UR270: 381 cuerdas; reconstrucción de los 6 grupos de 9).
- Urton, G. (2017). *Inka History in Knots* (cap. 9 y apéndice, vía `13_sistema` y `n_almacenes`).
- Urton, G. y Chu, A. (2015). "Accounting in the King's Storehouse: the Inkawasi Khipu Archive". *Latin American Antiquity* 26(4): 512–529 (citado a través de los informes previos; no consultado directamente).

**Contexto wanka:**
- Chirinos Rivera, A. (2010), fracciones 2/9, 3/9, 4/9 en Hatun Xauxa, citado en la ficha local `docs/fichas/2013-Curatola-quipu-colonial.md` (Curatola y de la Puente, "Contar concertando"). No consultado el original; se usa solo como contexto y se etiqueta como tal.

**Nota de transparencia.** Las citas de LeVine 1992 provienen del resumen del coordinador, no del libro completo; las de Hyslop 1985 y Urton & Chu 2015, de resúmenes y de los informes previos. Las cifras de quipus son de `analisis/datos/cuerdas.csv` y de la reconstrucción de `13_sistema_incahuasi`. Los datos de capacidad son los del encargo (202/250 cuartos, 3,5–4 m, 2–3,5 m, 40–80 %); no se midió ningún cuarto en el campo.
