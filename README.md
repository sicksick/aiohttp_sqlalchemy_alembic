# aiohttp_sqlalchemy_alembic

##### Rest api based on AIOHTTP with: 
```
    - sqlalchemy;
    - alembic and auto generating migrations;
    - provides session by redis storages;
    - postgres database; 
    - access control list;
    - authentication by JWT tokens.
```

### Alembic
```
    For genarate new migration:
        - alembic revision --autogenerate -m "some descriptions";
    For migrate:
        - alembic upgrade head;
```

### Installing for ubuntu
```
    sudo apt-get install build-essential libffi-dev python-dev redis-server
```