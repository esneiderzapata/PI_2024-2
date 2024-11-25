# Usa una imagen base con Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8080 (el puerto usado por Cloud Run)
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
