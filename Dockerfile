# Use uma imagem oficial do Python como imagem mãe
FROM python:3.11-slim-bullseye

# Define o diretório de trabalho no container
WORKDIR /usr/src/app

# Copia o conteúdo do diretório atual para o container em /usr/src/app
COPY prod_requirements.txt ./
COPY setup.py ./
COPY ./app ./app

# Instala os pacotes necessários especificados em requirements.txt
RUN pip install --no-cache-dir -r prod_requirements.txt

# Expõe a porta na qual o aplicativo é executado
EXPOSE 8000

# Define a variável de ambiente
ENV NAME PixzinhoBot

# Executa app.py quando o container é iniciado
CMD ["python", "setup.py"]
