### start worker
```
celery -A celery-projq.celery_app worker -l INFO

```

### start shell
```
celery -A celery-projq.celery_app shell
```

### start flower

celery >5 has bug, so use docker
```
docker network create redis_net
docker network connect redis_net redis-6.0
docker-comppose up -d
```