
# Todo app


## Подготовка backend окружения к разработке 

 Создать в папке `backend` файл `.env`. Пример есть в файле `.env.sample`. 
 Параметры `EMAIL`и `EMAIL_PASS` не стоит изменять для корректной работы.
Для запуска юнит тестов прописать `docker-compose run backend pytest`.


## Подготовка frontend окружения к разработке
Создать в папке `frontend` файл `.env`. Указать параметр `VUE_APP_BACKEND_URL=http://localhost:8000/api/v1/`.

## Запуск
При первом запуске прописывать `docker-compose up` с флагом `--build`. Фронт запускается на `localhost:8080`
