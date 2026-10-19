#!/usr/bin/env bash
# Prueba ciega: DeepSeek redescubre el sistema de Incahuasi sobre datos anonimizados con 15 % de cuerdas ocultas.
# Uso: bash analisis/ds/ciego.sh <carpeta> <modelo>. La carpeta está fuera del repo; las respuestas, fuera de su alcance.
d=$1; m=$2; cd "$d" || exit 1
for i in $(seq 1 8); do
  [ -s informe.md ] && grep -q "Para el coordinador" informe.md && [ -s predicciones.csv ] && { echo "fin ok $i $(date +%T)"; exit; }
  ses=$(opencode session list 2>/dev/null | awk -F'\t' -v t="ciego $(basename $d)" '$2==t{print $1; exit}')
  if [ -z "$ses" ]; then opencode run --standalone -m "$m" --auto --title "ciego $(basename $d)" "$(cat TAREA.md)" >> log.txt 2>&1
  else opencode run --standalone -m "$m" --auto --session "$ses" "Se cortó la conexión. Continúa donde la dejaste y termina informe.md (con 'Para el coordinador') y predicciones.csv. Encargo: $(cat TAREA.md)" >> log.txt 2>&1; fi
  sleep $((60 * i))
done; echo "fin FALLO"
