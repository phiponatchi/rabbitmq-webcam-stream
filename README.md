# RabbitMQ Webcam Streaming (Python)

A simple proof-of-concept that streams webcam frames through RabbitMQ using Python.

- **Producer**: captures webcam frames with OpenCV and publishes JPEG bytes to a RabbitMQ queue.
- **Consumer**: receives frames from the queue and displays them.

## 📦 Requirements

- Python 3.12+
- Docker & Docker Compose (to run RabbitMQ)

## ⚙️ Setup

1. Start RabbitMQ via Docker Compose:

   ```sh
   docker compose up -d
   ```

   This brings up RabbitMQ with the management UI on http://localhost:15672 (guest/guest).
2. Install python dependecies in this env using 
    ```sh
   uv sync
   ```

## ▶️ Running the Stream

### 1) Start the consumer (receiver / display)
You can run multiple instances of the consumer.

```sh
uv run python consumer.py
```

### 2) Start the producer (webcam publisher)

```sh
uv run python producer.py
```

Or just run, to run both docker rabbitmq instance, and the consumer and producer:
```sh
sh run.sh
```

You should see the webcam video window appear via the consumer.

## 🧩 Project Files

- `producer.py` — Captures webcam frames and sends them to RabbitMQ.
- `consumer.py` — Receives frames from RabbitMQ and shows them using OpenCV.
- `compose.yml` — Docker Compose configuration for RabbitMQ.

## 🧠 Notes

- Both scripts declare the queue (`stream`) if it does not already exist.
- If you change queue names, update both scripts.

# License
MIT
