echo "Waiting for postgres connection"

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

echo "Waiting for Kafka connection..."
while ! nc -z kafka 9092; do
    sleep 0.1
done
echo "Kafka started"

exec "$@"
