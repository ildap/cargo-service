### Собрать и запустить проект
```sh
$ docker-compose up -d --build
```

### документация будет доступна тут
http://localhost:8000/docs

### Команда для просмотра сообщений в кафке
```sh 
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic Cargoservice --from-beginning
# примеры сообщений:
{"level": "INFO", "name": "root", "message": "cargo-service.read by id 2", "datetime": "2024-11-23 20:02:23.875808"}
{"level": "INFO", "name": "root", "message": "cargo-service.read by id 2", "datetime": "2024-11-23 20:02:32.552408"}
```
