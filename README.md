#  Дашборд системы  Starsmap по оценке компетенций сотрудника
***
### Общее описание
> Разрабатываем дашборд системы  Starsmap по оценке компетенций сотрудника. Данный дашборд должен отображать 
  как статическое состояние навыков и компетенций команды на текущий момент, так и динамические данные за период 
  (3, 6, 12 месяцев). В дашборд должны входить метрики, которые будут отображать состояние навыков, сильные 
  навыки, пройденные оценки, состояние планов развития и запросов на обучение, состояние вовлеченности 
  сотрудников как в статике, так и в динамике.

### Цели сервиса:
  Ценность: дашборд сокращает руководителю время на анализ состояния команды, что позволяет эффективнее планировать 
  развитие команды и найм сотрудников.

***
### Установка и запуск

#### Создание файла .env переменнх окружения
- Создайте в корне проекта .env файл и заполните его следующими данными 
  (см. env_example.txt):
  ```
     # POSTGRES_USER — имя пользователя БД (необязательная переменная,
     #                 значение по умолчанию — postgres);
     # POSTGRES_PASSWORD — пароль пользователя БД (обязательная переменная
     #                     для создания БД в контейнере);
     # POSTGRES_DB — название базы данных (необязательная переменная, по
     #               умолчанию совпадает с POSTGRES_USER).
     # Таким образом, можно передать в окружение только переменную POSTGRES_PASSWORD —
     # и будет создана БД с названием postgres и пользователем postgres

     # DB_HOST — адрес, по которому Django будет соединяться с базой данных.
     #           При работе нескольких контейнеров в сети Docker network вместо
     #           адреса указывают имя контейнера, где запущен сервер БД, — в нашем
     #           случае это контейнер db.
     # DB_PORT — порт, по которому Django будет обращаться к базе данных. 5432 —
     #           это порт по умолчанию для PostgreSQL.name

     # DEBUG - вкл/выкл режим отладки Django
     # DB_TYPE - Выбор типа БД (postgres или sqlite)
  
  Можно передать в окружение только переменную POSTGRES_PASSWORD —
  и будет создана БД с названием postgres и пользователем postgres
  ```

### Запуск проекта на удаленном сервере:

- Зайдите на удаленный сервер через ssh:
  ```
  ssh -i <путь к ssh ключу> <логин_на_сервере>@<IP_сервера>
  ```
- Установите на сервер docker и docker-compose:
  ```
  sudo apt update
  sudo apt install curl
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo apt install docker-compose
  ```

- Скопируйте на сервер файлы docker-compose.yaml | nginx.conf | .env |
  ```
  scp -i <путь_к_ssh_ключу> docker-compose.yml nginx.conf .env \
  <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yml
  ```

- Добавьте в Secrets на Github следующие данные:

  ```
  DOCKER_USERNAME= Username в аккаунте на DockerHub
  DOCKER_PASSWORD= Пароль от аккаунта на DockerHub

  HOST= IP удалённого сервера
  USER= Логин на удалённом сервере
  SSH_KEY= SSH-ключ для доступа к удаленному серверу
  PASSPHRASE= Пароль от SSH-ключа

  ```
- Выполните команды:

  - git add .
  - git commit -m "Deploy"
  - git push

- Запустится workflow:

  - проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
  - сборка и доставка докер-образа для контейнера backend на Docker Hub
  - Деплой на удаленном сервере


- В процессе деплоя на удаленном сервере должны быть выполнены следующие действия:

  ```
  sudo docker compose stop
  sudo docker compose rm -f backend frontend
  sudo docker pull ${{ secrets.DOCKER_USERNAME }}/ros_bank_backend:latest
  sudo docker compose up -d
  sudo docker compose exec backend python3 manage.py makemigrations
  sudo docker compose exec backend python3 manage.py migrate
  sudo docker compose exec backend python3 manage.py collectstatic --no-input
  ```
- Создадим супер пользователя и загрузим в базу информацию об ингредиентах и теги:
  ```
  sudo docker compose exec backend python3 manage.py createsuperuser
  ```
- Откройте проект по адресу:
  ```
  http://<your_domain>
  ```


***

### Для запуска проекта на локальном компьтере в контейнерах:

- Cклонируйте репозиторий в рабочую папку:
  ```
  git clone git@github.com:PetrovKRS/Ros_b.git
  ```
- В корневую папку проелта поместите файл .env с переменными окружения:

- Установите docker compose
  ```
  sudo apt update
  sudo apt install curl
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo apt install docker-compose
  ```
- Перейдите в корневую папку склонированного репозитория:
- Запустите проект в docker контейнерах
  ```
  sudo docker compose up --build
  ```
- Выполните миграции
  ``` 
  sudo docker compose exec backend python3 manage.py makemigrations
  ```
- Выполните миграции
  ```
  sudo docker compose exec backend python3 manage.py migrate
  ```
- Соберите статику
  ```
  sudo docker compose exec backend python3 manage.py collectstatic --no-input
  ```
- Создайте пользователя:
  ```
  sudo docker compose exec backend python3 manage.py createsuperuser
  ```
- Откройте проект по адресу:
  ```
  http://localhost:8000
  ```

### Покрытие тестами Coverage
  ```
   cd backend && pytest --cov
    
  ```

### Документация к API сервису
[![SWAGGER](https://img.shields.io/badge/-swagger-df?style=for-the-badge&logo=swagger&labelColor=black&color=blue)](https://rosb-hakaton.ddns.net/swagger/)

***

### <b> Стек технологий: </b>

![Python](https://img.shields.io/badge/-Python_3.12-df?style=for-the-badge&logo=Python&labelColor=yellow&color=blue)
![Django](https://img.shields.io/badge/-Django-df?style=for-the-badge&logo=Django&labelColor=darkgreen&color=blue)
![REST](https://img.shields.io/badge/-REST-df?style=for-the-badge&logo=Django&labelColor=darkgreen&color=blue)
![Postman](https://img.shields.io/badge/-Postman-df?style=for-the-badge&logo=Postman&labelColor=black&color=blue)
![DOCKER](https://img.shields.io/badge/-DOCKER-df?style=for-the-badge&logo=DOCKER&labelColor=lightblue&color=blue)
![NGINX](https://img.shields.io/badge/-Nginx-df?style=for-the-badge&logo=NGINX&labelColor=green&color=blue)
![GUNICORN](https://img.shields.io/badge/-Gunicorn-df?style=for-the-badge&logo=Gunicorn&labelColor=lightgreen&color=blue)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-df?style=for-the-badge&logo=PostgreSQL&labelColor=lightblue&color=blue)
![GitHub](https://img.shields.io/badge/-GitHub-df?style=for-the-badge&logo=GitHub&labelColor=black&color=blue)
![GitHubActions](https://img.shields.io/badge/-GitHubActions-df?style=for-the-badge&logo=GitHubActions&labelColor=black&color=blue)
***
### Команда проекта: 
[![GitHub](https://img.shields.io/badge/-Андрей_Петров-df?style=for-the-badge&logo=GitHub&labelColor=black&color=blue)](https://github.com/PetrovKRS)
[![GitHub](https://img.shields.io/badge/-Шукало_Родион-df?style=for-the-badge&logo=GitHub&labelColor=black&color=blue)](https://github.com/SHURSHALO)

***
