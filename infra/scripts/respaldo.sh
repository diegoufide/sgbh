#!/usr/bin/env bash
# Respaldo diario de la base de datos y de los archivos (cron: 0 1 * * *).
# Conserva 30 días. Copiar luego la carpeta al almacenamiento externo.
set -euo pipefail

DESTINO="${DESTINO:-/var/respaldos/sgbh}"
FECHA="$(date +%Y%m%d_%H%M)"
mkdir -p "$DESTINO"

docker exec sgbh-db pg_dump -U "${POSTGRES_USER:-sgbh_app}" -d "${POSTGRES_DB:-sgbh}" -Fc > "$DESTINO/sgbh_db_$FECHA.dump"
docker run --rm -v sgbh_sgbh-archivos:/archivos:ro -v "$DESTINO":/destino alpine \
    tar -czf "/destino/sgbh_archivos_$FECHA.tar.gz" -C /archivos .

for f in "$DESTINO"/sgbh_*_"$FECHA".*; do
    openssl enc -aes-256-cbc -pbkdf2 -salt -in "$f" -out "$f.enc" -pass env:SGBH_RESPALDO_CLAVE
    rm -f "$f"
done

find "$DESTINO" -name 'sgbh_*.enc' -mtime +30 -delete
echo "Respaldo $FECHA terminado"
