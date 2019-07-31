docker-compose down --remove-orphans && docker-compose -f docker-compose.dev.yml up -d --build && docker-compose run -d channels ./manage.py runworker &&

#docker-compose run web --add-host="localhost:192.168.1.250"

##docker-compose logs -f web channels nginx worker_default redis_channels celery_beat
#docker exec -it thefarma_api /bin/bash
#docker-compose run web ./manage.py collectstatic --no-input && \
#docker-compose run web --add-host="localhost:192.168.1.250"
#docker-compose down --remove-orphans && docker-compose up --build -d && docker-compose run -d channels ./manage.py runworker && docker-compose logs -f web channels nginx worker_default redis_channels celery_beat