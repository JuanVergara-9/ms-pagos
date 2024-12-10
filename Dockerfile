# Usar una imagen base de Python
FROM python:3.12

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos y el código fuente
COPY requirements.txt requirements.txt
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que la aplicación se ejecutará
EXPOSE 5003

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]