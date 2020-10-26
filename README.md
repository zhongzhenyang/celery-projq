### start worker
```
celery -A celery-projq.celery_app worker -l INFO

```

### start shell
```
celery -A celery-projq.celery_app shell
```

### start flower
require celery 4.4.7

celery >5 has bug
```
flower -A celery-projq.celery_app --port=5555
```