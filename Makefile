include .env

db-up:
	docker-compose up -V --build --force-recreate -d test-db

db-logs:
	docker-compose logs -f -t test-db


db-build-docker:
	docker build -t dbtest:latest -f scripts/Dockerfile.pgvector .
db-down:
	docker-compose rm -sv test-db


db-upgrade:
	SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI_ADMIN} alembic upgrade head

db-downgrade:
	SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI_ADMIN} alembic downgrade 197e2ddf183c

db-dump:
	pg_dump -h localhost -p 5432 -U postgres -d notification > notification_dump.sql

db-dump-load:
	PGPASSWORD=password cat notification_dump.sql | docker exec -i notification-test-db-1 psql -U superuser -d notification

data-db-upgrade:
	SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_DATA_URI_ADMIN} flask db upgrade head

data-db-downgrade:
	SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_DATA_URI_ADMIN} flask db downgrade ba5663486ad9

run:
	flask run --host=0.0.0.0 --port=5555

test:
	pytest --showlocals -vv -rf --cache-clear --color=yes --tb=native tests/

coverage:
	pytest --showlocals -vv -rf --cache-clear --color=yes --tb=native --cov=app tests/
	coverage xml
	coverage html