# Usa la imagen oficial de PostgreSQL
FROM postgres

# Copia el script de inicialización al directorio que PostgreSQL utiliza para ello
COPY postgres-init/initdb.sql /docker-entrypoint-initdb.d/

# (Opcional) Puedes exponer el puerto, aunque docker-compose lo manejará
EXPOSE 5432
