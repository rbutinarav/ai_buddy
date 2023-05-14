# app/Dockerfile

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt


EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

#bash commands:
#docker build -t ai_buddy_dev .                                       #build docker image
#az login --scope https://management.core.windows.net//.default       #login to azure
#az acr login --name aibuddy                                          #login to azure container registry
#docker tag ai_buddy_dev aibuddy.azurecr.io/ai_buddy_dev:v0.1         #tag docker image
#docker push aibuddy.azurecr.io/ai_buddy_dev:v0.1                     #push docker image to azure container registry


