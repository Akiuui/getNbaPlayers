FROM python:3.9-slim

RUN apt update
RUN apt install -y python3-pip
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt app/
RUN pip3 install -r /app/requirements.txt

WORKDIR app

EXPOSE 8001

ENV MONGO_KEY="mongodb+srv://aleksastojanovic18:jasamaleksa@nbagames.4pfxa.mongodb.net/?retryWrites=true&w=majority&appName=NbaGames"
ENV API-KEY="df590377d88334e2c10bea17088d1cf6"

COPY . .

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8001", "app.app:app"]
