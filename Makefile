init:
	devbox install && \
		devbox run "pip install pipenv" && \
	devbox run initdb && \
		sed -i "s/#port = 5432/port = 5434/g" ./.devbox/virtenv/postgresql/data/postgresql.conf && \
		sed -i "s/#log_statement = 'none'/log_statement = 'all'/g" ./.devbox/virtenv/postgresql/data/postgresql.conf && \
		sed -i "s/#logging_collector = off/logging_collector = on/g" ./.devbox/virtenv/postgresql/data/postgresql.conf && \
		sed -i "s/#log_directory = 'log'/log_directory = 'log'/g" ./.devbox/virtenv/postgresql/data/postgresql.conf

create:
	devbox run "createdb -p 5434 bemi_dev_source && \
		createuser -p 5434 --superuser --replication postgres && \
		psql -p 5434 -U postgres -c \"ALTER SYSTEM SET wal_level = logical;\"" && \
		make down-services up-services

delete:
	devbox run "dropdb -p 5434 bemi_dev_source && dropuser -p 5434 postgres"

install:
	devbox run --env-file ./server/.env "bun install && \
		cd server && pipenv install && \
		cd ../client && bun install"

up: install
	devbox run "bun run concurrently \"make up-server\" \"make up-client\""

up-server:
	devbox run --env-file ./server/.env "cd server && fastapi dev main.py"

up-client:
	devbox run "cd client && PORT=4002 bun run react-scripts start"

up-postgres:
	devbox services up postgresql-source

up-services:
	devbox services start postgresql-source

down-services:
	devbox services stop

psql:
	devbox run psql bemi_dev_source -p 5434

logs:
	tail -f .devbox/virtenv/postgresql/data/log/postgresql-*.log

ps:
	@devbox services ls

sh:
	devbox --env-file ./server/.env shell

migrate:
	devbox run --env-file ./server/.env "cd server && alembic upgrade head"

rollback:
	devbox run --env-file ./server/.env "cd server && alembic downgrade -1"
