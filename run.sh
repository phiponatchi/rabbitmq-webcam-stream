docker compose up -d

until curl -s -u guest:guest http://localhost:15672/api/healthchecks/node | grep -q '"status":"ok"'; do
  echo "Waiting for RabbitMQ..."
  sleep 2
done

uv sync
uv run python consumer.py &
uv run python producer.py