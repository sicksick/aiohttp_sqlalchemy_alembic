# aiohttp nginx postgresql redis socker.io sqlalchemy alembic docker

##### Setup:
```
    cp docker-compose.dev.yml docker-compose.yml
    cp config/config_example.py config/config.py
    cp .env_example .env
    docker-compose up
```

 
##### Rest api based on AIOHTTP with: 
```
    - docker
    - sqlalchemy;
    - alembic and auto generating migrations;
    - provides session by redis storages;
    - postgres database; 
    - access control list;
    - authentication by JWT tokens
```

### Alembic for db migrations
```
    For genarate new migration:
        - alembic revision --autogenerate -m "some descriptions";
    For migrate:
        - alembic upgrade head;
    Genarate new migration in the docker:
        - docker-compose exec web alembic revision --autogenerate -m "create tables";
    Migrate in the docker:
        - docker-compose exec web alembic upgrade head
```