# aiohttp nginx postgresql redis docker
# socker.io sqlalchemy alembic 
# google and fasebook auth 


##### Setup:
```
    cp docker-compose.dev.yml docker-compose.yml
    cp config/config_example.py config/config.py
    cp .env_example .env
    docker-compose up -d
    docker-compose exec web alembic upgrade head
    docker-compose exec web python create_admin.py
```

##### Postman collection
```
    aiohttp_sqlalchemy_alembic.postman_collection.json
```

 
##### Rest api based on AIOHTTP with:
```
    - Socket.io;
    - Sqlalchemy;
    - Alembic and auto generating migrations;
    - Provides session by redis storages;
    - Postgres database; 
    - Access control list;
    - Authentication by JWT tokens.
```

### Alembic for db migrations
```
    Genarate new migration:
        - docker-compose exec web alembic revision --autogenerate -m "create tables";
    Migrate:
        - docker-compose exec web alembic upgrade head
    Migrate undo last:
        - docker-compose exec web alembic downgrade -1
```