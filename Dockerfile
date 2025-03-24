FROM python:3.8-slim

RUN apt update
RUN apt install -y python3-pip
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

WORKDIR /app

EXPOSE 8001

COPY . .

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8001", "app:app"]
