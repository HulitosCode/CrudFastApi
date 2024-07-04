FROM python:3.12-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o diretório de trabalho
COPY . .

# Instale as dependências necessárias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Torne o script de entrada executável
RUN chmod +x entrypoint.sh

# Defina o ponto de entrada
ENTRYPOINT ["./entrypoint.sh"]

# Expor a porta para o serviço
EXPOSE 8000

# Comando para iniciar o servidor com comando customizado (ajustar conforme necessário)
CMD ["fastapi", "dev", "app.py"]
#docker run -d -p 8000:8000 crudfastapi