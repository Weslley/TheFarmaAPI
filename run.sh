docker-compose down --remove-orphans && docker-compose -f docker-compose.homologacao.yml up -d --build && docker-compose exec -d channels ./manage.py runworker && docker-compose logs -f web channels nginx worker_default redis_channels celery_beat
#docker-compose exec -it thefarma_api /bin/bash
